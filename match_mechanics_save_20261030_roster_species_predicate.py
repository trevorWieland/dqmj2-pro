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
    parser.add_argument('--source', default='src/mechanics_save/20261030_roster_species_predicate.c')
    arguments = parser.parse_args()
    if Path(arguments.source).is_absolute() or '..' in Path(arguments.source).parts:
        raise AssertionError('Source must be repository-relative')
    import unicorn
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise AssertionError('Pinned Python/Unicorn runtime is required')
    verify_inputs()
    script = 'evidence/application/roster_species_predicate_fixtures_20261030.py'
    fixture_path = 'evidence/application/roster-species-predicate-fixtures-20261030.json'
    command = [sys.executable, str(ROOT / script), '--source', arguments.source]
    process = subprocess.run(command, capture_output=True, text=True, timeout=300)
    if process.returncode:
        raise AssertionError(process.stdout + process.stderr)
    oracle = json.loads((ROOT / fixture_path).read_text())
    row = dict(oracle['candidate'])
    row.update(row['realLinkSnapshot'])
    row.update({'outputSha256': row['linkedBinarySha256'], 'linked': False,
        'compilerPath': 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'})
    if row['sourceSha256'] != '67dc2650935d839517f46392aaacb4192c9103095d944df693a2b07c6ca3b4ba':
        raise AssertionError('Audited source hash changed')
    if oracle['nativeCaseDigest'] != 'af0b13ad4b397639c6a150e5e94dd201156caeae81c0131cf6f1350befa76b82':
        raise AssertionError('Native semantic vector identity changed')
    for dependency in oracle['runtimeDependencies']:
        if sha((ROOT / dependency['path']).read_bytes()) != dependency['sha256']:
            raise AssertionError('Current runtime dependency changed')
    if not row['exactByteEqual'] or row['compiledBytes'] != 144 or not dependencies_current(row):
        raise AssertionError('Complete source/closure did not match')
    for path_key, hash_key in [('source', 'sourceSha256'), ('object', 'objectSha256'),
        ('isolatedCallerBinary', 'isolatedCallerBinarySha256'),
        ('isolatedCallerLinkValidation', 'isolatedCallerLinkValidationSha256')]:
        if sha((ROOT / row[path_key]).read_bytes()) != row[hash_key]:
            raise AssertionError('Current source/object/real-link identity changed')
    cache = {}
    own = native_entry('main', 0x0206DB00, cache)
    if row['nativeAlias'] != own['nativeAlias'] or row['bytes'] != own['bytes'] or own['bytes'] != 144:
        raise AssertionError('Own measured identity differs')
    metadata, binary, functions = cache['main']
    offset = 0x0206DB00 - int(metadata['base'], 0)
    native = binary[offset:offset + 144]
    linked = (ROOT / row['isolatedCallerBinary']).read_bytes()
    validation = json.loads((ROOT / row['isolatedCallerLinkValidation']).read_text())
    if native != linked or len(linked) != 144 or validation.get('exactCallerBytes') is not True:
        raise AssertionError('Complete source/native/link bytes differ')
    if validation['linkerAttempt']['exitCode'] != 0 or validation['linkerSha256'] != 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74':
        raise AssertionError('Pinned real MW link did not succeed')
    if validation['sourceSha256'] != row['sourceSha256'] or validation['sourceObjectSha256'] != row['objectSha256']:
        raise AssertionError('Real link source/object differs')
    if validation['nativeSpanSha256'] != sha(native) or validation['linkedCallerSha256'] != sha(linked):
        raise AssertionError('Real link native/source identity differs')
    if oracle['counts']['exhaustiveInputs'] != 65536 or oracle['counts']['actualTopLevelReturns'] != 131852 or oracle['counts']['unsupportedStops'] != 4:
        raise AssertionError('Measured native/source case coverage changed')
    row.update({'exactBytes': 144, 'exactAfterDeclaredRelocation': True, 'exactAfterRealMwLink': True,
        'signature': 'u32 native_main_0206db00(s32 sprite)',
        'oracle': {'supported': True, 'cases': (oracle['counts']['exhaustiveInputs'] + oracle['counts']['boundaryPairs']),
            'actualReturns': oracle['counts']['actualTopLevelReturns'], 'report': fixture_path,
            'reportSha256': sha((ROOT / fixture_path).read_bytes()), 'limits': oracle['limits']}})
    table = (ROOT / oracle['exhaustiveResultFile']).read_bytes()
    if len(table) != 65536 or sha(table) != oracle['exhaustiveResultSha256'] or [index for index, value in enumerate(table) if value] != [139, 176, 188, 254, 350, 425, 426]:
        raise AssertionError('Measured exhaustive predicate output differs')
    entries = {row['name']: own}
    for relocation in row['relocations']:
        module, target = relocation['targetModule'], int(relocation['target'], 0)
        entries[relocation['symbol']] = data_entry(module, target, cache) if relocation['targetMode'] == 'data' else native_entry(module, target, cache)
    deps = [entry['path'] for entry in oracle['runtimeDependencies']]
    deps += [script, 'evidence/application/roster_species_predicate_build_20261030.py',
        'match_mechanics_save_20261030_roster_species_predicate.py', 'provenance/seed-manifest.json',
        'match_mechanics_save_20261029_record33.py', 'match_mechanics_save_20261029_item_use.py', 'source_dependencies.py']
    deps += [record[0]['symbolsFile'] for record in cache.values()]
    verify_inputs()
    report = {'schemaVersion': 1, 'romSha256': ROM_SHA, 'saveSha256': SAVE_SHA, 'arm9Sha256': MAIN_SHA,
        'matches': [row], 'matchedFunctions': 1, 'matchedBytes': 144,
        'nativeSymbolEntries': entries, 'nativeSymbols': {name: item['address'] for name, item in entries.items()},
        'nativeSymbolModules': {name: item['module'] for name, item in entries.items()},
        'sourceDependencies': [], 'replayDependencies': [file_identity(path) for path in sorted(set(deps))],
        'oracle': {'cases': (oracle['counts']['exhaustiveInputs'] + oracle['counts']['boundaryPairs']), 'actualReturns': oracle['counts']['actualTopLevelReturns'],
            'providers': 0,
            'providerKinds': 0,
            'nativeCaseDigest': oracle['nativeCaseDigest'],
            'reports': [row['oracle']], 'reproductionCommands': [command]},
        'wholeLinkedRebuild': False, 'registrationPerformedByThisScript': False, 'inputsUnchanged': True,
        'limitations': oracle['limits']}
    path = ROOT / 'evidence/matches/mechanics-save-20261030-roster-species-predicate.json'
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'matchedFunctions': 1, 'matchedBytes': 144, 'cases': (oracle['counts']['exhaustiveInputs'] + oracle['counts']['boundaryPairs']),
        'actualReturns': oracle['counts']['actualTopLevelReturns'], 'reportSha256': sha(path.read_bytes())}))


if __name__ == '__main__':
    main()
