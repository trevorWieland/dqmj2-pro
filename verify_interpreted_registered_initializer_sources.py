import copy
from project import ROOT, read_json, write_json
import interpreted_registered_initializer_sources as initializer


def main():
    relative = 'evidence/matches/scripts-20261030-registered-initializer.json'
    original = read_json(ROOT / relative)
    batch = initializer.candidates(original, relative, [initializer.GENERATOR])[0]
    image = next(row for row in read_json(ROOT / 'evidence/encounter/scripts-inventory-20261029.json')['images'] if row['codeSha256'] == batch['identity']['codeSha256'])
    directory = ROOT / 'work/interpreted-registered-initializer-proof-negatives'
    directory.mkdir(parents=True, exist_ok=True)
    controls = []

    def reject(name, mutate, reason):
        report, accepted = copy.deepcopy(original), copy.deepcopy(batch)
        mutate(report, accepted)
        path = directory / 'candidate.json'
        write_json(path, report)
        accepted['report'] = path.relative_to(ROOT).as_posix()
        try:
            initializer.validated(report, image, accepted)
        except (ValueError, AssertionError, OSError, KeyError, IndexError) as error:
            if reason not in str(error):
                raise AssertionError((name, 'Unexpected rejection', str(error), reason))
            controls.append({'name': name, 'rejected': True, 'reason': str(error)})
            print({'rejected': name}, flush=True)
            return
        raise AssertionError('Invalid registered initializer source accepted: ' + name)

    reject('wrong-ROM', lambda r, b: r.update(romSha256='0' * 64), 'report identity differs')
    reject('wrong-class', lambda r, b: r.update(evidenceClass='opcode-array'), 'report identity differs')
    reject('native-namespace-substitution', lambda r, b: b['nativeModuleHashes'].update(itcm='0' * 64), 'native VM namespace differs')
    reject('whole-ROM-claim', lambda r, b: r.update(wholeRomSourceMatch=True), 'partial source claims whole ROM')
    reject('generator-tamper', lambda r, b: r.update(generatorSha256='0' * 64), 'frozen generator differs')
    reject('validator-pin-tamper', lambda r, b: b['sourceHashes'].__setitem__('validate_scr_registered_initializer_20261030_batch18.py', '0' * 64),
        'frozen source/profile/validator closure changed')
    reject('entry-table-substitution', lambda r, b: b['identity'].update(entryTableSha256='0' * 64), 'inventoried image differs')
    reject('general-C-claim', lambda r, b: r['sourceOnlyBuild']['compilerEvidence'].update(generalCCompilerClaimed=True), 'language/global/initialization/padding scope differs')
    reject('branch-logic-claim', lambda r, b: r.update(branchDecisionLogicClaimed=True), 'language/global/initialization/padding scope differs')
    reject('module-globals-private', lambda r, b: r['boundariesAndStorage'].update(moduleGlobalsAreNotPrivateLocals=False), 'language/global/initialization/padding scope differs')
    reject('padding-credit', lambda r, b: r['boundariesAndStorage'].update(followingPaddingSourceCredit=8), 'language/global/initialization/padding scope differs')
    reject('natural-producer-claim', lambda r, b: r['boundariesAndStorage'].update(naturalInitializerOrRegistrationCallerReachabilityProven=True),
        'language/global/initialization/padding scope differs')
    reject('source-product-unavailable', lambda r, b: r['sourceOnlyBuild']['emittedBody'].update(path='work/interpreted-registered-initializer-proof-negatives/missing.scrfunc'),
        'missing.scrfunc')
    reject('false-private-return', lambda r, b: r['differential']['cases'][0]['first'].update(completeOwnEntryReturned=False), 'Complete private initializer return')
    reject('wrong-sentinel-write', lambda r, b: r['differential']['cases'][0]['first']['orderedGlobalWordStores'][0].update(value=0),
        'All20 ordered global writes/236 neighbors/persistent bytes')
    reject('lost-neighbor-state', lambda r, b: r['differential']['cases'][0]['first'].update(allOther236SlotsPreserved=False),
        'All20 ordered global writes/236 neighbors/persistent bytes')
    reject('lost-initial-NaN-bits', lambda r, b: r['differential']['cases'][4].update(initialRegisterFileHex='00' * 1024),
        'Raw arbitrary initial module/global and other register state')
    reject('changed-argument-bank', lambda r, b: r['differential']['cases'][0]['second'].update(unchangedArgumentBankSha256='0' * 64),
        'Unchanged nonformal VM argument bank')
    reject('native-count-as-entry-count', lambda r, b: r.update(pairedCompleteOwnEntryExecutions=r['pairedNativeReturningCalls']),
        'Separate complete initializer/native return totals')
    reject('native-source-credit', lambda r, b: r.update(nativeExecutableByteCredit=496), 'Zero excess source/state/image credit')
    reject('wrong-entry-alias', lambda r, b: b['range'].update(entrySlots=[255]), 'frozen complete range differs')
    reject('padding-appended-to-range', lambda r, b: b['range'].update(bytes=504, endExclusivePc=1056), 'frozen complete range differs')
    unit = initializer.validated(original, image, batch)
    assert unit['initializationOnly'] and not unit['branchDecisionLogicClaimed'] and unit['followingPaddingSourceCredit'] == 0
    result = {'passed': True, 'controls': controls, 'sourceUnits': 1, 'sourceBytes': unit['sourceByteCredit'],
        'completeScrEntryExecutions': unit['completeScrEntryExecutions'], 'nativeRoutineReturnObservations': unit['nativeRoutineReturnObservations'],
        'moduleGlobalSlots': unit['moduleGlobalSlots'], 'privateLocalSlots': [], 'initializationOnly': True, 'branchDecisionLogicClaimed': False,
        'nativeSourceCredit': 0, 'completeImageCredit': 0, 'followingPaddingSourceCredit': 0}
    write_json(ROOT / 'evidence/verification/interpreted-registered-initializer-source-negatives-20261030.json', result)
    print({key: value for key, value in result.items() if key != 'controls'}, flush=True)


if __name__ == '__main__':
    main()
