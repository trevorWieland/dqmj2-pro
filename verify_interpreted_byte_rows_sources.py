import copy
from project import ROOT, read_json, write_json
import interpreted_byte_rows_sources as rows


def main():
    relative = 'evidence/matches/scripts-20261030-byte-rows.json'
    original = read_json(ROOT / relative)
    batch = rows.candidates(original, relative, [rows.GENERATOR])[0]
    image = next(row for row in read_json(ROOT / 'evidence/encounter/scripts-inventory-20261029.json')['images'] if row['codeSha256'] == batch['identity']['codeSha256'])
    work = ROOT / 'work/interpreted-byte-rows-proof-negatives'
    work.mkdir(parents=True, exist_ok=True)
    controls = []

    def reject(name, mutate, reason):
        report, accepted = copy.deepcopy(original), copy.deepcopy(batch)
        mutate(report, accepted)
        path = work / 'candidate.json'
        write_json(path, report)
        accepted['report'] = path.relative_to(ROOT).as_posix()
        try:
            rows.validated(report, image, accepted)
        except (ValueError, AssertionError, OSError, KeyError, IndexError) as error:
            if reason not in str(error):
                raise AssertionError((name, 'Unexpected rejection', str(error), reason))
            controls.append({'name': name, 'rejected': True, 'reason': str(error)})
            print({'rejected': name}, flush=True)
            return
        raise AssertionError('Invalid byte-row configuration accepted: ' + name)

    reject('wrong-ROM', lambda r, b: r.update(romSha256='0' * 64), 'report identity differs')
    reject('wrong-class', lambda r, b: r.update(evidenceClass='data-array'), 'report identity differs')
    reject('wrong-native-namespace', lambda r, b: b['nativeModuleHashes'].update(itcm='0' * 64), 'native VM namespace differs')
    reject('whole-ROM-claim', lambda r, b: r.update(wholeRomSourceMatch=True), 'partial source claims whole ROM')
    reject('wrong-generator', lambda r, b: r.update(generatorSha256='0' * 64), 'frozen generator differs')
    reject('validator-pin-tamper', lambda r, b: b['sourceHashes'].__setitem__('validate_scr_byte_rows_20261030_batch15.py', '0' * 64),
        'frozen source/profile/validator closure changed')
    reject('entry-table-substitution', lambda r, b: b['identity'].update(entryTableSha256='0' * 64), 'inventoried image differs')
    reject('general-C-claim', lambda r, b: r['sourceOnlyBuild']['compilerEvidence'].update(generalCCompilerClaimed=True), 'language/configuration/domain/entry scope differs')
    reject('decision-logic-inflation', lambda r, b: r['boundariesAndStorage'].update(branchDecisionLogicClaimed=True), 'language/configuration/domain/entry scope differs')
    reject('variable-slot-effects', lambda r, b: r['boundariesAndStorage'].update(vmVariableSlotsReadOrWritten=[0]), 'language/configuration/domain/entry scope differs')
    reject('unbounded-byte-domain', lambda r, b: r['sourceOnlyBuild']['compilerEvidence'].update(byteValueDomain=[0, 65535]), 'language/configuration/domain/entry scope differs')
    reject('missing-source-product', lambda r, b: r['sourceOnlyBuild']['emittedBody'].update(path='work/interpreted-byte-rows-proof-negatives/missing.scrfunc'), 'missing.scrfunc')
    reject('false-private-return', lambda r, b: r['differential']['cases'][0]['first'].update(completeEntryReturned=False), 'Complete74-record/private-return execution')
    reject('wrong-configured-row', lambda r, b: r['differential']['cases'][0]['first']['configuredRows'][0].update(nativeRow=1), 'Every preset/ordered byte store/all table effects')
    reject('missing-byte-store', lambda r, b: r['differential']['cases'][0]['first']['orderedNativeByteStores'].pop(), 'Every preset/ordered byte store/all table effects')
    reject('lost-register-guard', lambda r, b: r['differential']['cases'][0]['first'].update(all256SlotsAndWordGuardsPreserved=False), 'All256 slots/guards/persistent preservation')
    reject('native-count-as-entry-count', lambda r, b: r.update(pairedCompleteOwnEntryExecutions=r['pairedNativeReturningCalls']), 'Separate complete-entry/native return totals')
    reject('missing-byte-boundary-control', lambda r, b: r['compilerControls']['all95LogicalByteCases'].pop(), 'All19 indices/five byte-pattern controls')
    reject('native-source-credit', lambda r, b: r.update(nativeExecutableByteCredit=1552), 'Zero excess/post-fault source credit')
    reject('wrong-entry-alias', lambda r, b: b['range'].update(entrySlots=[32]), 'frozen complete range differs')
    reject('truncated-range', lambda r, b: b['range'].update(bytes=1548), 'frozen complete range differs')
    unit = rows.validated(original, image, batch)
    assert unit['nativeByteCredit'] == unit['completeImageCredit'] == unit['nativeByteRowApiSourceCredit'] == 0
    result = {'passed': True, 'controls': controls, 'sourceUnits': 1, 'sourceBytes': unit['sourceByteCredit'],
        'configurationOnly': True, 'branchDecisionLogicClaimed': False, 'completeScrEntryExecutions': unit['completeScrEntryExecutions'],
        'nativeRoutineReturnObservations': unit['nativeRoutineReturnObservations'], 'separateCompilerControlNativeReturns': unit['separateCompilerControlNativeReturns'],
        'nativeSourceCredit': 0, 'completeImageCredit': 0}
    write_json(ROOT / 'evidence/verification/interpreted-byte-rows-source-negatives-20261030.json', result)
    print({key: value for key, value in result.items() if key != 'controls'}, flush=True)


if __name__ == '__main__':
    main()
