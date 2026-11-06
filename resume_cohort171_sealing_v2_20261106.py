import subprocess
import sys
from project import ROOT, read_json, write_json, sha256, now


def main():
    failed_resume = read_json(ROOT / 'evidence/verification/cohort171-sealing-resume-v1-20261106.json')
    assert failed_resume['state'] == 'failed' and failed_resume['exitCode'] == 1
    assert sha256(ROOT / failed_resume['log']) == failed_resume['logSha256']
    previous_name = 'evidence/verification/cohort171-continuation-driver-v41-20261105.json'
    previous = read_json(ROOT / previous_name)
    assert previous['state'] == 'failed' and len(previous['steps']) == 5
    assert all(s['exitCode'] == 0 for s in previous['steps'][:4]) and previous['steps'][-1]['exitCode'] == 1
    assert previous['steps'][-1]['command'][0] == 'finish_source_package_v24_20261106.py'
    for step in previous['steps']:
        assert sha256(ROOT / step['log']) == step['logSha256']
    driver = read_json(ROOT / 'evidence/verification/cohort171-validation-driver.json')
    assert driver['state'] == 'build-and-regression-checks-passed' and len(driver['steps']) == 16
    for step in driver['steps']:
        assert step['exitCode'] == 0 or step.get('externalApplicationSnapshotDifferences') is True
        assert sha256(ROOT / step['log']) == step['logSha256']
    plan = read_json(ROOT / 'evidence/verification/cohort-2026-10-29-171.json')
    assert not plan['linksPending'] and plan['newSourceFunctions'] == 24 and plan['newSourceBytes'] == 8994
    assert sha256(ROOT / 'recovery.json') == plan['sourceRegistrySha256']
    assert sha256(ROOT / 'source-preferences.json') == plan['sourcePreferenceSha256']
    proof = read_json(ROOT / 'evidence/verification/cohort171-archived-diagnostic-classification-v2-20261106.json')
    assert proof['passed'] and proof['rejectedScopeControls'] == 7
    assert sha256(ROOT / proof['newFinisher']) == proof['newFinisherSha256']
    output = ROOT / 'evidence/verification/cohort171-sealing-resume-v2-20261106.json'
    assert not output.exists()
    command = ['finish_source_package_v27_20261106.py', '--cohort', '171', '--stage',
        'stage_parallel_packet_wave171_v2_20261106.py', '--document',
        'docs/2026-11-06-parallel-wave-p-acceptance.md', '--label', 'parallel-wave-p']
    result = dict(state='running', sourceCredit=0, startedUtc=now(), previousTerminalFailedDriver=previous_name,
        previousDriverSha256=sha256(ROOT / previous_name), originalSixteenSharedStagesCompleted=True,
        completedPreparationPublicationValidationFinalizationNotRepeated=True,
        originalPackagingStageAndBothCommittedInputAuditsWillRun=True, command=command)
    write_json(output, result)
    log = ROOT / 'logs/integration/cohort171-sealing-resume-v2-20261106.txt'
    with log.open('w', encoding='utf-8') as stream:
        run = subprocess.run([sys.executable, str(ROOT / command[0]), *command[1:]], cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT)
    result.update(state='packaged' if run.returncode == 0 else 'failed', finishedUtc=now(), exitCode=run.returncode,
        log=log.relative_to(ROOT).as_posix(), logSha256=sha256(log))
    write_json(output, result)
    if run.returncode:
        raise SystemExit(run.returncode)
    receipt = 'evidence/verification/cohort171-expanded-source-closure-20261101.json'
    assert read_json(ROOT / receipt)['passed']
    assert subprocess.check_output(['git', 'show', 'HEAD:' + receipt], cwd=ROOT) == (ROOT / receipt).read_bytes()
    subprocess.run([sys.executable, str(ROOT / 'export_reconstruction_atlas_data_v2_20261106.py'),
        '--revision', 'HEAD', '--pending', 'cohort172-parallel-wave20261105-q-specification.json',
        '--pending', 'cohort173-parallel-wave20261105-r-specification.json'], cwd=ROOT, check=True)
    result.update(committedClosureVerified=True, acceptedAtlasRefreshed=True)
    write_json(output, result)


if __name__ == '__main__':
    main()
