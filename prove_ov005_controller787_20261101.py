import gzip
import hashlib
import json
import struct
import sys
import match_runtime as c
import unicorn
from project import ROOT, sha256, write_json
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from link_private_overlay_hypothesis_20261101 import link_private
import ov005_controller787_machine_20261101 as M
BASE = ROOT / 'nonmatching/overlay-lane/20261101-controller787'

def build(variant, origin):
    source = BASE / variant / 'source.c'
    c.WORK = ROOT / 'work/ol787' / variant / 'compile'
    rows, unused = c.compare(source, 'ov005', '2', 'off', False)
    row = rows[0]
    row['sourceDependencies'] = [dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(), sha256=sha256(source.with_name('context.h')))]
    directory = ROOT / 'work/ol787' / variant / 'canonical'
    bindings = qualified_bindings(row)
    try:
        canonical = validate(row, bindings, directory)
    except ValueError as error:
        if not isinstance(error.args[0], dict):
            raise
        canonical = error.args[0]
    if canonical.get('exactCallerBytes'):
        raise ValueError('787 near unexpectedly exact; requires separate acceptance protocol')
    proof, body = link_private(row, bindings, directory, ROOT / 'work/ol787' / variant / 'private', origin)
    return (row, canonical, proof, body)

def profiles():
    rows = []
    for state in list(range(29)) + [29, 255]:
        for v in range(6):
            rows.append(dict(ordinal=len(rows), state=state, mode=[0, 1, 255][v % 3], serviceWord=v // 3, selector=[7, 8, 9][v % 3], branch=v & 1, counter=250 if v & 1 else 3, delta=[-1, 0, 1][v % 3], position=[-512, 0, 512][v % 3], mask=[0, 256, 512, 4095, 2048, 65535][v], flags=2684354560 if v & 1 else 0))
    for mode in range(256):
        rows.append(dict(ordinal=len(rows), state=11, mode=mode, serviceWord=0, selector=7, branch=0, counter=250, delta=1, position=0, mask=4660, flags=0))
    return rows

def compact(result):
    return dict(rawR0=result['rawR0'], actuallyReturned=result['actuallyReturned'], getterReturns=result['getterReturns'], providedCalls=[dict(target=hex(a), result=b) for a, b in result['providedCalls']], rawCalls=result['rawCalls'], writes=result['writes'], ownContextHex=result['ownContext'].hex(), mmioSha256=hashlib.sha256(result['mmio']).hexdigest(), nonStackRamSha256=hashlib.sha256(result['state'] + result['topRam']).hexdigest(), instructions=result['instructions'], nativeEntries=result['nativeEntries'], nativeCompletions=result['nativeCompletions'], actualExtraReturnInstructions=result['actualExtraReturnInstructions'], slotModels=result['slotModels'], animationModels=result['animationModels'], modelFailures=result['modelFailures'], r3StackReads=result['r3StackReads'], r3SemanticReads=result['r3SemanticReads'])

def main():
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('787 pinned runtime differs')
    mainInfo, main, _ = measured_module('main')
    overlayInfo, overlay, _ = measured_module('ov005')
    near = build('repaired-third', 40173568)
    wrong = build('wrong-return', 40181760)
    missing = build('missing-third', 40189952)
    source32 = ROOT / 'src/runtime/20261101_cell_tick_explicit/native_main_0203515c.c'
    c.WORK = ROOT / 'work/ol787/cell32/compile'
    cellRows, _ = c.compare(source32, 'main', '2', 'off', False)
    cellRow = cellRows[0]
    cellProof = validate(cellRow, qualified_bindings(cellRow), ROOT / 'work/ol787/cell32/link')
    cellBody = (ROOT / 'work/ol787/cell32/link/caller.bin').read_bytes()
    if cellBody != main[217436:217468]:
        raise ValueError('787 Root32 reconstructed body differs')
    images = {40173568: near[3], 40181760: wrong[3], 40189952: missing[3], 33771868: cellBody}
    providers = near[2]['qualifiedZeroCodeAnchors']
    traces = []
    summaries = []
    totals = dict(pairs=0, actualTopReturns=0, actualNativeGetterReturns=0, suppliedCalls=0, independentModelPairs=0, orderedWriteDifferences=0, rawArgumentDifferences=0, actualExtraReturnInstructions=0, nativeEntryCompletions=0, slotModelPairs=0, animationModelPairs=0, r3SemanticReads=0, returningMissingThirdControls=0, missingThirdRejected=0, missingThirdPositive=0, returningWrongControls=0, wrongRejected=0, wrongPositive=0)
    for profile in profiles():
        originalVm = M.Machine(main, overlay, images, providers, profile)
        original = originalVm.run(M.ENTRY)
        candidateVm = M.Machine(main, overlay, images, providers, profile)
        candidate = candidateVm.run(40173568)
        wrongVm = M.Machine(main, overlay, images, providers, profile)
        bad = wrongVm.run(40181760)
        missingVm = M.Machine(main, overlay, images, providers, profile)
        omitted = missingVm.run(40189952)
        tested = M.model(originalVm, original)
        M.model(candidateVm, candidate)
        keys = ['rawR0', 'providedCalls', 'getterReturns', 'ownContext', 'mmio', 'state', 'topRam', 'actualExtraReturnInstructions']
        differences = [key for key in keys if original[key] != candidate[key]]
        if differences:
            write_json(ROOT / 'evidence/attempts/ov005-controller787-rejected-case-20261101.json', dict(profile=profile, differences=differences, original=compact(original), candidate=compact(candidate)))
            raise ValueError(('787 candidate differs', profile, differences))
        rejected = any((original[key] != bad[key] for key in keys))
        missingRejected = any((original[key] != omitted[key] for key in keys)) or bool(omitted['modelFailures'])
        totals['returningMissingThirdControls'] += 1
        totals['missingThirdRejected' if missingRejected else 'missingThirdPositive'] += 1
        totals['actualExtraReturnInstructions'] += original['actualExtraReturnInstructions'] + candidate['actualExtraReturnInstructions']
        totals['nativeEntryCompletions'] += len(original['nativeCompletions']) + len(candidate['nativeCompletions'])
        totals['slotModelPairs'] += len(original['slotModels'])
        totals['animationModelPairs'] += len(original['animationModels'])
        totals['r3SemanticReads'] += len(original['r3SemanticReads']) + len(candidate['r3SemanticReads'])
        rawDiff = sum((a['arguments'] != b['arguments'] or a['stackWords'] != b['stackWords'] for a, b in zip(original['rawCalls'], candidate['rawCalls'])))
        writeDiff = original['writes'] != candidate['writes']
        totals['pairs'] += 1
        totals['actualTopReturns'] += 2
        totals['actualNativeGetterReturns'] += original['getterReturns'] + candidate['getterReturns']
        totals['suppliedCalls'] += len(original['providedCalls']) + len(candidate['providedCalls'])
        totals['independentModelPairs'] += tested
        totals['orderedWriteDifferences'] += writeDiff
        totals['rawArgumentDifferences'] += rawDiff
        totals['returningWrongControls'] += 1
        totals['wrongRejected' if rejected else 'wrongPositive'] += 1
        summaries.append(dict(profile=profile, rawR0=original['rawR0'], nativeGetterReturns=original['getterReturns'], suppliedCalls=len(original['providedCalls']), independentModel=bool(tested), orderedWritesDiffer=writeDiff, rawArgumentDifferences=rawDiff, wrongRejected=rejected))
        traces.append(dict(profile=profile, original=compact(original), candidate=compact(candidate), wrong=compact(bad), missingThird=compact(omitted), missingThirdRejected=missingRejected, differences=differences))
    if totals['rawArgumentDifferences'] or totals['orderedWriteDifferences']:
        raise ValueError('787 full supplied-call words or write order differ')
    if not totals['wrongRejected'] or totals['independentModelPairs'] != 30:
        raise ValueError('787 controls/model coverage differ')
    direct = []
    for label, active, flags in [('inactive', 0, 0), ('active-positive', 1, 0), ('active-negative', 1, 2684354560)]:
        baseline = None
        for poison in [0, 1, 2147483648, 4294967295]:
            p = dict(profiles()[0], ordinal=787000, branch=active, flags=flags)
            vm = M.Machine(main, overlay, images, providers, p)
            result = vm.run(33851972, [M.CONTROLLER, 1, 3405643776, poison])
            M.model(vm, result)
            meaningful = {key: result[key] for key in ['rawR0', 'ownContext', 'mmio', 'state', 'topRam']}
            if result['rawR0'] != 0 or len(result['animationModels']) != 1 or result['providedCalls'] or result['r3SemanticReads']:
                raise ValueError('787 original R3 poison path invalid')
            if baseline is None:
                baseline = meaningful
            elif baseline != meaningful:
                raise ValueError('787 original R3 poison changes actual bounded effects')
            direct.append(dict(domain=label, incomingR3=poison, result=compact(result)))
    raw = json.dumps(dict(controllerPairs=traces, directR3Poison=direct), sort_keys=True, separators=(',', ':')).encode()
    path = ROOT / 'evidence/generated/ov005-controller787-functional-traces-20261101.json.gz'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(gzip.compress(raw, mtime=0))
    report = dict(schemaVersion=1, sourceCredit=0, nativeMatchingCredit=0, compiledCandidateBytes=near[0]['compiledBytes'], nativeBytes=2328, canonicalMatchingBytes=near[1]['matchingBytes'], candidate=near[0], canonicalComparison=near[1], privateLink=near[2], negativeEvidence=dict(returnWord=dict(source=wrong[0], canonicalComparison=wrong[1], privateLink=wrong[2]), missingThird=dict(source=missing[0], canonicalComparison=missing[1], privateLink=missing[2])), zeroCreditCellSourceAlternative=dict(source=cellRow, genuineLinkComparison=cellProof, installedAtCanonicalAddress=True, sourceCredit=0), romSha256=sha256(ROOT / 'inputs/game.nds'), mainSha256=mainInfo['sha256'], module='ov005', moduleSha256=overlayInfo['sha256'], address='0x021dcc78', mode='arm', processor='arm9', program='', generatorSha256=sha256(__file__), machineSha256=sha256(ROOT / 'ov005_controller787_machine_20261101.py'), totals=totals, caseSummaries=summaries, directR3Poison=dict(actualTopReturns=len(direct), actualExtraReturnInstructions=sum((r['result']['actualExtraReturnInstructions'] for r in direct)), nativeEntryCompletions=sum((len(r['result']['nativeCompletions']) for r in direct)), suppliedCalls=sum((len(r['result']['providedCalls']) for r in direct)), cases=direct), fullTraces=dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path), uncompressedSha256=hashlib.sha256(raw).hexdigest()), allPassed=True, fullObservedProvidedArgumentsEqual=totals['rawArgumentDifferences'] == 0, fullBehaviorQualified=False, runtime=dict(python=sys.version.split()[0], unicorn=unicorn.__version__, cpu='ARM946'), limits=['Only own return/final nonstack RAM/MMIO/call targets and supplied return values agree in these provided-callee scenarios.', 'Original raw-byte getter, zero-input41764/E0A84/2A634, slot forwarding/handle-field/status and inactive/active-no-advance animation chains execute;379EC and remaining source-body services are supplied without RAM effects. Full helper domains and ordinary scenes remain unqualified.', 'Full observed provided-call argument/stack snapshots and ordered writes are compared; remaining service effects and asynchronous/device behavior are unqualified.', 'Stack027E0000..027F0100 is excluded from RAM comparison for private PC/LR/frame storage. All three private code images are mapped identically in every VM; no code-storage exclusions.', 'Wrong-control executions are counted separately from positive actualTopReturns/nativeGetterReturns; early-return positive controls are retained.', 'No exact source credit, shared source/preference changes or application changes.'])
    write_json(ROOT / 'evidence/attempts/ov005-controller787-functional-near-20261101.json', report)
    print(totals, flush=True)
if __name__ == '__main__':
    main()
