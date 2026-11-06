import copy
from project import ROOT, read_json, write_json
import interpreted_context_words_sources as words


def main():
    relative = 'evidence/matches/scripts-20261030-context-words.json'
    original = read_json(ROOT / relative)
    batch = words.candidates(original, relative, [words.GENERATOR])[0]
    image = next(row for row in read_json(ROOT / 'evidence/encounter/scripts-inventory-20261029.json')['images']
        if row['codeSha256'] == batch['identity']['codeSha256'])
    work = ROOT / 'work/interpreted-context-words-proof-negatives'
    work.mkdir(parents=True, exist_ok=True)
    controls = []

    def reject(name, mutate, reason):
        report, accepted = copy.deepcopy(original), copy.deepcopy(batch)
        mutate(report, accepted)
        path = work / 'candidate.json'
        write_json(path, report)
        accepted['report'] = path.relative_to(ROOT).as_posix()
        try:
            words.validated(report, image, accepted)
        except (ValueError, AssertionError, OSError, KeyError, IndexError) as error:
            if reason not in str(error):
                raise AssertionError((name, 'Unexpected rejection', str(error), reason))
            controls.append({'name': name, 'rejected': True, 'reason': str(error)})
            print({'rejected': name}, flush=True)
            return
        raise AssertionError('Invalid context-word source proof accepted: ' + name)

    reject('wrong-ROM', lambda r, b: r.update(romSha256='0' * 64), 'report identity differs')
    reject('wrong-class', lambda r, b: r.update(evidenceClass='opcode-array'), 'report identity differs')
    reject('native-namespace-substitution', lambda r, b: b['nativeModuleHashes'].update(itcm='0' * 64), 'native VM namespace differs')
    reject('whole-ROM-claim', lambda r, b: r.update(wholeRomSourceMatch=True), 'partial source claims whole ROM')
    reject('wrong-generator', lambda r, b: r.update(generatorSha256='0' * 64), 'frozen generator differs')
    reject('validator-pin-tamper', lambda r, b: b['sourceHashes'].__setitem__('validate_scr_context_words_20261030_batch13.py', '0' * 64),
        'frozen source/profile/validator closure changed')
    reject('wrong-entry-table', lambda r, b: b['identity'].update(entryTableSha256='0' * 64), 'inventoried image differs')
    reject('general-C-claim', lambda r, b: r['sourceOnlyBuild']['compilerEvidence'].update(generalCCompilerClaimed=True),
        'language/typed-domain/entry scope differs')
    reject('arbitrary-float-ordering', lambda r, b: r['sourceOnlyBuild']['compilerEvidence'].update(orderedComparisonsRequireNumericByteProvenance=False),
        'language/typed-domain/entry scope differs')
    reject('unbounded-context-index', lambda r, b: r['sourceOnlyBuild']['compilerEvidence'].update(contextWordIndexDomain=[0, 255]),
        'language/typed-domain/entry scope differs')
    reject('opaque-global-completeness', lambda r, b: r['boundariesAndStorage'].update(opaqueNativeOrComputedSlotReferenceCoverageComplete=True),
        'language/typed-domain/entry scope differs')
    reject('source-product-unavailable', lambda r, b: r['sourceOnlyBuild']['emittedBody'].update(
        path='work/interpreted-context-words-proof-negatives/missing.scrfunc'), 'missing.scrfunc')
    reject('false-private-return', lambda r, b: r['differential']['cases'][0]['first'].update(completeEntryReturned=False),
        'Complete private-return termination')
    reject('missing-reset-word', lambda r, b: r['differential']['cases'][0]['first']['orderedContextWordStores'].pop(0),
        'Ordered reset/set word effects')
    reject('counter-byte-narrowing', lambda r, b: r['differential']['cases'][240].update(rawCounterWord=255),
        'Typed input/thread/counter population')
    reject('native-count-as-entry-count', lambda r, b: r.update(pairedCompleteOwnEntryExecutions=r['pairedNativeReturningCalls']),
        'Separate native/complete-entry return counts')
    reject('false-native-source-credit', lambda r, b: r.update(nativeExecutableByteCredit=1280), 'No excess credit or post-fault state')
    reject('wrong-entry-alias', lambda r, b: b['range'].update(entrySlots=[32]), 'frozen complete range differs')
    reject('truncated-complete-range', lambda r, b: b['range'].update(bytes=1248), 'frozen complete range differs')
    unit = words.validated(original, image, batch)
    assert unit['nativeByteCredit'] == unit['completeImageCredit'] == unit['nativeContextWordApiSourceCredit'] == 0
    result = {'passed': True, 'controls': controls, 'sourceUnits': 1, 'sourceBytes': unit['sourceByteCredit'],
        'completeScrEntryExecutions': unit['completeScrEntryExecutions'],
        'nativeRoutineReturnObservations': unit['nativeRoutineReturnObservations'],
        'separateCompilerControlNativeReturns': unit['separateCompilerControlNativeReturns'],
        'nativeSourceCredit': 0, 'completeImageCredit': 0}
    write_json(ROOT / 'evidence/verification/interpreted-context-words-source-negatives-20261030.json', result)
    print({key: value for key, value in result.items() if key != 'controls'}, flush=True)


if __name__ == '__main__':
    main()
