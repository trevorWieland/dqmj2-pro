import subprocess
import sys
from pathlib import Path
from project import ROOT, read_json, write_json, sha256, now
from recovery_registry import verify_sources


def main():
    verify_sources()
    plan = read_json(ROOT / 'evidence/verification/cohort-2026-10-29-114.json')
    assert sha256(ROOT / 'recovery.json') == plan['sourceRegistrySha256']
    manifest = read_json(ROOT / 'manifest.json')
    assert plan['expectedSourceLinkedBytes'] - manifest['sourceLinkedBytes'] == 60
    assert read_json(ROOT / 'evidence/attempts/list-count-validation-name-collision-20261101.json')['restored']
    output = ROOT / 'evidence/verification/cohort114-restored-build-retry-20261101.json'
    result = dict(cohort=114, startedUtc=now(), generator=Path(__file__).name,
        generatorSha256=sha256(__file__), state='running', steps=[],
        sourceCredit=0, stalePriorModuleProvenanceReused=False)
    commands = [['run_source_cohort_20261101.py', '--cohort', '114'],
        ['finalize_source_cohort_20261101.py', '--cohort', '114'],
        ['finish_source_package_v9_20261101.py', '--cohort', '114', '--stage', 'stage_cohort114_package_20261101.py',
         '--document', 'docs/2026-11-01-cohort114-full-word-and-pointer-portability.md',
         '--label', 'full word and pointer portability']]
    for number, command in enumerate(commands):
        result['currentCommand'] = command
        write_json(output, result)
        log = ROOT / f'logs/integration/cohort114-restored-build-retry-{number:02}-20261101.txt'
        with log.open('w', encoding='utf-8') as stream:
            run = subprocess.run([sys.executable, str(ROOT / command[0]), *command[1:]], cwd=ROOT,
                stdout=stream, stderr=subprocess.STDOUT)
        result['steps'].append(dict(command=command, exitCode=run.returncode,
            log=log.relative_to(ROOT).as_posix(), logSha256=sha256(log)))
        if run.returncode:
            result.update(state='failed', finishedUtc=now())
            write_json(output, result)
            raise SystemExit(run.returncode)
    result.update(state='packaged', finishedUtc=now())
    result.pop('currentCommand', None)
    write_json(output, result)
    print(dict(cohort=114, state='packaged'))


if __name__ == '__main__':
    main()
