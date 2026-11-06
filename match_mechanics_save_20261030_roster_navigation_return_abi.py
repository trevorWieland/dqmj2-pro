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
    parser.add_argument('--source', default='src/mechanics_save/20261030_roster_navigation_return_abi.c')
    arguments = parser.parse_args()
    if Path(arguments.source).is_absolute() or '..' in Path(arguments.source).parts:
        raise AssertionError('Source must be repository-relative')
    import unicorn
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise AssertionError('Pinned Python/Unicorn runtime is required')
    verify_inputs()
    script = 'evidence/application/roster_navigation_return_abi_fixtures_20261030.py'
    fixture_path = 'evidence/application/roster-navigation-return-abi-fixtures-20261030.json'
    command = [sys.executable, str(ROOT / script), '--source', arguments.source]
    process = subprocess.run(command, capture_output=True, text=True, timeout=300)
    if process.returncode:
        raise AssertionError(process.stdout + process.stderr)
    oracle = json.loads((ROOT / fixture_path).read_text())
    row = dict(oracle['candidate'])
    row.update(row['realLinkSnapshot'])
    row.update({'outputSha256': row['linkedBinarySha256'], 'linked': False,
        'compilerPath': 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'})
    if row['sourceSha256'] != '6aa89b3cb39c24b1b63032e8e15bce7fd7750b3e469109ba5546c1980611d991':
        raise AssertionError('Audited source hash changed')
    if oracle['nativeCaseDigest'] != '6d12a88497ada5c452a2fc866b26176ecfab9d5c481fb4c269fc5d416eed91d7':
        raise AssertionError('Native semantic vector identity changed')
    for dependency in oracle['runtimeDependencies']:
        if sha((ROOT / dependency['path']).read_bytes()) != dependency['sha256']:
            raise AssertionError('Current runtime dependency changed')
    if not row['exactByteEqual'] or row['compiledBytes'] != 1256 or not dependencies_current(row):
        raise AssertionError('Complete source/closure did not match')
    for path_key, hash_key in [('source', 'sourceSha256'), ('object', 'objectSha256'),
        ('isolatedCallerBinary', 'isolatedCallerBinarySha256'),
        ('isolatedCallerLinkValidation', 'isolatedCallerLinkValidationSha256')]:
        if sha((ROOT / row[path_key]).read_bytes()) != row[hash_key]:
            raise AssertionError('Current source/object/real-link identity changed')
    cache = {}
    own = native_entry('main', 0x0206940C, cache)
    if row['nativeAlias'] != own['nativeAlias'] or row['bytes'] != own['bytes'] or own['bytes'] != 1256:
        raise AssertionError('Own measured identity differs')
    metadata, binary, functions = cache['main']
    offset = 0x0206940C - int(metadata['base'], 0)
    native = binary[offset:offset + 1256]
    linked = (ROOT / row['isolatedCallerBinary']).read_bytes()
    validation = json.loads((ROOT / row['isolatedCallerLinkValidation']).read_text())
    if native != linked or len(linked) != 1256 or validation.get('exactCallerBytes') is not True:
        raise AssertionError('Complete source/native/link bytes differ')
    if validation['linkerAttempt']['exitCode'] != 0 or validation['linkerSha256'] != 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74':
        raise AssertionError('Pinned real MW link did not succeed')
    if validation['sourceSha256'] != row['sourceSha256'] or validation['sourceObjectSha256'] != row['objectSha256']:
        raise AssertionError('Real link source/object differs')
    if validation['nativeSpanSha256'] != sha(native) or validation['linkedCallerSha256'] != sha(linked):
        raise AssertionError('Real link native/source identity differs')
    if oracle['counts']['contexts'] != 878 or oracle['counts']['actualTopLevelReturns'] != 1756 or oracle['counts']['unsupportedStops'] != 10:
        raise AssertionError('Measured native/source case coverage changed')
    row.update({'exactBytes': 1256, 'exactAfterDeclaredRelocation': True, 'exactAfterRealMwLink': True,
        'signature': 'u32 native_main_0206940c(void)',
        'oracle': {'supported': True, 'cases': oracle['counts']['contexts'],
            'actualReturns': oracle['counts']['actualTopLevelReturns'], 'report': fixture_path,
            'reportSha256': sha((ROOT / fixture_path).read_bytes()), 'limits': oracle['limits']}})
    boundary = oracle['returnBoundaryProof']
    boundary_row = boundary['candidate']
    if boundary['actualTopLevelReturns'] != 18 or boundary['providers'] != 0 or not boundary_row['exactByteEqual'] or boundary_row['compiledBytes'] != 488:
        raise AssertionError('Return ABI proof changed')
    if boundary['nativeCaseDigest'] != 'baaaddadff8d532500189710f9f93c5e7a92048efab95c66efc1b966c6c02032':
        raise AssertionError('Native return-boundary vector identity changed')
    if not dependencies_current(boundary_row):
        raise AssertionError('Return ABI source/header closure changed')
    for path_key, hash_key in [('source', 'sourceSha256'), ('object', 'objectSha256'), ('linkedBinary', 'linkedBinarySha256')]:
        if sha((ROOT / boundary_row[path_key]).read_bytes()) != boundary_row[hash_key]:
            raise AssertionError('Current ABI proof provenance changed')
    snapshot = boundary_row['realLinkSnapshot']
    for key, value in snapshot.items():
        if not key.endswith('Sha256') and sha((ROOT / value).read_bytes()) != snapshot[key + 'Sha256']:
            raise AssertionError('Current ABI link artifact changed')
    boundary_validation = json.loads((ROOT / snapshot['isolatedCallerLinkValidation']).read_text())
    if boundary_validation['sourceSha256'] != boundary_row['sourceSha256'] or boundary_validation['sourceObjectSha256'] != boundary_row['objectSha256']:
        raise AssertionError('ABI source/object link provenance differs')
    if boundary_validation.get('exactCallerBytes') is not True or boundary_validation['linkerAttempt']['exitCode'] != 0 or boundary_validation['linkerSha256'] != 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74':
        raise AssertionError('ABI real pinned link did not validate')
    boundary_native = native_entry('main', 0x02072918, cache)
    if boundary_native['bytes'] != 488 or boundary_row['nativeAlias'] != boundary_native['nativeAlias']:
        raise AssertionError('ABI native identity differs')
    boundary_offset = 0x02072918 - int(metadata['base'], 0)
    if binary[boundary_offset:boundary_offset + 488] != (ROOT / snapshot['isolatedCallerBinary']).read_bytes():
        raise AssertionError('Complete ABI source/native binary differs')
    boundary_paths = [boundary_row['source'], *[item['path'] for item in boundary_row['sourceDependencies']]]
    entries = {row['name']: own}
    for relocation in row['relocations']:
        module, target = relocation['targetModule'], int(relocation['target'], 0)
        entries[relocation['symbol']] = data_entry(module, target, cache) if relocation['targetMode'] == 'data' else native_entry(module, target, cache)
    deps = [entry['path'] for entry in oracle['runtimeDependencies']]
    deps += [script, 'evidence/application/roster_navigation_return_abi_build_20261030.py',
        'match_mechanics_save_20261030_roster_navigation_return_abi.py', 'provenance/seed-manifest.json',
        'match_mechanics_save_20261029_record33.py', 'match_mechanics_save_20261029_item_use.py', 'source_dependencies.py']
    deps += [record[0]['symbolsFile'] for record in cache.values()]
    verify_inputs()
    report = {'schemaVersion': 1, 'romSha256': ROM_SHA, 'saveSha256': SAVE_SHA, 'arm9Sha256': MAIN_SHA,
        'matches': [row], 'matchedFunctions': 1, 'matchedBytes': 1256,
        'nativeSymbolEntries': entries, 'nativeSymbols': {name: item['address'] for name, item in entries.items()},
        'nativeSymbolModules': {name: item['module'] for name, item in entries.items()},
        'returnBoundaryProof': boundary, 'sourceDependencies': [{'path': path, 'sha256': sha((ROOT / path).read_bytes())} for path in boundary_paths], 'replayDependencies': [file_identity(path) for path in sorted(set(deps))],
        'oracle': {'cases': oracle['counts']['contexts'], 'actualReturns': oracle['counts']['actualTopLevelReturns'],
            'observedNativeHelperReturns': oracle['counts']['observedNativeHelperReturns'],
            'notificationProviderCalls': oracle['counts']['notificationProviderCalls'], 'providerKinds': 1,
            'nativeCaseDigest': oracle['nativeCaseDigest'],
            'reports': [row['oracle']], 'reproductionCommands': [command]},
        'wholeLinkedRebuild': False, 'registrationPerformedByThisScript': False, 'inputsUnchanged': True,
        'limitations': oracle['limits']}
    path = ROOT / 'evidence/matches/mechanics-save-20261030-roster-navigation-return-abi.json'
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'matchedFunctions': 1, 'matchedBytes': 1256, 'cases': oracle['counts']['contexts'],
        'actualReturns': oracle['counts']['actualTopLevelReturns'], 'reportSha256': sha(path.read_bytes())}))


if __name__ == '__main__':
    main()
