from pathlib import Path
import sys
from project import ROOT, configuration, read_json, sha256
from interpreted_sources import local
from interpreted_linked_sources import require, native_hashes

KIND = 'nested-primary-SCR-v4'
VALIDATORS = ('validate_scr_empty_family_20261029_batch04.py', 'validate_scr_numeric_transition_20261029_batch04.py', 'validate_scr_primary24_20261029_batch05.py')


def candidates(report, relative, reproduction):
    hashes = {row['path']: row['sha256'] for row in report['sourceClosure']}
    hashes[report['generator']] = report['generatorSha256']
    hashes.update({path: sha256(ROOT / path) for path in VALIDATORS})
    inventory = read_json(ROOT / 'evidence/encounter/scripts-inventory-20261029.json')
    image = next(row for row in inventory['images'] if row['codeSha256'] == report['codeSha256'])
    return [{'report': relative, 'reproduce': reproduction, 'proofKind': KIND, 'sourceHashes': hashes,
             'nativeModuleHashes': native_hashes(),
             'identity': {key: image[key] for key in ('scriptSha256', 'codeSha256', 'entryTableSha256')},
             'range': {'entrySlots': [102], **report['matchedRange']}}]


def validated(report, image, batch):
    require(report['evidenceClass'] == 'ordinary-C-complete-nested-primary24-SCR-match' and
            report['romSha256'] == configuration()['romSha256'], 'Primary SCR report identity differs')
    require(batch['nativeModuleHashes'] == native_hashes(), 'Primary SCR native VM namespace differs')
    require(report['wholeRomSourceMatch'] is False, 'Primary SCR partial source claims whole ROM')
    hashes = {row['path']: row['sha256'] for row in report['sourceClosure']}
    hashes[report['generator']] = report['generatorSha256']
    hashes.update({path: sha256(ROOT / path) for path in VALIDATORS})
    require(hashes == batch['sourceHashes'] and all(local(path).is_file() and sha256(local(path)) == pin for path, pin in hashes.items()),
            'Primary SCR frozen source/profile/validator closure changed')
    require(all(image[key] == value for key, value in batch['identity'].items()) and
            report['scriptSha256'] == image['scriptSha256'] and report['codeSha256'] == image['codeSha256'],
            'Primary SCR inventoried image differs')
    compiled = report['sourceOnlyBuild']
    require(compiled['pythonVersion'].startswith('3.13.5 ') and compiled['pythonExecutableSha256'] == sha256(Path(sys.executable)),
            'Primary SCR Python identity differs')
    require(compiled['generalCCompilerClaimed'] is False and compiled['interleavedOrReentrantSemanticsClaimed'] is False,
            'Primary SCR language/runtime scope differs')
    from validate_scr_primary24_20261029_batch05 import validate
    units = validate(ROOT, batch['report'])
    require(len(units) == 1, 'Primary SCR unit population differs')
    row = units[image['codeSha256'], batch['range']['startPc']]
    region = {'entrySlots': row['entryAliases'], **{key: row[key] for key in ('startPc', 'endExclusivePc', 'bytes', 'sha256')}}
    require(region == batch['range'] and 0 <= region['startPc'] < region['endExclusivePc'] <= image['codeBytes'],
            'Primary SCR frozen complete range differs')
    return {'id': report['romSha256'] + '/scr/' + image['codeSha256'] + '/' + str(row['startPc']),
            'scriptSha256': image['scriptSha256'], 'codeSha256': image['codeSha256'],
            'report': batch['report'], 'sourceHashes': batch['sourceHashes'], 'range': region,
            'sourceLanguage': 'restricted C99', 'function': compiled['function'],
            'sourceDefinitionId': row['sourceSha256'] + '/' + compiled['function'],
            'sourceByteCredit': row['bytes'], 'sourceUnitCredit': 1, 'completeImageCredit': 0,
            'nativeByteCredit': 0, 'implementationFamily': 'nested-primary-flag-decision',
            'wholeImageControlFlowCertified': False, 'outsideIndirectTransfersExhaustivelyRuledOut': False,
            'scratchCallAbi': 'serialized complete calls only'}
