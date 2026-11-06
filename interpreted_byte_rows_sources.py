from pathlib import Path
import sys
from project import ROOT, configuration, read_json, sha256
from interpreted_sources import local
from interpreted_linked_sources import require, native_hashes

KIND = 'complete-native-byte-row-configuration-SCR-v13'
GENERATOR = 'match_scr_byte_rows_20261030_batch15.py'
GENERATOR_HASH = '03aeeff13f6cb7e85034ffb968bb2472b3b0629e4554bad69adf47706d2fc3c0'
VALIDATORS = {'validate_scr_empty_family_20261029_batch04.py': 'c3e38cbf73c38d98484f799ba20e2fe05c34612dff4310949837eab6ebb94604',
    'validate_scr_numeric_transition_20261029_batch04.py': 'ea6f463ee6792297ad091b561ae10eb19bdcb14d6165e8b221c9740570ed4020',
    'validate_scr_byte_rows_20261030_batch15.py': '91942ae881e2ffdb430d6da2fdda08ccbb5c2a54f6e4c6306cfa72455a201ffb'}


def source_hashes(report):
    require(report['generator'] == GENERATOR and report['generatorSha256'] == GENERATOR_HASH, 'Byte-rows frozen generator differs')
    require(all(local(path).is_file() and sha256(local(path)) == pin for path, pin in VALIDATORS.items()), 'Byte-rows frozen validator differs')
    hashes = {row['path']: row['sha256'] for row in report['sourceClosure']}
    hashes[GENERATOR] = GENERATOR_HASH
    hashes.update(VALIDATORS)
    return hashes


def candidates(report, relative, reproduction):
    hashes = source_hashes(report)
    image = next(row for row in read_json(ROOT / 'evidence/encounter/scripts-inventory-20261029.json')['images'] if row['codeSha256'] == report['codeSha256'])
    return [{'report': relative, 'reproduce': reproduction, 'proofKind': KIND, 'sourceHashes': hashes, 'nativeModuleHashes': native_hashes(),
        'identity': {key: image[key] for key in ('scriptSha256', 'codeSha256', 'entryTableSha256')},
        'range': {'entrySlots': [11], **report['matchedRange']}}]


def validated(report, image, batch):
    require(report['evidenceClass'] == 'ordinary-C-complete-native-byte-row-configuration-SCR-source-match'
        and report['romSha256'] == configuration()['romSha256'], 'Byte-rows report identity differs')
    require(batch['nativeModuleHashes'] == native_hashes(), 'Byte-rows native VM namespace differs')
    require(report['wholeRomSourceMatch'] is False, 'Byte-rows partial source claims whole ROM')
    require(sha256(Path(sys.executable)) == read_json(ROOT / 'tools.lock.json')['python']['sha256'], 'Byte-rows pinned Python identity differs')
    hashes = source_hashes(report)
    require(hashes == batch['sourceHashes'] and all(local(path).is_file() and sha256(local(path)) == pin for path, pin in hashes.items()),
        'Byte-rows frozen source/profile/validator closure changed')
    require(all(image[key] == value for key, value in batch['identity'].items()) and report['scriptSha256'] == image['scriptSha256']
        and report['codeSha256'] == image['codeSha256'], 'Byte-rows inventoried image differs')
    compiled, scope = report['sourceOnlyBuild']['compilerEvidence'], report['boundariesAndStorage']
    require(compiled['generalCCompilerClaimed'] is False and compiled['configurationOnly'] is True and compiled['sourceContainsBranches'] is False
        and compiled['logicalIndexDomain'] == [0, 18] and compiled['byteValueDomain'] == [0, 255] and compiled['nativeApiSourceCredit'] == 0
        and scope['configurationOnly'] is True and scope['branchDecisionLogicClaimed'] is False and scope['vmVariableSlotsReadOrWritten'] == []
        and scope['serializedCompleteEntryDomainOnly'] is True and scope['opaqueNativeOrComputedGlobalReferenceCoverageComplete'] is False,
        'Byte-rows language/configuration/domain/entry scope differs')
    from validate_scr_byte_rows_20261030_batch15 import validate
    units = validate(ROOT, batch['report'])
    require(len(units) == 1, 'Byte-rows validated population differs')
    key = image['codeSha256'], batch['range']['startPc']
    require(key in units, 'Byte-rows selected identity not validated')
    row = units[key]
    region = {'entrySlots': row['entryAliases'], **{name: row[name] for name in ('startPc', 'endExclusivePc', 'bytes', 'sha256')}}
    require(region == batch['range'] and 0 <= region['startPc'] < region['endExclusivePc'] <= image['codeBytes'], 'Byte-rows frozen complete range differs')
    return {'id': report['romSha256'] + '/scr/' + image['codeSha256'] + '/' + str(row['startPc']), 'scriptSha256': image['scriptSha256'],
        'codeSha256': image['codeSha256'], 'report': batch['report'], 'sourceHashes': batch['sourceHashes'], 'range': region,
        'sourceLanguage': 'restricted C99', 'function': compiled['function'], 'sourceDefinitionId': row['sourceSha256'] + '/' + compiled['function'],
        'sourceByteCredit': row['bytes'], 'sourceUnitCredit': 1, 'completeImageCredit': 0, 'nativeByteCredit': 0, 'copyOnly': False,
        'implementationFamily': 'ordered-native-byte-row-configuration-presets', 'configurationOnly': True, 'branchDecisionLogicClaimed': False,
        'completeScrEntryExecutions': row['pairedCompleteOwnEntryExecutions'], 'nativeRoutineReturnObservations': row['pairedNativeReturningCalls'],
        'separateCompilerControlNativeReturns': report['separateRowControlNativeReturns'], 'nativeByteRowApiSourceCredit': 0,
        'entryDomainOnly': True, 'wholeImageControlFlowCertified': False, 'outsideIndirectTransfersExhaustivelyRuledOut': False,
        'naturalSceneOrRenewabilityMeaningProven': False, 'nativeTableBytes': 64, 'vmVariableSlotsReadOrWritten': [],
        'scratchCallAbi': 'serialized complete configuration entry; five exact integer arguments; all256 VM slots and guarded native byte rows retained'}
