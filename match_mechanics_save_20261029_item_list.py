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
    parser.add_argument('--list-source', default='src/mechanics_save/20261029_item_list.c')
    parser.add_argument('--append-source', default='src/mechanics_save/20261029_item_list_append.c')
    parser.add_argument('--predicate-source', default='src/mechanics_save/20261029_item_list_predicate.c')
    args = parser.parse_args()
    import unicorn
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise AssertionError('Pinned Python3.13.5 and Unicorn2.1.4 are required')
    verify_inputs()
    script = 'evidence/application/item_list_exact_fixtures_20261029.py'
    command = [sys.executable, str(ROOT / script), '--list-source', args.list_source,
               '--append-source', args.append_source, '--predicate-source', args.predicate_source]
    process = subprocess.run(command, capture_output=True, text=True, timeout=180)
    if process.returncode:
        raise AssertionError(process.stdout + process.stderr)
    report_path = 'evidence/application/item-list-exact-fixtures-20261029.json'
    oracle = json.loads((ROOT / report_path).read_text())
    entries, cache, matches = {}, {}, []
    for original in oracle['matches']:
        row = dict(original)
        row.pop('sourceCredit', None)
        row.pop('registered', None)
        if not row['exactByteEqual'] or row['compiledBytes'] != row['bytes']:
            raise AssertionError('Complete item-list source did not match')
        row.update(row['realLinkSnapshot'])
        row.update({'outputSha256': row['linkedBinarySha256'], 'linked': False, 'sourceDependencies': [],
                    'compilerPath': oracle['compiler'],
                    'oracle': {'supported': True, 'cases': oracle['cases'], 'actualReturns': oracle['actualReturns'],
                               'report': report_path, 'reportSha256': sha((ROOT / report_path).read_bytes()),
                               'limits': oracle['limits'], 'limitations': oracle['limitations']}})
        if not dependencies_current(row):
            raise AssertionError('Item-list source closure is not current')
        for path_key, hash_key in [('source', 'sourceSha256'), ('object', 'objectSha256'),
                                  ('isolatedCallerBinary', 'isolatedCallerBinarySha256'),
                                  ('isolatedCallerLinkValidation', 'isolatedCallerLinkValidationSha256')]:
            if sha((ROOT / row[path_key]).read_bytes()) != row[hash_key]:
                raise AssertionError('Item-list source/object/link identity changed')
        own = native_entry(row['module'], int(row['address'], 0), cache)
        if row['nativeAlias'] != own['nativeAlias']:
            raise AssertionError('Own item-list alias differs from measured config')
        metadata, native_body, functions = cache[row['module']]
        start = int(row['address'], 0) - int(metadata['base'], 0)
        native_span = native_body[start:start + row['bytes']]
        linked = (ROOT / row['isolatedCallerBinary']).read_bytes()
        validation = json.loads((ROOT / row['isolatedCallerLinkValidation']).read_text())
        if len(native_span) != row['bytes'] or linked != native_span:
            raise AssertionError('Current full native span differs from real-linked source')
        if validation.get('exactCallerBytes') is not True or validation['linkerAttempt']['exitCode'] != 0:
            raise AssertionError('Real MW linker did not validate complete caller bytes')
        if validation['sourceSha256'] != row['sourceSha256'] or validation['sourceObjectSha256'] != row['objectSha256']:
            raise AssertionError('Real-link validation belongs to different source/object')
        if validation['nativeSpanSha256'] != sha(native_span) or validation['linkedCallerSha256'] != sha(linked):
            raise AssertionError('Real-link native/source identities differ from current bytes')
        if validation['linkerSha256'] != 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74':
            raise AssertionError('Real-link validation used an unpinned linker')
        row.update({'exactBytes': sum(a == b for a, b in zip(linked, native_span)),
                    'exactAfterDeclaredRelocation': True, 'exactAfterRealMwLink': True})
        entries[row['name']] = own
        for relocation in row['relocations']:
            module, address = relocation['targetModule'], int(relocation['target'], 0)
            entry = data_entry(module, address, cache) if relocation['targetMode'] == 'data' else native_entry(module, address, cache)
            entries[relocation['symbol']] = entry
        matches.append(row)
    if len(matches) != 3 or sum(row['bytes'] for row in matches) != 452:
        raise AssertionError('Item-list batch extent changed')
    deps = [script, 'evidence/application/item_list_exact_build_20261029.py',
            'evidence/application/item_list_boundary_20261029.py',
            'evidence/application/target_cache_boundary_20261029.py',
            'evidence/application/preparation_machine_20261029.py', 'preparation_build_20261029.py',
            'match_mechanics_save_20261029_record33.py', 'match_mechanics_save_20261029_item_use.py',
            'match_mechanics_save_20261029_item_list.py', 'link_runtime_unit.py',
            'save_link_snapshots.py', 'source_dependencies.py', 'provenance/seed-manifest.json']
    deps += [metadata[0]['symbolsFile'] for metadata in cache.values()]
    verify_inputs()
    report = {'schemaVersion': 1, 'romSha256': ROM_SHA, 'saveSha256': SAVE_SHA, 'arm9Sha256': MAIN_SHA,
              'compilerSha256': matches[0]['compilerSha256'], 'sourceDependencies': [], 'matches': matches,
              'nativeSymbolEntries': entries, 'nativeSymbols': {name: value['address'] for name, value in entries.items()},
              'nativeSymbolModules': {name: value['module'] for name, value in entries.items()},
              'matchedFunctions': len(matches), 'matchedBytes': sum(row['exactBytes'] for row in matches),
              'oracle': {'cases': oracle['cases'], 'actualReturns': oracle['actualReturns'],
                         'report': report_path, 'reportSha256': sha((ROOT / report_path).read_bytes()),
                         'reproductionCommand': command, 'limits': oracle['limits'], 'limitations': oracle['limitations']},
              'replayDependencies': [file_identity(path) for path in sorted(set(deps))],
              'listCases': oracle['listCases'], 'appendCases': oracle['appendCases'], 'predicateCases': oracle['predicateCases'],
              'routineReturns': oracle['routineReturns'], 'setupControlReturns': oracle['setupControlReturns'],
              'nativeCalleeCodeOrSourceCredit': 0, 'reusedSourceCredit': 0, 'wholeLinkedRebuild': False,
              'registrationPerformedByThisScript': False, 'inputsUnchanged': True, 'limitations': oracle['limitations']}
    output = ROOT / 'evidence/matches/mechanics-save-20261029-item-list.json'
    output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'matchedFunctions': 3, 'matchedBytes': 452, 'oracleCases': oracle['cases'],
                      'actualReturns': oracle['actualReturns'], 'report': str(output.relative_to(ROOT)),
                      'reportSha256': sha(output.read_bytes())}))


if __name__ == '__main__':
    main()
