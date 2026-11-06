from pathlib import Path
import sys
from project import ROOT, configuration, read_json, sha256
from interpreted_sources import local
from interpreted_linked_sources import require, native_hashes

KIND = 'complete-native-record-capacity-decision-SCR-v17'
GENERATOR = 'match_scr_record_capacity_20261030_batch21.py'
GENERATOR_HASH = 'e046f4aa2eb4d33f0990725b8c92f11f8ecc250b4be119391eab27c84aa687de'
VALIDATORS = {'validate_scr_empty_family_20261029_batch04.py': 'c3e38cbf73c38d98484f799ba20e2fe05c34612dff4310949837eab6ebb94604',
    'validate_scr_numeric_transition_20261029_batch04.py': 'ea6f463ee6792297ad091b561ae10eb19bdcb14d6165e8b221c9740570ed4020',
    'validate_scr_record_capacity_20261030_batch21.py': '5e814a03f79480267be48b9b7ece68d02693141db73ae1931edff5c3d74696ba'}


def source_hashes(report):
    require(report['generator'] == GENERATOR and report['generatorSha256'] == GENERATOR_HASH, 'Record-capacity frozen generator differs')
    require(all(local(path).is_file() and sha256(local(path)) == pin for path, pin in VALIDATORS.items()), 'Record-capacity frozen validator differs')
    hashes = {row['path']: row['sha256'] for row in report['sourceClosure']}
    hashes[GENERATOR] = GENERATOR_HASH
    hashes.update(VALIDATORS)
    return hashes


def candidates(report, relative, reproduction):
    hashes = source_hashes(report)
    image = next(row for row in read_json(ROOT / 'evidence/encounter/scripts-inventory-20261029.json')['images'] if row['codeSha256'] == report['codeSha256'])
    return [{'report': relative, 'reproduce': reproduction, 'proofKind': KIND, 'sourceHashes': hashes, 'nativeModuleHashes': native_hashes(),
        'identity': {key: image[key] for key in ('scriptSha256', 'codeSha256', 'entryTableSha256')}, 'range': {'entrySlots': [279], **report['matchedRange']}}]


def validated(report, image, batch):
    require(report['evidenceClass'] == 'ordinary-C-complete-native-record-capacity-decision-SCR-source-match'
        and report['romSha256'] == configuration()['romSha256'], 'Record-capacity report identity differs')
    require(batch['nativeModuleHashes'] == native_hashes(), 'Record-capacity native VM namespace differs')
    require(report['wholeRomSourceMatch'] is False, 'Record-capacity partial source claims whole ROM')
    require(sha256(Path(sys.executable)) == read_json(ROOT / 'tools.lock.json')['python']['sha256'], 'Record-capacity pinned Python identity differs')
    hashes = source_hashes(report)
    require(hashes == batch['sourceHashes'] and all(local(path).is_file() and sha256(local(path)) == pin for path, pin in hashes.items()),
        'Record-capacity frozen source/profile/validator closure changed')
    require(all(image[key] == value for key, value in batch['identity'].items()) and report['scriptSha256'] == image['scriptSha256']
        and report['codeSha256'] == image['codeSha256'], 'Record-capacity inventoried image differs')
    compiled, scope, proof = report['sourceOnlyBuild']['compilerEvidence'], report['boundariesAndStorage'], report['differential']
    require(compiled['sourceReturnType'] == 'float' and compiled['returnConvention'] == 'VM argument register0 raw binary32'
        and compiled['generalCCompilerClaimed'] is False and compiled['moduleAndArgumentObjectsAreNotPrivateLocals'] is True
        and compiled['opaqueGlobalDomainProofClaimed'] is False and scope['moduleGlobalSlots'] == [0, 1, 2] and scope['privateLocalSlots'] == []
        and scope['argumentBankLiveIns'] == scope['argumentBankCallClobbers'] == [0] and scope['followingPaddingSourceCredit'] == 0
        and scope['opaqueNativeComputedReferenceCoverageComplete'] is False and scope['naturalCallerReachabilityProven'] is False
        and proof['providerCount'] == 0 and proof['allOriginalCounterCallsRetained'] is True and proof['nativeUIDWordCountOnly'] is True
        and proof['fullRecordValidityOwnershipImportLegalityOrSceneReachabilityProven'] is False
        and report['nativeRecordValidityOwnershipImportLegalityOrNaturalSceneReachabilityProven'] is False,
        'Record-capacity float/shared/counter/record-validity scope differs')
    from validate_scr_record_capacity_20261030_batch21 import validate
    units = validate(ROOT, batch['report'])
    key = image['codeSha256'], batch['range']['startPc']
    require(len(units) == 1 and key in units, 'Record-capacity qualified unit not validated')
    row = units[key]
    region = {'entrySlots': row['entryAliases'], **{name: row[name] for name in ('startPc', 'endExclusivePc', 'bytes', 'sha256')}}
    require(region == batch['range'] and 0 <= region['startPc'] < region['endExclusivePc'] <= image['codeBytes'], 'Record-capacity frozen complete range differs')
    return {'id': report['romSha256'] + '/scr/' + image['codeSha256'] + '/0', 'scriptSha256': image['scriptSha256'], 'codeSha256': image['codeSha256'],
        'report': batch['report'], 'sourceHashes': batch['sourceHashes'], 'range': region, 'sourceLanguage': 'restricted C99', 'function': row['function'],
        'sourceDefinitionId': row['sourceSha256'] + '/' + row['function'], 'sourceByteCredit': 544, 'sourceUnitCredit': 1,
        'nativeByteCredit': 0, 'completeImageCredit': 0, 'copyOnly': False, 'implementationFamily': 'three-mode-threshold-decision-on-original-native-UID-word-count',
        'completeScrEntryExecutions': row['pairedCompleteOwnEntryExecutions'], 'nativeRoutineReturnObservations': row['pairedNativeReturningCalls'],
        'nativeNestedCounterReturnObservations': row['pairedActualNestedCounterReturns'], 'moduleGlobalSlots': [0, 1, 2], 'privateLocalSlots': [],
        'argumentBankLiveIns': [0], 'argumentBankCallClobbers': [0], 'allOriginalCounterCallsRetained': True, 'nativeUIDWordCountOnly': True,
        'recordValidityOwnershipImportLegalityOrNaturalSceneReachabilityProven': False, 'wholeImageControlFlowCertified': False,
        'outsideIndirectTransfersExhaustivelyRuledOut': False,
        'scratchCallAbi': 'explicit raw argument0 and module slots0–2; original five counter calls; finite count0..100; scalar float0/1 return; serialized reentry'}
