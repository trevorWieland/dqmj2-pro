import copy
from project import ROOT, read_json, write_json
import interpreted_byte_modes_sources as modes


def main():
    relative = 'evidence/matches/scripts-20261030-byte-modes.json'
    original = read_json(ROOT / relative)
    batch = modes.candidates(original, relative, [modes.GENERATOR])[0]
    image = next(row for row in read_json(ROOT / 'evidence/encounter/scripts-inventory-20261029.json')['images']
        if row['codeSha256'] == batch['identity']['codeSha256'])
    work = ROOT / 'work/interpreted-byte-modes-proof-negatives'
    work.mkdir(parents=True, exist_ok=True)
    controls = []

    def reject(name, mutate, reason):
        report, accepted = copy.deepcopy(original), copy.deepcopy(batch)
        mutate(report, accepted)
        path = work / 'candidate.json'
        write_json(path, report)
        accepted['report'] = path.relative_to(ROOT).as_posix()
        try:
            modes.validated(report, image, accepted)
        except (ValueError, AssertionError, OSError, KeyError, IndexError) as error:
            if reason not in str(error):
                raise AssertionError((name, 'Unexpected rejection', str(error), reason))
            controls.append({'name': name, 'rejected': True, 'reason': str(error)})
            print({'rejected': name}, flush=True)
            return
        raise AssertionError('Invalid byte-mode proof accepted: ' + name)

    reject('wrong-ROM', lambda r, b: r.update(romSha256='0' * 64), 'report identity differs')
    reject('wrong-class', lambda r, b: r.update(evidenceClass='bytecode-array'), 'report identity differs')
    reject('wrong-native-namespace', lambda r, b: b['nativeModuleHashes'].update(itcm='0' * 64), 'native VM namespace differs')
    reject('whole-ROM-claim', lambda r, b: r.update(wholeRomSourceMatch=True), 'partial source claims whole ROM')
    reject('wrong-generator', lambda r, b: r.update(generatorSha256='0' * 64), 'frozen generator differs')
    reject('validator-pin-tamper', lambda r, b: b['sourceHashes'].__setitem__('validate_scr_byte_modes_20261030_batch14.py', '0' * 64),
        'frozen source/profile/validator closure changed')
    reject('entry-table-substitution', lambda r, b: b['identity'].update(entryTableSha256='0' * 64), 'inventoried image differs')
    reject('general-C-claim', lambda r, b: r['sourceOnlyBuild']['compilerEvidence'].update(generalCCompilerClaimed=True),
        'language/domain/raw-formal/entry scope differs')
    reject('numeric-formal-conversion', lambda r, b: r['sourceOnlyBuild']['compilerEvidence']['formalArguments'][0].update(copyRepresentation='numeric float conversion'),
        'language/domain/raw-formal/entry scope differs')
    reject('unbounded-mode-domain', lambda r, b: r['sourceOnlyBuild']['compilerEvidence'].update(byteModeDomain=[0, 255]),
        'language/domain/raw-formal/entry scope differs')
    reject('opaque-global-completeness', lambda r, b: r['boundariesAndStorage'].update(opaqueNativeOrComputedSlotReferenceCoverageComplete=True),
        'language/domain/raw-formal/entry scope differs')
    reject('missing-source-product', lambda r, b: r['sourceOnlyBuild']['emittedBody'].update(path='work/interpreted-byte-modes-proof-negatives/missing.scrfunc'),
        'missing.scrfunc')
    reject('false-private-return', lambda r, b: r['differential']['cases'][0]['first'].update(completeEntryReturned=False),
        'Complete private-return termination')
    reject('lost-raw-formal', lambda r, b: r['differential']['cases'][1]['first'].update(capturedFormalWord=0),
        'Raw formal/other slots/guards/persistent invariant')
    reject('wrong-native-byte-write', lambda r, b: r['differential']['cases'][0]['first']['orderedNativeByteStores'][0].update(value=0),
        'Ordered four-byte copies/full-table effects')
    reject('changed-table-guards', lambda r, b: r['differential']['cases'][0]['first'].update(allOtherSlotsAndTableGuardsPreserved=False),
        'Raw formal/other slots/guards/persistent invariant')
    reject('missing-primary-outcome', lambda r, b: r['differential']['branchCoverage']['52360'].pop(),
        'Both outcomes of all six primary predicates')
    reject('helper-count-as-entry-count', lambda r, b: r.update(pairedCompleteOwnEntryExecutions=r['pairedNativeReturningCalls']),
        'Separate complete-entry/native counts')
    reject('missing-mode-control', lambda r, b: r['compilerControls']['all76LogicalModeCases'].pop(), 'All logical19/mode4 controls')
    reject('native-source-credit', lambda r, b: r.update(nativeExecutableByteCredit=1000), 'Zero excess/post-fault source credit')
    reject('wrong-entry-alias', lambda r, b: b['range'].update(entrySlots=[32]), 'frozen complete range differs')
    reject('truncated-range', lambda r, b: b['range'].update(bytes=976), 'frozen complete range differs')
    unit = modes.validated(original, image, batch)
    assert unit['nativeByteCredit'] == unit['completeImageCredit'] == unit['nativeByteModeApiSourceCredit'] == 0
    result = {'passed': True, 'controls': controls, 'sourceUnits': 1, 'sourceBytes': unit['sourceByteCredit'],
        'completeScrEntryExecutions': unit['completeScrEntryExecutions'], 'nativeRoutineReturnObservations': unit['nativeRoutineReturnObservations'],
        'separateCompilerControlNativeReturns': unit['separateCompilerControlNativeReturns'], 'nativeSourceCredit': 0, 'completeImageCredit': 0}
    write_json(ROOT / 'evidence/verification/interpreted-byte-modes-source-negatives-20261030.json', result)
    print({key: value for key, value in result.items() if key != 'controls'}, flush=True)


if __name__ == '__main__':
    main()
