from pathlib import Path
import sys
from project import ROOT, configuration, read_json, sha256
from interpreted_sources import local
from interpreted_linked_sources import require, native_hashes

KIND = 'complete-runtime-primary-loop-SCR-v10'
GENERATOR = 'match_scr_runtime_flags_20261030_batch12.py'
GENERATOR_HASH = '4aa270e05a37ae5028642a9ecb6a4d99d431d81cd3614ec270f8f8373e7a8576'
VALIDATORS = {'validate_scr_empty_family_20261029_batch04.py': 'c3e38cbf73c38d98484f799ba20e2fe05c34612dff4310949837eab6ebb94604',
    'validate_scr_numeric_transition_20261029_batch04.py': 'ea6f463ee6792297ad091b561ae10eb19bdcb14d6165e8b221c9740570ed4020',
    'validate_scr_runtime_flags_20261030_batch12.py': '042edb374dff9f3149069696182fa8877042c302d24738386e41877e5b22280d'}


def source_hashes(report):
    require(report['generator'] == GENERATOR and report['generatorSha256'] == GENERATOR_HASH,
            'Runtime-loop frozen generator differs')
    require(all(local(path).is_file() and sha256(local(path)) == pin for path, pin in VALIDATORS.items()),
            'Runtime-loop frozen validator differs')
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
        'range': {'entrySlots': [257], **report['matchedRange']}}]


def validated(report, image, batch):
    require(report['evidenceClass'] == 'ordinary-C-complete-runtime-primary-flag-loop-SCR-source-match'
            and report['romSha256'] == configuration()['romSha256'], 'Runtime-loop report identity differs')
    require(batch['nativeModuleHashes'] == native_hashes(), 'Runtime-loop native VM namespace differs')
    require(report['wholeRomSourceMatch'] is False, 'Runtime-loop partial source claims whole ROM')
    require(sha256(Path(sys.executable)) == read_json(ROOT / 'tools.lock.json')['python']['sha256'],
            'Runtime-loop pinned Python identity differs')
    hashes = source_hashes(report)
    require(hashes == batch['sourceHashes'] and all(local(path).is_file() and sha256(local(path)) == pin for path, pin in hashes.items()),
            'Runtime-loop frozen source/profile/validator closure changed')
    require(all(image[key] == value for key, value in batch['identity'].items())
            and report['scriptSha256'] == image['scriptSha256'] and report['codeSha256'] == image['codeSha256'],
            'Runtime-loop inventoried image differs')
    compiled, scope = report['sourceOnlyBuild']['compilerEvidence'], report['boundariesAndStorage']
    require(compiled['generalCCompilerClaimed'] is False and compiled['runtimeLoop'] is True
            and compiled['constantLoopUnrolled'] is False and compiled['entryNonemptyConditionStaticallyProven'] is True
            and compiled['counter']['sourceType'] == 'int' and compiled['counter']['allIntegerValuesExactlyRepresentable'] is True
            and scope['serializedCompleteEntryDomainOnly'] is True and scope['unreachableJoinNotCountedAsExecuted'] is True
            and scope['opaqueNativeOrComputedSlotReferenceCoverageComplete'] is False,
            'Runtime-loop language/integer-domain/entry scope differs')
    from validate_scr_runtime_flags_20261030_batch12 import validate
    units = validate(ROOT, batch['report'])
    require(len(units) == 1, 'Runtime-loop validated population differs')
    key = image['codeSha256'], batch['range']['startPc']
    require(key in units, 'Runtime-loop selected identity not validated')
    row = units[key]
    region = {'entrySlots': row['entryAliases'], **{name: row[name] for name in ('startPc', 'endExclusivePc', 'bytes', 'sha256')}}
    require(region == batch['range'] and 0 <= region['startPc'] < region['endExclusivePc'] <= image['codeBytes'],
            'Runtime-loop frozen complete range differs')
    return {'id': report['romSha256'] + '/scr/' + image['codeSha256'] + '/' + str(row['startPc']),
        'scriptSha256': image['scriptSha256'], 'codeSha256': image['codeSha256'], 'report': batch['report'],
        'sourceHashes': batch['sourceHashes'], 'range': region, 'sourceLanguage': 'restricted C99', 'function': compiled['function'],
        'sourceDefinitionId': row['sourceSha256'] + '/' + compiled['function'], 'sourceByteCredit': row['bytes'],
        'sourceUnitCredit': 1, 'completeImageCredit': 0, 'nativeByteCredit': 0, 'copyOnly': False,
        'implementationFamily': 'constant-bounded-integer-counter-runtime-primary-flag-loop',
        'completeScrEntryExecutions': row['pairedCompleteOwnEntryExecutions'],
        'nativeRoutineReturnObservations': row['pairedNativeReturningCalls'],
        'primarySetterExecutions': row['pairedPrimarySetterExecutions'],
        'separateCompilerControlNativeReturns': report['separateBoundaryControlNativeReturns'],
        'compilerGeneratedUnreachableJoinBytes': row['compilerGeneratedUnreachableJoinBytes'],
        'compilerGeneratedUnreachableJoinPcs': scope['compilerGeneratedUnreachableJoins'],
        'entryDomainOnly': True, 'wholeImageControlFlowCertified': False, 'outsideIndirectTransfersExhaustivelyRuledOut': False,
        'runtimeLoop': True, 'constantLoopUnrolled': False, 'sourceCounterType': 'int',
        'counterVmRepresentation': compiled['counter']['vmRepresentation'],
        'finiteIntegerCounterDomain': {name: compiled['counter'][name] for name in
            ('start', 'endExclusive', 'step', 'iterations', 'finalValue')},
        'naturalSceneOrRenewabilityMeaningProven': False,
        'scratchCallAbi': 'serialized entry-domain runtime loop; finite C integers exactly represented in binary32; only counter slot33 changes'}
