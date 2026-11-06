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
    parser.add_argument('--source', default='src/mechanics_save/20261029_item_effect_wrapper.c')
    args = parser.parse_args()
    import unicorn
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise AssertionError('Pinned Python3.13.5 and Unicorn2.1.4 are required')
    verify_inputs()
    script = 'evidence/application/effect_wrapper_fixtures_20261029.py'
    command = [sys.executable, str(ROOT / script), '--source', args.source]
    process = subprocess.run(command, capture_output=True, text=True, timeout=120)
    if process.returncode:
        raise AssertionError(process.stdout + process.stderr)
    report_path = 'evidence/application/effect-wrapper-fixtures-20261029.json'
    oracle = json.loads((ROOT / report_path).read_text())
    row = dict(oracle['source'])
    row.pop('sourceCredit', None)
    row.pop('registered', None)
    if not row['exactByteEqual'] or row['compiledBytes'] != row['bytes']:
        raise AssertionError('Complete wrapper source did not match')
    row.update(row['realLinkSnapshot'])
    row.update({'outputSha256': row['linkedBinarySha256'], 'linked': False, 'sourceDependencies': [],
                'compilerPath': oracle['compiler'],
                'oracle': {'supported': True, 'cases': oracle['cases'], 'actualReturns': oracle['actualReturns'],
                           'nativeAndRecompiledCalls': oracle['actualReturns'], 'report': report_path,
                           'reportSha256': sha((ROOT / report_path).read_bytes()),
                           'limits': oracle['limits'], 'limitations': oracle['limitations']}})
    if not dependencies_current(row):
        raise AssertionError('Wrapper source closure is not current')
    for path_key, hash_key in [('source', 'sourceSha256'), ('object', 'objectSha256'),
                                ('isolatedCallerBinary', 'isolatedCallerBinarySha256'),
                                ('isolatedCallerLinkValidation', 'isolatedCallerLinkValidationSha256')]:
        if sha((ROOT / row[path_key]).read_bytes()) != row[hash_key]:
            raise AssertionError('Wrapper source/object/link identity changed')
    entries, cache = {}, {}
    for relocation in row['relocations']:
        entries[relocation['symbol']] = native_entry(relocation['targetModule'], int(relocation['target'], 0), cache)
    entries[row['name']] = native_entry('ov000', int(row['address'], 0), cache)
    if row['nativeAlias'] != entries[row['name']]['nativeAlias']:
        raise AssertionError('Wrapper own alias differs from its qualified native span')
    deps = [script, 'evidence/application/effect_wrapper_build_20261029.py',
            'evidence/application/preparation_machine_20261029.py', 'preparation_build_20261029.py',
            'evidence/application/eligibility_machine_20261029.py', 'evidence/application/effect_fixtures_20261029.py',
            'evidence/application/effect_build_20261029.py', 'evidence/application/eligibility_exact_fixtures_20261029.py',
            'evidence/application/eligibility_build_20261029.py',
            'match_mechanics_save_20261029_record33.py', 'match_mechanics_save_20261029_item_effect_wrapper.py',
            'link_runtime_unit.py', 'save_link_snapshots.py', 'source_dependencies.py']
    verify_inputs()
    report = {'schemaVersion': 1, 'romSha256': ROM_SHA, 'saveSha256': SAVE_SHA, 'arm9Sha256': MAIN_SHA,
              'compilerSha256': row['compilerSha256'], 'sourceDependencies': [], 'matches': [row],
              'nativeSymbolEntries': entries, 'nativeSymbols': {name: value['address'] for name, value in entries.items()},
              'nativeSymbolModules': {name: value['module'] for name, value in entries.items()},
              'matchedFunctions': 1, 'matchedBytes': 96,
              'oracle': {'cases': oracle['cases'], 'actualReturns': oracle['actualReturns'],
                         'nativeAndRecompiledCalls': oracle['actualReturns'], 'report': report_path,
                         'reportSha256': sha((ROOT / report_path).read_bytes()),
                         'reproductionCommand': command, 'limits': oracle['limits'],
                         'limitations': oracle['limitations']},
              'replayDependencies': [file_identity(path) for path in deps],
              'connectedRoutineReturns': oracle['routineReturns'], 'boundaryOnlyReturns': oracle['boundaryOnlyReturns'],
              'leafControlReturns': oracle['leafControlReturns'], 'nativeEffectSourceCredit': 0,
              'nativeCalleeCodeOrSourceCredit': 0, 'wholeLinkedRebuild': False,
              'registrationPerformedByThisScript': False, 'inputsUnchanged': True,
              'limitations': oracle['limitations']}
    output = ROOT / 'evidence/matches/mechanics-save-20261029-item-effect-wrapper.json'
    output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'matchedFunctions': 1, 'matchedBytes': 96, 'oracleCases': oracle['cases'],
                      'actualReturns': oracle['actualReturns'], 'report': str(output.relative_to(ROOT)),
                      'reportSha256': sha(output.read_bytes())}))


if __name__ == '__main__':
    main()
