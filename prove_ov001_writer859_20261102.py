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
import ov001_writer859_machine_20261102 as M
import ov001_writer859_model_20261102 as G

SOURCE = ROOT / 'nonmatching/overlay-lane/20261102-writer859/candidate'
WORK = ROOT / 'work/ol859-proof'


def build(source, name, origin=None):
    c.WORK = WORK / name / 'compile'
    rows, unused = c.compare(source, 'ov001', '2', 'off', True)
    if len(rows) != 1 or rows[0].get('compileFailed'):
        raise ValueError(('859 compiler failed', rows))
    row = rows[0]
    row['sourceDependencies'] = [dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(), sha256=sha256(source.with_name('context.h')))]
    directory = WORK / name / 'canonical'
    bindings = qualified_bindings(row)
    if origin is None:
        try:
            proof = validate(row, bindings, directory)
        except ValueError as error:
            if not error.args or not isinstance(error.args[0], dict):
                raise
            proof = error.args[0]
        return dict(source=row, canonicalComparison=proof), (directory / 'caller.bin').read_bytes()
    try:
        canonical = validate(row, bindings, directory)
    except ValueError as error:
        if not error.args or not isinstance(error.args[0], dict):
            raise
        canonical = error.args[0]
    proof, body = link_private(row, bindings, directory, WORK / name / 'private', origin)
    return dict(source=row, canonicalComparison=canonical, privateLink=proof), body


def compact(result):
    return {key: value for key, value in result.items() if key not in ['observableMemory', 'rows', 'state', 'actors', 'cache']} | dict(rowsHex=result['rows'].hex(), stateHex=result['state'].hex(), actorsHex=result['actors'].hex(), cacheHex=result['cache'].hex(), observableMemorySha256=hashlib.sha256(result['observableMemory']).hexdigest())


def execute():
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('859 pinned runtime differs')
    pins = read_json(ROOT / 'evidence/verification/ov001-writer859-inputs-20261102.json')
    for row in pins['files']:
        if sha256(ROOT / row['path']) != row['sha256']:
            raise ValueError(('859 input differs', row['path']))
    mainInfo, main, unused = measured_module('main')
    moduleInfo, overlay, unused = measured_module('ov001')
    candidate, body = build(SOURCE / 'source.c', 'candidate')
    if candidate['canonicalComparison'].get('exactCallerBytes'):
        raise ValueError('859 research mismatch unexpectedly changed; review separately')
    template = (SOURCE / 'source.c').read_text()
    wrongReturn = template.replace('    return var_r5;', '    return 0U;')
    old = 'M2C_FIELD(temp_r6_2, u8 *, 0x1FE) = temp_r7;'
    wrongSelector = template.replace(old, 'M2C_FIELD(temp_r6_2, u8 *, 0x1FE) = 0;')
    if wrongReturn == template or wrongSelector == template:
        raise ValueError('859 whole-C control site absent')
    images = {}
    controls = []
    for index, (name, text) in enumerate([('wrong-return', wrongReturn), ('wrong-selector', wrongSelector)]):
        origin = 0x02650000 + index * 0x2000
        directory = ROOT / 'nonmatching/overlay-lane/20261102-writer859' / name
        directory.mkdir(parents=True, exist_ok=True)
        source = directory / 'source.c'
        if source.exists() and source.read_text() != text:
            raise ValueError('859 frozen control changed')
        source.write_text(text)
        source.with_name('context.h').write_bytes((SOURCE / 'context.h').read_bytes())
        proof, wrong = build(source, name, origin)
        images[origin] = wrong
        controls.append(dict(name=name, origin=origin, proof=proof, actualTopReturns=0, rejected=0, positive=0))
    totals = dict(pairs=0, actualTopReturns=0, actualNativeReturnInstructions=0, suppliedCalls=0, independentModelPairs=0)
    pcs = set()
    scratchDifferences = set()
    traces = []
    cases = []
    for profile in G.profiles():
        results = []
        failures = []
        for kind, entry in [('native', M.ENTRY), ('candidate', M.ENTRY)] + [(row['name'], row['origin']) for row in controls]:
            vm = M.Machine(main, overlay, images, profile)
            if kind == 'candidate':
                vm.u.mem_write(M.ENTRY, body)
            result = vm.run(entry)
            result['kind'] = kind
            results.append(result)
            failures.append(G.model(vm, result))
        original, hypothesis = results[:2]
        if failures[0] or failures[1]:
            write_json(ROOT / 'evidence/attempts/ov001-writer859-model-rejected-20261102.json', dict(profile=profile, failures=failures, results=list(map(compact, results))))
            raise ValueError(('859 model failed', profile['ordinal'], failures[:2]))
        fields = ['calls', 'writes', 'rows', 'state', 'actors', 'cache', 'observableMemory', 'actualNativeReturnInstructions']
        differences = [field for field in fields if original[field] != hypothesis[field]]
        if differences or original['registers'][0] != hypothesis['registers'][0]:
            raise ValueError(('859 consumed ABI/effect difference', profile['ordinal'], differences))
        scratch = [index for index in [1, 2, 3, 12] if original['registers'][index] != hypothesis['registers'][index]]
        scratchDifferences.update(scratch)
        pcs.update(original['ownPcs'])
        totals['pairs'] += 1
        totals['actualTopReturns'] += 2
        totals['independentModelPairs'] += 1
        count = original['actualNativeReturnInstructions'] + hypothesis['actualNativeReturnInstructions']
        totals['actualNativeReturnInstructions'] += count
        totals['suppliedCalls'] += len(original['calls']) + len(hypothesis['calls'])
        for index, control in enumerate(controls):
            control['actualTopReturns'] += 1
            control['rejected' if failures[index + 2] else 'positive'] += 1
        trace = dict(profile=profile, results=list(map(compact, results)), modelFailures=failures, consumedAbiDifferences=differences, scratchRegisterDifferences=scratch, cpsrDiffers=original['cpsr'] != hypothesis['cpsr'])
        raw = json.dumps(trace, sort_keys=True, separators=(',', ':')).encode()
        cases.append(dict(ordinal=profile['ordinal'], traceSha256=hashlib.sha256(raw).hexdigest(), actualTopReturns=2, actualNativeDependencyReturns=count))
        traces.append(trace)
    if any(not row['rejected'] for row in controls):
        raise ValueError('859 returning wrong-C rejection missing')
    raw = json.dumps(traces, sort_keys=True, separators=(',', ':')).encode()
    artifact = ROOT / 'evidence/generated/ov001-writer859-traces-20261102.json.gz'
    artifact.write_bytes(gzip.compress(raw, mtime=0))
    report = dict(schemaVersion=1, romSha256=configuration()['romSha256'], processor='arm9', program='', module='ov001', moduleSha256=moduleInfo['sha256'], mainSha256=mainInfo['sha256'], sourceCredit=0, canonicalMatchedFunctions=0, canonicalMatchedBytes=0, allPassed=True, candidate=candidate, totals=totals, consumedAbiAndOrderedOwnEffectsEqual=True, completeObservableRamEqual=True, sourceScratchRegisterDifferences=sorted(scratchDifferences), nativeOwnInstructionAddresses=sorted(pcs), cases=cases, negativeEvidence=controls, generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(), sha256=sha256(artifact), uncompressedSha256=hashlib.sha256(raw).hexdigest()), limits=['Case2-only behavior-qualified near C; whole1132 native span remains nonmatching, compiled1116 with canonical comparison preserved. No source/module/whole-ROM credit.', 'Raw context2239C10+0C=2, valid selected slot0..2, row/actor/cache initialization and all four UI/controller callbacks are explicitly supplied. No ordinary-scene reachability or valid selector/domain meaning is inferred.', 'All256 incoming byte selectors and all byte flag values are exercised, with equal/different previous-action comparisons and actual22360/DB438 helpers. Original formal arity/types and other switch cases remain unqualified.', 'Exact own effects: selector is mirrored to cache222EDCC+slot and actor+1FE; comparison with actor+35C clears/sets bit2 of actor+35D; selected row+12/+13 and context+0A are updated. Those fields remain raw.', 'Physical caller-saved scratch/CPSR/call-unused-word differences remain recorded rather than asserted equal. Both machines properly return with callee-saved GPRs and SP intact.', 'Observable RAM comparison excludes only original caller code storage and bounded callee-private stack below SP; all shared private wrong-image storage is identical across executions.', 'Actual lower callback behavior, malformed/negative slots, other modes, full battle/action semantics, source-to-host execution and record33 lifecycle remain unsupported.'])
    write_json(ROOT / 'evidence/application/ov001-writer859-behavior-20261102.json', report)
    print(dict(**totals, sourceCredit=0, scratchRegisters=sorted(scratchDifferences), controls=[{key: row[key] for key in ['name', 'actualTopReturns', 'rejected', 'positive']} for row in controls]), flush=True)


if __name__ == '__main__':
    execute()
