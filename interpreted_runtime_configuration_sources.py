from pathlib import Path
import sys
from project import ROOT, configuration, read_json, sha256
from interpreted_sources import local
from interpreted_linked_sources import require, native_hashes

KIND = 'complete-shared-module-primary-configuration-SCR-v16'
GENERATOR = 'match_scr_runtime_configuration_20261030_batch19.py'
GENERATOR_HASH = '0311afc386e8fd86a2a3685fd82b3a2b136f4dbb9f86961e703d5d5167cd90e8'
VALIDATORS = {'validate_scr_empty_family_20261029_batch04.py': 'c3e38cbf73c38d98484f799ba20e2fe05c34612dff4310949837eab6ebb94604',
    'validate_scr_numeric_transition_20261029_batch04.py': 'ea6f463ee6792297ad091b561ae10eb19bdcb14d6165e8b221c9740570ed4020',
    'validate_scr_runtime_configuration_20261030_batch19.py': '87d2bdf6c79dbc0fad5754d6c63426ab834545fe04203899e2ff4082959b70ab'}


def source_hashes(report):
    require(report['generator'] == GENERATOR and report['generatorSha256'] == GENERATOR_HASH, 'Runtime-configuration frozen generator differs')
    require(all(local(path).is_file() and sha256(local(path)) == pin for path, pin in VALIDATORS.items()), 'Runtime-configuration frozen validator differs')
    hashes = {row['path']: row['sha256'] for row in report['sourceClosure']}
    hashes[GENERATOR] = GENERATOR_HASH
    hashes.update(VALIDATORS)
    return hashes


def candidates(report, relative, reproduction):
    hashes = source_hashes(report)
    image = next(row for row in read_json(ROOT / 'evidence/encounter/scripts-inventory-20261029.json')['images'] if row['codeSha256'] == report['codeSha256'])
    return [{'report': relative, 'reproduce': reproduction, 'proofKind': KIND, 'sourceHashes': hashes, 'nativeModuleHashes': native_hashes(),
        'identity': {key: image[key] for key in ('scriptSha256', 'codeSha256', 'entryTableSha256')},
        'range': {'entrySlots': [unit['entry']], **unit['range']}} for unit in report['sourceOnlyBuild']['units']]


def validated(report, image, batch):
    require(report['evidenceClass'] == 'ordinary-C-complete-shared-module-primary-configuration-SCR-source-match'
        and report['romSha256'] == configuration()['romSha256'], 'Runtime-configuration report identity differs')
    require(batch['nativeModuleHashes'] == native_hashes(), 'Runtime-configuration native VM namespace differs')
    require(report['wholeRomSourceMatch'] is False, 'Runtime-configuration partial source claims whole ROM')
    require(sha256(Path(sys.executable)) == read_json(ROOT / 'tools.lock.json')['python']['sha256'], 'Runtime-configuration pinned Python identity differs')
    hashes = source_hashes(report)
    require(hashes == batch['sourceHashes'] and all(local(path).is_file() and sha256(local(path)) == pin for path, pin in hashes.items()),
        'Runtime-configuration frozen source/profile/validator closure changed')
    require(all(image[key] == value for key, value in batch['identity'].items()) and report['scriptSha256'] == image['scriptSha256']
        and report['codeSha256'] == image['codeSha256'], 'Runtime-configuration inventoried image differs')
    proof = report['differential']
    require(report['originalConstructorRetained'] is True and report['constructorCapacityExhaustedReturnOnly'] is True
        and report['freePoolSuccessOrNaturalSceneReachabilityProven'] is False and proof['providerCount'] == 0 and proof['originalConstructorRetained'] is True
        and proof['all16PoolRecordsNonzeroActiveRequired'] is True and proof['constructorCapacityExhaustedReturnOnly'] is True
        and proof['freePoolSuccessOrNaturalSceneReachabilityProven'] is False and proof['primaryIndexDomain'] == [0, 1535]
        and proof['coordinateDomain'] == 'finite binary32 values with absolute value <=4096', 'Runtime-configuration native full-pool/ABI/domain scope differs')
    for product, scope in zip(report['sourceOnlyBuild']['units'], report['boundariesAndStorage']):
        compiled = product['compilerEvidence']
        require(compiled['generalCCompilerClaimed'] is False and compiled['moduleAndArgumentObjectsAreNotPrivateLocals'] is True
            and compiled['opaqueGlobalDomainProofClaimed'] is False and compiled['configurationFloatInputsRequireQualifiedNativeConversionDomain'] is True
            and scope['privateLocalSlots'] == [] and scope['moduleAndArgumentObjectsAreNotPrivateLocals'] is True
            and scope['argumentBankLiveIns'] == [0, 1, 2, 3, 4] and scope['argumentBankCallClobbers'] == list(range(7))
            and scope['followingPaddingSourceCredit'] == 0 and scope['opaqueNativeComputedReferenceCoverageComplete'] is False
            and scope['naturalCallerReachabilityProven'] is False, 'Runtime-configuration shared globals/argument/boundary scope differs')
    from validate_scr_runtime_configuration_20261030_batch19 import validate
    units = validate(ROOT, batch['report'])
    require(len(units) == 2, 'Runtime-configuration grouped population differs')
    key = image['codeSha256'], batch['range']['startPc']
    require(key in units, 'Runtime-configuration selected identity not validated')
    row = units[key]
    region = {'entrySlots': row['entryAliases'], **{name: row[name] for name in ('startPc', 'endExclusivePc', 'bytes', 'sha256')}}
    require(region == batch['range'] and 0 <= region['startPc'] < region['endExclusivePc'] <= image['codeBytes'], 'Runtime-configuration frozen complete range differs')
    return {'id': report['romSha256'] + '/scr/' + image['codeSha256'] + '/' + str(row['startPc']), 'scriptSha256': image['scriptSha256'],
        'codeSha256': image['codeSha256'], 'report': batch['report'], 'sourceHashes': batch['sourceHashes'], 'range': region,
        'sourceLanguage': 'restricted C99', 'function': row['function'], 'sourceDefinitionId': row['sourceSha256'] + '/' + row['function'],
        'sourceByteCredit': row['bytes'], 'sourceUnitCredit': 1, 'nativeByteCredit': 0, 'completeImageCredit': 0, 'copyOnly': False,
        'implementationFamily': 'primary-flag-selects-original-runtime-constructor-mode-with-shared-argument-captures',
        'completeScrEntryExecutions': row['pairedCompleteOwnEntryExecutions'], 'nativeRoutineReturnObservations': row['pairedNativeReturningCalls'],
        'moduleGlobalSlots': row['moduleGlobalSlots'], 'privateLocalSlots': [], 'argumentBankLiveIns': row['argumentBankLiveIns'],
        'argumentBankCallClobbers': row['argumentBankCallClobbers'], 'originalConstructorRetained': True, 'providerCount': 0,
        'supportedNativeContext': 'all16-pool-records-nonzero-active; original capacity-exhausted return only',
        'freePoolSuccessOrNaturalSceneReachabilityProven': False, 'wholeImageControlFlowCertified': False,
        'outsideIndirectTransfersExhaustivelyRuledOut': False, 'naturalSceneOrRenewabilityMeaningProven': False,
        'scratchCallAbi': 'explicit module/argument globals; finite coordinate domain; primary index0..1535; full pool; serialized reentry'}
