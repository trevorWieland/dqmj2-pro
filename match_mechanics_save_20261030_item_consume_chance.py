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
    parser.add_argument('--source', default='src/mechanics_save/20261030_item_consume_chance.c')
    args = parser.parse_args()
    import unicorn
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise AssertionError('Pinned Python3.13.5 and Unicorn2.1.4 are required')
    verify_inputs()
    script = 'evidence/application/item_consume_chance_fixtures_20261030.py'
    command = [sys.executable, str(ROOT / script), '--source', args.source]
    process = subprocess.run(command, capture_output=True, text=True, timeout=300)
    if process.returncode:
        raise AssertionError(process.stdout + process.stderr)
    report_path = 'evidence/application/item-consume-chance-fixtures-20261030.json'
    oracle = json.loads((ROOT / report_path).read_text())
    row = dict(oracle['source'])
    row.pop('sourceCredit', None)
    row.pop('registered', None)
    row.update(row['realLinkSnapshot'])
    if not row['exactByteEqual'] or row['compiledBytes'] != 40 or row['bytes'] != 40:
        raise AssertionError('Complete explicit item-word chance source did not match')
    row.update({'outputSha256': row['linkedBinarySha256'], 'linked': False,
                'sourceDependencies': [], 'compilerPath': oracle['compiler']})
    if not dependencies_current(row):
        raise AssertionError('Explicit chance source closure is not current')
    for path_key, hash_key in [('source', 'sourceSha256'), ('object', 'objectSha256'),
                              ('isolatedCallerBinary', 'isolatedCallerBinarySha256'),
                              ('isolatedCallerLinkValidation', 'isolatedCallerLinkValidationSha256')]:
        if sha((ROOT / row[path_key]).read_bytes()) != row[hash_key]:
            raise AssertionError('Chance source/object/link identity changed')
    cache, entries = {}, {}
    own = native_entry('main', 0x02065DEC, cache)
    if own['nativeAlias'] != row['nativeAlias'] or own['bytes'] != 40:
        raise AssertionError('Chance own native identity differs from measured config')
    metadata, native_body, functions = cache['main']
    start = 0x02065DEC - int(metadata['base'], 0)
    native = native_body[start:start + 40]
    linked = (ROOT / row['isolatedCallerBinary']).read_bytes()
    validation = json.loads((ROOT / row['isolatedCallerLinkValidation']).read_text())
    if linked != native or len(native) != 40 or validation.get('exactCallerBytes') is not True:
        raise AssertionError('Current complete native/real-link bytes differ')
    if validation['linkerAttempt']['exitCode'] != 0 or validation['linkerSha256'] != 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74':
        raise AssertionError('Pinned real MW link did not succeed')
    if validation['sourceSha256'] != row['sourceSha256'] or validation['sourceObjectSha256'] != row['objectSha256']:
        raise AssertionError('Real-link source/object identity differs')
    if validation['nativeSpanSha256'] != sha(native) or validation['linkedCallerSha256'] != sha(linked):
        raise AssertionError('Real-link native/source identity differs')
    row.update({'exactBytes': sum(a == b for a, b in zip(linked, native)),
                'exactAfterDeclaredRelocation': True, 'exactAfterRealMwLink': True,
                'oracle': {'supported': True, 'cases': oracle['cases'], 'routineReturns': oracle['routineReturns'],
                           'actualReturns': oracle['actualReturns'], 'report': report_path,
                           'reportSha256': sha((ROOT / report_path).read_bytes()),
                           'limits': oracle['limits'], 'limitations': oracle['limitations']}})
    entries[row['name']] = own
    for relocation in row['relocations']:
        entries[relocation['symbol']] = native_entry(relocation['targetModule'], int(relocation['target'], 0), cache)
    migration = {'performed': False, 'netNewFunctions': 0, 'netNewBytes': 0,
                 'expectedOldPrimarySource': oracle['oldPrimarySource'],
                 'expectedOldPrimarySourceSha256': oracle['oldPrimarySourceSha256'],
                 'proposedPrimarySource': row['source'], 'proposedPrimarySourceSha256': row['sourceSha256'],
                 'reason': 'Replace implicit hardware item-R0 retention with an explicit signed32-bit item argument and typed getter(item), retaining identical code and actual native RNG behavior.',
                 'requiredIntegratorChecks': 'Audit current primary identity, retain old source/evidence, select the explicit source, and rerun full module/source/ROM/regression gates without increasing coverage.'}
    deps = [script, 'evidence/application/item_consume_chance_build_20261030.py',
            'evidence/application/preparation_machine_20261029.py', 'preparation_build_20261029.py',
            'match_mechanics_save_20261029_record33.py', 'match_mechanics_save_20261030_item_consume_chance.py',
            'link_runtime_unit.py', 'save_link_snapshots.py', 'source_dependencies.py', 'provenance/seed-manifest.json']
    deps += [record[0]['symbolsFile'] for record in cache.values()]
    verify_inputs()
    report = {'schemaVersion': 1, 'romSha256': ROM_SHA, 'saveSha256': SAVE_SHA, 'arm9Sha256': MAIN_SHA,
              'matches': [row], 'matchedFunctions': 1, 'matchedBytes': row['exactBytes'],
              'netNewFunctions': 0, 'netNewBytes': 0, 'reusedSourceCredit': 40,
              'primaryMigrationProposal': migration, 'nativeSymbolEntries': entries,
              'nativeSymbols': {name: value['address'] for name, value in entries.items()},
              'nativeSymbolModules': {name: value['module'] for name, value in entries.items()},
              'sourceDependencies': [], 'replayDependencies': [file_identity(path) for path in sorted(set(deps))],
              'oracle': {'cases': oracle['cases'], 'routineReturns': oracle['routineReturns'],
                         'rngControlReturns': oracle['rngControlReturns'], 'actualReturns': oracle['actualReturns'],
                         'nestedRngReturns': oracle['nestedRngReturns'], 'report': report_path,
                         'reportSha256': sha((ROOT / report_path).read_bytes()), 'reproductionCommand': command,
                         'limits': oracle['limits'], 'limitations': oracle['limitations']},
              'wholeLinkedRebuild': False, 'registrationPerformedByThisScript': False,
              'inputsUnchanged': True, 'limitations': oracle['limitations']}
    output = ROOT / 'evidence/matches/mechanics-save-20261030-item-consume-chance.json'
    output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'matchedBytes': row['exactBytes'], 'netNewBytes': 0, 'cases': oracle['cases'],
                      'actualReturns': oracle['actualReturns'], 'report': str(output.relative_to(ROOT)),
                      'sha256': sha(output.read_bytes())}))


if __name__ == '__main__':
    main()
