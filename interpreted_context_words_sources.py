from pathlib import Path
import sys
from project import ROOT, configuration, read_json, sha256
from interpreted_sources import local
from interpreted_linked_sources import require, native_hashes

KIND = 'complete-numeric-primary-context-words-SCR-v11'
GENERATOR = 'match_scr_context_words_20261030_batch13.py'
GENERATOR_HASH = '347259ba0f56beff89b083d020e233a9acc0dbe44f4d82629573489b3e627b44'
VALIDATORS = {'validate_scr_empty_family_20261029_batch04.py': 'c3e38cbf73c38d98484f799ba20e2fe05c34612dff4310949837eab6ebb94604',
    'validate_scr_numeric_transition_20261029_batch04.py': 'ea6f463ee6792297ad091b561ae10eb19bdcb14d6165e8b221c9740570ed4020',
    'validate_scr_context_words_20261030_batch13.py': '4351288dcde12aaabb0fcd38b8b56d04b7d3703215cfd1950a8e69725b23ea7c'}


def source_hashes(report):
    require(report['generator'] == GENERATOR and report['generatorSha256'] == GENERATOR_HASH,
        'Context-words frozen generator differs')
    require(all(local(path).is_file() and sha256(local(path)) == pin for path, pin in VALIDATORS.items()),
        'Context-words frozen validator differs')
    hashes = {row['path']: row['sha256'] for row in report['sourceClosure']}
    hashes[GENERATOR] = GENERATOR_HASH
    hashes.update(VALIDATORS)
    return hashes


def candidates(report, relative, reproduction):
    hashes = source_hashes(report)
    image = next(row for row in read_json(ROOT / 'evidence/encounter/scripts-inventory-20261029.json')['images']
        if row['codeSha256'] == report['codeSha256'])
    return [{'report': relative, 'reproduce': reproduction, 'proofKind': KIND, 'sourceHashes': hashes,
        'nativeModuleHashes': native_hashes(),
        'identity': {key: image[key] for key in ('scriptSha256', 'codeSha256', 'entryTableSha256')},
        'range': {'entrySlots': [272], **report['matchedRange']}}]


def validated(report, image, batch):
    require(report['evidenceClass'] == 'ordinary-C-complete-numeric-primary-context-word-SCR-source-match'
        and report['romSha256'] == configuration()['romSha256'], 'Context-words report identity differs')
    require(batch['nativeModuleHashes'] == native_hashes(), 'Context-words native VM namespace differs')
    require(report['wholeRomSourceMatch'] is False, 'Context-words partial source claims whole ROM')
    require(sha256(Path(sys.executable)) == read_json(ROOT / 'tools.lock.json')['python']['sha256'],
        'Context-words pinned Python identity differs')
    hashes = source_hashes(report)
    require(hashes == batch['sourceHashes'] and all(local(path).is_file() and sha256(local(path)) == pin for path, pin in hashes.items()),
        'Context-words frozen source/profile/validator closure changed')
    require(all(image[key] == value for key, value in batch['identity'].items())
        and report['scriptSha256'] == image['scriptSha256'] and report['codeSha256'] == image['codeSha256'],
        'Context-words inventoried image differs')
    compiled, scope = report['sourceOnlyBuild']['compilerEvidence'], report['boundariesAndStorage']
    require(compiled['generalCCompilerClaimed'] is False and compiled['orderedComparisonsRequireNumericByteProvenance'] is True
        and compiled['generatedLabelsFromSourceOnly'] is True and compiled['contextWordIndexDomain'] == [0, 15]
        and compiled['contextWordValueDomain'] == [0, 16777216] and scope['serializedCompleteEntryDomainOnly'] is True
        and scope['opaqueNativeOrComputedSlotReferenceCoverageComplete'] is False,
        'Context-words language/typed-domain/entry scope differs')
    from validate_scr_context_words_20261030_batch13 import validate
    units = validate(ROOT, batch['report'])
    require(len(units) == 1, 'Context-words validated population differs')
    key = image['codeSha256'], batch['range']['startPc']
    require(key in units, 'Context-words selected identity not validated')
    row = units[key]
    region = {'entrySlots': row['entryAliases'], **{name: row[name] for name in ('startPc', 'endExclusivePc', 'bytes', 'sha256')}}
    require(region == batch['range'] and 0 <= region['startPc'] < region['endExclusivePc'] <= image['codeBytes'],
        'Context-words frozen complete range differs')
    return {'id': report['romSha256'] + '/scr/' + image['codeSha256'] + '/' + str(row['startPc']),
        'scriptSha256': image['scriptSha256'], 'codeSha256': image['codeSha256'], 'report': batch['report'],
        'sourceHashes': batch['sourceHashes'], 'range': region, 'sourceLanguage': 'restricted C99', 'function': compiled['function'],
        'sourceDefinitionId': row['sourceSha256'] + '/' + compiled['function'], 'sourceByteCredit': row['bytes'],
        'sourceUnitCredit': 1, 'completeImageCredit': 0, 'nativeByteCredit': 0, 'copyOnly': False,
        'implementationFamily': 'numeric-primary-decisions-with-native-context-word-reset-and-set',
        'completeScrEntryExecutions': row['pairedCompleteOwnEntryExecutions'],
        'nativeRoutineReturnObservations': row['pairedNativeReturningCalls'],
        'separateCompilerControlNativeReturns': report['separateByteControlNativeReturns'],
        'entryDomainOnly': True, 'wholeImageControlFlowCertified': False, 'outsideIndirectTransfersExhaustivelyRuledOut': False,
        'nativeContextWordApiSourceCredit': 0, 'nativeContextWordCount': 16,
        'rawCounterResetValues': [0, 1, 10800, 4294967295], 'allOwnRecordsExecuted': True,
        'naturalSceneOrRenewabilityMeaningProven': False,
        'scratchCallAbi': 'serialized complete entry with private slots67/68, native sixteen-word reset/set effects and full persistent invariance'}
