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
    parser.add_argument('--bounds-source', default='src/mechanics_save/20261030_allocation_bounds.c')
    parser.add_argument('--count-source', default='src/mechanics_save/20261030_skill_last_entry.c')
    args = parser.parse_args()
    for value in [args.bounds_source, args.count_source]:
        if Path(value).is_absolute() or '..' in Path(value).parts:
            raise AssertionError('Sources must be repository-relative')
    import unicorn
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise AssertionError('Pinned Python3.13.5 and Unicorn2.1.4 are required')
    verify_inputs()
    specifications = [
        ('evidence/application/allocation_bounds_fixtures_20261030.py', 'evidence/application/allocation-bounds-fixtures-20261030.json', args.bounds_source, 0x020768D8, 276),
        ('evidence/application/skill_last_entry_fixtures_20261030.py', 'evidence/application/skill-last-entry-fixtures-20261030.json', args.count_source, 0x0207AD3C, 68)]
    rows, entries, cache, oracles, commands = [], {}, {}, [], []
    for script, report_path, source, address, length in specifications:
        command = [sys.executable, str(ROOT / script), '--source', source]
        process = subprocess.run(command, capture_output=True, text=True, timeout=300)
        if process.returncode:
            raise AssertionError(process.stdout + process.stderr)
        oracle = json.loads((ROOT / report_path).read_text())
        row = dict(oracle['source'])
        row.pop('sourceCredit', None)
        row.update(row['realLinkSnapshot'])
        if not row['exactByteEqual'] or row['compiledBytes'] != length or row['bytes'] != length:
            raise AssertionError('Complete bounds/count source did not match')
        row.update({'outputSha256': row['linkedBinarySha256'], 'linked': False,
                    'sourceDependencies': [], 'compilerPath': oracle['compiler']})
        if not dependencies_current(row):
            raise AssertionError('Bounds/count source closure is not current')
        for path_key, hash_key in [('source', 'sourceSha256'), ('object', 'objectSha256'),
                                  ('isolatedCallerBinary', 'isolatedCallerBinarySha256'),
                                  ('isolatedCallerLinkValidation', 'isolatedCallerLinkValidationSha256')]:
            if sha((ROOT / row[path_key]).read_bytes()) != row[hash_key]:
                raise AssertionError('Source/object/link identity changed')
        own = native_entry('main', address, cache)
        if own['nativeAlias'] != row['nativeAlias'] or own['bytes'] != length or int(row['address'], 0) != address:
            raise AssertionError('Own function identity differs from measured config')
        metadata, binary, functions = cache['main']
        start = address - int(metadata['base'], 0)
        native = binary[start:start + length]
        linked = (ROOT / row['isolatedCallerBinary']).read_bytes()
        validation = json.loads((ROOT / row['isolatedCallerLinkValidation']).read_text())
        if linked != native or len(native) != length or validation.get('exactCallerBytes') is not True:
            raise AssertionError('Current complete native/real-link bytes differ')
        if validation['linkerAttempt']['exitCode'] != 0 or validation['linkerSha256'] != 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74':
            raise AssertionError('Pinned real MW link did not succeed')
        if validation['sourceSha256'] != row['sourceSha256'] or validation['sourceObjectSha256'] != row['objectSha256']:
            raise AssertionError('Real-link source/object identity differs')
        if validation['nativeSpanSha256'] != sha(native) or validation['linkedCallerSha256'] != sha(linked):
            raise AssertionError('Real-link native/source identity differs')
        row.update({'exactBytes': length, 'exactAfterDeclaredRelocation': True, 'exactAfterRealMwLink': True,
                    'oracle': {'supported': True, 'cases': oracle['cases'], 'routineReturns': oracle['routineReturns'],
                               'actualReturns': oracle['actualReturns'], 'report': report_path,
                               'reportSha256': sha((ROOT / report_path).read_bytes()),
                               'limits': oracle['limits'], 'limitations': oracle['limitations']}})
        entries[row['name']] = own
        for relocation in row['relocations']:
            module, target = relocation['targetModule'], int(relocation['target'], 0)
            entries[relocation['symbol']] = data_entry(module, target, cache) if relocation['targetMode'] == 'data' else native_entry(module, target, cache)
        rows.append(row)
        oracles.append(row['oracle'])
        commands.append(command)
    deps = [item[0] for item in specifications] + [
        'evidence/application/allocation_bounds_build_20261030.py', 'evidence/application/skill_last_entry_build_20261030.py',
        'evidence/application/preparation_machine_20261029.py', 'evidence/application/target_cache_boundary_20261029.py',
        'preparation_build_20261029.py', 'match_mechanics_save_20261029_record33.py',
        'match_mechanics_save_20261029_item_use.py', 'match_mechanics_save_20261030_allocation_bounds.py',
        'link_runtime_unit.py', 'save_link_snapshots.py', 'source_dependencies.py', 'provenance/seed-manifest.json']
    deps += [record[0]['symbolsFile'] for record in cache.values()]
    verify_inputs()
    report = {'schemaVersion': 1, 'romSha256': ROM_SHA, 'saveSha256': SAVE_SHA, 'arm9Sha256': MAIN_SHA,
              'matches': rows, 'matchedFunctions': len(rows), 'matchedBytes': sum(row['exactBytes'] for row in rows),
              'nativeSymbolEntries': entries, 'nativeSymbols': {name: row['address'] for name, row in entries.items()},
              'nativeSymbolModules': {name: row['module'] for name, row in entries.items()},
              'sourceDependencies': [], 'replayDependencies': [file_identity(path) for path in sorted(set(deps))],
              'oracle': {'cases': sum(row['cases'] for row in oracles), 'actualReturns': sum(row['actualReturns'] for row in oracles),
                         'reports': oracles, 'reproductionCommands': commands},
              'wholeLinkedRebuild': False, 'registrationPerformedByThisScript': False, 'inputsUnchanged': True,
              'limitations': ['Complete matched source candidates and bounded effects are measured; integrator module/ROM acceptance is still required.',
                              'The bounds helper supplies navigation limits. No unconditional commit/import prohibition or ordinary scene eligibility is inferred.']}
    output = ROOT / 'evidence/matches/mechanics-save-20261030-allocation-bounds.json'
    output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'matchedFunctions': len(rows), 'matchedBytes': report['matchedBytes'],
                      'cases': report['oracle']['cases'], 'actualReturns': report['oracle']['actualReturns'],
                      'report': str(output.relative_to(ROOT)), 'sha256': sha(output.read_bytes())}))


if __name__ == '__main__':
    main()
