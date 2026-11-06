import copy
from project import ROOT, read_json, write_json
import interpreted_registered_flags_sources as flags


def main():
    relative = 'evidence/matches/scripts-20261030-registered-flags.json'
    original = read_json(ROOT / relative)
    batch = flags.candidates(original, relative, [flags.GENERATOR])[0]
    image = next(row for row in read_json(ROOT / 'evidence/encounter/scripts-inventory-20261029.json')['images'] if row['codeSha256'] == batch['identity']['codeSha256'])
    directory = ROOT / 'work/interpreted-registered-flags-proof-negatives'
    directory.mkdir(parents=True, exist_ok=True)
    controls = []

    def reject(name, mutate, reason):
        report, accepted = copy.deepcopy(original), copy.deepcopy(batch)
        mutate(report, accepted)
        path = directory / 'candidate.json'
        write_json(path, report)
        accepted['report'] = path.relative_to(ROOT).as_posix()
        try:
            flags.validated(report, image, accepted)
        except (ValueError, AssertionError, OSError, KeyError, IndexError) as error:
            if reason not in str(error):
                raise AssertionError((name, 'Unexpected rejection', str(error), reason))
            controls.append({'name': name, 'rejected': True, 'reason': str(error)})
            print({'rejected': name}, flush=True)
            return
        raise AssertionError('Invalid registered-flag source accepted: ' + name)

    reject('wrong-ROM', lambda r, b: r.update(romSha256='0' * 64), 'report identity differs')
    reject('wrong-class', lambda r, b: r.update(evidenceClass='opcode-array'), 'report identity differs')
    reject('native-namespace-substitution', lambda r, b: b['nativeModuleHashes'].update(itcm='0' * 64), 'native VM namespace differs')
    reject('whole-ROM-claim', lambda r, b: r.update(wholeRomSourceMatch=True), 'partial source claims whole ROM')
    reject('generator-tamper', lambda r, b: r.update(generatorSha256='0' * 64), 'frozen generator differs')
    reject('validator-pin-tamper', lambda r, b: b['sourceHashes'].__setitem__('validate_scr_registered_flags_20261030_batch17.py', '0' * 64),
        'frozen source/profile/validator closure changed')
    reject('entry-table-substitution', lambda r, b: b['identity'].update(entryTableSha256='0' * 64), 'inventoried image differs')
    reject('general-C-claim', lambda r, b: r['sourceOnlyBuild']['compilerEvidence'].update(generalCCompilerClaimed=True), 'language/raw-return/global/dynamic-index scope differs')
    reject('integer-return-conflation', lambda r, b: r['sourceOnlyBuild']['compilerEvidence'].update(sourceReturnType='int'), 'language/raw-return/global/dynamic-index scope differs')
    reject('module-globals-private', lambda r, b: r['boundariesAndStorage'].update(moduleGlobalsAreNotPrivateLocals=False), 'language/raw-return/global/dynamic-index scope differs')
    reject('arbitrary-dynamic-index-domain', lambda r, b: r['sourceOnlyBuild']['compilerEvidence'].update(dynamicPrimaryIndexRequiresQualifiedFiniteIntegerDomain=[0, 65535]),
        'language/raw-return/global/dynamic-index scope differs')
    reject('global-domain-claim', lambda r, b: r['sourceOnlyBuild']['compilerEvidence'].update(opaqueGlobalDomainProofClaimed=True), 'language/raw-return/global/dynamic-index scope differs')
    reject('source-product-unavailable', lambda r, b: r['sourceOnlyBuild']['emittedBody'].update(path='work/interpreted-registered-flags-proof-negatives/missing.scrfunc'), 'missing.scrfunc')
    reject('false-private-return', lambda r, b: r['differential']['cases'][0]['first'].update(completeEntryReturned=False), 'Complete private scalar return')
    reject('wrong-first-matching-key', lambda r, b: r['differential']['cases'][0]['first'].update(selectedKeySlot=1), 'Exact scalar/module selection/input/state carry')
    reject('lost-raw-scalar-return', lambda r, b: r['differential']['cases'][0]['first'].update(returnedScalarWord=0), 'Raw scalar return/sentinel/index-local representation')
    reject('wrong-primary-RMW', lambda r, b: r['differential']['cases'][0]['first']['orderedPrimaryWordStores'][0].update(
        value=r['differential']['cases'][0]['first']['orderedPrimaryWordStores'][0]['value'] ^ 1), 'Ordered aligned-word setter/neighbors/all module/global state')
    reject('lost-global-register-state', lambda r, b: r['differential']['cases'][0]['first'].update(allOtherSlotsIncludingModuleGlobalsPreserved=False),
        'Ordered aligned-word setter/neighbors/all module/global state')
    reject('domain-guard-as-native-error', lambda r, b: r['compilerControls']['unsupportedDynamicIndexContexts'][0].update(nativeErrorPathClaimed=True),
        'Unsupported contexts receive no native-error/return/state credit')
    reject('native-count-as-entry-count', lambda r, b: r.update(pairedCompleteOwnEntryExecutions=r['pairedNativeReturningCalls']), 'Separate complete-entry/native-return totals')
    reject('native-source-credit', lambda r, b: r.update(nativeExecutableByteCredit=1128), 'Zero excess/post-fault source credit')
    reject('wrong-entry-alias', lambda r, b: b['range'].update(entrySlots=[258]), 'frozen complete range differs')
    reject('truncated-range', lambda r, b: b['range'].update(bytes=1100), 'frozen complete range differs')
    unit = flags.validated(original, image, batch)
    assert unit['nativeByteCredit'] == unit['completeImageCredit'] == unit['unsupportedContextNativeErrorCredit'] == 0
    result = {'passed': True, 'controls': controls, 'sourceUnits': 1, 'sourceBytes': unit['sourceByteCredit'],
        'completeScrEntryExecutions': unit['completeScrEntryExecutions'], 'nativeRoutineReturnObservations': unit['nativeRoutineReturnObservations'],
        'moduleGlobalSlots': unit['moduleGlobalSlots'], 'privateLocalSlots': unit['privateLocalSlots'], 'sourceReturnType': 'float',
        'nativeSourceCredit': 0, 'completeImageCredit': 0, 'unsupportedContextNativeErrorCredit': 0}
    write_json(ROOT / 'evidence/verification/interpreted-registered-flags-source-negatives-20261030.json', result)
    print({key: value for key, value in result.items() if key != 'controls'}, flush=True)


if __name__ == '__main__':
    main()
