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
    parser.add_argument('--member-source', default='src/mechanics_save/20261029_skill_entry_member.c')
    parser.add_argument('--transition-source', default='src/mechanics_save/20261029_skill_transition_match.c')
    args = parser.parse_args()
    import unicorn
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise AssertionError('Pinned Python3.13.5 and Unicorn2.1.4 are required')
    verify_inputs()
    script = 'evidence/application/skill_dependency_fixtures_20261029.py'
    command = [sys.executable, str(ROOT / script), '--member-source', args.member_source,
               '--transition-source', args.transition_source]
    process = subprocess.run(command, capture_output=True, text=True, timeout=180)
    if process.returncode:
        raise AssertionError(process.stdout + process.stderr)
    report_path = 'evidence/application/skill-dependency-fixtures-20261029.json'
    oracle = json.loads((ROOT / report_path).read_text())
    rows, entries, cache = [], {}, {}
    for source in oracle['sources']:
        row = dict(source)
        row.pop('sourceCredit', None)
        row.pop('registered', None)
        if not row['exactByteEqual'] or row['compiledBytes'] != row['bytes']:
            raise AssertionError('Complete skill source did not match')
        row.update(row['realLinkSnapshot'])
        row.update({'outputSha256': row['linkedBinarySha256'], 'linked': False, 'sourceDependencies': [],
                    'compilerPath': 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe',
                    'oracle': {'supported': True, 'cases': oracle['cases'], 'actualReturns': oracle['actualReturns'],
                               'report': report_path, 'reportSha256': sha((ROOT / report_path).read_bytes()),
                               'limits': oracle['limits'], 'limitations': oracle['limitations']}})
        if not dependencies_current(row):
            raise AssertionError('Skill source closure is not current')
        for path_key, hash_key in [('source', 'sourceSha256'), ('object', 'objectSha256'),
                                  ('isolatedCallerBinary', 'isolatedCallerBinarySha256'),
                                  ('isolatedCallerLinkValidation', 'isolatedCallerLinkValidationSha256')]:
            if sha((ROOT / row[path_key]).read_bytes()) != row[hash_key]:
                raise AssertionError('Skill source/object/link identity changed')
        for relocation in row['relocations']:
            entries[relocation['symbol']] = native_entry(relocation['targetModule'], int(relocation['target'], 0), cache)
        own = native_entry('main', int(row['address'], 0), cache)
        if row['nativeAlias'] != own['nativeAlias']:
            raise AssertionError('Own alias differs from measured native function')
        entries[row['name']] = own
        rows.append(row)
    deps = [script, 'evidence/application/skill_entry_member_build_20261029.py',
            'evidence/application/skill_transition_build_20261029.py',
            'evidence/application/allocation_parent_fixtures_20261029.py',
            'evidence/application/allocation_parent_build_20261029.py',
            'evidence/application/preparation_machine_20261029.py',
            'evidence/application/preparation_fixtures_20261029.py', 'preparation_build_20261029.py',
            'match_mechanics_save_20261029_record33.py', 'match_mechanics_save_20261029_skill_dependencies.py',
            'link_runtime_unit.py', 'save_link_snapshots.py', 'source_dependencies.py', oracle['parentReference']]
    verify_inputs()
    report = {'schemaVersion': 1, 'romSha256': ROM_SHA, 'saveSha256': SAVE_SHA, 'arm9Sha256': MAIN_SHA,
              'compilerSha256': rows[0]['compilerSha256'], 'sourceDependencies': [], 'matches': rows,
              'nativeSymbolEntries': entries, 'nativeSymbols': {name: value['address'] for name, value in entries.items()},
              'nativeSymbolModules': {name: value['module'] for name, value in entries.items()},
              'matchedFunctions': len(rows), 'matchedBytes': sum(row['bytes'] for row in rows),
              'oracle': {'cases': oracle['cases'], 'actualReturns': oracle['actualReturns'],
                         'report': report_path, 'reportSha256': sha((ROOT / report_path).read_bytes()),
                         'reproductionCommand': command, 'limits': oracle['limits'], 'limitations': oracle['limitations']},
              'directActualReturns': oracle['directActualReturns'], 'connectedActualReturns': oracle['connectedActualReturns'],
              'nestedConnectedHelperReturns': oracle['nestedConnectedHelperReturns'],
              'replayDependencies': [file_identity(path) for path in deps], 'nativeCalleeCodeOrSourceCredit': 0,
              'reusedSourceCredit': 0, 'wholeLinkedRebuild': False, 'registrationPerformedByThisScript': False,
              'inputsUnchanged': True, 'limitations': oracle['limitations']}
    output = ROOT / 'evidence/matches/mechanics-save-20261029-skill-dependencies.json'
    output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'matchedFunctions': len(rows), 'matchedBytes': report['matchedBytes'],
                      'oracleCases': oracle['cases'], 'actualReturns': oracle['actualReturns'],
                      'report': str(output.relative_to(ROOT)), 'reportSha256': sha(output.read_bytes())}))


if __name__ == '__main__':
    main()
