from pathlib import Path
import sys
from project import ROOT, configuration, read_json, sha256
from interpreted_sources import local
from interpreted_linked_sources import require, native_hashes

KIND = 'complete-bounded-selection-SCR-v9'
GENERATOR = 'match_scr_world17_20261030_batch11.py'
GENERATOR_HASH = 'b405d19b31a6a5d85f1c66ba2ec3fee66410482a7c34d6bed352bd65b3d0d1ff'
VALIDATORS = {'validate_scr_empty_family_20261029_batch04.py': 'c3e38cbf73c38d98484f799ba20e2fe05c34612dff4310949837eab6ebb94604',
    'validate_scr_numeric_transition_20261029_batch04.py': 'ea6f463ee6792297ad091b561ae10eb19bdcb14d6165e8b221c9740570ed4020',
    'validate_scr_world17_20261030_batch11.py': '49ced7585baaf67f55de3ce504955f76b7a9d107bd133e44753fd4e58c9bfec2'}


def source_hashes(report):
    require(report['generator'] == GENERATOR and report['generatorSha256'] == GENERATOR_HASH,
            'Bounded-selection frozen generator differs')
    require(all(local(path).is_file() and sha256(local(path)) == pin for path, pin in VALIDATORS.items()),
            'Bounded-selection frozen validator differs')
    hashes = {row['path']: row['sha256'] for row in report['sourceClosure']}
    hashes[GENERATOR] = GENERATOR_HASH
    hashes.update(VALIDATORS)
    return hashes


def candidates(report, relative, reproduction):
    hashes = source_hashes(report)
    inventory = read_json(ROOT / 'evidence/encounter/scripts-inventory-20261029.json')
    image = next(row for row in inventory['images'] if row['codeSha256'] == report['codeSha256'])
    return [{'report': relative, 'reproduce': reproduction, 'proofKind': KIND, 'sourceHashes': hashes,
        'nativeModuleHashes': native_hashes(),
        'identity': {key: image[key] for key in ('scriptSha256', 'codeSha256', 'entryTableSha256')},
        'range': {'entrySlots': [17], **report['matchedRange']}}]


def validated(report, image, batch):
    require(report['evidenceClass'] == 'ordinary-C-complete-bounded-random-early-return-SCR-source-match'
            and report['romSha256'] == configuration()['romSha256'], 'Bounded-selection report identity differs')
    require(batch['nativeModuleHashes'] == native_hashes(), 'Bounded-selection native VM namespace differs')
    require(report['wholeRomSourceMatch'] is False, 'Bounded-selection partial source claims whole ROM')
    require(sha256(Path(sys.executable)) == read_json(ROOT / 'tools.lock.json')['python']['sha256'],
            'Bounded-selection pinned Python identity differs')
    hashes = source_hashes(report)
    require(hashes == batch['sourceHashes'] and all(local(path).is_file() and sha256(local(path)) == pin for path, pin in hashes.items()),
            'Bounded-selection frozen source/profile/validator closure changed')
    require(all(image[key] == value for key, value in batch['identity'].items()) and report['scriptSha256'] == image['scriptSha256']
            and report['codeSha256'] == image['codeSha256'], 'Bounded-selection inventoried image differs')
    compiled, scope = report['sourceOnlyBuild']['compilerEvidence'], report['boundariesAndStorage']
    require(compiled['generalCCompilerClaimed'] is False and scope['serializedCompleteEntryDomainOnly'] is True
            and scope['unreachableJoinsNotCountedAsExecuted'] is True and report['unreachableCompilerJoinRecordsNotForced'] is True
            and scope['opaqueNativeOrComputedSlotReferenceCoverageComplete'] is False,
            'Bounded-selection language/entry-domain scope differs')
    from validate_scr_world17_20261030_batch11 import validate
    units = validate(ROOT, batch['report'])
    require(len(units) == 1, 'Bounded-selection validated population differs')
    key = image['codeSha256'], batch['range']['startPc']
    require(key in units, 'Bounded-selection selected identity not validated')
    row = units[key]
    region = {'entrySlots': row['entryAliases'], **{key: row[key] for key in ('startPc', 'endExclusivePc', 'bytes', 'sha256')}}
    require(region == batch['range'] and 0 <= region['startPc'] < region['endExclusivePc'] <= image['codeBytes'],
            'Bounded-selection frozen complete range differs')
    return {'id': report['romSha256'] + '/scr/' + image['codeSha256'] + '/' + str(row['startPc']),
        'scriptSha256': image['scriptSha256'], 'codeSha256': image['codeSha256'], 'report': batch['report'],
        'sourceHashes': batch['sourceHashes'], 'range': region, 'sourceLanguage': 'restricted C99', 'function': compiled['function'],
        'sourceDefinitionId': row['sourceSha256'] + '/' + compiled['function'], 'sourceByteCredit': row['bytes'],
        'sourceUnitCredit': 1, 'completeImageCredit': 0, 'nativeByteCredit': 0, 'copyOnly': False,
        'implementationFamily': 'bounded-native-random-selection-with-qualified-early-returns',
        'completeScrEntryExecutions': row['pairedCompleteOwnEntryExecutions'],
        'nativeRoutineReturnObservations': row['pairedNativeReturningCalls'],
        'separateCompilerControlNativeReturns': row['syntheticByteControlNativeReturns'],
        'compilerGeneratedUnreachableJoinBytes': row['compilerGeneratedUnreachableJoinBytes'],
        'compilerGeneratedUnreachableJoinPcs': scope['compilerGeneratedUnreachableJoins'],
        'excludedBranchOutcomes': report['excludedBranchOutcomes'],
        'entryDomainOnly': True, 'wholeImageControlFlowCertified': False, 'outsideIndirectTransfersExhaustivelyRuledOut': False,
        'scratchCallAbi': 'serialized entry-domain calls with genuine bound6 RNG; unreachable joins and impossible final false outcome excluded'}
