import copy
from project import ROOT, read_json, write_json
import interpreted_primary_pair_sources as primary


def main():
    relative = 'evidence/matches/scripts-20261030-primary24-pair.json'
    original = read_json(ROOT / relative)
    batches = primary.candidates(original, relative, ['match_scr_primary24_pair_20261030_batch10.py'])
    inventory = read_json(ROOT / 'evidence/encounter/scripts-inventory-20261029.json')
    images = {row['codeSha256']: row for row in inventory['images']}
    work = ROOT / 'work/interpreted-primary-pair-proof-negatives'
    work.mkdir(parents=True, exist_ok=True)
    controls = []

    def reject(name, mutate, reason):
        report, batch = copy.deepcopy(original), copy.deepcopy(batches[0])
        mutate(report, batch)
        path = work / 'candidate.json'
        write_json(path, report)
        batch['report'] = path.relative_to(ROOT).as_posix()
        try:
            primary.validated(report, images[batches[0]['identity']['codeSha256']], batch)
        except (ValueError, AssertionError, OSError, IndexError, KeyError) as error:
            if reason not in str(error):
                raise AssertionError((name, 'Unexpected rejection', str(error), reason))
            controls.append({'name': name, 'rejected': True, 'reason': str(error)})
            print({'negativeControl': name, 'rejected': True}, flush=True)
            return
        raise AssertionError('Invalid primary pair accepted: ' + name)

    reject('wrong-ROM', lambda r, b: r.update(romSha256='0' * 64), 'report identity differs')
    reject('wrong-class', lambda r, b: r.update(evidenceClass='generated-bytecode-transcript'), 'report identity differs')
    reject('wrong-native-namespace', lambda r, b: b['nativeModuleHashes'].update(main='0' * 64), 'native VM namespace differs')
    reject('whole-ROM-claim', lambda r, b: r.update(wholeRomSourceMatch=True), 'partial source claims whole ROM')
    reject('wrong-generator', lambda r, b: r.update(generatorSha256='0' * 64), 'frozen generator differs')
    reject('validator-pin-tamper', lambda r, b: b['sourceHashes'].__setitem__('validate_scr_primary24_pair_20261030_batch10.py', '0' * 64),
           'frozen source/profile/validator closure changed')
    reject('entry-table-substitution', lambda r, b: b['identity'].update(entryTableSha256='0' * 64), 'inventoried image differs')
    reject('cross-unit-range-substitution', lambda r, b: b.update(range={'entrySlots': [102], **r['units'][1]['matchedRange']}),
           'qualified unit identity differs')
    reject('false-general-C', lambda r, b: r['units'][0]['sourceOnlyBuild']['compilerEvidence'].update(generalCCompilerClaimed=True),
           'language/assignment/runtime scope differs')
    reject('uninitialized-definition-credit', lambda r, b: r['units'][0]['boundariesAndStorage'].update(uninitializedDeclarationDoesNotDefineAValue=False),
           'language/assignment/runtime scope differs')
    reject('missing-dominance', lambda r, b: r['units'][1]['boundariesAndStorage']['readDominance'][0].update(definitelyAssignedBeforeRead=[]),
           'Actual assignments dominate every source read')
    reject('false-whole-entry-return', lambda r, b: r['units'][0]['differential']['cases'][0]['first'].update(completeEntryReturned=False), 'Whole entry return')
    reject('outer-prefix-return-credit', lambda r, b: r['units'][0]['differential']['qualifiedCallerPrefixes'][0].update(outerEntryReturned=True),
           'No outer/natural launch credit')
    reject('clobbered-unentered-local', lambda r, b: r['units'][1]['differential']['cases'][0]['first'].update(unenteredStateSlotPreserved=False),
           'Entire256-slot effect')
    reject('helper-count-as-entry-count', lambda r, b: r.update(pairedCompleteOwnEntryExecutions=r['pairedNativeReturningCalls']),
           'Accurate complete-entry versus helper totals')
    reject('native-source-credit', lambda r, b: r.update(nativeExecutableByteCredit=1016), 'Evidence scope')
    reject('missing-source-product', lambda r, b: r['units'][1]['sourceOnlyBuild']['emittedBody'].update(path='work/interpreted-primary-pair-proof-negatives/missing.scrfunc'),
           'missing.scrfunc')
    reject('truncated-range', lambda r, b: b['range'].update(bytes=348), 'frozen complete range differs')
    units = [primary.validated(original, images[b['identity']['codeSha256']], b) for b in batches]
    assert all(u['completeImageCredit'] == u['nativeByteCredit'] == u['callerPrefixOuterReturnCredit'] == 0 for u in units)
    result = {'passed': True, 'controls': controls, 'sourceUnits': len(units), 'sourceBytes': sum(u['sourceByteCredit'] for u in units),
        'completeScrEntryExecutions': sum(u['completeScrEntryExecutions'] for u in units),
        'nativeRoutineReturnObservations': sum(u['nativeRoutineReturnObservations'] for u in units),
        'separateCallerPrefixNativeReturns': sum(u['separateCallerPrefixNativeReturns'] for u in units),
        'callerPrefixOuterReturnCredit': 0, 'completeImages': 0, 'nativeSourceByteCredit': 0}
    write_json(ROOT / 'evidence/verification/interpreted-primary-pair-source-negatives-20261030.json', result)
    print({key: value for key, value in result.items() if key != 'controls'}, flush=True)


if __name__ == '__main__':
    main()
