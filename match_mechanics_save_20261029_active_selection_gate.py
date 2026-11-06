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
    parser.add_argument('--source', default='src/mechanics_save/20261029_active_selection_gate.c')
    args = parser.parse_args()
    import unicorn
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise AssertionError('Pinned Python3.13.5 and Unicorn2.1.4 are required')
    verify_inputs()
    script = 'evidence/application/active_selection_gate_fixtures_20261029.py'
    command = [sys.executable, str(ROOT / script), '--source', args.source]
    process = subprocess.run(command, capture_output=True, text=True, timeout=90)
    if process.returncode:
        raise AssertionError(process.stdout + process.stderr)
    report_path = 'evidence/application/active-selection-gate-fixtures-20261029.json'
    oracle = json.loads((ROOT / report_path).read_text())
    row = dict(oracle['source'])
    row.pop('sourceCredit', None)
    row.pop('registered', None)
    if not row['exactByteEqual'] or row['compiledBytes'] != row['bytes']:
        raise AssertionError('Complete menu source did not match')
    row.update(row['realLinkSnapshot'])
    row.update({'outputSha256': row['linkedBinarySha256'], 'linked': False, 'sourceDependencies': [],
                'compilerPath': oracle['compiler'],
                'oracle': {'supported': True, 'cases': oracle['cases'], 'actualReturns': oracle['actualReturns'],
                           'nativeAndRecompiledCalls': oracle['actualReturns'], 'report': report_path,
                           'reportSha256': sha((ROOT / report_path).read_bytes()),
                           'limits': oracle['limits'], 'limitations': oracle['limitations']}})
    if not dependencies_current(row):
        raise AssertionError('Menu source closure is not current')
    for path_key, hash_key in [('source', 'sourceSha256'), ('object', 'objectSha256'),
                                ('isolatedCallerBinary', 'isolatedCallerBinarySha256'),
                                ('isolatedCallerLinkValidation', 'isolatedCallerLinkValidationSha256')]:
        if sha((ROOT / row[path_key]).read_bytes()) != row[hash_key]:
            raise AssertionError('Menu source/object/link identity changed')
    entries, cache = {}, {}
    for relocation in row['relocations']:
        entries[relocation['symbol']] = native_entry(relocation['targetModule'], int(relocation['target'], 0), cache)
    entries[row['name']] = native_entry('main', int(row['address'], 0), cache)
    deps = [script, 'evidence/application/active_selection_gate_build_20261029.py',
            'evidence/application/record33_menu_build_20261029.py',
            'src/mechanics_save/20261029_record33_menu.c',
            'evidence/application/preparation_machine_20261029.py', 'preparation_build_20261029.py',
            'match_mechanics_save_20261029_record33.py', 'match_mechanics_save_20261029_active_selection_gate.py',
            'link_runtime_unit.py', 'save_link_snapshots.py', 'source_dependencies.py']
    verify_inputs()
    report = {'schemaVersion': 1, 'romSha256': ROM_SHA, 'saveSha256': SAVE_SHA, 'arm9Sha256': MAIN_SHA,
              'compilerSha256': row['compilerSha256'], 'sourceDependencies': [], 'matches': [row],
              'nativeSymbolEntries': entries, 'nativeSymbols': {name: value['address'] for name, value in entries.items()},
              'nativeSymbolModules': {name: value['module'] for name, value in entries.items()},
              'matchedFunctions': 1, 'matchedBytes': 172,
              'oracle': {'cases': oracle['cases'], 'actualReturns': oracle['actualReturns'],
                         'nativeAndRecompiledCalls': oracle['actualReturns'], 'report': report_path,
                         'reportSha256': sha((ROOT / report_path).read_bytes()),
                         'reproductionCommand': command, 'limits': oracle['limits'],
                         'limitations': oracle['limitations']},
              'replayDependencies': [file_identity(path) for path in deps],
              'reusedCaller': oracle['reusedCaller'], 'directOracleCases': oracle['directCases'],
              'connectedOracleCases': oracle['connectedCases'], 'reusedCallerSourceCredit': 0,
              'nativeCalleeCodeOrSourceCredit': 0, 'wholeLinkedRebuild': False,
              'registrationPerformedByThisScript': False, 'inputsUnchanged': True,
              'limitations': ['Complete172-byte ordinary C body matches after real MW linking; coordinator registration and module/full-ROM gates remain separate.',
                              'The provider-free oracle covers direct mask2-clear/set ID membership plus connected caller initial-false and mask2-set paths.',
                              'The connected208-byte caller is reused with zero new source credit; its mode2 entity path remains unsupported.',
                              'No status/ownership label or ordinary menu reachability is promoted.']}
    output = ROOT / 'evidence/matches/mechanics-save-20261029-active-selection-gate.json'
    output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'matchedFunctions': 1, 'matchedBytes': 172, 'oracleCases': oracle['cases'],
                      'actualReturns': oracle['actualReturns'], 'report': str(output.relative_to(ROOT)),
                      'reportSha256': sha(output.read_bytes())}))


if __name__ == '__main__':
    main()
