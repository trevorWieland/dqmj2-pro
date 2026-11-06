from pathlib import Path
import sys
from project import ROOT, configuration, read_json, sha256
from interpreted_sources import local
from interpreted_linked_sources import require, native_hashes

KIND = 'source-linked-world-reset-SCR-v7'
VALIDATORS = ('validate_scr_empty_family_20261029_batch04.py',
              'validate_scr_numeric_transition_20261029_batch04.py', 'validate_scr_world32_20261030_batch09.py')


def candidates(report, relative, reproduction):
    hashes = {row['path']: row['sha256'] for row in report['sourceClosure']}
    hashes[report['generator']] = report['generatorSha256']
    hashes.update({path: sha256(ROOT / path) for path in VALIDATORS})
    inventory = read_json(ROOT / 'evidence/encounter/scripts-inventory-20261029.json')
    image = next(row for row in inventory['images'] if row['codeSha256'] == report['codeSha256'])
    return [{'report': relative, 'reproduce': reproduction, 'proofKind': KIND, 'sourceHashes': hashes,
             'nativeModuleHashes': native_hashes(),
             'identity': {key: image[key] for key in ('scriptSha256', 'codeSha256', 'entryTableSha256')},
             'range': {'entrySlots': [32], **report['matchedRange']}}]


def validated(report, image, batch):
    require(report['evidenceClass'] == 'ordinary-C-complete-reset-caller-with-source-linked-SCR-callees' and
            report['romSha256'] == configuration()['romSha256'], 'Reset SCR report identity differs')
    require(batch['nativeModuleHashes'] == native_hashes(), 'Reset SCR native VM namespace differs')
    require(report['wholeRomSourceMatch'] is False, 'Reset SCR partial source claims whole ROM')
    require(sha256(Path(sys.executable)) == read_json(ROOT / 'tools.lock.json')['python']['sha256'],
            'Reset SCR pinned Python identity differs')
    hashes = {row['path']: row['sha256'] for row in report['sourceClosure']}
    hashes[report['generator']] = report['generatorSha256']
    hashes.update({path: sha256(ROOT / path) for path in VALIDATORS})
    require(hashes == batch['sourceHashes'] and all(local(path).is_file() and sha256(local(path)) == pin for path, pin in hashes.items()),
            'Reset SCR frozen source/profile/validator closure changed')
    require(all(image[key] == value for key, value in batch['identity'].items()) and
            report['scriptSha256'] == image['scriptSha256'] and report['codeSha256'] == image['codeSha256'],
            'Reset SCR inventoried image differs')
    compiled = report['sourceOnlyBuilds'][0]['build']['compilerEvidence']
    require(compiled['generalCCompilerClaimed'] is False and
            report['boundariesAndLinks']['serializedCompleteCallsOnly'] is True, 'Reset SCR language/runtime scope differs')
    from validate_scr_world32_20261030_batch09 import validate
    units = validate(ROOT, batch['report'])
    require(len(units) == 1, 'Reset SCR unit population differs')
    row = units[image['codeSha256'], batch['range']['startPc']]
    region = {'entrySlots': row['entryAliases'], **{key: row[key] for key in ('startPc', 'endExclusivePc', 'bytes', 'sha256')}}
    require(region == batch['range'] and 0 <= region['startPc'] < region['endExclusivePc'] <= image['codeBytes'],
            'Reset SCR frozen complete range differs')
    return {'id': report['romSha256'] + '/scr/' + image['codeSha256'] + '/' + str(row['startPc']),
            'scriptSha256': image['scriptSha256'], 'codeSha256': image['codeSha256'], 'report': batch['report'],
            'sourceHashes': batch['sourceHashes'], 'range': region, 'sourceLanguage': 'restricted C99',
            'function': compiled['function'], 'sourceDefinitionId': row['sourceSha256'] + '/' + compiled['function'],
            'sourceByteCredit': row['bytes'], 'sourceUnitCredit': 1, 'completeImageCredit': 0, 'nativeByteCredit': 0,
            'implementationFamily': 'world-reset-caller-with-fresh-source-linked-callees', 'copyOnly': False,
            'completeScrEntryExecutions': len(report['differential']['cases']) * 4,
            'nativeRoutineReturnObservations': report['actualReturningCallsTotal'],
            'sourceLinkedCalleeReuseBytes': row['sourceLinkedCalleeReuseBytes'], 'sourceLinkedCalleeNewCredit': 0,
            'originalCalleeSourceCredit': 0, 'wholeImageControlFlowCertified': False,
            'outsideIndirectTransfersExhaustivelyRuledOut': False, 'scratchCallAbi': 'serialized complete named calls only'}
