from pathlib import Path
import sys
from project import ROOT, configuration, read_json, sha256
from interpreted_sources import local
from interpreted_linked_sources import require, native_hashes

KIND = 'grouped-empty-SCR-family-v4'
VALIDATOR = 'validate_scr_empty_family_20261029_batch04.py'


def candidates(report, relative, reproduction):
    hashes = {row['path']: row['sha256'] for row in report['sourceClosure']}
    hashes[report['generator']] = report['generatorSha256']
    hashes[VALIDATOR] = sha256(ROOT / VALIDATOR)
    units = []
    for module in report['modules']:
        identity = {key: module[key] for key in ('scriptSha256', 'codeSha256', 'entryTableSha256')}
        for row in module['matchedRanges']:
            units.append({'identity': identity, 'range': {'entrySlots': row['entryAliases'],
                          **{key: row[key] for key in ('startPc', 'endExclusivePc', 'bytes', 'sha256')}}})
    return [{'report': relative, 'reproduce': reproduction, 'proofKind': KIND, 'sourceHashes': hashes,
             'nativeModuleHashes': native_hashes(), 'units': units}]


def measure(report, inventory, batch):
    require(report['evidenceClass'] == 'reused-empty-C-family-source-rebuild-and-native-execution' and
            report['romSha256'] == configuration()['romSha256'], 'Empty SCR report identity differs')
    require(batch['nativeModuleHashes'] == native_hashes(), 'Empty SCR native VM namespace differs')
    require(sha256(Path(sys.executable)) == read_json(ROOT / 'tools.lock.json')['python']['sha256'], 'Empty SCR pinned Python identity differs')
    require(report['memberAliasesGiveNoDuplicateCredit'] is True and report['wholeRomSourceMatch'] is False,
            'Empty SCR alias/whole-ROM scope differs')
    hashes = {row['path']: row['sha256'] for row in report['sourceClosure']}
    hashes[report['generator']] = report['generatorSha256']
    hashes[VALIDATOR] = sha256(ROOT / VALIDATOR)
    require(hashes == batch['sourceHashes'], 'Empty SCR frozen source/validator closure changed')
    require(all(local(path).is_file() and sha256(local(path)) == pin for path, pin in hashes.items()),
            'Empty SCR frozen source/compiler changed')
    expected_declarations = []
    for module in report['modules']:
        identity = {key: module[key] for key in ('scriptSha256', 'codeSha256', 'entryTableSha256')}
        for row in module['matchedRanges']:
            expected_declarations.append({'identity': identity, 'range': {'entrySlots': row['entryAliases'],
                                          **{key: row[key] for key in ('startPc', 'endExclusivePc', 'bytes', 'sha256')}}})
    require(batch['units'] == expected_declarations, 'Empty SCR frozen range declarations differ')
    from validate_scr_empty_family_20261029_batch04 import validate
    qualified = validate(ROOT, batch['report'])
    declared = {(row['identity']['codeSha256'], row['range']['startPc']) for row in batch['units']}
    require(len(declared) == len(batch['units']) and declared == set(qualified), 'Empty SCR declared ranges are duplicate or incomplete')
    images = {row['codeSha256']: row for row in inventory['images']}
    modules = {row['codeSha256']: row for row in report['modules']}
    results = []
    for declaration in batch['units']:
        identity, region = declaration['identity'], declaration['range']
        row = qualified[identity['codeSha256'], region['startPc']]
        image, module = images[identity['codeSha256']], modules[identity['codeSha256']]
        require(all(image[key] == module[key] == value for key, value in identity.items()), 'Empty SCR inventoried image identity differs')
        expected = {'entrySlots': row['entryAliases'], 'startPc': row['startPc'], 'endExclusivePc': row['endExclusivePc'],
                    'bytes': row['bytes'], 'sha256': row['sha256']}
        require(region == expected and 0 <= region['startPc'] < region['endExclusivePc'] <= image['codeBytes'],
                'Empty SCR frozen owned range differs')
        definition = row['sourceDefinition']
        results.append({'id': report['romSha256'] + '/scr/' + image['codeSha256'] + '/' + str(row['startPc']),
                        'scriptSha256': image['scriptSha256'], 'codeSha256': image['codeSha256'],
                        'report': batch['report'], 'sourceHashes': batch['sourceHashes'], 'range': region,
                        'sourceLanguage': 'restricted C99', 'function': definition['function'],
                        'sourceDefinitionId': definition['sha256'] + '/' + definition['function'],
                        'implementationFamily': row['sourceDefinition']['family'],
                        'sourceByteCredit': row['bytes'], 'sourceUnitCredit': 1, 'completeImageCredit': 0,
                        'nativeByteCredit': 0, 'newAuthoredDefinitionCredit': 0, 'newImplementationFamilyCredit': 0,
                        'substantiveDecisionLogicByteCredit': 0, 'wholeImageControlFlowCertified': False,
                        'outsideIndirectTransfersExhaustivelyRuledOut': False})
    return results
