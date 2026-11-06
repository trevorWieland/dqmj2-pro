import argparse
from pathlib import Path
import subprocess
import sys
from project import ROOT, read_json, write_json, sha256, now, configuration
from recovery_registry import verify_sources


def validate(failed, relocation):
    steps = failed['steps']
    if failed['state'] != 'failed' or len(steps) != 16:
        raise ValueError('Only the completed final workspace failure can resume')
    if any(row['exitCode'] != 0 for row in steps[:15]):
        raise ValueError('An earlier failed acceptance gate must be rerun')
    if steps[-1]['command'] != ['verify_workspace.py'] or steps[-1]['exitCode'] == 0:
        raise ValueError('Last gate is not a failed workspace verification')
    if not relocation['originalDiagnosticsPreserved'] or relocation['matchedSourceInputsChanged'] is not False:
        raise ValueError('Resume requires preserved generated diagnostics and unchanged matching inputs')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cohort', type=int, required=True)
    parser.add_argument('--relocation', required=True)
    parser.add_argument('--failure-archive', required=True)
    parser.add_argument('--stage', required=True)
    parser.add_argument('--document', required=True)
    parser.add_argument('--label', required=True)
    options = parser.parse_args()
    cohort = options.cohort
    driver_path = ROOT / f'evidence/verification/cohort{cohort}-validation-driver.json'
    failed = read_json(driver_path)
    relocation = read_json(ROOT / options.relocation)
    validate(failed, relocation)
    for row in failed['steps']:
        if sha256(ROOT / row['log']) != row['logSha256']:
            raise ValueError('Previously completed gate log changed')
    archive = read_json(ROOT / options.failure_archive / 'receipt.json')
    original = next(row for row in archive['files'] if row['original'] == driver_path.relative_to(ROOT).as_posix())
    if original['originalSha256'] != sha256(driver_path) or sha256(ROOT / original['archived']) != original['archivedSha256']:
        raise ValueError('Failed workspace driver was not preserved exactly')
    workspace_record = next(row for row in archive['files'] if row['original'] == 'evidence/verification/workspace.json')
    if sha256(ROOT / workspace_record['archived']) != workspace_record['archivedSha256']:
        raise ValueError('Original workspace failure archive changed')
    original_workspace = read_json(ROOT / workspace_record['archived'])
    moved = {row['old'] for row in relocation['moves']}
    if (original_workspace['sourcePolicy']['passed'] or not original_workspace['isolation']['baselineAndInputsUnchanged']
        or not all(row['path'] in moved for row in original_workspace['sourcePolicy']['failures'])):
        raise ValueError('Relocation does not cover the preserved generated-source policy failure')
    for row in relocation['moves']:
        if (ROOT / row['old']).exists() or sha256(ROOT / row['new']) != row['sha256']:
            raise ValueError('Generated research relocation is not byte preserving')
    verify_sources()
    plan = read_json(ROOT / f'evidence/verification/cohort-2026-10-29-{cohort}.json')
    registry = sha256(ROOT / 'recovery.json')
    if registry != failed['sourceRegistrySha256'] or registry != plan['sourceRegistrySha256']:
        raise ValueError('Native replay scope changed after completed gates')
    log = ROOT / f'logs/integration/cohort{cohort}-workspace-relocation-resume.txt'
    with log.open('w', encoding='utf-8') as stream:
        run = subprocess.run([sys.executable, str(ROOT / 'verify_workspace.py')], cwd=ROOT,
            stdout=stream, stderr=subprocess.STDOUT)
    workspace = read_json(ROOT / 'evidence/verification/workspace.json')
    allowed = (workspace['sourcePolicy']['passed'] and workspace['isolation']['baselineAndInputsUnchanged'] is True
        and workspace['isolation']['auditAvailable'] and not workspace['gitRemotes']
        and workspace['isolation']['applicationObservedUnchanged'] is False)
    row = dict(command=['verify_workspace.py'], exitCode=run.returncode,
        log=log.relative_to(ROOT).as_posix(), logSha256=sha256(log), externalApplicationSnapshotDifferences=allowed)
    receipt_path = ROOT / f'evidence/verification/cohort{cohort}-workspace-relocation-resume-20261101.json'
    result = dict(cohort=cohort, sourceCredit=0, preservedSuccessfulGates=15,
        failureArchive=options.failure_archive, relocation=options.relocation,
        generator=Path(__file__).name, generatorSha256=sha256(__file__), resumedWorkspaceGate=row,
        sourceRegistrySha256=registry, passed=run.returncode == 0 or allowed)
    write_json(receipt_path, result)
    if not result['passed']:
        raise SystemExit(run.returncode or 1)
    verify_sources()
    manifest = read_json(ROOT / 'manifest.json')
    if (sha256(ROOT / 'recovery.json') != registry or manifest['functionMatched'] != plan['expectedSourceMatchedFunctions']
        or manifest['sourceLinkedBytes'] != plan['expectedSourceLinkedBytes']
        or not manifest['exactContainerMatchWithScaffolding'] or manifest['rejectedMatchEvidence']
        or sha256(ROOT / 'build/exact-layout.nds') != configuration()['romSha256']):
        raise ValueError('Source scope or exact build changed during workspace repair')
    failed.update(state='build-and-regression-checks-passed', steps=failed['steps'][:15] + [row],
        finishedUtc=now(), sourceMatchedFunctions=manifest['functionMatched'], sourceLinkedBytes=manifest['sourceLinkedBytes'],
        resumedBy=Path(__file__).name, failedAttemptArchive=options.failure_archive,
        workspaceResumeReceipt=receipt_path.relative_to(ROOT).as_posix())
    failed.pop('currentCommand', None)
    failed.pop('currentCommandStartedUtc', None)
    write_json(driver_path, failed)
    commands = [['finalize_source_cohort_20261101.py', '--cohort', str(cohort)],
        ['finish_source_package_v14_20261102.py', '--cohort', str(cohort), '--stage', options.stage,
            '--document', options.document, '--label', options.label]]
    for command in commands:
        subprocess.run([sys.executable, str(ROOT / command[0]), *command[1:]], cwd=ROOT, check=True)
    print(dict(cohort=cohort, packaged=True, preservedSuccessfulGates=15))


if __name__ == '__main__':
    main()
