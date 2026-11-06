import copy
from project import ROOT, read_json, write_json
import interpreted_reset_sources as reset


def main():
    relative = 'evidence/matches/scripts-20261030-world32.json'
    original = read_json(ROOT / relative)
    batch = reset.candidates(original, relative, ['match_scr_world32_20261030_batch09.py'])[0]
    inventory = read_json(ROOT / 'evidence/encounter/scripts-inventory-20261029.json')
    image = next(row for row in inventory['images'] if row['codeSha256'] == batch['identity']['codeSha256'])
    work = ROOT / 'work/interpreted-reset-proof-negatives'
    work.mkdir(parents=True, exist_ok=True)
    controls = []

    def reject(name, mutate, reason):
        report, accepted = copy.deepcopy(original), copy.deepcopy(batch)
        mutate(report, accepted)
        path = work / 'candidate.json'
        write_json(path, report)
        accepted['report'] = path.relative_to(ROOT).as_posix()
        try:
            reset.validated(report, image, accepted)
        except ValueError as error:
            if reason not in str(error):
                raise AssertionError((name, str(error), reason))
            controls.append({'name': name, 'rejected': True, 'reason': str(error)})
            print({'negativeControl': name, 'rejected': True}, flush=True)
            return
        raise AssertionError('Invalid reset source accepted: ' + name)

    reject('wrong-ROM', lambda r, b: r.update(romSha256='0' * 64), 'report identity differs')
    reject('wrong-native-namespace', lambda r, b: b['nativeModuleHashes'].update(main='0' * 64), 'native VM namespace differs')
    reject('whole-ROM-claim', lambda r, b: r.update(wholeRomSourceMatch=True), 'partial source claims whole ROM')
    reject('false-general-C', lambda r, b: r['sourceOnlyBuilds'][0]['build']['compilerEvidence'].update(generalCCompilerClaimed=True), 'language/runtime scope differs')
    reject('concurrent-scratch-calls', lambda r, b: r['boundariesAndLinks'].update(serializedCompleteCallsOnly=False), 'language/runtime scope differs')
    reject('duplicate-callee-credit', lambda r, b: r.update(reusedSourceLinkedCalleeNewCredit=1368), 'No additional credit')
    reject('original-callee-credit', lambda r, b: r.update(qualifiedOriginalCalleeSourceCredit=4), 'No additional credit')
    reject('false-entry-return', lambda r, b: r['differential']['cases'][0]['first'].update(entry32Returned=False), 'Whole caller return')
    reject('missing-formal-thread-case', lambda r, b: r['differential']['cases'].pop(), 'All4threads/4formal inputs')
    reject('invented-renewability', lambda r, b: r['differential'].update(naturalSceneOrRenewabilityMeaningProven=True), 'Execution scope/bounds')
    reject('inflated-native-return-count', lambda r, b: r.update(actualReturningCallsTotal=52077), 'Paired whole-entry proof totals')
    reject('truncated-owned-range', lambda r, b: b['range'].update(bytes=3736), 'frozen complete range differs')
    unit = reset.validated(original, image, batch)
    result = {'passed': True, 'controls': controls, 'sourceUnits': 1,
              **{key: unit[key] for key in ('sourceByteCredit', 'completeScrEntryExecutions',
                 'nativeRoutineReturnObservations', 'sourceLinkedCalleeReuseBytes', 'sourceLinkedCalleeNewCredit')},
              'completeImages': 0, 'nativeSourceByteCredit': 0}
    write_json(ROOT / 'evidence/verification/interpreted-reset-source-negatives-20261030.json', result)
    print({key: value for key, value in result.items() if key != 'controls'}, flush=True)


if __name__ == '__main__':
    main()
