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
    parser.add_argument('--source-directory', default='src/mechanics_save/20261030_lane_word_arrays')
    arguments = parser.parse_args()
    if Path(arguments.source_directory).is_absolute() or '..' in Path(arguments.source_directory).parts:
        raise AssertionError('Source must be repository-relative')
    import unicorn
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise AssertionError('Pinned Python/Unicorn runtime is required')
    verify_inputs()
    script = 'evidence/application/save_core_word_array_fixtures_20261030.py'
    fixture_path = 'evidence/lanes/save-core/word-array-fixtures-20261030.json'
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
        if row['sourceSha256'] not in ['455ae019ba8cfa9683fe0142cc98e76ad559956b8c766cbda345a2a797cd0998', 'f8304ef0bb9e3c3ec4c39cc4af712923332787724a00776430fb8d7b1d6d80d6']:
            raise AssertionError('Audited source hash changed')
        if oracle['nativeCaseDigest'] != 'fc9866561df9e7084db20c85debe5c9b0aa2849f317184174d17e5938889591c':
            raise AssertionError('Native semantic vector identity changed')
        for dependency in oracle['runtimeDependencies']:
            if sha((ROOT / dependency['path']).read_bytes()) != dependency['sha256']:
                raise AssertionError('Current runtime dependency changed')
        if not row['exactByteEqual'] or row['compiledBytes'] != 76 or not dependencies_current(row):
            raise AssertionError('Complete source/closure did not match')
        for path_key, hash_key in [('source', 'sourceSha256'), ('object', 'objectSha256'),
            ('isolatedCallerBinary', 'isolatedCallerBinarySha256'),
            ('isolatedCallerLinkValidation', 'isolatedCallerLinkValidationSha256')]:
            if sha((ROOT / row[path_key]).read_bytes()) != row[hash_key]:
                raise AssertionError('Current source/object/real-link identity changed')
        address = int(row['address'],0)
        assert address in (0x020C36B8,0x020C3724)
        own = native_entry('main', address, cache)
        if row['nativeAlias'] != own['nativeAlias'] or row['bytes'] != own['bytes'] or own['bytes'] != 76:
            raise AssertionError('Own measured identity differs')
        metadata, binary, functions = cache['main']
        offset = address - int(metadata['base'], 0)
        native = binary[offset:offset + 76]
        linked = (ROOT / row['isolatedCallerBinary']).read_bytes()
        validation = json.loads((ROOT / row['isolatedCallerLinkValidation']).read_text())
        if native != linked or len(linked) != 76 or validation.get('exactCallerBytes') is not True:
            raise AssertionError('Complete source/native/link bytes differ')
        if validation['linkerAttempt']['exitCode'] != 0 or validation['linkerSha256'] != 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74':
            raise AssertionError('Pinned real MW link did not succeed')
        if validation['sourceSha256'] != row['sourceSha256'] or validation['sourceObjectSha256'] != row['objectSha256']:
            raise AssertionError('Real link source/object differs')
        if validation['nativeSpanSha256'] != sha(native) or validation['linkedCallerSha256'] != sha(linked):
            raise AssertionError('Real link native/source identity differs')
        row.update({'exactBytes':76,'exactAfterDeclaredRelocation':True,'exactAfterRealMwLink':True,
            'signature':f"u32 {row['name']}(u32 *input)",
            'oracle':{'supported':True,'cases':625,'actualReturns':1250,'report':fixture_path,
                'reportSha256':sha((ROOT/fixture_path).read_bytes()),'limits':oracle['limits']}})
        entries[row['name']] = own
        for relocation in row['relocations']:
            module,target = relocation['targetModule'],int(relocation['target'],0)
            entries[relocation['symbol']] = data_entry(module,target,cache) if relocation['targetMode']=='data' else native_entry(module,target,cache)
        rows.append(row)
    assert len(rows)==2 and oracle['counts']['contexts']==1250 and oracle['counts']['actualTopLevelReturns']==2500
    assert oracle['counts']['providers']==0 and oracle['counts']['unsupportedStops']==4
    deps = [entry['path'] for entry in oracle['runtimeDependencies']]
    deps += [script, 'evidence/application/save_core_word_array_machine_20261030.py', 'evidence/application/save_core_word_array_build_20261030.py',
        'match_mechanics_save_20261030_lane_word_arrays.py', 'provenance/seed-manifest.json',
        'match_mechanics_save_20261029_record33.py', 'match_mechanics_save_20261029_item_use.py', 'source_dependencies.py']
    deps += [record[0]['symbolsFile'] for record in cache.values()]
    verify_inputs()
    report = {'schemaVersion': 1, 'romSha256': ROM_SHA, 'saveSha256': SAVE_SHA, 'arm9Sha256': MAIN_SHA,
        'matches': rows, 'matchedFunctions': 2, 'matchedBytes': 152,
        'nativeSymbolEntries': entries, 'nativeSymbols': {name: item['address'] for name, item in entries.items()},
        'nativeSymbolModules': {name: item['module'] for name, item in entries.items()},
        'sourceDependencies': [], 'replayDependencies': [file_identity(path) for path in sorted(set(deps))],
        'oracle': {'cases': oracle['counts']['contexts'], 'actualReturns': oracle['counts']['actualTopLevelReturns'],
            'providers': oracle['counts']['providers'],
            'providerKinds': 0,
            'nativeCaseDigest': oracle['nativeCaseDigest'],
            'reports': [x['oracle'] for x in rows], 'reproductionCommands': [command]},
        'wholeLinkedRebuild': False, 'registrationPerformedByThisScript': False, 'inputsUnchanged': True,
        'limitations': oracle['limits']}
    path = ROOT / 'evidence/matches/mechanics-save-20261030-lane-word-arrays.json'
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'matchedFunctions': 2, 'matchedBytes': 152, 'cases': oracle['counts']['contexts'],
        'actualReturns': oracle['counts']['actualTopLevelReturns'], 'reportSha256': sha(path.read_bytes())}))


if __name__ == '__main__':
    main()
