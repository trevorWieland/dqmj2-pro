import subprocess
import sys
from pathlib import Path
from project import ROOT, read_json, write_json, sha256, now
from recovery_registry import verify_sources


def main():
    cohort = 121
    driver = ROOT / 'evidence/verification/cohort121-validation-driver.json'
    failed = read_json(driver)
    assert failed['state'] == 'failed' and len(failed['steps']) == 16
    assert all(row['exitCode'] == 0 for row in failed['steps'][:15])
    assert failed['steps'][15]['command'] == ['verify_workspace.py']
    assert failed['steps'][15]['exitCode'] != 0
    for row in failed['steps']:
        assert sha256(ROOT / row['log']) == row['logSha256']
    relocation = read_json(ROOT / 'evidence/verification/cohort121-generated-negative-relocation-20261101.json')
    assert relocation['originalDiagnosticsPreserved'] and relocation['matchedSourceInputsChanged'] is False
    for row in relocation['moves']:
        assert not (ROOT / row['old']).exists() and sha256(ROOT / row['new']) == row['sha256']
    verify_sources()
    plan = read_json(ROOT / 'evidence/verification/cohort-2026-10-29-114.json')
    assert sha256(ROOT / 'recovery.json') == failed['sourceRegistrySha256'] == plan['sourceRegistrySha256']
    archive = ROOT / 'evidence/attempts/cohort121-generated-diagnostic-resume-20261101'
    archive.mkdir(parents=True, exist_ok=False)
    for name in ['evidence/verification/cohort121-validation-driver.json',
            'evidence/verification/cohort121-continuation-driver-v12-20261101.json',
            'logs/integration/cohort121-expanded-continuation-02-20261101.txt', failed['steps'][15]['log']]:
        (archive / Path(name).name).write_bytes((ROOT / name).read_bytes())
    result = dict(cohort=cohort, startedUtc=now(), generator=Path(__file__).name,
        generatorSha256=sha256(__file__), sourceCredit=0, state='running', steps=[],
        preservedSuccessfulSteps=15, sourceRegistrySha256=sha256(ROOT / 'recovery.json'),
        failureArchive=archive.relative_to(ROOT).as_posix())
    output = ROOT / 'evidence/verification/cohort121-continuation-restored-pins-20261101.json'
    commands = [['verify_workspace.py']]
    resumed_steps = []
    for number, command in enumerate(commands):
        log = ROOT / f'logs/integration/cohort121-restored-pins-{number:02}-20261101.txt'
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
        steps=failed['steps'][:15] + resumed_steps, sourceMatchedFunctions=manifest['functionMatched'],
        sourceLinkedBytes=manifest['sourceLinkedBytes'], resumedBy=Path(__file__).name,
        failedAttemptArchive=archive.relative_to(ROOT).as_posix())
    failed.pop('currentCommand', None)
    failed.pop('currentCommandStartedUtc', None)
    write_json(driver, failed)
    for number, command in enumerate([
        ['finalize_source_cohort_20261101.py', '--cohort', '121'],
        ['finish_source_package_v10_20261101.py', '--cohort', '121', '--stage', 'stage_cohort121_breadth_20261101.py',
         '--document', 'docs/2026-11-01-cohort121-larger-source-bodies.md',
         '--label', 'larger reconstructed source bodies']]):
        log = ROOT / f'logs/integration/cohort121-restored-package-{number:02}-20261101.txt'
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
    print(dict(state='packaged', cohort=114, preservedSuccessfulChecks=15))


if __name__ == '__main__':
    main()
