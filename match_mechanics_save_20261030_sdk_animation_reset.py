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
    parser.add_argument('--source', default='src/mechanics_save/20261030_sdk_animation/native_main_02034f90.c')
    arguments = parser.parse_args()
    if Path(arguments.source).is_absolute() or '..' in Path(arguments.source).parts:
        raise AssertionError('Source must be repository-relative')
    import unicorn
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise AssertionError('Pinned Python/Unicorn runtime is required')
    verify_inputs()
    script = 'evidence/application/sdk_animation_reset_fixtures_20261030.py'
    fixture_path = 'evidence/application/sdk-animation-reset-fixtures-20261030.json'
    command = [sys.executable, str(ROOT / script), '--source', arguments.source]
    process = subprocess.run(command, capture_output=True, text=True, timeout=300)
    if process.returncode:
        raise AssertionError(process.stdout + process.stderr)
    oracle = json.loads((ROOT / fixture_path).read_text())
    row = dict(oracle['candidate'])
    row.update(row['realLinkSnapshot'])
    row.update({'outputSha256': row['linkedBinarySha256'], 'linked': False,
        'compilerPath': 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'})
    if row['sourceSha256'] != 'd8fc535fc25ecef5157f2077696d1c1f4b6b62b5653ca0bdcb9315314c36c6f0':
        raise AssertionError('Audited source hash changed')
    if oracle['nativeCaseDigest'] != '65fba8a8b65b9c5f9f191d6f9a9968fad4ed4e98bfb4c3c4a593dadab9ae43a6':
        raise AssertionError('Native semantic vectors changed')
    if row['sourceDependencies'] != [{'path': 'src\\mechanics_save\\20261030_sdk_animation\\animation_types_v2.h', 'sha256': 'ea24e0db385b54a4d5dc8f0aacbf5ba363542a0dfcebd761bf8df7b2dd09f0c4'}]:
        raise AssertionError('Audited SDK header closure changed')
    if not row['exactByteEqual'] or row['compiledBytes'] != 96 or not dependencies_current(row):
        raise AssertionError('Complete source/closure did not match')
    for path_key, hash_key in [('source', 'sourceSha256'), ('object', 'objectSha256'),
        ('isolatedCallerBinary', 'isolatedCallerBinarySha256'),
        ('isolatedCallerLinkValidation', 'isolatedCallerLinkValidationSha256')]:
        if sha((ROOT / row[path_key]).read_bytes()) != row[hash_key]:
            raise AssertionError('Current source/object/real-link identity changed')
    cache = {}
    own = native_entry('main', 0x02034F90, cache)
    if row['nativeAlias'] != own['nativeAlias'] or row['bytes'] != own['bytes'] or own['bytes'] != 96:
        raise AssertionError('Own measured identity differs')
    metadata, binary, functions = cache['main']
    offset = 0x02034F90 - int(metadata['base'], 0)
    native = binary[offset:offset + 96]
    linked = (ROOT / row['isolatedCallerBinary']).read_bytes()
    validation = json.loads((ROOT / row['isolatedCallerLinkValidation']).read_text())
    if native != linked or len(linked) != 96 or validation.get('exactCallerBytes') is not True:
        raise AssertionError('Complete source/native/link bytes differ')
    if validation['linkerAttempt']['exitCode'] != 0 or validation['linkerSha256'] != 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74':
        raise AssertionError('Pinned real MW link did not succeed')
    if validation['sourceSha256'] != row['sourceSha256'] or validation['sourceObjectSha256'] != row['objectSha256']:
        raise AssertionError('Real link source/object differs')
    if validation['nativeSpanSha256'] != sha(native) or validation['linkedCallerSha256'] != sha(linked):
        raise AssertionError('Real link native/source identity differs')
    if oracle['counts']['connectedCases'] != 692 or oracle['counts']['directCases'] != 120 or oracle['counts']['actualTargetResetReturns'] != 1624:
        raise AssertionError('Measured native/source case coverage changed')
    row.update({'exactBytes': 96, 'exactAfterDeclaredRelocation': True, 'exactAfterRealMwLink': True,
        'signature': 'void native_main_02034f90(AnimationControl *control)',
        'oracle': {'supported': True, 'cases': (oracle['counts']['connectedCases'] + oracle['counts']['directCases']),
            'actualReturns': oracle['counts']['actualTargetResetReturns'], 'report': fixture_path,
            'reportSha256': sha((ROOT / fixture_path).read_bytes()), 'limits': oracle['limits']}})
    entries = {row['name']: own}
    for relocation in row['relocations']:
        module, target = relocation['targetModule'], int(relocation['target'], 0)
        entries[relocation['symbol']] = data_entry(module, target, cache) if relocation['targetMode'] == 'data' else native_entry(module, target, cache)
    deps = [script, 'evidence/application/sdk_animation_reset_build_20261030.py',
        'evidence/application/sdk_animation_source_20261030.py', 'evidence/application/sdk_animation_machine_20261030.py',
        'evidence/application/sdk_animation_virtual_link_20261030.py', 'evidence/application/sdk_animation_build_20261030.py',
        'evidence/application/roster_frame_selection_source_20261030.py',
        'evidence/application/roster_frame_selection_machine_20261030.py',
        'evidence/application/roster_frame_selection_build_20261030.py',
        'evidence/application/roster_position_source_20261030.py',
        'evidence/application/roster_position_build_20261030.py',
        'evidence/application/record_lookup_abi_machine_20261030.py',
        'evidence/application/roster-current-uid-arm7-20261030.py',
        'evidence/application/roster-collector-callers-arm7-20261030-setup.py',
        'evidence/application/roster-collectors-arm7-20261030.py',
        'evidence/application/allocation-constructor-other-modes-arm7-20261030.py',
        'evidence/application/allocation-constructor-arm7-20261030-setup.py',
        'evidence/application/allocation-constructor-arm7-20261030.py',
        'evidence/application/preparation_machine_20261029.py', 'evidence/application/eligibility_machine_20261029.py',
        'preparation_build_20261029.py', 'match_mechanics_save_20261029_record33.py',
        'match_mechanics_save_20261029_item_use.py', 'match_mechanics_save_20261030_sdk_animation_reset.py',
        'link_runtime_unit.py', 'save_link_snapshots.py', 'source_dependencies.py', 'provenance/seed-manifest.json']
    deps += [record[0]['symbolsFile'] for record in cache.values()]
    verify_inputs()
    report = {'schemaVersion': 1, 'romSha256': ROM_SHA, 'saveSha256': SAVE_SHA, 'arm9Sha256': MAIN_SHA,
        'matches': [row], 'matchedFunctions': 1, 'matchedBytes': 96,
        'nativeSymbolEntries': entries, 'nativeSymbols': {name: item['address'] for name, item in entries.items()},
        'nativeSymbolModules': {name: item['module'] for name, item in entries.items()},
        'sourceDependencies': [], 'replayDependencies': [file_identity(path) for path in sorted(set(deps))],
        'oracle': {'cases': (oracle['counts']['connectedCases'] + oracle['counts']['directCases']), 'actualReturns': oracle['counts']['actualTargetResetReturns'],
            'connectedCallerReturns': oracle['counts']['connectedCallerReturns'],
            'directResetReturns': oracle['counts']['directResetReturns'], 'supportedActualHostReturns': oracle['counts']['supportedActualHostReturns'],
            'nativeCaseDigest': oracle['nativeCaseDigest'],
            'reports': [row['oracle']], 'reproductionCommands': [command]},
        'wholeLinkedRebuild': False, 'registrationPerformedByThisScript': False, 'inputsUnchanged': True,
        'limitations': oracle['limits']}
    path = ROOT / 'evidence/matches/mechanics-save-20261030-sdk-animation-reset.json'
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'matchedFunctions': 1, 'matchedBytes': 96, 'cases': (oracle['counts']['connectedCases'] + oracle['counts']['directCases']),
        'actualReturns': oracle['counts']['actualTargetResetReturns'], 'reportSha256': sha(path.read_bytes())}))


if __name__ == '__main__':
    main()
