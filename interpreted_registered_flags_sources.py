from pathlib import Path
import sys
from project import ROOT, configuration, read_json, sha256
from interpreted_sources import local
from interpreted_linked_sources import require, native_hashes

KIND = 'complete-registered-dynamic-primary-float-return-SCR-v14'
GENERATOR = 'match_scr_registered_flags_20261030_batch17.py'
GENERATOR_HASH = '4e598094ada3d74c3a3ada59494b001a1a2d116b0d43f8eae93b046da412d023'
VALIDATORS = {'validate_scr_empty_family_20261029_batch04.py': 'c3e38cbf73c38d98484f799ba20e2fe05c34612dff4310949837eab6ebb94604',
    'validate_scr_numeric_transition_20261029_batch04.py': 'ea6f463ee6792297ad091b561ae10eb19bdcb14d6165e8b221c9740570ed4020',
    'validate_scr_registered_flags_20261030_batch17.py': '2dff9d1fe00b72514a295fb7e9a38b16d28d258ed28f2f2e61dd65d96dae7c21'}


def source_hashes(report):
    require(report['generator'] == GENERATOR and report['generatorSha256'] == GENERATOR_HASH, 'Registered-flags frozen generator differs')
    require(all(local(path).is_file() and sha256(local(path)) == pin for path, pin in VALIDATORS.items()), 'Registered-flags frozen validator differs')
    hashes = {row['path']: row['sha256'] for row in report['sourceClosure']}
    hashes[GENERATOR] = GENERATOR_HASH
    hashes.update(VALIDATORS)
    return hashes


def candidates(report, relative, reproduction):
    hashes = source_hashes(report)
    image = next(row for row in read_json(ROOT / 'evidence/encounter/scripts-inventory-20261029.json')['images'] if row['codeSha256'] == report['codeSha256'])
    return [{'report': relative, 'reproduce': reproduction, 'proofKind': KIND, 'sourceHashes': hashes, 'nativeModuleHashes': native_hashes(),
        'identity': {key: image[key] for key in ('scriptSha256', 'codeSha256', 'entryTableSha256')},
        'range': {'entrySlots': [259], **report['matchedRange']}}]


def validated(report, image, batch):
    require(report['evidenceClass'] == 'ordinary-C-complete-registered-dynamic-primary-float-return-SCR-source-match'
        and report['romSha256'] == configuration()['romSha256'], 'Registered-flags report identity differs')
    require(batch['nativeModuleHashes'] == native_hashes(), 'Registered-flags native VM namespace differs')
    require(report['wholeRomSourceMatch'] is False, 'Registered-flags partial source claims whole ROM')
    require(sha256(Path(sys.executable)) == read_json(ROOT / 'tools.lock.json')['python']['sha256'], 'Registered-flags pinned Python identity differs')
    hashes = source_hashes(report)
    require(hashes == batch['sourceHashes'] and all(local(path).is_file() and sha256(local(path)) == pin for path, pin in hashes.items()),
        'Registered-flags frozen source/profile/validator closure changed')
    require(all(image[key] == value for key, value in batch['identity'].items()) and report['scriptSha256'] == image['scriptSha256']
        and report['codeSha256'] == image['codeSha256'], 'Registered-flags inventoried image differs')
    compiled, scope = report['sourceOnlyBuild']['compilerEvidence'], report['boundariesAndStorage']
    require(compiled['generalCCompilerClaimed'] is False and compiled['sourceReturnType'] == 'float'
        and compiled['returnConvention'] == 'VM argument register0 raw binary32' and compiled['formalCopyRepresentation'] == 'raw IEEE754 binary32 bits'
        and compiled['dynamicPrimaryIndexRequiresQualifiedFiniteIntegerDomain'] == [0, 1535] and compiled['floatEqualityUsesNativeVmComparison'] is True
        and compiled['opaqueGlobalDomainProofClaimed'] is False and scope['moduleGlobalsAreNotPrivateLocals'] is True
        and scope['moduleGlobalSlots'] == list(range(3, 23)) and scope['localSlots'] == [42, 43, 44]
        and scope['serializedCompleteEntryDomainOnly'] is True and scope['opaqueNativeOrComputedGlobalReferenceCoverageComplete'] is False,
        'Registered-flags language/raw-return/global/dynamic-index scope differs')
    from validate_scr_registered_flags_20261030_batch17 import validate
    units = validate(ROOT, batch['report'])
    require(len(units) == 1, 'Registered-flags validated population differs')
    key = image['codeSha256'], batch['range']['startPc']
    require(key in units, 'Registered-flags selected identity not validated')
    row = units[key]
    region = {'entrySlots': row['entryAliases'], **{name: row[name] for name in ('startPc', 'endExclusivePc', 'bytes', 'sha256')}}
    require(region == batch['range'] and 0 <= region['startPc'] < region['endExclusivePc'] <= image['codeBytes'], 'Registered-flags frozen complete range differs')
    return {'id': report['romSha256'] + '/scr/' + image['codeSha256'] + '/' + str(row['startPc']), 'scriptSha256': image['scriptSha256'],
        'codeSha256': image['codeSha256'], 'report': batch['report'], 'sourceHashes': batch['sourceHashes'], 'range': region,
        'sourceLanguage': 'restricted C99', 'function': compiled['function'], 'sourceDefinitionId': row['sourceSha256'] + '/' + compiled['function'],
        'sourceByteCredit': row['bytes'], 'sourceUnitCredit': 1, 'nativeByteCredit': 0, 'completeImageCredit': 0, 'copyOnly': False,
        'implementationFamily': 'first-matching-module-key-conditional-dynamic-primary-set-with-raw-float-return',
        'completeScrEntryExecutions': row['pairedCompleteOwnEntryExecutions'], 'nativeRoutineReturnObservations': row['pairedNativeReturningCalls'],
        'moduleGlobalSlots': row['moduleGlobalSlots'], 'privateLocalSlots': row['privateLocalSlots'], 'sourceReturnType': 'float',
        'returnConvention': row['returnConvention'], 'selectedDynamicIndexDomain': [0, 1535], 'domainAppliesOnlyWhenActuallyUsed': True,
        'unsupportedContextNativeErrorCredit': 0, 'moduleGlobalNaturalProducerDomainProven': False, 'entryDomainOnly': True,
        'wholeImageControlFlowCertified': False, 'outsideIndirectTransfersExhaustivelyRuledOut': False,
        'naturalSceneOrRenewabilityMeaningProven': False,
        'scratchCallAbi': 'serialized raw float formal/result; twenty explicit module globals; three private locals; selected finite integral primary index only'}
