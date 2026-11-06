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
    parser.add_argument('--source', default='src/mechanics_save/20261030_roster_cleanup_all.c')
    arguments = parser.parse_args()
    if Path(arguments.source).is_absolute() or '..' in Path(arguments.source).parts:
        raise AssertionError('Source must be repository-relative')
    import unicorn
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise AssertionError('Pinned Python/Unicorn runtime is required')
    verify_inputs()
    script = 'evidence/application/roster_cleanup_all_fixtures_20261030.py'
    fixture_path = 'evidence/application/roster-cleanup-all-fixtures-20261030.json'
    command = [sys.executable, str(ROOT / script), '--source', arguments.source]
    process = subprocess.run(command, capture_output=True, text=True, timeout=300)
    if process.returncode:
        raise AssertionError(process.stdout + process.stderr)
    oracle = json.loads((ROOT / fixture_path).read_text())
    row = dict(oracle['candidate'])
    row.update(row['realLinkSnapshot'])
    row.update({'outputSha256': row['linkedBinarySha256'], 'linked': False,
        'compilerPath': 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'})
    if row['sourceSha256'] != '3b4860fd20fc3e115545898f524416f0c2c317a03d79e02b15101a2ba15b5b9d':
        raise AssertionError('Audited source hash changed')
    if oracle['nativeCaseDigest'] != '80a1a0bffde62e1add6b874ab444ef2f5a1a2ede59d4273a7a351d98be20a6f0':
        raise AssertionError('Native semantic vectors changed')
    if not row['exactByteEqual'] or row['compiledBytes'] != 64 or not dependencies_current(row):
        raise AssertionError('Complete source/closure did not match')
    for path_key, hash_key in [('source', 'sourceSha256'), ('object', 'objectSha256'),
        ('isolatedCallerBinary', 'isolatedCallerBinarySha256'),
        ('isolatedCallerLinkValidation', 'isolatedCallerLinkValidationSha256')]:
        if sha((ROOT / row[path_key]).read_bytes()) != row[hash_key]:
            raise AssertionError('Current source/object/real-link identity changed')
    cache = {}
    own = native_entry('main', 0x0206D7F8, cache)
    if row['nativeAlias'] != own['nativeAlias'] or row['bytes'] != own['bytes'] or own['bytes'] != 64:
        raise AssertionError('Own measured identity differs')
    metadata, binary, functions = cache['main']
    offset = 0x0206D7F8 - int(metadata['base'], 0)
    native = binary[offset:offset + 64]
    linked = (ROOT / row['isolatedCallerBinary']).read_bytes()
    validation = json.loads((ROOT / row['isolatedCallerLinkValidation']).read_text())
    if native != linked or len(linked) != 64 or validation.get('exactCallerBytes') is not True:
        raise AssertionError('Complete source/native/link bytes differ')
    if validation['linkerAttempt']['exitCode'] != 0 or validation['linkerSha256'] != 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74':
        raise AssertionError('Pinned real MW link did not succeed')
    if validation['sourceSha256'] != row['sourceSha256'] or validation['sourceObjectSha256'] != row['objectSha256']:
        raise AssertionError('Real link source/object differs')
    if validation['nativeSpanSha256'] != sha(native) or validation['linkedCallerSha256'] != sha(linked):
        raise AssertionError('Real link native/source identity differs')
    if oracle['counts']['contexts'] != 168 or oracle['counts']['actualTopLevelReturns'] != 336 or oracle['counts']['unsupportedStops'] != 10:
        raise AssertionError('Measured native/source case coverage changed')
    row.update({'exactBytes': 64, 'exactAfterDeclaredRelocation': True, 'exactAfterRealMwLink': True,
        'signature': 'void native_main_0206d7f8(void)',
        'oracle': {'supported': True, 'cases': oracle['counts']['contexts'],
            'actualReturns': oracle['counts']['actualTopLevelReturns'], 'report': fixture_path,
            'reportSha256': sha((ROOT / fixture_path).read_bytes()), 'limits': oracle['limits']}})
    entries = {row['name']: own}
    for relocation in row['relocations']:
        module, target = relocation['targetModule'], int(relocation['target'], 0)
        entries[relocation['symbol']] = data_entry(module, target, cache) if relocation['targetMode'] == 'data' else native_entry(module, target, cache)
    deps = [script, 'evidence/application/roster_cleanup_all_build_20261030.py',
        'evidence/application/record_lookup_abi_machine_20261030.py',
        'evidence/application/roster-current-uid-arm7-20261030.py',
        'evidence/application/roster-collector-callers-arm7-20261030-setup.py',
        'evidence/application/roster-collectors-arm7-20261030.py',
        'evidence/application/allocation-constructor-other-modes-arm7-20261030.py',
        'evidence/application/allocation-constructor-arm7-20261030-setup.py',
        'evidence/application/allocation-constructor-arm7-20261030.py',
        'evidence/application/preparation_machine_20261029.py', 'evidence/application/eligibility_machine_20261029.py',
        'preparation_build_20261029.py', 'match_mechanics_save_20261029_record33.py',
        'match_mechanics_save_20261029_item_use.py', 'match_mechanics_save_20261030_roster_cleanup_all.py',
        'link_runtime_unit.py', 'save_link_snapshots.py', 'source_dependencies.py', 'provenance/seed-manifest.json']
    deps += [record[0]['symbolsFile'] for record in cache.values()]
    verify_inputs()
    report = {'schemaVersion': 1, 'romSha256': ROM_SHA, 'saveSha256': SAVE_SHA, 'arm9Sha256': MAIN_SHA,
        'matches': [row], 'matchedFunctions': 1, 'matchedBytes': 64,
        'nativeSymbolEntries': entries, 'nativeSymbols': {name: item['address'] for name, item in entries.items()},
        'nativeSymbolModules': {name: item['module'] for name, item in entries.items()},
        'sourceDependencies': [], 'replayDependencies': [file_identity(path) for path in sorted(set(deps))],
        'oracle': {'cases': oracle['counts']['contexts'], 'actualReturns': oracle['counts']['actualTopLevelReturns'],
            'observedNativeCleanupReturns': oracle['counts']['observedNativeCleanupReturns'],
            'nativeCaseDigest': oracle['nativeCaseDigest'],
            'reports': [row['oracle']], 'reproductionCommands': [command]},
        'wholeLinkedRebuild': False, 'registrationPerformedByThisScript': False, 'inputsUnchanged': True,
        'limitations': oracle['limits']}
    path = ROOT / 'evidence/matches/mechanics-save-20261030-roster-cleanup-all.json'
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'matchedFunctions': 1, 'matchedBytes': 64, 'cases': oracle['counts']['contexts'],
        'actualReturns': oracle['counts']['actualTopLevelReturns'], 'reportSha256': sha(path.read_bytes())}))


if __name__ == '__main__':
    main()
