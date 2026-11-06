import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from match_mechanics_save_20261029_record33 import sha, file_identity, verify_inputs, native_entry, ROM_SHA, SAVE_SHA, MAIN_SHA
from source_dependencies import dependencies_current


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-directory', default='src/mechanics_save')
    args = parser.parse_args()
    path = Path(args.source_directory)
    if path.is_absolute() or '..' in path.parts:
        raise AssertionError('Source directory must be repository-relative')
    import unicorn
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise AssertionError('Pinned Python3.13.5 and Unicorn2.1.4 are required')
    verify_inputs()
    script = 'evidence/application/record_argument_fixtures_20261030.py'
    command = [sys.executable, str(ROOT / script), '--source-directory', args.source_directory]
    process = subprocess.run(command, capture_output=True, text=True, timeout=300)
    if process.returncode:
        raise AssertionError(process.stdout + process.stderr)
    report_path = 'evidence/application/record-argument-fixtures-20261030.json'
    oracle = json.loads((ROOT / report_path).read_text())
    rows, entries, cache, migrations = [], {}, {}, []
    for source in oracle['sources']:
        row = dict(source)
        row.pop('sourceCredit', None)
        row.update(row['realLinkSnapshot'])
        if not row['exactByteEqual'] or row['compiledBytes'] != row['bytes'] or row['bytes'] not in [24, 44, 60]:
            raise AssertionError('Complete explicit record-argument source did not match')
        row.update({'outputSha256': row['linkedBinarySha256'], 'linked': False,
                    'sourceDependencies': [], 'compilerPath': oracle['compiler']})
        if not dependencies_current(row):
            raise AssertionError('Explicit record source closure is not current')
        for path_key, hash_key in [('source', 'sourceSha256'), ('object', 'objectSha256'),
                                  ('isolatedCallerBinary', 'isolatedCallerBinarySha256'),
                                  ('isolatedCallerLinkValidation', 'isolatedCallerLinkValidationSha256')]:
            if sha((ROOT / row[path_key]).read_bytes()) != row[hash_key]:
                raise AssertionError('Record source/object/link identity changed')
        address = int(row['address'], 0)
        own = native_entry('main', address, cache)
        if own['nativeAlias'] != row['nativeAlias'] or own['bytes'] != row['bytes']:
            raise AssertionError('Own record helper identity differs from measured config')
        metadata, binary, functions = cache['main']
        start = address - int(metadata['base'], 0)
        native = binary[start:start + row['bytes']]
        linked = (ROOT / row['isolatedCallerBinary']).read_bytes()
        validation = json.loads((ROOT / row['isolatedCallerLinkValidation']).read_text())
        if linked != native or validation.get('exactCallerBytes') is not True:
            raise AssertionError('Current complete native/real-link bytes differ')
        if validation['linkerAttempt']['exitCode'] != 0 or validation['linkerSha256'] != 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74':
            raise AssertionError('Pinned real MW link did not succeed')
        if validation['sourceSha256'] != row['sourceSha256'] or validation['sourceObjectSha256'] != row['objectSha256']:
            raise AssertionError('Real-link source/object identity differs')
        if validation['nativeSpanSha256'] != sha(native) or validation['linkedCallerSha256'] != sha(linked):
            raise AssertionError('Real-link native/source identity differs')
        counts = oracle['perFunction'][row['address']]
        row.update({'exactBytes': len(native), 'exactAfterDeclaredRelocation': True, 'exactAfterRealMwLink': True,
                    'oracle': {'supported': True, **counts, 'actualReturns': counts['routineReturns'],
                               'report': report_path, 'reportSha256': sha((ROOT / report_path).read_bytes()),
                               'limits': oracle['limits'], 'limitations': oracle['limitations']}})
        entries[row['name']] = own
        for relocation in row['relocations']:
            entries[relocation['symbol']] = native_entry(relocation['targetModule'], int(relocation['target'], 0), cache)
        migrations.append({'performed': False, 'module': 'main', 'processor': 'arm9', 'mode': 'arm',
                           'address': row['address'], 'bytes': row['bytes'], 'netNewFunctions': 0, 'netNewBytes': 0,
                           'expectedOldPrimarySource': row['oldPrimarySource'],
                           'expectedOldPrimarySourceSha256': row['oldPrimarySourceSha256'],
                           'proposedPrimarySource': row['source'], 'proposedPrimarySourceSha256': row['sourceSha256'],
                           'reason': 'Explicitly forward the real full-word native ID to a typed record lookup, preserving the measured native return and effects.',
                           'requiredIntegratorChecks': 'Audit current primary, retain old source/evidence, select explicit source by hash and rerun complete module/source/ROM/regression gates without increasing coverage.'})
        rows.append(row)
    deps = [script, 'evidence/application/record_arguments_build_20261030.py',
            'evidence/application/preparation_machine_20261029.py', 'evidence/application/target_cache_boundary_20261029.py',
            'preparation_build_20261029.py', 'match_mechanics_save_20261029_record33.py',
            'match_mechanics_save_20261030_record_arguments.py', 'link_runtime_unit.py', 'save_link_snapshots.py',
            'source_dependencies.py', 'provenance/seed-manifest.json']
    deps += [record[0]['symbolsFile'] for record in cache.values()]
    verify_inputs()
    report = {'schemaVersion': 1, 'romSha256': ROM_SHA, 'saveSha256': SAVE_SHA, 'arm9Sha256': MAIN_SHA,
              'matches': rows, 'matchedFunctions': len(rows), 'matchedBytes': sum(r['exactBytes'] for r in rows),
              'netNewFunctions': 0, 'netNewBytes': 0, 'reusedSourceCredit': sum(r['exactBytes'] for r in rows),
              'primaryMigrationProposals': migrations, 'nativeSymbolEntries': entries,
              'nativeSymbols': {name: value['address'] for name, value in entries.items()},
              'nativeSymbolModules': {name: value['module'] for name, value in entries.items()},
              'sourceDependencies': [], 'replayDependencies': [file_identity(path) for path in sorted(set(deps))],
              'oracle': {'cases': oracle['cases'], 'routineReturns': oracle['routineReturns'], 'actualReturns': oracle['actualReturns'],
                         'perFunction': oracle['perFunction'], 'report': report_path, 'reportSha256': sha((ROOT / report_path).read_bytes()),
                         'reproductionCommand': command, 'limits': oracle['limits'], 'limitations': oracle['limitations']},
              'wholeLinkedRebuild': False, 'registrationPerformedByThisScript': False, 'inputsUnchanged': True,
              'limitations': oracle['limitations']}
    output = ROOT / 'evidence/matches/mechanics-save-20261030-record-arguments.json'
    output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'matchedBytes': report['matchedBytes'], 'netNewBytes': 0, 'cases': oracle['cases'],
                      'actualReturns': oracle['actualReturns'], 'report': str(output.relative_to(ROOT)), 'sha256': sha(output.read_bytes())}))


if __name__ == '__main__':
    main()
