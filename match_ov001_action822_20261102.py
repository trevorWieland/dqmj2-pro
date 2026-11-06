import gzip
import hashlib
import json
import re
import sys
import match_runtime as c
import unicorn
from project import ROOT, configuration, read_json, sha256, write_json
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from link_private_overlay_hypothesis_20261101 import link_private
import ov001_action822_machine_20261102 as M
import ov001_action822_model_20261102 as G
from ov001_action822_profiles_20261102 import profiles

SOURCE = ROOT / 'src/overlays/ov001_20261102_action822'
WORK = ROOT / 'work/ol822-proof'


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def build(source, name, origin=None):
    c.WORK = WORK / name / 'compile'
    previous = c.symbol_address

    def resolver(symbol):
        if re.fullmatch(r'_(?:[us](?:32|64)|f|d)_\w+', symbol):
            raise ValueError('822 unqualified compiler intrinsic ' + symbol)
        return previous(symbol)

    c.symbol_address = resolver
    try:
        rows, unused = c.compare(source, 'ov001', '2', 'off', True)
    finally:
        c.symbol_address = previous
    if len(rows) != 1 or rows[0].get('compileFailed'):
        raise ValueError(('822 compiler failed', rows))
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
    return {key: value for key, value in result.items() if key not in ['memory', 'context', 'actors']} | dict(contextHex=result['context'].hex(), actorsHex={hex(key): value.hex() for key, value in result['actors'].items()}, completeRamSha256=hashlib.sha256(result['memory']).hexdigest())


def execute():
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('822 pinned runtime differs')
    pinPath = ROOT / 'evidence/verification/ov001-action822-inputs-20261102.json'
    pins = read_json(pinPath)
    for item in pins['files']:
        if sha256(ROOT / item['path']) != item['sha256']:
            raise ValueError(('822 frozen input differs', item['path']))
    selected = read_json(ROOT / pins['acceptedSnapshot'])['functions']
    if any(row['processor'] == 'arm9' and not row.get('program') and row['module'] == 'ov001' and max(row['address'], M.ENTRY) < min(row['address'] + row['bytes'], M.ENTRY + 1540) for row in selected):
        raise ValueError('822 selected source overlap')
    mainInfo, main, unused = measured_module('main')
    moduleInfo, overlay, unused = measured_module('ov001')
    match, body = build(SOURCE / 'dispatch.c', 'source')
    if len(body) != 1540:
        raise ValueError('822 canonical span differs')
    template = (SOURCE / 'dispatch.c').read_text()
    replacements = [('wrong-return', '    return 0U;', '    return 1U;', 0x02650000), ('wrong-phase', 'M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x1B) = 3;', 'M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x1B) = 4;', 0x02652000)]
    controls = []
    images = {}
    for name, before, after, origin in replacements:
        if template.count(before) != 1:
            raise ValueError(('822 control replacement ambiguous', name))
        directory = ROOT / 'nonmatching/overlay-lane/20261102-action822-controls' / name
        directory.mkdir(parents=True, exist_ok=True)
        source = directory / 'source.c'
        text = template.replace(before, after)
        if source.exists() and source.read_text() != text:
            raise ValueError(('822 frozen wrong source differs', name))
        source.write_text(text)
        source.with_name('context.h').write_bytes((SOURCE / 'context.h').read_bytes())
        proof, wrong = build(source, name, origin)
        images[origin] = wrong
        controls.append(dict(name=name, origin=origin, proof=proof, actualTopReturns=0, rejected=0, positive=0))
    totals = dict(pairs=0, actualTopReturns=0, actualNativeReturnInstructions=0, suppliedCalls=0, independentModelPairs=0)
    traces = []
    cases = []
    own = set()
    counts = {}
    outcomes = set()
    for profile in profiles():
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
            write_json(ROOT / 'evidence/attempts/ov001-action822-model-rejected-20261102.json', dict(profile=profile, failures=failures, results=list(map(compact, results))))
            raise ValueError(('822 original/source model failed', profile['ordinal'], failures[:2]))
        keys = ['registers', 'cpsr', 'calls', 'rawCalls', 'nativeEntries', 'nativeCompletions', 'writes', 'context', 'actors', 'memory', 'actualNativeReturnInstructions']
        differences = [key for key in keys if original[key] != candidate[key]]
        if differences:
            write_json(ROOT / 'evidence/attempts/ov001-action822-source-rejected-20261102.json', dict(profile=profile, differences=differences, results=list(map(compact, results))))
            raise ValueError(('822 source/native differs', profile['ordinal'], differences))
        totals['pairs'] += 1
        totals['actualTopReturns'] += 2
        totals['independentModelPairs'] += 1
        count = original['actualNativeReturnInstructions'] + candidate['actualNativeReturnInstructions']
        totals['actualNativeReturnInstructions'] += count
        totals['suppliedCalls'] += len(original['calls']) + len(candidate['calls'])
        own.update(original['ownPcs'])
        outcomes.add(original['context'][0x1B])
        for result in results[:2]:
            for row in result['nativeCompletions']:
                counts[row['address']] = counts.get(row['address'], 0) + 1
        for index, control in enumerate(controls):
            control['actualTopReturns'] += 1
            control['rejected' if failures[index + 2] else 'positive'] += 1
        trace = dict(profile=profile, results=list(map(compact, results)), failures=failures, originalSourceDifferences=differences)
        cases.append(dict(ordinal=profile['ordinal'], actualTopReturns=2, actualNativeDependencyReturns=count, suppliedCalls=len(original['calls']) + len(candidate['calls']), traceSha256=hashlib.sha256(encoded(trace)).hexdigest()))
        traces.append(trace)
    expectedOwn = set(range(M.ENTRY, M.ENTRY + 1524, 4))
    missingOwn = sorted(expectedOwn - own)
    if missingOwn:
        write_json(ROOT / 'evidence/attempts/ov001-action822-coverage-rejected-20261102.json', dict(missingPcs=list(map(hex, missingOwn)), observed=len(own)))
        raise ValueError(('822 own instruction coverage incomplete', len(missingOwn)))
    if any(not control['rejected'] for control in controls):
        raise ValueError('822 missing returning whole-C rejection')
    raw = encoded(traces)
    artifact = ROOT / 'evidence/generated/ov001-action822-traces-20261102.json.gz'
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    report = dict(schemaVersion=1, romSha256=configuration()['romSha256'], processor='arm9', program='', module='ov001', moduleSha256=moduleInfo['sha256'], mainSha256=mainInfo['sha256'], matches=[match], canonicalMatchedFunctions=1, canonicalMatchedBytes=1540, sourceCreditPendingIntegrator=1540, allPassed=True, totals=totals, nativeDependencyCounts=counts, allCoreRegistersAndCpsrEqual=True, completeRamIncludingStackEqual=True, allRawCallWordsAndOrderedWritesEqual=True, allOwnCodeObserved=dict(codeBytes=1524, literalBytes=16, unclassifiedBytes=0), observedRawContext1B=sorted(outcomes), cases=cases, negativeEvidence=controls, generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(), sha256=sha256(artifact), uncompressedSha256=hashlib.sha256(raw).hexdigest()), limits=['One genuine1540-byte ordinary C caller match; integrator/module/whole-ROM acceptance remains separate.', 'Main MoveTbl pointer/flag/cost wrappers and overlay actor lookup/raw eligibility/signed16 accessor/deduction/policy getter execute original instructions. Cost adjustment7CE3C and maximum-valueDBCF0 remain supplied, as do listed UI/resource/dispatch policies.', 'Context phase/timer/frame, synthetic MoveTbl rows,12actor buffers/descriptor flags and cached actor+1FF marker are supplied. No ordinary-scene reachability, record33 cache initialization, asset legality, item/ability names or future RNG claim.', 'Rows use bounded move IDs0..511 and valid mapped descriptors; actor lookup sides0..3 plus raw4/255 null-result cases. Null current actor, malformed pointers, asynchronous effects and hardware/device paths are unsupported.', 'All provider contracts are measured caller raw-word views, with legal caller-saved/CPSR clobbers; historical selected-C projections do not establish original formal types. Services perform no RAM mutations in this fixture.', 'Negative controls run complete fresh wrong C at genuine private linker origins, preserving original neighboring code. Their top returns and model rejections are separate from positive totals.', 'No Windows/Android execution or application adapter/UI edits.'])
    write_json(ROOT / 'evidence/matches/ov001-20261102-action822.json', report)
    print(dict(**totals, matchedBytes=1540, controls=[{key: row[key] for key in ['name', 'actualTopReturns', 'rejected', 'positive']} for row in controls], observedRawContext1B=sorted(outcomes)), flush=True)


if __name__ == '__main__':
    execute()
