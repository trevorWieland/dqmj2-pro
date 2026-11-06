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
import ov001_dispatch849_machine_20261102 as M
import ov001_dispatch849_model_20261102 as G

SOURCE = ROOT / 'src/overlays/ov001_20261102_dispatch849'
WORK = ROOT / 'work/ol849-proof'


def build(source, name, origin=None):
    c.WORK = WORK / name / 'compile'
    rows, unused = c.compare(source, 'ov001', '2', 'off', True)
    if len(rows) != 1 or rows[0].get('compileFailed'):
        raise ValueError(('849 compiler failed', rows))
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
    return {key: value for key, value in result.items() if key not in ['memory', 'table', 'state', 'actor', 'move']} | dict(actorHex=result['actor'].hex(), moveHex=result['move'].hex(), tableHex=result['table'].hex(), stateHex=result['state'].hex(), completeRamSha256=hashlib.sha256(result['memory']).hexdigest())


def execute():
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('849 pinned runtime differs')
    pins = read_json(ROOT / 'evidence/verification/ov001-dispatch849-inputs-20261102.json')
    for row in pins['files']:
        if sha256(ROOT / row['path']) != row['sha256']:
            raise ValueError(('849 frozen input differs', row['path']))
    selected = read_json(ROOT / pins['acceptedSnapshot'])['functions']
    if any(row['processor'] == 'arm9' and not row.get('program') and row['module'] == 'ov001' and max(row['address'], M.ENTRY) < min(row['address'] + row['bytes'], M.ENTRY + 544) for row in selected):
        raise ValueError('849 selected overlap')
    mainInfo, main, unused = measured_module('main')
    moduleInfo, overlay, unused = measured_module('ov001')
    match, body = build(SOURCE / 'dispatcher.c', 'source')
    template = (SOURCE / 'dispatcher.c').read_text()
    wrongReturn = template.replace('    return 0U;', '    return 1U;')
    wrongNibble = template.replace('>> 0x1C) == 1)', '>> 0x1C) == 2)')
    wrongBoolean = template.replace('var_r2 = temp_r0 == 1;', 'var_r2 = temp_r0 != 0;')
    if any(text == template for text in [wrongReturn, wrongNibble, wrongBoolean]):
        raise ValueError('849 wrong-C site absent')
    controls = []
    images = {}
    for index, (name, text) in enumerate([('wrong-return', wrongReturn), ('wrong-nibble', wrongNibble), ('wrong-boolean', wrongBoolean)]):
        origin = 0x02650000 + index * 0x2000
        directory = ROOT / 'nonmatching/overlay-lane/20261102-dispatch849-controls' / name
        directory.mkdir(parents=True, exist_ok=True)
        source = directory / 'source.c'
        if source.exists() and source.read_text() != text:
            raise ValueError(('849 frozen wrong source differs', name))
        source.write_text(text)
        source.with_name('context.h').write_bytes((SOURCE / 'context.h').read_bytes())
        proof, wrong = build(source, name, origin)
        images[origin] = wrong
        controls.append(dict(name=name, origin=origin, proof=proof, actualTopReturns=0, rejected=0, positive=0))
    totals = dict(pairs=0, actualTopReturns=0, actualNativeReturnInstructions=0, suppliedCalls=0, independentModelPairs=0)
    traces = []
    cases = []
    pcs = set()
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
            write_json(ROOT / 'evidence/attempts/ov001-dispatch849-model-rejected-20261102.json', dict(profile=profile, failures=failures, results=list(map(compact, results))))
            raise ValueError(('849 model failed', profile['ordinal'], failures[:2]))
        keys = ['registers', 'cpsr', 'calls', 'rawCalls', 'nativeEntries', 'nativeCompletions', 'writes', 'table', 'state', 'actor', 'move', 'memory', 'actualNativeReturnInstructions']
        differences = [key for key in keys if original[key] != candidate[key]]
        if differences:
            raise ValueError(('849 source/native difference', profile['ordinal'], differences))
        totals['pairs'] += 1
        totals['actualTopReturns'] += 2
        totals['independentModelPairs'] += 1
        count = original['actualNativeReturnInstructions'] + candidate['actualNativeReturnInstructions']
        totals['actualNativeReturnInstructions'] += count
        totals['suppliedCalls'] += len(original['calls']) + len(candidate['calls'])
        pcs.update(original['ownPcs'])
        for index, control in enumerate(controls):
            control['actualTopReturns'] += 1
            control['rejected' if failures[index + 2] else 'positive'] += 1
        trace = dict(profile=profile, results=list(map(compact, results)), modelFailures=failures, originalSourceDifferences=differences)
        raw = json.dumps(trace, sort_keys=True, separators=(',', ':')).encode()
        cases.append(dict(ordinal=profile['ordinal'], actualTopReturns=2, actualNativeDependencyReturns=count, suppliedCalls=len(original['calls']) + len(candidate['calls']), traceSha256=hashlib.sha256(raw).hexdigest()))
        traces.append(trace)
    if pcs != set(range(M.ENTRY, M.ENTRY + 536, 4)):
        raise ValueError(('849 own coverage incomplete', len(pcs), sorted(set(range(M.ENTRY, M.ENTRY + 536, 4)) - pcs)))
    if any(not row['rejected'] for row in controls):
        raise ValueError('849 returning wrong-C rejection missing')
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = ROOT / 'evidence/generated/ov001-dispatch849-traces-20261102.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    report = dict(schemaVersion=1, romSha256=configuration()['romSha256'], processor='arm9', program='', module='ov001', moduleSha256=moduleInfo['sha256'], mainSha256=mainInfo['sha256'], matches=[match], canonicalMatchedFunctions=1, canonicalMatchedBytes=544, sourceCreditPendingIntegrator=544, allPassed=True, totals=totals, allCoreRegistersAndCpsrEqual=True, completeRamIncludingStackEqual=True, allRawCallWordsAndOrderedWritesEqual=True, allOwnCodeObserved=dict(codeBytes=536, literalBytes=8, unclassifiedBytes=0), cases=cases, negativeEvidence=controls, generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(), sha256=sha256(artifact), uncompressedSha256=hashlib.sha256(raw).hexdigest()), limits=['Genuine544-byte ordinary C caller; integrator/module/ROM admission pending.', 'Actual main7AFEC MoveTbl pointer, main7B058 byte25/word-mask predicate and main65D88 stride88 pointer calculation execute. Table bases, move/row records, target actor/context/frame are synthetic.', 'UI/policy/animation/name/identifier services are supplied with explicit no-memory effects and legal caller-saved-register/CPSR clobbers. No scene reachability, action availability, recipient progression or resource lifetime claim.', 'The u16 left-shift has an explicit pre-shift u32 cast and is C-defined. Signed right shift of the frame word is measured as arithmetic under the pinned ARM compiler; no host/device claim.', 'Own raw phase0E, context0A/13 and unsigned29, actor signed1E4/236 and unsigned31E/1FD, move halfword8/byte25 and item byte2D are independently modeled without assigned game meanings.', 'All canonical physical registers, stack/RAM, raw call words and ordered writes agree. Whole-C private-linked wrong images properly return; rejected and unaffected positive cases remain separate.', 'No saved-record33 initialization, actor trait meaning, app adapter/UI edits, shared preference edits or original callee source credit.'])
    write_json(ROOT / 'evidence/matches/ov001-20261102-dispatch849.json', report)
    print(dict(**totals, matchedBytes=544, controls=[{key: row[key] for key in ['name', 'actualTopReturns', 'rejected', 'positive']} for row in controls]), flush=True)


if __name__ == '__main__':
    execute()
