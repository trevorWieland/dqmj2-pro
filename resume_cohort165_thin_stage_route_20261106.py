import subprocess
import sys
from project import ROOT, read_json, write_json, sha256
from recovery_registry import verify_sources


def main():
    original = 'evidence/verification/cohort165-continuation-driver-v28-20261105.json'
    driver = read_json(ROOT / original)
    assert driver['state'] == 'failed' and len(driver['steps']) == 5
    assert all(s['exitCode'] == 0 for s in driver['steps'][:4])
    assert driver['steps'][-1]['command'][0] == 'finish_source_package_v17_20261105.py'
    assert driver['steps'][-1]['exitCode'] == 1
    for step in driver['steps']:
        assert sha256(ROOT / step['log']) == step['logSha256']
    validation_name = 'evidence/verification/cohort165-validation-driver.json'
    validation = read_json(ROOT / validation_name)
    assert validation['state'] == 'build-and-regression-checks-passed'
    assert len(validation['steps']) == 16
    for step in validation['steps']:
        assert sha256(ROOT / step['log']) == step['logSha256']
        assert step['exitCode'] == 0 or (step['command'] == ['verify_workspace.py']
                and step['exitCode'] == 1 and step['externalApplicationSnapshotDifferences'])
    workspace = read_json(ROOT / 'evidence/verification/workspace.json')
    assert workspace['sourcePolicy']['passed'] and workspace['isolation']['baselineAndInputsUnchanged']
    assert workspace['isolation']['auditAvailable'] and not workspace['gitRemotes']
    plan = read_json(ROOT / 'evidence/verification/cohort-2026-10-29-165.json')
    assert not plan['linksPending'] and plan['sourceMatchedFunctions'] == plan['expectedSourceMatchedFunctions'] == 11093
    assert plan['sourceLinkedBytes'] == plan['expectedSourceLinkedBytes'] == 1124271
    assert sha256(ROOT / 'recovery.json') == plan['sourceRegistrySha256']
    assert sha256(ROOT / 'source-preferences.json') == plan['sourcePreferenceSha256']
    manifest = read_json(ROOT / 'manifest.json')
    assert manifest['functionMatched'] == 11093 and manifest['sourceLinkedBytes'] == 1124271
    assert manifest['exactContainerMatchWithScaffolding'] and not manifest['rejectedMatchEvidence']
    assert not (ROOT / 'evidence/verification/cohort165-captured-oracle-closure-20261031.json').exists()
    stage_log = (ROOT / 'logs/integration/cohort165-stage-20261101.txt').read_text(encoding='utf-8')
    assert 'FileNotFoundError' in stage_log and 'cohort165-parallel-wave20261105-i-package.json' in stage_log
    archive_name = 'evidence/attempts/cohort165-thin-stage-route-failure-20261106/verbatim-inputs.json'
    archive = read_json(ROOT / archive_name)
    for name in [original, driver['steps'][-1]['log'], 'logs/integration/cohort165-stage-20261101.txt']:
        assert archive['files'][name]['sha256'] == sha256(ROOT / name)
    correction_name = 'evidence/verification/cohort165-thin-stage-route-correction-20261106.json'
    correction = read_json(ROOT / correction_name)
    stage = correction['correctedWrapper']
    assert correction['passed'] and stage == 'stage_parallel_packet_wave165_v2_20261106.py'
    assert sha256(ROOT / stage) == correction['correctedWrapperSha256']
    verify_sources()
    receipt = 'evidence/verification/cohort165-verified-thin-stage-resumption-20261106.json'
    write_json(ROOT / receipt, dict(passed=True, sourceCredit=0, nativeAcceptanceStillPending=True,
        allSixteenSharedStageLogHashesVerified=True, sourceRegistrySha256=plan['sourceRegistrySha256'],
        sourcePreferenceSha256=plan['sourcePreferenceSha256'], sourceFunctions=11093, sourceBytes=1124271,
        validation=validation_name, validationSha256=sha256(ROOT / validation_name),
        originalFailedDriver=original, originalFailedDriverSha256=sha256(ROOT / original),
        correction=correction_name, correctionSha256=sha256(ROOT / correction_name),
        originalFailureArchive=archive_name, originalFailureArchiveSha256=sha256(ROOT / archive_name),
        noCaptureOrNativeStageSkipped=True, unchangedOriginalFinisher='finish_source_package_v17_20261105.py',
        unchangedOriginalFinisherSha256=sha256(ROOT / 'finish_source_package_v17_20261105.py'),
        generatorSha256=sha256(__file__)))
    package_name = 'cohort165-parallel-wave20261105-j-package.json'
    package = read_json(ROOT / package_name)
    for name in [__file__.split('\\')[-1], receipt, original]:
        if name not in package['extra']:
            package['extra'].append(name)
    write_json(ROOT / package_name, package)
    command = [sys.executable, str(ROOT / 'finish_source_package_v17_20261105.py'), '--cohort', '165',
               '--stage', stage, '--document', 'docs/2026-11-06-parallel-wave-j-acceptance.md',
               '--label', 'parallel-wave-j']
    subprocess.run(command, cwd=ROOT, check=True)


if __name__ == '__main__':
    main()
