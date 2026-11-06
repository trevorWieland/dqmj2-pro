from pathlib import Path
import sys
from project import ROOT, configuration, read_json, sha256
from interpreted_sources import local
from interpreted_linked_sources import require, native_hashes

KIND = 'complete-primary24-formal-pair-SCR-v8'
GENERATOR = 'match_scr_primary24_pair_20261030_batch10.py'
GENERATOR_HASH = '1184cbc5a2ad6a0ada8947f5d43d9fde6eb9657a8300fd063a4bd370991706e2'
VALIDATORS = {'validate_scr_empty_family_20261029_batch04.py': 'c3e38cbf73c38d98484f799ba20e2fe05c34612dff4310949837eab6ebb94604',
    'validate_scr_numeric_transition_20261029_batch04.py': 'ea6f463ee6792297ad091b561ae10eb19bdcb14d6165e8b221c9740570ed4020',
    'validate_scr_primary24_pair_20261030_batch10.py': '950f72fa5937c16d77f9a9a9ddcaf0ebdf18f323a7cdc85c0a41fe777f006195'}


def source_hashes(report):
    require(report['generator'] == GENERATOR and report['generatorSha256'] == GENERATOR_HASH,
            'Primary-pair frozen generator differs')
    require(all(local(path).is_file() and sha256(local(path)) == pin for path, pin in VALIDATORS.items()),
            'Primary-pair frozen validator differs')
    hashes = {row['path']: row['sha256'] for row in report['sourceClosure']}
    hashes[GENERATOR] = GENERATOR_HASH
    hashes.update(VALIDATORS)
    return hashes


def candidates(report, relative, reproduction):
    hashes = source_hashes(report)
    inventory = read_json(ROOT / 'evidence/encounter/scripts-inventory-20261029.json')
    rows = []
    require(len(report['units']) == 2, 'Primary-pair unit population differs')
    for unit in report['units']:
        image = next(row for row in inventory['images'] if row['codeSha256'] == unit['codeSha256'])
        rows.append({'report': relative, 'reproduce': reproduction, 'proofKind': KIND, 'sourceHashes': hashes,
            'nativeModuleHashes': native_hashes(),
            'identity': {key: image[key] for key in ('scriptSha256', 'codeSha256', 'entryTableSha256')},
            'range': {'entrySlots': [102], **unit['matchedRange']}})
    return rows


def validated(report, image, batch):
    require(report['evidenceClass'] == 'ordinary-C-complete-formal-primary24-set-clear-SCR-source-match'
            and report['romSha256'] == configuration()['romSha256'], 'Primary-pair report identity differs')
    require(batch['nativeModuleHashes'] == native_hashes(), 'Primary-pair native VM namespace differs')
    require(report['wholeRomSourceMatch'] is False, 'Primary-pair partial source claims whole ROM')
    require(sha256(Path(sys.executable)) == read_json(ROOT / 'tools.lock.json')['python']['sha256'],
            'Primary-pair pinned Python identity differs')
    hashes = source_hashes(report)
    require(hashes == batch['sourceHashes'] and all(local(path).is_file() and sha256(local(path)) == pin for path, pin in hashes.items()),
            'Primary-pair frozen source/profile/validator closure changed')
    require(all(image[key] == value for key, value in batch['identity'].items()), 'Primary-pair inventoried image differs')
    matches = [row for row in report['units'] if row['codeSha256'] == image['codeSha256'] and row['matchedRange']['startPc'] == batch['range']['startPc']]
    require(len(matches) == 1, 'Primary-pair qualified unit identity differs')
    selected = matches[0]
    require(selected['scriptSha256'] == image['scriptSha256'], 'Primary-pair inventoried script differs')
    compiled, scope = selected['sourceOnlyBuild']['compilerEvidence'], selected['boundariesAndStorage']
    require(compiled['generalCCompilerClaimed'] is False and compiled['uninitializedLocalReadsRejected'] is True
            and compiled['uninitializedDeclarationsEmitNoStore'] is True and compiled['branchLocalInitializationNotAssumedOutsideBranch'] is True
            and scope['allOwnReadsDominatedByAssignments'] is True and scope['uninitializedDeclarationDoesNotDefineAValue'] is True
            and scope['serializedCompleteCallsOnly'] is True and scope['opaqueNativeOrComputedSlotReferenceCoverageComplete'] is False,
            'Primary-pair language/assignment/runtime scope differs')
    from validate_scr_primary24_pair_20261030_batch10 import validate
    units = validate(ROOT, batch['report'])
    require(len(units) == 2, 'Primary-pair validated population differs')
    key = image['codeSha256'], batch['range']['startPc']
    require(key in units, 'Primary-pair selected identity not validated')
    row = units[key]
    region = {'entrySlots': row['entryAliases'], **{key: row[key] for key in ('startPc', 'endExclusivePc', 'bytes', 'sha256')}}
    require(region == batch['range'] and 0 <= region['startPc'] < region['endExclusivePc'] <= image['codeBytes'],
            'Primary-pair frozen complete range differs')
    require(selected['pairedCompleteOwnEntryExecutions'] == row['pairedCompleteOwnEntryExecutions']
            and selected['pairedNativeReturningCalls'] == row['pairedNativeReturningCalls'], 'Primary-pair entry/helper counts differ')
    return {'id': report['romSha256'] + '/scr/' + image['codeSha256'] + '/' + str(row['startPc']),
        'scriptSha256': image['scriptSha256'], 'codeSha256': image['codeSha256'], 'report': batch['report'],
        'sourceHashes': batch['sourceHashes'], 'range': region, 'sourceLanguage': 'restricted C99', 'function': compiled['function'],
        'sourceDefinitionId': row['sourceSha256'] + '/' + compiled['function'], 'sourceByteCredit': row['bytes'],
        'sourceUnitCredit': 1, 'completeImageCredit': 0, 'nativeByteCredit': 0, 'copyOnly': False,
        'implementationFamily': 'primary24-formal-conditional-' + selected['kind'],
        'completeScrEntryExecutions': row['pairedCompleteOwnEntryExecutions'],
        'nativeRoutineReturnObservations': row['pairedNativeReturningCalls'],
        'separateCallerPrefixNativeReturns': selected['prefixNativeReturningCalls'],
        'separateCallerPrefixTargetEntryExecutions': len(selected['differential']['qualifiedCallerPrefixes']) * 2,
        'callerPrefixOuterReturnCredit': 0, 'callerPrefixAdditionalSourceCredit': 0,
        'rawFloatFormalArgumentAbi': True, 'sourceLocalReadsRequireAssignedValues': True,
        'wholeImageControlFlowCertified': False, 'outsideIndirectTransfersExhaustivelyRuledOut': False,
        'scratchCallAbi': 'serialized fixed-slot float formal with measured assignment dominance and retained untouched slots'}
