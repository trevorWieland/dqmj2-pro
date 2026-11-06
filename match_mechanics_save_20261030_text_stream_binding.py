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
    parser.add_argument('--source', default='src/mechanics_save/20261030_text_stream_binding.c')
    args = parser.parse_args()
    if Path(args.source).is_absolute() or '..' in Path(args.source).parts:
        raise AssertionError('Source must be repository-relative')
    import unicorn
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise AssertionError('Pinned Python/Unicorn runtime is required')
    verify_inputs()
    script = 'evidence/application/text_stream_binding_fixtures_20261030.py'
    fixture_path = 'evidence/application/text-stream-binding-fixtures-20261030.json'
    command = [sys.executable, str(ROOT / script), '--source', args.source]
    process = subprocess.run(command, capture_output=True, text=True, timeout=300)
    if process.returncode:
        raise AssertionError(process.stdout + process.stderr)
    oracle = json.loads((ROOT / fixture_path).read_text())
    row = dict(oracle['source'])
    row.pop('sourceCredit', None)
    row.update(row['realLinkSnapshot'])
    row.update({'outputSha256': row['linkedBinarySha256'], 'linked': False, 'compilerPath': oracle['compiler']})
    if row['sourceSha256'] != '86b8e189f8946c2d459c75ff7330b6233529e360937ad0761d3a0d9f53c03a28':
        raise AssertionError('Source hash changed')
    if not row['exactByteEqual'] or row['compiledBytes'] != 60 or not dependencies_current(row):
        raise AssertionError('Complete header source/closure did not match')
    for path_key, hash_key in [('source', 'sourceSha256'), ('object', 'objectSha256'),
                              ('isolatedCallerBinary', 'isolatedCallerBinarySha256'),
                              ('isolatedCallerLinkValidation', 'isolatedCallerLinkValidationSha256')]:
        if sha((ROOT / row[path_key]).read_bytes()) != row[hash_key]:
            raise AssertionError('Pinned source/object/real-link identity changed')
    cache = {}
    own = native_entry('main', 0x020853C8, cache)
    if row['nativeAlias'] != own['nativeAlias'] or row['bytes'] != own['bytes'] or own['bytes'] != 60:
        raise AssertionError('Own measured function identity differs')
    metadata, binary, functions = cache['main']
    offset = 0x020853C8 - int(metadata['base'], 0)
    native = binary[offset:offset + 60]
    linked = (ROOT / row['isolatedCallerBinary']).read_bytes()
    validation = json.loads((ROOT / row['isolatedCallerLinkValidation']).read_text())
    if native != linked or len(linked) != 60 or validation.get('exactCallerBytes') is not True:
        raise AssertionError('Complete source/native/link bytes differ')
    if validation['linkerAttempt']['exitCode'] != 0 or validation['linkerSha256'] != 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74':
        raise AssertionError('Pinned real MW link did not succeed')
    if validation['sourceSha256'] != row['sourceSha256'] or validation['sourceObjectSha256'] != row['objectSha256']:
        raise AssertionError('Real link source/object differs')
    if validation['nativeSpanSha256'] != sha(native) or validation['linkedCallerSha256'] != sha(linked):
        raise AssertionError('Real link native/source identity differs')
    row.update({'exactBytes': 60, 'exactAfterDeclaredRelocation': True, 'exactAfterRealMwLink': True,
                'signature': 'TextBinding *native_main_020853c8(TextBinding *target, const u16 *stream)',
                'oracle': {'supported': True, 'cases': oracle['cases'], 'routineReturns': oracle['routineReturns'],
                           'actualReturns': oracle['actualReturns'], 'report': fixture_path,
                           'reportSha256': sha((ROOT / fixture_path).read_bytes()),
                           'limits': oracle['limits'], 'limitations': oracle['limitations']}})
    entries = {row['name']: own}
    for relocation in row['relocations']:
        module, target = relocation['targetModule'], int(relocation['target'], 0)
        entries[relocation['symbol']] = data_entry(module, target, cache) if relocation['targetMode'] == 'data' else native_entry(module, target, cache)
    deps = [script, 'evidence/application/text_stream_binding_build_20261030.py',
            'evidence/application/allocation-constructor-other-modes-arm7-20261030.py',
            'evidence/application/allocation-constructor-arm7-20261030-setup.py',
            'evidence/application/allocation-constructor-arm7-20261030.py',
            'evidence/application/preparation_machine_20261029.py',
            'evidence/application/eligibility_machine_20261029.py', 'preparation_build_20261029.py',
            'match_mechanics_save_20261029_record33.py', 'match_mechanics_save_20261029_item_use.py',
            'match_mechanics_save_20261030_text_stream_binding.py', 'link_runtime_unit.py',
            'save_link_snapshots.py', 'source_dependencies.py', 'provenance/seed-manifest.json']
    deps += [record[0]['symbolsFile'] for record in cache.values()]
    verify_inputs()
    report = {'schemaVersion': 1, 'romSha256': ROM_SHA, 'saveSha256': SAVE_SHA, 'arm9Sha256': MAIN_SHA,
              'matches': [row], 'matchedFunctions': 1, 'matchedBytes': 60,
              'nativeSymbolEntries': entries, 'nativeSymbols': {name: item['address'] for name, item in entries.items()},
              'nativeSymbolModules': {name: item['module'] for name, item in entries.items()},
              'sourceDependencies': [], 'replayDependencies': [file_identity(path) for path in sorted(set(deps))],
              'oracle': {'cases': oracle['cases'], 'actualReturns': oracle['actualReturns'],
                         'reports': [row['oracle']], 'reproductionCommands': [command]},
              'wholeLinkedRebuild': False, 'registrationPerformedByThisScript': False, 'inputsUnchanged': True,
              'limitations': ['The exact complete C candidate and bounded effects are measured; integrator module/ROM acceptance remains required.',
                              'Leaf routine executes with no provider calls; unterminated32 retains count1 and null input faults remain excluded.']}
    path = ROOT / 'evidence/matches/mechanics-save-20261030-text-stream-binding.json'
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'matchedFunctions': 1, 'matchedBytes': 60, 'cases': oracle['cases'],
                      'actualReturns': oracle['actualReturns'], 'reportSha256': sha(path.read_bytes())}))


if __name__ == '__main__':
    main()
