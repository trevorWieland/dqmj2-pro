import copy
from project import ROOT, read_json, write_json
import interpreted_record_capacity_sources as capacity


def main():
    relative = 'evidence/matches/scripts-20261030-record-capacity.json'
    original = read_json(ROOT / relative)
    batch = capacity.candidates(original, relative, [capacity.GENERATOR])[0]
    image = next(row for row in read_json(ROOT / 'evidence/encounter/scripts-inventory-20261029.json')['images'] if row['codeSha256'] == batch['identity']['codeSha256'])
    directory = ROOT / 'work/interpreted-record-capacity-proof-negatives'
    directory.mkdir(parents=True, exist_ok=True)
    controls = []

    def reject(name, mutate, reason):
        report, accepted = copy.deepcopy(original), copy.deepcopy(batch)
        mutate(report, accepted)
        path = directory / 'candidate.json'
        write_json(path, report)
        accepted['report'] = path.relative_to(ROOT).as_posix()
        try:
            capacity.validated(report, image, accepted)
        except (ValueError, AssertionError, OSError, KeyError, IndexError) as error:
            if reason not in str(error):
                raise AssertionError((name, 'Unexpected rejection', str(error), reason))
            controls.append({'name': name, 'rejected': True, 'reason': str(error)})
            print({'rejected': name}, flush=True)
            return
        raise AssertionError('Invalid record-capacity source accepted: ' + name)

    reject('wrong-ROM', lambda r, b: r.update(romSha256='0' * 64), 'report identity differs')
    reject('native-namespace-substitution', lambda r, b: b['nativeModuleHashes'].update(itcm='0' * 64), 'native VM namespace differs')
    reject('whole-ROM-claim', lambda r, b: r.update(wholeRomSourceMatch=True), 'partial source claims whole ROM')
    reject('generator-tamper', lambda r, b: r.update(generatorSha256='0' * 64), 'frozen generator differs')
    reject('validator-pin-tamper', lambda r, b: b['sourceHashes'].__setitem__('validate_scr_record_capacity_20261030_batch21.py', '0' * 64),
        'frozen source/profile/validator closure changed')
    reject('entry-table-substitution', lambda r, b: b['identity'].update(entryTableSha256='0' * 64), 'inventoried image differs')
    reject('integer-return-conflation', lambda r, b: r['sourceOnlyBuild']['compilerEvidence'].update(sourceReturnType='int'), 'float/shared/counter/record-validity scope differs')
    reject('fake-private-locals', lambda r, b: r['boundariesAndStorage'].update(privateLocalSlots=[0, 1, 2]), 'float/shared/counter/record-validity scope differs')
    reject('getter-provider', lambda r, b: r['differential'].update(providerCount=1), 'float/shared/counter/record-validity scope differs')
    reject('record-validity-claim', lambda r, b: r.update(nativeRecordValidityOwnershipImportLegalityOrNaturalSceneReachabilityProven=True), 'float/shared/counter/record-validity scope differs')
    reject('source-product-unavailable', lambda r, b: r['sourceOnlyBuild']['emittedBody'].update(path='work/interpreted-record-capacity-proof-negatives/missing.scrfunc'), 'missing.scrfunc')
    reject('false-private-return', lambda r, b: r['differential']['cases'][0]['first'].update(completeOwnEntryReturned=False), 'Complete private capacity entry return')
    reject('wrong-threshold-result', lambda r, b: r['differential']['cases'][0]['first'].update(returnedScalarWord=0x3F800000), 'Raw decision/query/five-real-counter/full-UID ABI')
    reject('wrong-secondary-count', lambda r, b: r['differential']['cases'][15]['first']['nativeCounterReturns'][1].update(resultWord=1), 'Raw decision/query/five-real-counter/full-UID ABI')
    reject('truncated-UID', lambda r, b: r['differential']['cases'][15]['first']['uidLookupWords'].__setitem__(0, 0), 'Raw decision/query/five-real-counter/full-UID ABI')
    reject('NaN-mode-invented-query', lambda r, b: r['differential']['cases'][23]['first'].update(queryResultWords=[0]), 'Raw decision/query/five-real-counter/full-UID ABI')
    reject('lost-module-state', lambda r, b: r['differential']['cases'][0]['first'].update(allOther253SlotsPreserved=False), 'Exact shared module/253-neighbor/record-state effects')
    reject('native-count-as-entry-count', lambda r, b: r.update(pairedCompleteOwnEntryExecutions=r['pairedNativeReturningCalls']), 'Separate native/complete/nested counter totals')
    reject('wrong-UID-field-offset', lambda r, b: r['nativeCounterIdentity'].update(testedNonzeroWordOffset=16), 'Qualified original count identity')
    reject('native-source-credit', lambda r, b: r.update(nativeExecutableByteCredit=544), 'One bounded definition/zero excess semantic or byte credit')
    reject('wrong-entry-alias', lambda r, b: b['range'].update(entrySlots=[0]), 'frozen complete range differs')
    reject('padding-credit', lambda r, b: b['range'].update(bytes=552, endExclusivePc=552), 'frozen complete range differs')
    unit = capacity.validated(original, image, batch)
    result = {'passed': True, 'controls': controls, 'sourceUnits': 1, 'sourceBytes': 544,
        'completeScrEntryExecutions': unit['completeScrEntryExecutions'], 'nativeRoutineReturnObservations': unit['nativeRoutineReturnObservations'],
        'nestedCounterReturns': unit['nativeNestedCounterReturnObservations'], 'nativeSourceCredit': 0, 'completeImageCredit': 0,
        'recordValidityOwnershipImportLegalityOrSceneReachabilityProven': False}
    write_json(ROOT / 'evidence/verification/interpreted-record-capacity-source-negatives-20261030.json', result)
    print({key: value for key, value in result.items() if key != 'controls'}, flush=True)


if __name__ == '__main__':
    main()
