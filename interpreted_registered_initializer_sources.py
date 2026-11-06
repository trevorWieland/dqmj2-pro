from pathlib import Path
import sys
from project import ROOT, configuration, read_json, sha256
from interpreted_sources import local
from interpreted_linked_sources import require, native_hashes

KIND = 'complete-module-global-float-initializer-SCR-v15'
GENERATOR = 'match_scr_registered_initializer_20261030_batch18.py'
GENERATOR_HASH = 'd797fafe52ee93d09628445d7d1e0d68ac348edb8f8de624d192ab913815ace1'
VALIDATORS = {'validate_scr_empty_family_20261029_batch04.py': 'c3e38cbf73c38d98484f799ba20e2fe05c34612dff4310949837eab6ebb94604',
    'validate_scr_numeric_transition_20261029_batch04.py': 'ea6f463ee6792297ad091b561ae10eb19bdcb14d6165e8b221c9740570ed4020',
    'validate_scr_registered_initializer_20261030_batch18.py': '9e450b2a001d9572d45ef246948a669b83099c49db69f38a30114a6d762d7672'}


def source_hashes(report):
    require(report['generator'] == GENERATOR and report['generatorSha256'] == GENERATOR_HASH, 'Registered-initializer frozen generator differs')
    require(all(local(path).is_file() and sha256(local(path)) == pin for path, pin in VALIDATORS.items()), 'Registered-initializer frozen validator differs')
    hashes = {row['path']: row['sha256'] for row in report['sourceClosure']}
    hashes[GENERATOR] = GENERATOR_HASH
    hashes.update(VALIDATORS)
    return hashes


def candidates(report, relative, reproduction):
    hashes = source_hashes(report)
    image = next(row for row in read_json(ROOT / 'evidence/encounter/scripts-inventory-20261029.json')['images'] if row['codeSha256'] == report['codeSha256'])
    return [{'report': relative, 'reproduce': reproduction, 'proofKind': KIND, 'sourceHashes': hashes, 'nativeModuleHashes': native_hashes(),
        'identity': {key: image[key] for key in ('scriptSha256', 'codeSha256', 'entryTableSha256')},
        'range': {'entrySlots': [256], **report['matchedRange']}}]


def validated(report, image, batch):
    require(report['evidenceClass'] == 'ordinary-C-complete-module-global-float-initializer-SCR-source-match'
        and report['romSha256'] == configuration()['romSha256'], 'Registered-initializer report identity differs')
    require(batch['nativeModuleHashes'] == native_hashes(), 'Registered-initializer native VM namespace differs')
    require(report['wholeRomSourceMatch'] is False, 'Registered-initializer partial source claims whole ROM')
    require(sha256(Path(sys.executable)) == read_json(ROOT / 'tools.lock.json')['python']['sha256'], 'Registered-initializer pinned Python identity differs')
    hashes = source_hashes(report)
    require(hashes == batch['sourceHashes'] and all(local(path).is_file() and sha256(local(path)) == pin for path, pin in hashes.items()),
        'Registered-initializer frozen source/profile/validator closure changed')
    require(all(image[key] == value for key, value in batch['identity'].items()) and report['scriptSha256'] == image['scriptSha256']
        and report['codeSha256'] == image['codeSha256'], 'Registered-initializer inventoried image differs')
    compiled, scope = report['sourceOnlyBuild']['compilerEvidence'], report['boundariesAndStorage']
    require(report['initializationOnly'] is True and report['branchDecisionLogicClaimed'] is False and compiled['initializationOnly'] is True
        and compiled['branchDecisionLogicClaimed'] is False and compiled['sourceReturnType'] == 'void' and compiled['implicitPrivateReturn'] is True
        and compiled['generalCCompilerClaimed'] is False and compiled['opaqueGlobalDomainProofClaimed'] is False
        and scope['moduleGlobalsAreNotPrivateLocals'] is True and scope['moduleGlobalSlots'] == list(range(3, 23)) and scope['privateLocalSlots'] == []
        and scope['knownFollowingPaddingRange'] == [1048, 1056] and scope['followingPaddingSourceCredit'] == 0
        and scope['opaqueNativeComputedReferenceCoverageComplete'] is False and scope['naturalInitializerOrRegistrationCallerReachabilityProven'] is False,
        'Registered-initializer language/global/initialization/padding scope differs')
    from validate_scr_registered_initializer_20261030_batch18 import validate
    units = validate(ROOT, batch['report'])
    require(len(units) == 1, 'Registered-initializer validated population differs')
    key = image['codeSha256'], batch['range']['startPc']
    require(key in units, 'Registered-initializer selected identity not validated')
    row = units[key]
    region = {'entrySlots': row['entryAliases'], **{name: row[name] for name in ('startPc', 'endExclusivePc', 'bytes', 'sha256')}}
    require(region == batch['range'] and 0 <= region['startPc'] < region['endExclusivePc'] <= image['codeBytes'], 'Registered-initializer frozen complete range differs')
    return {'id': report['romSha256'] + '/scr/' + image['codeSha256'] + '/' + str(row['startPc']), 'scriptSha256': image['scriptSha256'],
        'codeSha256': image['codeSha256'], 'report': batch['report'], 'sourceHashes': batch['sourceHashes'], 'range': region,
        'sourceLanguage': 'restricted C99', 'function': compiled['function'], 'sourceDefinitionId': row['sourceSha256'] + '/' + compiled['function'],
        'sourceByteCredit': row['bytes'], 'sourceUnitCredit': 1, 'nativeByteCredit': 0, 'completeImageCredit': 0, 'copyOnly': False,
        'initializationOnly': True, 'branchDecisionLogicClaimed': False, 'implementationFamily': 'module-global-binary32-sentinel-initialization',
        'completeScrEntryExecutions': row['pairedCompleteOwnEntryExecutions'], 'nativeRoutineReturnObservations': row['pairedNativeReturningCalls'],
        'moduleGlobalSlots': row['moduleGlobalSlots'], 'privateLocalSlots': [], 'followingPaddingSourceCredit': 0,
        'moduleGlobalNaturalProducerDomainProven': False, 'wholeImageControlFlowCertified': False,
        'outsideIndirectTransfersExhaustivelyRuledOut': False, 'naturalSceneOrRenewabilityMeaningProven': False,
        'scratchCallAbi': 'no formals; twenty explicit VM-context module-global float stores; all236 other slots preserved; serialized reentry'}
