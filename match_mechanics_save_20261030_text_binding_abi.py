import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT), str(ROOT / 'deps/native'), str(ROOT / 'evidence/application')]
from match_mechanics_save_20261029_record33 import sha, file_identity, verify_inputs, native_entry, ROM_SHA, SAVE_SHA, MAIN_SHA
from match_mechanics_save_20261029_item_use import data_entry
from source_dependencies import dependencies_current


def load_builder():
    path = ROOT / 'evidence/application/text_binding_abi_canonical_build_20261030.py'
    spec = importlib.util.spec_from_file_location('canonical_text_binding_abi_builder', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', action='append', default=[], help='module:0xaddress=repository-relative-source')
    args = parser.parse_args()
    overrides = {}
    for value in args.source:
        identity, relative = value.split('=', 1)
        module, address = identity.split(':', 1)
        if Path(relative).is_absolute() or '..' in Path(relative).parts:
            raise AssertionError('Alternative source must be repository-relative')
        key = module, int(address, 0)
        if key in overrides:
            raise AssertionError('Duplicate alternative source')
        overrides[key] = relative
    verify_inputs()
    command = [sys.executable, str(ROOT / 'evidence/application/text_binding_abi_fixtures_20261030.py')]
    process = subprocess.run(command, capture_output=True, text=True, timeout=300)
    if process.returncode:
        raise AssertionError(process.stdout + process.stderr)
    fixture_path = ROOT / 'evidence/application/text-binding-abi-fixtures-20261030.json'
    if sha(fixture_path.read_bytes()) != '9ebe6ca43b9875f0bca4fd2fdcff13f8af4c9b792773fa6860eb87f7b08ad2c1':
        raise AssertionError('Frozen typed ABI behavior report changed')
    oracle = json.loads(fixture_path.read_text())
    inventory = oracle['sourceAlternatives']
    builder, cache, matches, symbols = load_builder(), {}, [], {}
    for alternative, original in zip(inventory['alternatives'], inventory['originalPrimaries']):
        module, address = alternative['module'], int(alternative['address'], 0)
        relative = overrides.pop((module, address), alternative['source'])
        if sha((ROOT / relative).read_bytes()) != alternative['sourceSha256']:
            raise AssertionError('Explicit alternative source differs from reviewed source identity')
        if sha((ROOT / original['source']).read_bytes()) != original['sha256']:
            raise AssertionError('Frozen original primary source changed')
        builder.MODULE, builder.ENTRY, builder.LENGTH = module, address, alternative['bytes']
        builder.NAME, builder.SOURCE, builder.FLAGS = alternative['name'], relative, list(alternative['flags'])
        own = native_entry(module, address, cache)
        metadata, binary, functions = cache[module]
        offset = address - int(metadata['base'], 0)
        native = binary[offset:offset + own['bytes']]
        row, body = builder.build(native)
        if body != native or own['bytes'] != row['compiledBytes'] or not row['exactByteEqual'] or not dependencies_current(row):
            raise AssertionError('Complete source/native/module extent differs')
        row.pop('sourceCredit', None)
        row.update(row['realLinkSnapshot'])
        validation = json.loads((ROOT / row['isolatedCallerLinkValidation']).read_text())
        if validation.get('exactCallerBytes') is not True or validation['linkerAttempt']['exitCode'] != 0:
            raise AssertionError('Independent real MW link did not pass')
        if validation['linkerSha256'] != 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74':
            raise AssertionError('Linker identity changed')
        if validation['sourceSha256'] != row['sourceSha256'] or validation['sourceObjectSha256'] != row['objectSha256']:
            raise AssertionError('Source/object/link closure differs')
        row.update({'exactBytes': own['bytes'], 'exactAfterDeclaredRelocation': True, 'exactAfterRealMwLink': True,
            'outputSha256': row['linkedBinarySha256'], 'linked': False, 'netNewCoverageBytes': 0,
            'replacesOriginalSource': original['source'], 'replacesOriginalSourceSha256': original['sha256'],
            'sourceMigration': True, 'oracle': {'supported': True, 'report': str(fixture_path.relative_to(ROOT)),
                'reportSha256': sha(fixture_path.read_bytes()), 'actualReturns': oracle['counts']['totalActualReturns'],
                'sharedClosureReport': True, 'limitations': oracle['limits']}})
        if row['nativeAlias'] != own['nativeAlias']:
            raise AssertionError('Own module-qualified alias differs')
        symbols[row['name']] = own
        for relocation in row['relocations']:
            target_module, target = relocation['targetModule'], int(relocation['target'], 0)
            symbols[relocation['symbol']] = data_entry(target_module, target, cache) if relocation['targetMode'] == 'data' else native_entry(target_module, target, cache)
        matches.append(row)
    if overrides:
        raise AssertionError('Override refers to an undeclared migration')
    verify_inputs()
    deps = ['match_mechanics_save_20261030_text_binding_abi.py',
        'evidence/application/text_binding_abi_fixtures_20261030.py', 'evidence/application/text_binding_abi_machine_20261030.py',
        'evidence/application/text_binding_abi_build_20261030.py', 'evidence/application/text_binding_abi_canonical_build_20261030.py',
        'evidence/application/text-binding-abi-alternatives-20261030.json',
        'evidence/application/allocation-constructor-other-modes-arm7-20261030.py',
        'evidence/application/allocation-constructor-arm7-20261030-setup.py', 'evidence/application/allocation-constructor-arm7-20261030.py',
        'evidence/application/preparation_machine_20261029.py', 'evidence/application/eligibility_machine_20261029.py',
        'preparation_build_20261029.py', 'match_mechanics_save_20261029_record33.py', 'match_mechanics_save_20261029_item_use.py',
        'link_runtime_unit.py', 'save_link_snapshots.py', 'source_dependencies.py', 'provenance/seed-manifest.json']
    deps += [item[0]['symbolsFile'] for item in cache.values()]
    report = {'schemaVersion': 1, 'romSha256': ROM_SHA, 'saveSha256': SAVE_SHA, 'arm9Sha256': MAIN_SHA,
        'matches': matches, 'matchedFunctions': len(matches), 'matchedBytes': sum(row['bytes'] for row in matches),
        'netNewMatchedFunctions': 0, 'netNewMatchedBytes': 0, 'sourceMigrationsOnly': True,
        'nativeSymbolEntries': symbols, 'nativeSymbols': {name: row['address'] for name, row in symbols.items()},
        'nativeSymbolModules': {name: row['module'] for name, row in symbols.items()}, 'sourceDependencies': [],
        'replayDependencies': [file_identity(path) for path in sorted(set(deps))],
        'oracle': {'actualReturns': oracle['counts']['totalActualReturns'], 'callerPairs': oracle['counts']['callerPairs'],
            'publisherPairs': oracle['counts']['publisherPairs'], 'report': str(fixture_path.relative_to(ROOT)),
            'reportSha256': sha(fixture_path.read_bytes()), 'reproductionCommands': [command]},
        'sourcePreferenceChanged': False, 'registrationPerformedByThisScript': False,
        'limitations': ['These five byte-identical replacements repair explicit caller/callee interfaces at already accepted ranges and add zero executable coverage.',
            'Actual helpers and bounded lower UI/formatting contracts are qualified by the frozen report; no full rendering/resource/scene claim.',
            'Root must explicitly select reviewed source primaries and rerun integration; this script mutates no shared registry/preference/build artifact.']}
    path = ROOT / 'evidence/matches/mechanics-save-20261030-text-binding-abi.json'
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'sourceMigrations': len(matches), 'comparedBytes': report['matchedBytes'], 'netNewBytes': 0,
        'actualReturns': report['oracle']['actualReturns'], 'reportSha256': sha(path.read_bytes())}))


if __name__ == '__main__':
    main()
