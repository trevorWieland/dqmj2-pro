import gzip
import hashlib
import json
import sys
import match_runtime as c
import unicorn
from project import ROOT, configuration, read_json, sha256, write_json
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from link_private_overlay_hypothesis_20261101 import link_private
import ov006_row841_machine_20261102 as M
import ov006_row841_model_20261102 as G

SOURCE = ROOT / 'src/overlays/ov006_20261102_row841'
WORK = ROOT / 'work/ol841-proof'


def build(source, name, origin=None):
    c.WORK = WORK / name / 'compile'
    rows, unused = c.compare(source, 'ov006', '2', 'off', True)
    if len(rows) != 1 or rows[0].get('compileFailed'):
        raise ValueError(('841 compiler failed', rows))
    row = rows[0]
    row['sourceDependencies'] = [dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(), sha256=sha256(source.with_name('context.h')))]
    directory = WORK / name / 'canonical'
    bindings = qualified_bindings(row)
    if origin is None:
        proof = validate(row, bindings, directory)
        return dict(**row, realLink=proof), (directory / 'caller.bin').read_bytes()
    try:
        canonical = validate(row, bindings, directory)
    except ValueError as error:
        if not error.args or not isinstance(error.args[0], dict):
            raise
        canonical = error.args[0]
    proof, body = link_private(row, bindings, directory, WORK / name / 'private', origin)
    return dict(source=row, canonicalComparison=canonical, privateLink=proof), body


def compact(result):
    return {key: value for key, value in result.items() if key not in ['memory', 'rows', 'state']} | dict(rowWindowHex=result['rows'].hex(), stateHex=result['state'].hex(), completeRamSha256=hashlib.sha256(result['memory']).hexdigest())


def execute():
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('841 pinned runtime differs')
    pins = read_json(ROOT / 'evidence/verification/ov006-row841-inputs-20261102.json')
    for row in pins['files']:
        if sha256(ROOT / row['path']) != row['sha256']:
            raise ValueError(('841 frozen input differs', row['path']))
    selected = read_json(ROOT / pins['acceptedSnapshot'])['functions']
    if any(row['processor'] == 'arm9' and not row.get('program') and row['module'] == 'ov006' and max(row['address'], M.ENTRY) < min(row['address'] + row['bytes'], M.ENTRY + 532) for row in selected):
        raise ValueError('841 selected overlap')
    mainInfo, main, unused = measured_module('main')
    moduleInfo, overlay, unused = measured_module('ov006')
    match, body = build(SOURCE / 'row.c', 'source')
    template = (SOURCE / 'row.c').read_text()
    start = template.rfind('    return native_fn_ov006_021dc08c(')
    end = template.rfind('}')
    if start < 0:
        raise ValueError('841 returning-control site absent')
    wrongReturn = template[:start] + template[start:end].replace('    return ', '    ', 1) + '    return 0U;\n' + template[end:]
    before = 's32 *, 0x34) == 1\n'
    if template.count(before) != 1:
        raise ValueError('841 conditional-control site ambiguous')
    wrongFlag = template.replace(before, 's32 *, 0x34) != 0\n')
    controls = []
    images = {}
    for name, text, origin in [('wrong-return', wrongReturn, 0x02650000), ('wrong-flag', wrongFlag, 0x02652000)]:
        directory = ROOT / 'nonmatching/overlay-lane/20261102-row841-controls' / name
        directory.mkdir(parents=True, exist_ok=True)
        source = directory / 'source.c'
        if source.exists() and source.read_text() != text:
            raise ValueError(('841 frozen wrong source differs', name))
        source.write_text(text)
        source.with_name('context.h').write_bytes((SOURCE / 'context.h').read_bytes())
        proof, wrong = build(source, name, origin)
        images[origin] = wrong
        controls.append(dict(name=name, origin=origin, proof=proof, actualTopReturns=0, rejected=0, positive=0))
    totals = dict(pairs=0, actualTopReturns=0, actualNativeReturnInstructions=0, suppliedCalls=0, independentModelPairs=0)
    traces = []
    cases = []
    pcs = set()
    categories = set()
    for profile in G.profiles():
        results = []
        failures = []
        for kind, entry in [('native', M.ENTRY), ('source', M.ENTRY)] + [(row['name'], row['origin']) for row in controls]:
            vm = M.Machine(main, overlay, images, profile)
            if kind == 'source':
                vm.u.mem_write(M.ENTRY, body)
            result = vm.run(entry)
            result['kind'] = kind
            results.append(result)
            failures.append(G.model(vm, result))
        original, candidate = results[:2]
        if failures[0] or failures[1]:
            write_json(ROOT / 'evidence/attempts/ov006-row841-model-rejected-20261102.json', dict(profile=profile, failures=failures, results=list(map(compact, results))))
            raise ValueError(('841 model failed', profile['ordinal'], failures[:2]))
        keys = ['registers', 'cpsr', 'calls', 'rawCalls', 'nativeEntries', 'nativeCompletions', 'writes', 'rows', 'state', 'memory', 'actualNativeReturnInstructions']
        differences = [key for key in keys if original[key] != candidate[key]]
        if differences:
            raise ValueError(('841 source/native difference', profile['ordinal'], differences))
        totals['pairs'] += 1
        totals['actualTopReturns'] += 2
        totals['independentModelPairs'] += 1
        count = original['actualNativeReturnInstructions'] + candidate['actualNativeReturnInstructions']
        totals['actualNativeReturnInstructions'] += count
        totals['suppliedCalls'] += len(original['calls']) + len(candidate['calls'])
        pcs.update(original['ownPcs'])
        categories.update(row['rawR0'] for row in original['nativeCompletions'] if row['address'] == '0x2067d54')
        for index, control in enumerate(controls):
            control['actualTopReturns'] += 1
            control['rejected' if failures[index + 2] else 'positive'] += 1
        trace = dict(profile=profile, results=list(map(compact, results)), modelFailures=failures, originalSourceDifferences=differences)
        raw = json.dumps(trace, sort_keys=True, separators=(',', ':')).encode()
        cases.append(dict(ordinal=profile['ordinal'], actualTopReturns=2, actualNativeDependencyReturns=count, suppliedCalls=len(original['calls']) + len(candidate['calls']), traceSha256=hashlib.sha256(raw).hexdigest()))
        traces.append(trace)
    if pcs != set(range(M.ENTRY, M.ENTRY + 524, 4)) or categories != set(range(8)):
        raise ValueError(('841 own coverage/classifier corpus incomplete', len(pcs), categories))
    if any(not row['rejected'] for row in controls):
        raise ValueError('841 returning wrong-C rejection missing')
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = ROOT / 'evidence/generated/ov006-row841-traces-20261102.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    report = dict(schemaVersion=1, romSha256=configuration()['romSha256'], processor='arm9', program='', module='ov006', moduleSha256=moduleInfo['sha256'], mainSha256=mainInfo['sha256'], matches=[match], canonicalMatchedFunctions=1, canonicalMatchedBytes=532, sourceCreditPendingIntegrator=532, allPassed=True, totals=totals, allCoreRegistersAndCpsrEqual=True, completeRamIncludingStackEqual=True, allRawCallWordsAndOrderedWritesEqual=True, allOwnCodeObserved=dict(codeBytes=524, literalBytes=8, unclassifiedBytes=0), nativeClassifierOutputs=sorted(categories), cases=cases, negativeEvidence=controls, generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(), sha256=sha256(artifact), uncompressedSha256=hashlib.sha256(raw).hexdigest()), limits=['Genuine532-byte ordinary C caller; integrator/module/ROM admission pending.', 'Actual fixed-address main63EEC getter and main67D54 signed-threshold classifier execute; preceding DE1A8 raw result is explicitly forwarded into R0, independently of Ghidra omitted-argument output.', 'Selected index0..7 and stride48/header-relative row fields, renderer returns and all UI/parser/lookup services are supplied. Main46AF4 writes a synthetic64-byte stack payload; no original parser/text representation/bounds or scene claim.', 'All caller raw words,64-byte forwarding, full renderer-return R0, exact-one versus nonzero flags and actual native classifier thresholds are modeled. Call word views do not assert full original callee formal types.', 'Wrong C controls execute complete genuine private-linked images; proper returning counts, rejected and unaffected positive cases remain separate.', 'No saved-record33 initialization/meaning, host/device execution, audio, app adapter/UI or shared source/ledger changes.'])
    write_json(ROOT / 'evidence/matches/ov006-20261102-row841.json', report)
    print(dict(**totals, matchedBytes=532, controls=[{key: row[key] for key in ['name', 'actualTopReturns', 'rejected', 'positive']} for row in controls]), flush=True)


if __name__ == '__main__':
    execute()
