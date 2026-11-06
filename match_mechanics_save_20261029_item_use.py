import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from match_mechanics_save_20261029_record33 import sha, file_identity, verify_inputs, native_entry, ROM_SHA, SAVE_SHA, MAIN_SHA
from source_dependencies import dependencies_current


def data_entry(module, address, cache):
    metadata, body, functions = cache[module]
    path = ROOT / metadata['symbolsFile']
    records = re.findall(r'^(\S+) kind:(bss|data)(?:\([^)]*\))? addr:0x' + f'{address:08x}' + r'$', path.read_text(), re.M)
    if len(records) != 1:
        raise AssertionError(('Binding is not an unambiguous declared native data address', module, hex(address)))
    name, storage = records[0]
    return {'address': hex(address), 'mode': 'data', 'module': module, 'processor': 'arm9', 'kind': 'data',
            'nativeAlias': name, 'nativeStorageKind': storage, 'nativeModuleSha256': metadata['sha256'],
            'symbolTable': metadata['symbolsFile'], 'symbolTableSha256': sha(path.read_bytes()),
            'verification': 'Declared native BSS/data address in measured module config; no ROM-backed content or source-data credit claimed.'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', default='src/mechanics_save/20261029_item_use.c')
    args = parser.parse_args()
    import unicorn
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise AssertionError('Pinned Python3.13.5 and Unicorn2.1.4 are required')
    verify_inputs()
    script = 'evidence/application/item_use_exact_fixtures_20261029.py'
    command = [sys.executable, str(ROOT / script), '--source', args.source]
    process = subprocess.run(command, capture_output=True, text=True, timeout=180)
    if process.returncode:
        raise AssertionError(process.stdout + process.stderr)
    report_path = 'evidence/application/item-use-exact-fixtures-20261029.json'
    oracle = json.loads((ROOT / report_path).read_text())
    row = dict(oracle['source'])
    row.pop('sourceCredit', None)
    row.pop('registered', None)
    if not row['exactByteEqual'] or row['compiledBytes'] != row['bytes']:
        raise AssertionError('Complete item-use source did not match')
    row.update(row['realLinkSnapshot'])
    row.update({'outputSha256': row['linkedBinarySha256'], 'linked': False, 'sourceDependencies': [],
                'compilerPath': oracle['compiler'],
                'oracle': {'supported': True, 'cases': oracle['cases'], 'actualReturns': oracle['actualReturns'],
                           'report': report_path, 'reportSha256': sha((ROOT / report_path).read_bytes()),
                           'limits': oracle['limits'], 'limitations': oracle['limitations']}})
    if not dependencies_current(row):
        raise AssertionError('Item-use source closure is not current')
    for path_key, hash_key in [('source', 'sourceSha256'), ('object', 'objectSha256'),
                              ('isolatedCallerBinary', 'isolatedCallerBinarySha256'),
                              ('isolatedCallerLinkValidation', 'isolatedCallerLinkValidationSha256')]:
        if sha((ROOT / row[path_key]).read_bytes()) != row[hash_key]:
            raise AssertionError('Item-use source/object/link identity changed')
    entries, cache = {}, {}
    own = native_entry('main', int(row['address'], 0), cache)
    if row['nativeAlias'] != own['nativeAlias']:
        raise AssertionError('Own item-use alias differs from measured config')
    entries[row['name']] = own
    for relocation in row['relocations']:
        module, address = relocation['targetModule'], int(relocation['target'], 0)
        if relocation['targetMode'] == 'data':
            entry = data_entry(module, address, cache)
        else:
            entry = native_entry(module, address, cache)
        entries[relocation['symbol']] = entry
    deps = [script, 'evidence/application/item_use_match_build_20261029.py',
            'evidence/application/preparation_machine_20261029.py', 'evidence/application/eligibility_machine_20261029.py',
            'evidence/application/preparation_fixtures_20261029.py', 'evidence/application/effect_fixtures_20261029.py',
            'evidence/application/effect_build_20261029.py', 'evidence/application/eligibility_exact_fixtures_20261029.py',
            'evidence/application/eligibility_build_20261029.py', 'preparation_build_20261029.py',
            'match_mechanics_save_20261029_record33.py', 'match_mechanics_save_20261029_item_use.py',
            'link_runtime_unit.py', 'save_link_snapshots.py', 'source_dependencies.py', 'provenance/seed-manifest.json']
    deps += [metadata[0]['symbolsFile'] for metadata in cache.values()]
    verify_inputs()
    report = {'schemaVersion': 1, 'romSha256': ROM_SHA, 'saveSha256': SAVE_SHA, 'arm9Sha256': MAIN_SHA,
              'compilerSha256': row['compilerSha256'], 'sourceDependencies': [], 'matches': [row],
              'nativeSymbolEntries': entries, 'nativeSymbols': {name: value['address'] for name, value in entries.items()},
              'nativeSymbolModules': {name: value['module'] for name, value in entries.items()},
              'matchedFunctions': 1, 'matchedBytes': 968,
              'oracle': {'cases': oracle['cases'], 'actualReturns': oracle['actualReturns'],
                         'report': report_path, 'reportSha256': sha((ROOT / report_path).read_bytes()),
                         'reproductionCommand': command, 'limits': oracle['limits'], 'limitations': oracle['limitations']},
              'replayDependencies': [file_identity(path) for path in sorted(set(deps))],
              'stateCases': oracle['stateCases'], 'bookCases': oracle['bookCases'],
              'routineReturns': oracle['routineReturns'], 'leafControlReturns': oracle['leafControlReturns'],
              'nativeCalleeCodeOrSourceCredit': 0, 'reusedSourceCredit': 0, 'wholeLinkedRebuild': False,
              'registrationPerformedByThisScript': False, 'inputsUnchanged': True, 'limitations': oracle['limitations']}
    output = ROOT / 'evidence/matches/mechanics-save-20261029-item-use.json'
    output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'matchedFunctions': 1, 'matchedBytes': 968, 'oracleCases': oracle['cases'],
                      'actualReturns': oracle['actualReturns'], 'report': str(output.relative_to(ROOT)),
                      'reportSha256': sha(output.read_bytes())}))


if __name__ == '__main__':
    main()
