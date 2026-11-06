import importlib
import subprocess
import sys
from pathlib import Path
from project import ROOT, read_json, write_json, sha256
from recovery_registry import verify_sources


def main():
    lane = 'evidence/lanes/parallel-wave20261105/itcm-reset-next/'
    missing = [lane + 'copied-root-canonical-bridge-proof-v2.json', lane + 'copied-root-canonical-bridge-proof.json']
    capture_name = 'evidence/verification/cohort168-captured-oracle-closure-20261031.json'
    capture = read_json(ROOT / capture_name)
    assert capture['missingRequiredPaths'] == sorted(missing)
    assert all(not (ROOT / name).exists() for name in missing)
    assert capture['registrySha256'] == sha256(ROOT / 'recovery.json')
    for name, digest in capture['sourceAndEvidenceHashes'].items():
        assert sha256(ROOT / name) == digest, name
    driver = read_json(ROOT / 'evidence/verification/cohort168-validation-driver.json')
    assert driver['state'] == 'build-and-regression-checks-passed' and len(driver['steps']) == 16
    for step in driver['steps']:
        assert sha256(ROOT / step['log']) == step['logSha256']
        assert step['exitCode'] == 0 or (step['command'] == ['verify_workspace.py'] and
            step['exitCode'] == 1 and step['externalApplicationSnapshotDifferences'])
    plan = read_json(ROOT / 'evidence/verification/cohort-2026-10-29-168.json')
    assert not plan['linksPending'] and plan['sourceMatchedFunctions'] == 11339 and plan['sourceLinkedBytes'] == 1172627
    assert plan['sourceRegistrySha256'] == sha256(ROOT / 'recovery.json')
    assert plan['sourcePreferenceSha256'] == sha256(ROOT / 'source-preferences.json')
    ready_name = lane + 'ready.json'
    assert sha256(ROOT / ready_name) == '05af2b4591202fd99bc301cc980d1b5b027b3d4a842fb86c8dfc47edfa059bb9'
    ready = read_json(ROOT / ready_name)
    frozen = {pin['path']: pin['sha256'] for pin in ready['files']}
    assert all(sha256(ROOT / name) == digest for name, digest in frozen.items())
    qualified_name = lane + 'copied-root-canonical-bridge-proof-v3.json'
    proof = read_json(ROOT / qualified_name)
    assert proof['status'] == 'passed' and proof['functions'] == 1 and proof['bytes'] == 168
    assert proof['objectHashesChanged'] == 1 and proof['canonicalReportFresh']
    assert proof['immutableExternalInputMutationRejected'] and not proof['originalWorkObjectsCopied']
    clone = Path(proof['copiedRoot'])
    descriptor_name = 'evidence/lanes/parallel-wave20261105/itcm-reset-next/canonical-packet-v3.json'
    descriptor = read_json(ROOT / descriptor_name)
    assert sha256(clone / descriptor['canonicalReport']) == proof['canonicalReportSha256']
    rows = read_json(clone / descriptor['canonicalReport'])['matches']
    assert len(rows) == 1 and rows[0]['sourceSha256'] == '24cc5b73f8257025c0d66f4db8fbc9905bfc78411d9ac26372b07dec67fbd65c'
    assert rows[0]['realLink']['exactCallerBytes'] and rows[0]['targetSha256'] == '144f2b25e4fd6288efed8b924f8ebda234fab22a58e8eb3b42ea3633126ad68c'
    assert sha256(clone / rows[0]['object']) == rows[0]['objectSha256']
    assert sha256(clone / rows[0]['realLink']['linkedElf']) == rows[0]['realLink']['linkedElfSha256']
    logs = [lane + 'copied-root-v2.log', lane + 'copied-root.log']
    for name in logs:
        text = (ROOT / name).read_text(encoding='utf-8')
        assert 'Traceback' in text and 'returned non-zero exit status 1' in text
    archive = 'evidence/attempts/cohort168-missing-historical-itcm-copy-records-20261106/verbatim-inputs.json'
    assert not (ROOT / archive).exists()
    names = [capture_name, 'logs/integration/cohort168-stage-20261101.txt',
        'evidence/verification/cohort168-continuation-driver-v37-20261105.json', *logs]
    write_json(ROOT / archive, dict(sourceCredit=0, originalFailurePreserved=True,
        files=[dict(path=name, sha256=sha256(ROOT / name), text=(ROOT / name).read_text(encoding='utf-8')) for name in names]))
    for name, log in zip(missing, logs):
        write_json(ROOT / name, dict(status='failed-historical-unqualified-copied-root-replay', sourceCredit=0,
            copiedRootCanonicalReplayPassed=False, canonicalReportFresh=False,
            originalAttemptLog=log, originalAttemptLogSha256=sha256(ROOT / log),
            measuredFailure='Retired copied-root producer exited1 during caller compilation/replay; no successful proof was emitted.',
            selectedQualifiedCopyIsSeparate=True, selectedQualifiedReady=ready_name,
            selectedQualifiedReadySha256=sha256(ROOT / ready_name), selectedQualifiedProof=qualified_name,
            selectedQualifiedProofSha256=sha256(ROOT / qualified_name), restoredAsFailureRecordOnly=True,
            newNativeExecutionCredit=0, newFunctionCredit=0, newByteCredit=0, generatorSha256=sha256(__file__)))
    for module_name in ['wave20261106_itcm_reset_next_ready', 'wave20261106_itcm_reset_next_ready_v2']:
        retired = importlib.import_module(module_name)
        try:
            retired.ready()
        except ValueError as error:
            assert 'Canonical proof incomplete' in str(error)
        else:
            raise AssertionError('Retired failed-copy readiness accepted')
    assert all(sha256(ROOT / name) == digest for name, digest in frozen.items())
    assert all(sha256(ROOT / name) == digest for name, digest in capture['sourceAndEvidenceHashes'].items())
    verify_sources()
    receipt = 'evidence/verification/cohort168-historical-itcm-copy-record-resumption-20261106.json'
    write_json(ROOT / receipt, dict(passed=True, sourceCredit=0, nativeAcceptanceStillPending=True,
        restoredFailureRecords=[dict(path=name, sha256=sha256(ROOT / name)) for name in missing],
        selectedQualifiedV3ProofUnchanged=True, retiredReadinessBothRejectFailedCopies=True,
        selectedRuntimePinsUnchanged=len(frozen), previousCapturedHashesUnchanged=len(capture['sourceAndEvidenceHashes']),
        originalSixteenSharedStagesVerified=True, freshFullCaptureStillRequired=True,
        originalFinisherAndCaptureChecksUnchanged=True, failureArchive=archive, generatorSha256=sha256(__file__)))
    package_name = 'cohort168-parallel-wave20261105-m-package.json'
    package = read_json(ROOT / package_name)
    for name in [Path(__file__).name, receipt, archive, *missing]:
        if name not in package['extra']:
            package['extra'].append(name)
    write_json(ROOT / package_name, package)
    subprocess.run([sys.executable, str(ROOT / 'finish_source_package_v21_20261106.py'), '--cohort', '168',
        '--stage', 'stage_parallel_packet_wave168_v2_20261106.py',
        '--document', 'docs/2026-11-06-parallel-wave-m-acceptance.md', '--label', 'parallel-wave-m'], cwd=ROOT, check=True)


if __name__ == '__main__':
    main()
