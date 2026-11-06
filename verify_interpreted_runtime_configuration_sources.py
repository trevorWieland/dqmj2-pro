import copy
from project import ROOT, read_json, write_json
import interpreted_runtime_configuration_sources as configuration


def main():
    relative = 'evidence/matches/scripts-20261030-runtime-configuration.json'
    original = read_json(ROOT / relative)
    batches = configuration.candidates(original, relative, [configuration.GENERATOR])
    image = next(row for row in read_json(ROOT / 'evidence/encounter/scripts-inventory-20261029.json')['images'] if row['codeSha256'] == batches[0]['identity']['codeSha256'])
    directory = ROOT / 'work/interpreted-runtime-configuration-proof-negatives'
    directory.mkdir(parents=True, exist_ok=True)
    controls = []

    def reject(name, mutate, reason):
        report, accepted = copy.deepcopy(original), copy.deepcopy(batches[0])
        mutate(report, accepted)
        path = directory / 'candidate.json'
        write_json(path, report)
        accepted['report'] = path.relative_to(ROOT).as_posix()
        try:
            configuration.validated(report, image, accepted)
        except (ValueError, AssertionError, OSError, KeyError, IndexError) as error:
            if reason not in str(error):
                raise AssertionError((name, 'Unexpected rejection', str(error), reason))
            controls.append({'name': name, 'rejected': True, 'reason': str(error)})
            print({'rejected': name}, flush=True)
            return
        raise AssertionError('Invalid runtime configuration source accepted: ' + name)

    reject('wrong-ROM', lambda r, b: r.update(romSha256='0' * 64), 'report identity differs')
    reject('native-namespace-substitution', lambda r, b: b['nativeModuleHashes'].update(itcm='0' * 64), 'native VM namespace differs')
    reject('whole-ROM-claim', lambda r, b: r.update(wholeRomSourceMatch=True), 'partial source claims whole ROM')
    reject('generator-tamper', lambda r, b: r.update(generatorSha256='0' * 64), 'frozen generator differs')
    reject('validator-pin-tamper', lambda r, b: b['sourceHashes'].__setitem__('validate_scr_runtime_configuration_20261030_batch19.py', '0' * 64),
        'frozen source/profile/validator closure changed')
    reject('entry-table-substitution', lambda r, b: b['identity'].update(entryTableSha256='0' * 64), 'inventoried image differs')
    reject('constructor-provider-substitution', lambda r, b: r['differential'].update(providerCount=1), 'native full-pool/ABI/domain scope differs')
    reject('free-pool-success-claim', lambda r, b: r.update(freePoolSuccessOrNaturalSceneReachabilityProven=True), 'native full-pool/ABI/domain scope differs')
    reject('unrestricted-coordinate-domain', lambda r, b: r['differential'].update(coordinateDomain='all float bit patterns'), 'native full-pool/ABI/domain scope differs')
    reject('module-globals-private', lambda r, b: r['boundariesAndStorage'][0].update(privateLocalSlots=[23, 24, 25, 26, 31]), 'shared globals/argument/boundary scope differs')
    reject('lost-argument-clobbers', lambda r, b: r['boundariesAndStorage'][0].update(argumentBankCallClobbers=[]), 'shared globals/argument/boundary scope differs')
    reject('padding-credit', lambda r, b: r['boundariesAndStorage'][0].update(followingPaddingSourceCredit=8), 'shared globals/argument/boundary scope differs')
    reject('source-product-unavailable', lambda r, b: r['sourceOnlyBuild']['units'][1]['emittedBody'].update(path='work/interpreted-runtime-configuration-proof-negatives/missing.scrfunc'),
        'missing.scrfunc')
    reject('false-private-return', lambda r, b: r['differential']['cases'][0]['first'].update(completeOwnEntryReturned=False), 'Complete source-range private configuration return')
    reject('wrong-coordinate-scale', lambda r, b: r['differential']['cases'][0]['first']['constructorCalls'][0]['words'].__setitem__(2, 1000),
        'Actual eight-word original constructor/scaled signed-coordinate ABI')
    reject('wrong-mode', lambda r, b: r['differential']['cases'][0]['first']['constructorCalls'][0]['words'].__setitem__(5, 2),
        'Actual eight-word original constructor/scaled signed-coordinate ABI')
    reject('wrong-slot-store', lambda r, b: r['differential']['cases'][0]['first']['orderedGlobalWordStores'][0].update(value=1),
        'Exact ordered shared-global/251-neighbor/persistent/full-pool effects')
    reject('lost-pool-state', lambda r, b: r['differential']['cases'][0]['first'].update(unchangedFullPoolSha256='0' * 64),
        'Exact ordered shared-global/251-neighbor/persistent/full-pool effects')
    reject('unsigned-failure-return', lambda r, b: r['differential']['cases'][0]['first'].update(configurationResultRawWord=0x4F800000),
        'Actual capacity failure float return/argument clobbers')
    reject('native-count-as-entry-count', lambda r, b: r.update(pairedCompleteOwnEntryExecutions=r['pairedNativeReturningCalls']), 'Separate paired SCR/native execution totals')
    reject('native-source-credit', lambda r, b: r.update(nativeExecutableByteCredit=1248), 'Zero excess/provider/free-pool/post-fault credit')
    reject('wrong-entry-alias', lambda r, b: b['range'].update(entrySlots=[273]), 'frozen complete range differs')
    units = [configuration.validated(original, image, batch) for batch in batches]
    assert len(units) == 2 and all(row['providerCount'] == row['nativeByteCredit'] == row['completeImageCredit'] == 0 for row in units)
    result = {'passed': True, 'controls': controls, 'sourceUnits': 2, 'sourceBytes': sum(row['sourceByteCredit'] for row in units),
        'completeScrEntryExecutions': sum(row['completeScrEntryExecutions'] for row in units),
        'nativeRoutineReturnObservations': sum(row['nativeRoutineReturnObservations'] for row in units), 'implementationFamilies': 1,
        'originalConstructorRetained': True, 'constructorCapacityExhaustedReturnOnly': True, 'providerCount': 0,
        'freePoolSuccessOrNaturalSceneReachabilityProven': False, 'nativeSourceCredit': 0, 'completeImageCredit': 0}
    write_json(ROOT / 'evidence/verification/interpreted-runtime-configuration-source-negatives-20261030.json', result)
    print({key: value for key, value in result.items() if key != 'controls'}, flush=True)


if __name__ == '__main__':
    main()
