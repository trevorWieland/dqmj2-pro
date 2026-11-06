import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from match_mechanics_save_20261029_record33 import sha, file_identity, verify_inputs, native_entry, ROM_SHA, SAVE_SHA, MAIN_SHA
from match_mechanics_save_20261029_item_use import data_entry
from source_dependencies import dependencies_current


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-directory', default='src/mechanics_save/20261030_widget_registry')
    arguments = parser.parse_args()
    if Path(arguments.source_directory).is_absolute() or '..' in Path(arguments.source_directory).parts:
        raise AssertionError('Source must be repository-relative')
    import unicorn
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise AssertionError('Pinned Python/Unicorn runtime is required')
    verify_inputs()
    script = 'evidence/application/widget_registry_fixtures_20261030.py'
    fixture_path = 'evidence/application/widget-registry-fixtures-20261030.json'
    command = [sys.executable, str(ROOT / script), '--source-directory', arguments.source_directory]
    process = subprocess.run(command, capture_output=True, text=True, timeout=300)
    if process.returncode:
        raise AssertionError(process.stdout + process.stderr)
    oracle = json.loads((ROOT / fixture_path).read_text())
    cache,entries,rows = {},{},[]
    for raw in oracle['matches']:
        row = dict(raw)
        row.update(row['realLinkSnapshot'])
        row.update({'outputSha256': row['linkedBinarySha256'], 'linked': False,
            'compilerPath': 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'})
        if row['sourceSha256'] not in ['c2adc32d149959b78b51763c02319e7dc1e03ae0b0b44776ec0594087aabba5b', '071d3cffe46e6dfb2ae951867d477b9103dbbf1f136a92d18058ad70e1ceaab6']:
            raise AssertionError('Audited source hash changed')
        if oracle['nativeCaseDigest'] != 'bbbec500d683b0ebca94a2c798cab98cffaf2b90c75bb7db1006792a9a8fb6fd':
            raise AssertionError('Native semantic vector identity changed')
        for dependency in oracle['runtimeDependencies']:
            if sha((ROOT / dependency['path']).read_bytes()) != dependency['sha256']:
                raise AssertionError('Current runtime dependency changed')
        if not row['exactByteEqual'] or row['compiledBytes'] != row['bytes'] or not dependencies_current(row):
            raise AssertionError('Complete source/closure did not match')
        for path_key, hash_key in [('source', 'sourceSha256'), ('object', 'objectSha256'),
            ('isolatedCallerBinary', 'isolatedCallerBinarySha256'),
            ('isolatedCallerLinkValidation', 'isolatedCallerLinkValidationSha256')]:
            if sha((ROOT / row[path_key]).read_bytes()) != row[hash_key]:
                raise AssertionError('Current source/object/real-link identity changed')
        address = int(row['address'],0)
        length = {0x020485C8:84,0x0204861C:40}[address]
        own = native_entry('main', address, cache)
        if row['nativeAlias'] != own['nativeAlias'] or row['bytes'] != own['bytes'] or own['bytes'] != length:
            raise AssertionError('Own measured identity differs')
        metadata, binary, functions = cache['main']
        offset = address - int(metadata['base'], 0)
        native = binary[offset:offset + length]
        linked = (ROOT / row['isolatedCallerBinary']).read_bytes()
        validation = json.loads((ROOT / row['isolatedCallerLinkValidation']).read_text())
        if native != linked or len(linked) != length or validation.get('exactCallerBytes') is not True:
            raise AssertionError('Complete source/native/link bytes differ')
        if validation['linkerAttempt']['exitCode'] != 0 or validation['linkerSha256'] != 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74':
            raise AssertionError('Pinned real MW link did not succeed')
        if validation['sourceSha256'] != row['sourceSha256'] or validation['sourceObjectSha256'] != row['objectSha256']:
            raise AssertionError('Real link source/object differs')
        if validation['nativeSpanSha256'] != sha(native) or validation['linkedCallerSha256'] != sha(linked):
            raise AssertionError('Real link native/source identity differs')
        cases = oracle['counts']['insertionContexts' if length == 84 else 'removalContexts']
        row.update({'exactBytes':length,'exactAfterDeclaredRelocation':True,'exactAfterRealMwLink':True,
            'signature':'u32 native_main_020485c8(u32 kind, RegistryWidget *widget)' if length == 84 else 'void native_main_0204861c(u32 kind, u32 index)',
            'oracle':{'supported':True,'cases':cases,'actualReturns':2*cases,'report':fixture_path,
                'reportSha256':sha((ROOT/fixture_path).read_bytes()),'limits':oracle['limits']}})
        entries[row['name']] = own
        for relocation in row['relocations']:
            module,target = relocation['targetModule'],int(relocation['target'],0)
            entries[relocation['symbol']] = data_entry(module,target,cache) if relocation['targetMode'] == 'data' else native_entry(module,target,cache)
        rows.append(row)
    assert len(rows)==2 and oracle['counts']['primitiveContexts']==2724 and oracle['counts']['primitiveActualReturns']==5448
    assert oracle['counts']['primitiveProviderKinds']==0 and oracle['counts']['unsupportedStops']==8
    deps = [entry['path'] for entry in oracle['runtimeDependencies']]
    deps += [script, 'evidence/application/widget_registry_machine_20261030.py', 'evidence/application/widget_registry_exact_build_20261030.py',
        'evidence/application/roster_sprite_placement_source_20261030.py','evidence/application/roster_sprite_placement_machine_20261030.py',
        'evidence/application/roster_sprite_placement_model_20261030.py','evidence/application/roster_sprite_placement_preferred_build_20261030.py',
        'evidence/application/roster_sprite_release_fixtures_20261030.py','evidence/application/roster_sprite_release_machine_20261030.py',
        'evidence/application/roster_sprite_release_exact_build_20261030.py',
        'match_mechanics_save_20261030_widget_registry.py', 'provenance/seed-manifest.json',
        'match_mechanics_save_20261029_record33.py', 'match_mechanics_save_20261029_item_use.py', 'source_dependencies.py']
    deps += [record[0]['symbolsFile'] for record in cache.values()]
    verify_inputs()
    report = {'schemaVersion': 1, 'romSha256': ROM_SHA, 'saveSha256': SAVE_SHA, 'arm9Sha256': MAIN_SHA,
        'matches': rows, 'matchedFunctions': 2, 'matchedBytes': 124,
        'nativeSymbolEntries': entries, 'nativeSymbols': {name: item['address'] for name, item in entries.items()},
        'nativeSymbolModules': {name: item['module'] for name, item in entries.items()},
        'sourceDependencies': [], 'replayDependencies': [file_identity(path) for path in sorted(set(deps))],
        'oracle': {'cases': oracle['counts']['primitiveContexts'], 'actualReturns': oracle['counts']['primitiveActualReturns'],
            'providers': oracle['counts']['connectedAllocationProviderCalls']+oracle['counts']['connectedHeapFreeProviderCalls'],
            'providerKinds': 2, 'primitiveProviders': 0, 'connectedActualReturns': 12,
            'nativeCaseDigest': oracle['nativeCaseDigest'],
            'reports': [x['oracle'] for x in rows], 'reproductionCommands': [command]},
        'wholeLinkedRebuild': False, 'registrationPerformedByThisScript': False, 'inputsUnchanged': True,
        'limitations': oracle['limits']}
    path = ROOT / 'evidence/matches/mechanics-save-20261030-widget-registry.json'
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'matchedFunctions': 2, 'matchedBytes': 124, 'cases': oracle['counts']['primitiveContexts'],
        'actualReturns': oracle['counts']['primitiveActualReturns'], 'reportSha256': sha(path.read_bytes())}))


if __name__ == '__main__':
    main()
