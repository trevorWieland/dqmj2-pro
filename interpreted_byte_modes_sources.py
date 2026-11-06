from pathlib import Path
import sys
from project import ROOT, configuration, read_json, sha256
from interpreted_sources import local
from interpreted_linked_sources import require, native_hashes

KIND = 'complete-primary-byte-modes-SCR-v12'
GENERATOR = 'match_scr_byte_modes_20261030_batch14.py'
GENERATOR_HASH = 'f47a610f68ab4c3c1506fb264b5bef6fb0ca4548eb32d90525e01645db6bfbfb'
VALIDATORS = {'validate_scr_empty_family_20261029_batch04.py': 'c3e38cbf73c38d98484f799ba20e2fe05c34612dff4310949837eab6ebb94604',
    'validate_scr_numeric_transition_20261029_batch04.py': 'ea6f463ee6792297ad091b561ae10eb19bdcb14d6165e8b221c9740570ed4020',
    'validate_scr_byte_modes_20261030_batch14.py': 'acd81055061cc7d9d76a8b095da4f713f3bee26f97a9f3188f4e69bda3c74ab6'}


def source_hashes(report):
    require(report['generator'] == GENERATOR and report['generatorSha256'] == GENERATOR_HASH,
        'Byte-modes frozen generator differs')
    require(all(local(path).is_file() and sha256(local(path)) == pin for path, pin in VALIDATORS.items()),
        'Byte-modes frozen validator differs')
    hashes = {row['path']: row['sha256'] for row in report['sourceClosure']}
    hashes[GENERATOR] = GENERATOR_HASH
    hashes.update(VALIDATORS)
    return hashes


def candidates(report, relative, reproduction):
    hashes = source_hashes(report)
    image = next(row for row in read_json(ROOT / 'evidence/encounter/scripts-inventory-20261029.json')['images']
        if row['codeSha256'] == report['codeSha256'])
    return [{'report': relative, 'reproduce': reproduction, 'proofKind': KIND, 'sourceHashes': hashes,
        'nativeModuleHashes': native_hashes(), 'identity': {key: image[key] for key in ('scriptSha256', 'codeSha256', 'entryTableSha256')},
        'range': {'entrySlots': [12], **report['matchedRange']}}]


def validated(report, image, batch):
    require(report['evidenceClass'] == 'ordinary-C-complete-primary-conditional-byte-mode-SCR-source-match'
        and report['romSha256'] == configuration()['romSha256'], 'Byte-modes report identity differs')
    require(batch['nativeModuleHashes'] == native_hashes(), 'Byte-modes native VM namespace differs')
    require(report['wholeRomSourceMatch'] is False, 'Byte-modes partial source claims whole ROM')
    require(sha256(Path(sys.executable)) == read_json(ROOT / 'tools.lock.json')['python']['sha256'], 'Byte-modes pinned Python identity differs')
    hashes = source_hashes(report)
    require(hashes == batch['sourceHashes'] and all(local(path).is_file() and sha256(local(path)) == pin for path, pin in hashes.items()),
        'Byte-modes frozen source/profile/validator closure changed')
    require(all(image[key] == value for key, value in batch['identity'].items())
        and report['scriptSha256'] == image['scriptSha256'] and report['codeSha256'] == image['codeSha256'], 'Byte-modes inventoried image differs')
    compiled, scope = report['sourceOnlyBuild']['compilerEvidence'], report['boundariesAndStorage']
    require(compiled['generalCCompilerClaimed'] is False and compiled['uninitializedLocalReadsRejected'] is True
        and compiled['byteModeLogicalIndexDomain'] == [0, 18] and compiled['byteModeDomain'] == [0, 3]
        and compiled['formalArguments'][0]['copyRepresentation'] == 'raw IEEE754 binary32 bits'
        and scope['serializedCompleteEntryDomainOnly'] is True and scope['formalCopiedBeforeArgumentRegistersReused'] is True
        and scope['formalUnusedByOwnLogicButAbiCaptureRetained'] is True and scope['opaqueNativeOrComputedSlotReferenceCoverageComplete'] is False,
        'Byte-modes language/domain/raw-formal/entry scope differs')
    from validate_scr_byte_modes_20261030_batch14 import validate
    units = validate(ROOT, batch['report'])
    require(len(units) == 1, 'Byte-modes validated population differs')
    key = image['codeSha256'], batch['range']['startPc']
    require(key in units, 'Byte-modes selected identity not validated')
    row = units[key]
    region = {'entrySlots': row['entryAliases'], **{name: row[name] for name in ('startPc', 'endExclusivePc', 'bytes', 'sha256')}}
    require(region == batch['range'] and 0 <= region['startPc'] < region['endExclusivePc'] <= image['codeBytes'], 'Byte-modes frozen complete range differs')
    return {'id': report['romSha256'] + '/scr/' + image['codeSha256'] + '/' + str(row['startPc']),
        'scriptSha256': image['scriptSha256'], 'codeSha256': image['codeSha256'], 'report': batch['report'], 'sourceHashes': batch['sourceHashes'],
        'range': region, 'sourceLanguage': 'restricted C99', 'function': compiled['function'],
        'sourceDefinitionId': row['sourceSha256'] + '/' + compiled['function'], 'sourceByteCredit': row['bytes'], 'sourceUnitCredit': 1,
        'completeImageCredit': 0, 'nativeByteCredit': 0, 'copyOnly': False,
        'implementationFamily': 'primary-predicates-with-raw-formal-capture-and-native-byte-mode-selection',
        'completeScrEntryExecutions': row['pairedCompleteOwnEntryExecutions'], 'nativeRoutineReturnObservations': row['pairedNativeReturningCalls'],
        'separateCompilerControlNativeReturns': report['separateModeControlNativeReturns'], 'nativeByteModeApiSourceCredit': 0,
        'entryDomainOnly': True, 'wholeImageControlFlowCertified': False, 'outsideIndirectTransfersExhaustivelyRuledOut': False,
        'formalRawWords': report['differential']['formalRawWords'], 'nativeTableBytes': 64, 'allOwnRecordsExecuted': True,
        'naturalSceneOrRenewabilityMeaningProven': False,
        'scratchCallAbi': 'serialized raw binary32 formal captured in private slot81; primary predicates use private slot82; actual native four-byte copies retained'}
