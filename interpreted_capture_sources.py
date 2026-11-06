from pathlib import Path
import sys
from project import ROOT, configuration, read_json, sha256
from interpreted_sources import local
from interpreted_linked_sources import require, native_hashes

KIND = 'grouped-context-captures-SCR-v4'
VALIDATORS = ('validate_scr_empty_family_20261029_batch04.py', 'validate_scr_numeric_transition_20261029_batch04.py',
              'validate_scr_captures_20261029_batch06.py')


def candidates(report, relative, reproduction):
    hashes = {row['path']: row['sha256'] for row in report['sourceClosure']}
    hashes[report['generator']] = report['generatorSha256']
    hashes.update({path: sha256(ROOT / path) for path in VALIDATORS})
    units = []
    for module in report['modules']:
        identity = {key: module[key] for key in ('scriptSha256', 'codeSha256', 'entryTableSha256')}
        for row in module['matchedRanges']:
            units.append({'identity': identity, 'range': {'entrySlots': row['entryAliases'],
                          **{key: row[key] for key in ('startPc', 'endExclusivePc', 'bytes', 'sha256')}}})
    return [{'report': relative, 'reproduce': reproduction, 'proofKind': KIND, 'sourceHashes': hashes,
             'nativeModuleHashes': native_hashes(), 'units': units}]


def measure(report, inventory, batch):
    require(report['evidenceClass'] == 'ordinary-C-fixed-slot-input-capture-SCR-source-matches' and
            report['romSha256'] == configuration()['romSha256'], 'Capture SCR report identity differs')
    require(batch['nativeModuleHashes'] == native_hashes(), 'Capture SCR native VM namespace differs')
    require(sha256(Path(sys.executable)) == read_json(ROOT / 'tools.lock.json')['python']['sha256'],
            'Capture SCR pinned Python identity differs')
    require(report['wholeRomSourceMatch'] is False and report['heldUnitSourceCredit'] == 0 and
            report['sourceDefinitionGroupsAreNotDistinctControlFlowLogicClaims'] is True,
            'Capture SCR held-unit/logic/whole-ROM scope differs')
    hashes = {row['path']: row['sha256'] for row in report['sourceClosure']}
    hashes[report['generator']] = report['generatorSha256']
    hashes.update({path: sha256(ROOT / path) for path in VALIDATORS})
    require(hashes == batch['sourceHashes'] and all(local(path).is_file() and sha256(local(path)) == pin for path, pin in hashes.items()),
            'Capture SCR frozen source/profile/validator closure changed')
    expected = []
    for module in report['modules']:
        identity = {key: module[key] for key in ('scriptSha256', 'codeSha256', 'entryTableSha256')}
        for row in module['matchedRanges']:
            expected.append({'identity': identity, 'range': {'entrySlots': row['entryAliases'],
                             **{key: row[key] for key in ('startPc', 'endExclusivePc', 'bytes', 'sha256')}}})
    require(expected == batch['units'], 'Capture SCR frozen declarations differ')
    from validate_scr_captures_20261029_batch06 import validate
    qualified = validate(ROOT, batch['report'])
    keys = {(row['identity']['codeSha256'], row['range']['startPc']) for row in batch['units']}
    require(len(keys) == len(batch['units']) and keys == set(qualified), 'Capture SCR qualified population differs')
    images = {row['codeSha256']: row for row in inventory['images']}
    modules = {row['codeSha256']: row for row in report['modules']}
    result = []
    for declaration in batch['units']:
        identity, region = declaration['identity'], declaration['range']
        image, module = images[identity['codeSha256']], modules[identity['codeSha256']]
        require(all(image[key] == module[key] == value for key, value in identity.items()), 'Capture SCR inventoried image differs')
        row = qualified[identity['codeSha256'], region['startPc']]
        own = {'entrySlots': row['entryAliases'], **{key: row[key] for key in ('startPc', 'endExclusivePc', 'bytes', 'sha256')}}
        require(region == own and 0 <= region['startPc'] < region['endExclusivePc'] <= image['codeBytes'], 'Capture SCR owned range differs')
        definition = row['sourceDefinition']
        result.append({'id': report['romSha256'] + '/scr/' + image['codeSha256'] + '/' + str(row['startPc']),
                       'scriptSha256': image['scriptSha256'], 'codeSha256': image['codeSha256'], 'report': batch['report'],
                       'sourceHashes': batch['sourceHashes'], 'range': region, 'sourceLanguage': 'restricted C99',
                       'function': definition['name'], 'sourceDefinitionId': definition['sha256'] + '/' + definition['name'],
                       'implementationFamily': row['sourceFamily'], 'copyOnly': True,
                       'sourceByteCredit': row['bytes'], 'sourceUnitCredit': 1, 'completeImageCredit': 0,
                       'nativeByteCredit': 0, 'substantiveDecisionLogicByteCredit': 0,
                       'wholeImageControlFlowCertified': False, 'outsideIndirectTransfersExhaustivelyRuledOut': False,
                       'scratchCallAbi': 'fixed slots with all known outside reads qualified; serialized complete calls only'})
    return result
