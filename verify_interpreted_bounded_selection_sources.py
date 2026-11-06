import copy
from project import ROOT, read_json, write_json
import interpreted_bounded_selection_sources as bounded


def main():
    relative = 'evidence/matches/scripts-20261030-world17.json'
    original = read_json(ROOT / relative)
    batch = bounded.candidates(original, relative, ['match_scr_world17_20261030_batch11.py'])[0]
    inventory = read_json(ROOT / 'evidence/encounter/scripts-inventory-20261029.json')
    image = next(row for row in inventory['images'] if row['codeSha256'] == batch['identity']['codeSha256'])
    work = ROOT / 'work/interpreted-bounded-selection-proof-negatives'
    work.mkdir(parents=True, exist_ok=True)
    controls = []

    def reject(name, mutate, reason):
        report, accepted = copy.deepcopy(original), copy.deepcopy(batch)
        mutate(report, accepted)
        path = work / 'candidate.json'
        write_json(path, report)
        accepted['report'] = path.relative_to(ROOT).as_posix()
        try:
            bounded.validated(report, image, accepted)
        except (ValueError, AssertionError, OSError, IndexError, KeyError) as error:
            if reason not in str(error):
                raise AssertionError((name, 'Unexpected rejection', str(error), reason))
            controls.append({'name': name, 'rejected': True, 'reason': str(error)})
            print({'negativeControl': name, 'rejected': True}, flush=True)
            return
        raise AssertionError('Invalid bounded selection accepted: ' + name)

    reject('wrong-ROM', lambda r, b: r.update(romSha256='0' * 64), 'report identity differs')
    reject('wrong-class', lambda r, b: r.update(evidenceClass='opcode-array'), 'report identity differs')
    reject('wrong-native-namespace', lambda r, b: b['nativeModuleHashes'].update(itcm='0' * 64), 'native VM namespace differs')
    reject('whole-ROM-claim', lambda r, b: r.update(wholeRomSourceMatch=True), 'partial source claims whole ROM')
    reject('wrong-generator', lambda r, b: r.update(generatorSha256='0' * 64), 'frozen generator differs')
    reject('validator-pin-tamper', lambda r, b: b['sourceHashes'].__setitem__('validate_scr_world17_20261030_batch11.py', '0' * 64),
           'frozen source/profile/validator closure changed')
    reject('entry-table-substitution', lambda r, b: b['identity'].update(entryTableSha256='0' * 64), 'inventoried image differs')
    reject('false-general-C', lambda r, b: r['sourceOnlyBuild']['compilerEvidence'].update(generalCCompilerClaimed=True), 'language/entry-domain scope differs')
    reject('opaque-program-completeness', lambda r, b: r['boundariesAndStorage'].update(opaqueNativeOrComputedSlotReferenceCoverageComplete=True),
           'language/entry-domain scope differs')
    reject('unreachable-join-coverage', lambda r, b: r['executedOwnRecordPcs'].append(59192), 'Only reachable entry-domain records executed')
    reject('removed-unreachable-join', lambda r, b: r['boundariesAndStorage']['compilerGeneratedUnreachableJoins'].pop(), 'Current direct/private bounds')
    reject('last-false-outcome-injection', lambda r, b: r['differential']['branchCoverage']['60140'].insert(0, False), 'All feasible branch outcomes')
    reject('out-of-domain-RNG', lambda r, b: r['excludedBranchOutcomes'][0].update(outOfDomainRngInjected=True), 'Explicit impossible outcome')
    reject('invalid-selection', lambda r, b: r['differential']['cases'][48]['first'].update(selection=6), 'Typed inputs/domain/RNG effects')
    reject('missing-byte-domain-case', lambda r, b: r['compilerControls']['all256ByteRelationCases'].pop(), 'Exhaustive byte comparisons')
    reject('false-whole-entry-return', lambda r, b: r['differential']['cases'][0]['first'].update(completeEntry17Returned=False), 'Complete own entry return')
    reject('helper-count-as-entry-count', lambda r, b: r.update(pairedCompleteOwnEntryExecutions=r['pairedNativeReturningCalls']), 'Separate native/complete-entry totals')
    reject('native-source-credit', lambda r, b: r.update(nativeExecutableByteCredit=1148), 'Zero excess credit')
    reject('missing-source-product', lambda r, b: r['sourceOnlyBuild']['emittedBody'].update(path='work/interpreted-bounded-selection-proof-negatives/missing.scrfunc'),
           'missing.scrfunc')
    reject('truncated-range', lambda r, b: b['range'].update(bytes=1112), 'frozen complete range differs')
    unit = bounded.validated(original, image, batch)
    assert unit['nativeByteCredit'] == unit['completeImageCredit'] == 0
    result = {'passed': True, 'controls': controls, 'sourceUnits': 1, 'sourceBytes': unit['sourceByteCredit'],
        'completeScrEntryExecutions': unit['completeScrEntryExecutions'], 'nativeRoutineReturnObservations': unit['nativeRoutineReturnObservations'],
        'separateCompilerControlNativeReturns': unit['separateCompilerControlNativeReturns'],
        'compilerGeneratedUnreachableJoinBytes': unit['compilerGeneratedUnreachableJoinBytes'],
        'excludedLastFalseOutcome': True, 'completeImages': 0, 'nativeSourceByteCredit': 0}
    write_json(ROOT / 'evidence/verification/interpreted-bounded-selection-source-negatives-20261030.json', result)
    print({key: value for key, value in result.items() if key != 'controls'}, flush=True)


if __name__ == '__main__':
    main()
