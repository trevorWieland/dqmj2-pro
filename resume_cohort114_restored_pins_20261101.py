import subprocess
import sys
from pathlib import Path
from project import ROOT, read_json, write_json, sha256, now
from recovery_registry import verify_sources


def main():
    cohort = 114
    driver = ROOT / 'evidence/verification/cohort114-validation-driver.json'
    failed = read_json(driver)
    assert failed['state'] == 'failed' and len(failed['steps']) == 15
    assert all(row['exitCode'] == 0 for row in failed['steps'][:14])
    assert failed['steps'][14]['command'] == ['validate_evidence_ash_cache_20261031.py']
    assert failed['steps'][14]['exitCode'] != 0
    for row in failed['steps']:
        assert sha256(ROOT / row['log']) == row['logSha256']
    failed_text = (ROOT / failed['steps'][14]['log']).read_text(encoding='utf-8')
    assert 'Accepted source changed: match_main_list_count60_20261101.py' in failed_text
    assert read_json(ROOT / 'evidence/attempts/list-count-validation-name-collision-20261101.json')['restored']
    verify_sources()
    plan = read_json(ROOT / 'evidence/verification/cohort-2026-10-29-114.json')
    assert sha256(ROOT / 'recovery.json') == failed['sourceRegistrySha256'] == plan['sourceRegistrySha256']
    archive = ROOT / 'evidence/attempts/cohort114-restored-proof-name-collision-20261101'
    archive.mkdir(parents=True, exist_ok=False)
    for name in ['evidence/verification/cohort114-validation-driver.json',
            'evidence/verification/cohort114-continuation-driver-v10-20261101.json',
            'logs/integration/cohort114-continuation-02-20261101.txt', failed['steps'][14]['log']]:
        (archive / Path(name).name).write_bytes((ROOT / name).read_bytes())
    result = dict(cohort=cohort, startedUtc=now(), generator=Path(__file__).name,
        generatorSha256=sha256(__file__), sourceCredit=0, state='running', steps=[],
        preservedSuccessfulSteps=14, sourceRegistrySha256=sha256(ROOT / 'recovery.json'),
        failureArchive=archive.relative_to(ROOT).as_posix())
    output = ROOT / 'evidence/verification/cohort114-continuation-restored-pins-20261101.json'
    commands = [['validate_evidence_ash_cache_20261031.py'], ['verify_workspace.py']]
    resumed_steps = []
    for number, command in enumerate(commands):
        log = ROOT / f'logs/integration/cohort114-restored-pins-{number:02}-20261101.txt'
        with log.open('w', encoding='utf-8') as stream:
            run = subprocess.run([sys.executable, str(ROOT / command[0]), *command[1:]], cwd=ROOT,
                stdout=stream, stderr=subprocess.STDOUT)
        row = dict(command=command, exitCode=run.returncode,
            log=log.relative_to(ROOT).as_posix(), logSha256=sha256(log))
        if run.returncode and command == ['verify_workspace.py']:
            workspace = read_json(ROOT / 'evidence/verification/workspace.json')
            allowed = workspace['sourcePolicy']['passed'] and workspace['isolation']['baselineAndInputsUnchanged'] is True
            allowed &= workspace['isolation']['auditAvailable'] and not workspace['gitRemotes']
            allowed &= workspace['isolation']['applicationObservedUnchanged'] is False
            row['externalApplicationSnapshotDifferences'] = allowed
        else:
            allowed = run.returncode == 0
        resumed_steps.append(row)
        result['steps'].append(row)
        result['state'] = 'running' if allowed else 'failed'
        write_json(output, result)
        assert allowed, log.read_text(encoding='utf-8')[-4000:]
    manifest = read_json(ROOT / 'manifest.json')
    assert manifest['functionMatched'] == plan['expectedSourceMatchedFunctions']
    assert manifest['sourceLinkedBytes'] == plan['expectedSourceLinkedBytes']
    assert manifest['exactContainerMatchWithScaffolding'] is True and not manifest['rejectedMatchEvidence']
    failed.update(state='build-and-regression-checks-passed', finishedUtc=now(),
        steps=failed['steps'][:14] + resumed_steps, sourceMatchedFunctions=manifest['functionMatched'],
        sourceLinkedBytes=manifest['sourceLinkedBytes'], resumedBy=Path(__file__).name,
        failedAttemptArchive=archive.relative_to(ROOT).as_posix())
    failed.pop('currentCommand', None)
    failed.pop('currentCommandStartedUtc', None)
    write_json(driver, failed)
    for number, command in enumerate([
        ['finalize_source_cohort_20261101.py', '--cohort', '114'],
        ['finish_source_package_v9_20261101.py', '--cohort', '114', '--stage', 'stage_cohort114_package_20261101.py',
         '--document', 'docs/2026-11-01-cohort114-full-word-and-pointer-portability.md',
         '--label', 'full word and pointer portability']]):
        log = ROOT / f'logs/integration/cohort114-restored-package-{number:02}-20261101.txt'
        with log.open('w', encoding='utf-8') as stream:
            run = subprocess.run([sys.executable, str(ROOT / command[0]), *command[1:]], cwd=ROOT,
                stdout=stream, stderr=subprocess.STDOUT)
        result['steps'].append(dict(command=command, exitCode=run.returncode,
            log=log.relative_to(ROOT).as_posix(), logSha256=sha256(log)))
        result['state'] = 'running' if run.returncode == 0 else 'failed'
        write_json(output, result)
        assert run.returncode == 0, log.read_text(encoding='utf-8')[-4000:]
    result.update(state='packaged', finishedUtc=now())
    write_json(output, result)
    print(dict(state='packaged', cohort=114, preservedSuccessfulChecks=14))


if __name__ == '__main__':
    main()
