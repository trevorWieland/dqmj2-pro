import copy
from project import ROOT, read_json, write_json
import interpreted_runtime_loop_sources as loops


def main():
    relative = 'evidence/matches/scripts-20261030-runtime-flags.json'
    original = read_json(ROOT / relative)
    batch = loops.candidates(original, relative, [loops.GENERATOR])[0]
    inventory = read_json(ROOT / 'evidence/encounter/scripts-inventory-20261029.json')
    image = next(row for row in inventory['images'] if row['codeSha256'] == batch['identity']['codeSha256'])
    work = ROOT / 'work/interpreted-runtime-loop-proof-negatives'
    work.mkdir(parents=True, exist_ok=True)
    controls = []

    def reject(name, mutate, reason):
        report, accepted = copy.deepcopy(original), copy.deepcopy(batch)
        mutate(report, accepted)
        path = work / 'candidate.json'
        write_json(path, report)
        accepted['report'] = path.relative_to(ROOT).as_posix()
        try:
            loops.validated(report, image, accepted)
        except (ValueError, AssertionError, OSError, IndexError, KeyError) as error:
            if reason not in str(error):
                raise AssertionError((name, 'Unexpected rejection', str(error), reason))
            controls.append({'name': name, 'rejected': True, 'reason': str(error)})
            print({'negativeControl': name, 'rejected': True}, flush=True)
            return
        raise AssertionError('Invalid runtime-loop proof accepted: ' + name)

    reject('wrong-ROM', lambda r, b: r.update(romSha256='0' * 64), 'report identity differs')
    reject('wrong-class', lambda r, b: r.update(evidenceClass='opcode-array'), 'report identity differs')
    reject('wrong-native-namespace', lambda r, b: b['nativeModuleHashes'].update(itcm='0' * 64), 'native VM namespace differs')
    reject('whole-ROM-claim', lambda r, b: r.update(wholeRomSourceMatch=True), 'partial source claims whole ROM')
    reject('wrong-generator', lambda r, b: r.update(generatorSha256='0' * 64), 'frozen generator differs')
    reject('validator-pin-tamper', lambda r, b: b['sourceHashes'].__setitem__('validate_scr_runtime_flags_20261030_batch12.py', '0' * 64),
        'frozen source/profile/validator closure changed')
    reject('entry-table-substitution', lambda r, b: b['identity'].update(entryTableSha256='0' * 64), 'inventoried image differs')
    reject('false-general-C', lambda r, b: r['sourceOnlyBuild']['compilerEvidence'].update(generalCCompilerClaimed=True),
        'language/integer-domain/entry scope differs')
    reject('unrolled-loop-claim', lambda r, b: r['sourceOnlyBuild']['compilerEvidence'].update(constantLoopUnrolled=True),
        'language/integer-domain/entry scope differs')
    reject('inexact-integer-domain', lambda r, b: r['sourceOnlyBuild']['compilerEvidence']['counter'].update(allIntegerValuesExactlyRepresentable=False),
        'language/integer-domain/entry scope differs')
    reject('opaque-program-completeness', lambda r, b: r['boundariesAndStorage'].update(opaqueNativeOrComputedSlotReferenceCoverageComplete=True),
        'language/integer-domain/entry scope differs')
    reject('unreachable-join-executed', lambda r, b: r['executedOwnRecordPcs'].append(1248), 'Only reachable records count as executed')
    reject('removed-unreachable-join', lambda r, b: r['boundariesAndStorage']['compilerGeneratedUnreachableJoins'].pop(),
        'Complete direct/private bounds')
    reject('invented-outside-counter-reference', lambda r, b: r['boundariesAndStorage'].update(knownOutsideCounterReferences=1),
        'Complete direct/private bounds')
    reject('bytecode-input-to-compiler', lambda r, b: r['sourceOnlyBuild'].update(originalBytecodeCompilerInput=True),
        'Actual source-only command/directory')
    reject('false-entry-return', lambda r, b: r['differential']['cases'][0]['first'].update(completeEntryReturned=False),
        'Exact complete runtime-loop trace/private return')
    reject('wrong-counter-increment', lambda r, b: r['differential']['cases'][0]['first']['counterValuesAfterIncrements'].__setitem__(0, 452),
        'Every runtime counter and primary index')
    reject('missing-setter-iteration', lambda r, b: r['differential']['cases'][0]['first']['setters'].pop(),
        'Every runtime counter and primary index')
    reject('wrong-primary-index', lambda r, b: r['differential']['cases'][0]['first']['setters'][0].update(index=449),
        'Every runtime counter and primary index')
    reject('missing-loop-exit', lambda r, b: r['differential']['cases'][0]['first']['branchOutcomes'].__setitem__(-1, False),
        'Every loop continuation and sole exit')
    reject('wrong-aligned-word-store', lambda r, b: r['differential']['cases'][0]['first']['orderedPrimaryWordStores'][0].update(value=1),
        'Ordered aligned-word RMW and neighboring bytes')
    reject('changed-other-VM-slots', lambda r, b: r['differential']['cases'][0]['first'].update(allOtherSlotsPreserved=False),
        'Exact floating representation')
    reject('changed-neighboring-primary-bits', lambda r, b: r['differential']['cases'][0]['first'].update(neighboringPrimaryBitsPreserved=False),
        'Exact floating representation')
    reject('missing-boundary-control', lambda r, b: r['compilerControls']['boundaryControls'].pop(),
        'Actual boundary and word-crossing controls')
    reject('false-source-rejection', lambda r, b: r['compilerControls']['rejectedSourceProfiles'][0].update(rejectedBeforeOutput=False),
        'Reproducible source/domain error')
    reject('helper-count-as-entry-count', lambda r, b: r.update(pairedCompleteOwnEntryExecutions=r['pairedNativeReturningCalls']),
        'Separate complete-entry/native helper/setter counts')
    reject('setter-count-as-helper-count', lambda r, b: r.update(pairedPrimarySetterExecutions=r['pairedNativeReturningCalls']),
        'Separate complete-entry/native helper/setter counts')
    reject('post-fault-state-credit', lambda r, b: r.update(postFaultStateUsedForProof=True), 'No excess credit/post-fault proof')
    reject('native-source-credit', lambda r, b: r.update(nativeExecutableByteCredit=220), 'No excess credit/post-fault proof')
    reject('missing-source-product', lambda r, b: r['sourceOnlyBuild']['emittedBody'].update(
        path='work/interpreted-runtime-loop-proof-negatives/missing.scrfunc'), 'missing.scrfunc')
    reject('truncated-complete-range', lambda r, b: b['range'].update(bytes=208), 'frozen complete range differs')
    unit = loops.validated(original, image, batch)
    assert unit['nativeByteCredit'] == unit['completeImageCredit'] == 0
    assert unit['sourceByteCredit'] == 220 and unit['sourceUnitCredit'] == 1
    assert unit['runtimeLoop'] and not unit['constantLoopUnrolled']
    result = {'passed': True, 'controls': controls, 'sourceUnits': 1, 'sourceBytes': 220,
        'completeScrEntryExecutions': unit['completeScrEntryExecutions'],
        'nativeRoutineReturnObservations': unit['nativeRoutineReturnObservations'],
        'primarySetterExecutions': unit['primarySetterExecutions'],
        'separateCompilerControlNativeReturns': unit['separateCompilerControlNativeReturns'],
        'compilerGeneratedUnreachableJoinBytes': unit['compilerGeneratedUnreachableJoinBytes'],
        'runtimeLoopUnrolled': False, 'completeImages': 0, 'nativeSourceByteCredit': 0}
    write_json(ROOT / 'evidence/verification/interpreted-runtime-loop-source-negatives-20261030.json', result)
    print({key: value for key, value in result.items() if key != 'controls'}, flush=True)


if __name__ == '__main__':
    main()
