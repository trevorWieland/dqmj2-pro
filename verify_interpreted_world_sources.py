import copy
from project import ROOT, read_json, write_json
import interpreted_world_sources as world


def main():
    original = read_json(ROOT / 'evidence/matches/scripts-20261030-world34.json')
    batch = world.candidates(original, 'evidence/matches/scripts-20261030-world34.json',
                             ['match_scr_world34_20261030_batch08.py'])[0]
    inventory = read_json(ROOT / 'evidence/encounter/scripts-inventory-20261029.json')
    image = next(row for row in inventory['images'] if row['codeSha256'] == batch['identity']['codeSha256'])
    work = ROOT / 'work/interpreted-world-proof-negatives'
    work.mkdir(parents=True, exist_ok=True)
    controls = []

    def reject(name, mutate, reason):
        report, accepted = copy.deepcopy(original), copy.deepcopy(batch)
        mutate(report, accepted)
        path = work / 'candidate.json'
        write_json(path, report)
        accepted['report'] = path.relative_to(ROOT).as_posix()
        try:
            world.validated(report, image, accepted)
        except ValueError as error:
            if reason not in str(error):
                raise AssertionError((name, 'Unexpected rejection', str(error), reason))
            controls.append({'name': name, 'rejected': True, 'reason': str(error)})
            print({'negativeControl': name, 'rejected': True}, flush=True)
            return
        raise AssertionError('Invalid world source accepted: ' + name)

    reject('wrong-ROM', lambda r, b: r.update(romSha256='0' * 64), 'report identity differs')
    reject('wrong-class', lambda r, b: r.update(evidenceClass='generated-CFG'), 'report identity differs')
    reject('wrong-native-namespace', lambda r, b: b['nativeModuleHashes'].update(main='0' * 64), 'native VM namespace differs')
    reject('whole-ROM-claim', lambda r, b: r.update(wholeRomSourceMatch=True), 'partial source claims whole ROM')
    reject('private-global-lifetime', lambda r, b: r['boundariesAndModuleObjects'].update(moduleGlobalObjectsAreNotPrivateLocals=False),
           'global/language/runtime scope differs')
    reject('false-general-C-support', lambda r, b: r['sourceOnlyBuild'].update(generalCCompilerClaimed=True), 'global/language/runtime scope differs')
    reject('missing-byte-domain-control', lambda r, b: r['compilerControls']['all256ByteValues'].pop(), 'Exhaustive numeric-byte domain')
    reject('false-whole-entry-return', lambda r, b: r['differential']['cases'][0]['first'].update(completeEntry34Returned=False),
           'Whole entry termination')
    reject('missing-thread', lambda r, b: r['differential']['cases'].pop(), 'Complete cases/all4threads')
    reject('missing-branch-outcome', lambda r, b: r['differential']['branchCoverage'].__setitem__('64528', [True]), 'Every own branch outcome')
    reject('clobbered-other-slots', lambda r, b: r['differential']['cases'][0]['first'].update(allOtherSlotsPreserved=False), 'Whole256-slot file')
    reject('lost-global-value', lambda r, b: r['differential']['cases'][0]['first']['moduleGlobalWords'].update(cached_numeric_twenty=0x7FC00001),
           'Retained module objects')
    reject('truncated-range', lambda r, b: b['range'].update(bytes=1348), 'frozen complete range differs')
    unit = world.validated(original, image, batch)
    assert unit['historicalCallerPrefix']['outerEntryReturnCredit'] == 0
    result = {'passed': True, 'controls': controls, 'sourceUnits': 1, 'sourceBytes': unit['sourceByteCredit'],
              'completeScrEntryExecutions': unit['completeScrEntryExecutions'],
              'nativeRoutineReturnObservations': unit['nativeRoutineReturnObservations'],
              'separateCompilerControlNativeReturns': unit['separateCompilerControlNativeReturns'],
              'historicalOuterEntryReturnCredit': 0, 'completeImages': 0, 'nativeSourceByteCredit': 0}
    write_json(ROOT / 'evidence/verification/interpreted-world-source-negatives-20261030.json', result)
    print({key: value for key, value in result.items() if key != 'controls'}, flush=True)


if __name__ == '__main__':
    main()
