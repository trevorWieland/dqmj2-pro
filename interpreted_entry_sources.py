from pathlib import Path
import sys
from project import ROOT, configuration, read_json, sha256
from interpreted_sources import local
from interpreted_linked_sources import require, native_hashes

KIND = 'complete-entry-original-calls-SCR-v5'
VALIDATORS = ('validate_scr_empty_family_20261029_batch04.py',
              'validate_scr_numeric_transition_20261029_batch04.py', 'validate_scr_entry129_20261029_batch07.py')


def candidates(report, relative, reproduction):
    hashes = {row['path']: row['sha256'] for row in report['sourceClosure']}
    hashes[report['generator']] = report['generatorSha256']
    hashes.update({path: sha256(ROOT / path) for path in VALIDATORS})
    inventory = read_json(ROOT / 'evidence/encounter/scripts-inventory-20261029.json')
    image = next(row for row in inventory['images'] if row['codeSha256'] == report['codeSha256'])
    return [{'report': relative, 'reproduce': reproduction, 'proofKind': KIND, 'sourceHashes': hashes,
             'nativeModuleHashes': native_hashes(),
             'identity': {key: image[key] for key in ('scriptSha256', 'codeSha256', 'entryTableSha256')},
             'range': {'entrySlots': [129], **report['matchedRange']}}]


def validated(report, image, batch):
    require(report['evidenceClass'] == 'ordinary-C-complete-entry129-typed-script-call-SCR-match' and
            report['romSha256'] == configuration()['romSha256'], 'Entry SCR report identity differs')
    require(batch['nativeModuleHashes'] == native_hashes(), 'Entry SCR native VM namespace differs')
    require(report['wholeRomSourceMatch'] is False, 'Entry SCR partial source claims whole ROM')
    require(sha256(Path(sys.executable)) == read_json(ROOT / 'tools.lock.json')['python']['sha256'],
            'Entry SCR pinned Python identity differs')
    hashes = {row['path']: row['sha256'] for row in report['sourceClosure']}
    hashes[report['generator']] = report['generatorSha256']
    hashes.update({path: sha256(ROOT / path) for path in VALIDATORS})
    require(hashes == batch['sourceHashes'] and all(local(path).is_file() and sha256(local(path)) == pin for path, pin in hashes.items()),
            'Entry SCR frozen source/profile/validator closure changed')
    require(all(image[key] == value for key, value in batch['identity'].items()) and
            report['scriptSha256'] == image['scriptSha256'] and report['codeSha256'] == image['codeSha256'],
            'Entry SCR inventoried image differs')
    require(report['sourceOnlyBuild']['generalCCompilerClaimed'] is False and
            report['boundariesAndLocalStorage']['serializedCompleteCallsOnly'] is True, 'Entry SCR language/runtime scope differs')
    from validate_scr_entry129_20261029_batch07 import validate
    units = validate(ROOT, batch['report'])
    require(len(units) == 1, 'Entry SCR unit population differs')
    row = units[image['codeSha256'], batch['range']['startPc']]
    region = {'entrySlots': row['entryAliases'], **{key: row[key] for key in ('startPc', 'endExclusivePc', 'bytes', 'sha256')}}
    require(region == batch['range'] and 0 <= region['startPc'] < region['endExclusivePc'] <= image['codeBytes'],
            'Entry SCR frozen complete range differs')
    return {'id': report['romSha256'] + '/scr/' + image['codeSha256'] + '/' + str(row['startPc']),
            'scriptSha256': image['scriptSha256'], 'codeSha256': image['codeSha256'],
            'report': batch['report'], 'sourceHashes': batch['sourceHashes'], 'range': region,
            'sourceLanguage': 'restricted C99', 'function': report['sourceOnlyBuild']['function'],
            'sourceDefinitionId': row['sourceSha256'] + '/' + report['sourceOnlyBuild']['function'],
            'sourceByteCredit': row['bytes'], 'sourceUnitCredit': 1, 'completeImageCredit': 0,
            'nativeByteCredit': 0, 'implementationFamily': 'complete-entry-control-with-original-script-callees',
            'copyOnly': False, 'originalScriptCalleeSourceCredit': 0, 'unsupportedBoundFailureReturnCredit': 0,
            'completeScrEntryExecutions': len(report['differential']['cases']) * 4,
            'nativeRoutineReturnObservations': report['actualReturningCallsTotal'],
            'wholeImageControlFlowCertified': False, 'outsideIndirectTransfersExhaustivelyRuledOut': False,
            'scratchCallAbi': 'serialized complete calls only; synthetic unknown u16 021C0ECC equals zero'}
