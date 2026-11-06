import subprocess
import sys
from project import ROOT, read_json, write_json, sha256
from recovery_registry import verify_sources


def main():
    missing = 'evidence/lanes/parallel-wave20261105/gpi-connect-next/profilecallback/copied-root-canonical-bridge-proof.json'
    qualified = 'evidence/lanes/parallel-wave20261105/gpi-connect-next/profilecallback/qualified-copied-root-canonical-bridge-proof.json'
    ready_name = 'evidence/lanes/parallel-wave20261105/gpi-connect-next/profilecallback-qualified/ready.json'
    capture_name = 'evidence/verification/cohort165-captured-oracle-closure-20261031.json'
    capture = read_json(ROOT / capture_name)
    assert capture['missingRequiredPaths'] == [missing] and not (ROOT / missing).exists()
    assert capture['registrySha256'] == sha256(ROOT / 'recovery.json')
    for name, digest in capture['sourceAndEvidenceHashes'].items():
        assert sha256(ROOT / name) == digest, name
    validation = read_json(ROOT / 'evidence/verification/cohort165-validation-driver.json')
    assert validation['state'] == 'build-and-regression-checks-passed' and len(validation['steps']) == 16
    for step in validation['steps']:
        assert sha256(ROOT / step['log']) == step['logSha256']
        assert step['exitCode'] == 0 or (step['command'] == ['verify_workspace.py']
                and step['exitCode'] == 1 and step['externalApplicationSnapshotDifferences'])
    plan = read_json(ROOT / 'evidence/verification/cohort-2026-10-29-165.json')
    assert not plan['linksPending'] and plan['sourceMatchedFunctions'] == 11093 and plan['sourceLinkedBytes'] == 1124271
    assert sha256(ROOT / 'recovery.json') == plan['sourceRegistrySha256']
    assert sha256(ROOT / 'source-preferences.json') == plan['sourcePreferenceSha256']
    ready = read_json(ROOT / ready_name)
    descriptor_name = 'evidence/lanes/parallel-wave20261105/gpi-connect-next/profilecallback/qualified-canonical-packet.json'
    descriptor = read_json(ROOT / descriptor_name)
    output_name = descriptor['workerReport']
    assert output_name == 'evidence/lanes/parallel-wave20261105/gpi-connect-next/profilecallback/match.json'
    before = {}
    for pin in ready['files']:
        digest = sha256(ROOT / pin['path'])
        assert pin['path'] == output_name or digest == pin['sha256']
        before[pin['path']] = digest
    manifest_pin = ready['frozenInputManifest']
    assert sha256(ROOT / manifest_pin['path']) == manifest_pin['sha256']
    for pin in read_json(ROOT / manifest_pin['path'])['files']:
        assert sha256(ROOT / pin['path']) == pin['sha256']
    proof = read_json(ROOT / qualified)
    assert proof['status'] == 'passed' and proof['functions'] == 4 and proof['bytes'] == 720
    assert proof['objectHashesChanged'] == 4 and proof['immutableExternalInputMutationRejected']
    assert before[qualified] == sha256(ROOT / qualified)
    clone = __import__('pathlib').Path(proof['copiedRoot'])
    assert sha256(clone / descriptor['canonicalReport']) == proof['canonicalReportSha256']
    rows = read_json(clone / descriptor['canonicalReport'])['matches']
    assert len(rows) == 4
    fields = ['program', 'processor', 'module', 'mode', 'address', 'bytes', 'source', 'sourceSha256',
              'sourceDependencies', 'targetSha256', 'compiler', 'compilerSha256', 'compilerFlags',
              'nativeSymbolEntries', 'relocations', 'ordinaryCBytes', 'justifiedAssemblyBytes']
    projection = lambda items: [{field: row[field] for field in fields} for row in items]
    assert projection(rows) == projection(read_json(ROOT / output_name)['matches'])
    for row in rows:
        assert sha256(clone / row['object']) == row['objectSha256']
        assert row['realLink']['exactCallerBytes']
        assert sha256(clone / row['realLink']['linkedElf']) == row['realLink']['linkedElfSha256']
    log_name = 'evidence/lanes/parallel-wave20261105/gpi-connect-next/profilecallback/copied-root.log'
    log = (ROOT / log_name).read_text(encoding='utf-8')
    assert 'FileNotFoundError' in log and 'seed-manifest.json' in log
    archive = 'evidence/attempts/cohort165-missing-historical-copy-record-20261106/verbatim-inputs.json'
    assert not (ROOT / archive).exists()
    files = {}
    for name in [capture_name, 'logs/integration/cohort165-stage-20261101.txt',
                 'logs/integration/cohort165-thin-stage-route-finish-resumption-20261106.txt', log_name]:
        files[name] = dict(sha256=sha256(ROOT / name), text=(ROOT / name).read_text(encoding='utf-8'))
    write_json(ROOT / archive, dict(sourceCredit=0, originalFailurePreserved=True, files=files))
    write_json(ROOT / missing, dict(status='failed-historical-unqualified-copied-root-replay',
        sourceCredit=0, copiedRootCanonicalReplayPassed=False, canonicalReportFresh=False,
        originalAttemptLog=log_name, originalAttemptLogSha256=sha256(ROOT / log_name),
        measuredFailure='The retired unqualified copied root lacked provenance/seed-manifest.json.',
        qualifiedCopyIsSeparate=True, selectedQualifiedReady=ready_name, selectedQualifiedReadySha256=sha256(ROOT / ready_name),
        selectedQualifiedProof=qualified, selectedQualifiedProofSha256=sha256(ROOT / qualified),
        restoredAsFailureRecordOnly=True, newNativeExecutionCredit=0, newFunctionCredit=0, newByteCredit=0,
        generatorSha256=sha256(__file__)))
    import wave20261105_gpi_connect_next_profilecallback_ready as retired
    try:
        retired.ready()
    except ValueError as error:
        assert 'Canonical proof incomplete' in str(error)
    else:
        raise AssertionError('Retired failed-copy readiness was accepted')
    for name, digest in before.items():
        assert sha256(ROOT / name) == digest
    for name, digest in capture['sourceAndEvidenceHashes'].items():
        assert sha256(ROOT / name) == digest, name
    verify_sources()
    receipt = 'evidence/verification/cohort165-historical-copy-record-resumption-20261106.json'
    write_json(ROOT / receipt, dict(passed=True, sourceCredit=0, nativeAcceptanceStillPending=True,
        missingRequiredPath=missing, restoredRecordSha256=sha256(ROOT / missing),
        selectedQualifiedProofUnchanged=True, retiredReadinessStillRejectsFailedCopy=True,
        selectedRuntimePinsUnchanged=len(before), previousCapturedHashesUnchanged=len(capture['sourceAndEvidenceHashes']),
        originalSixteenSharedStagesVerified=True, freshFullCaptureStillRequired=True,
        originalFinisherAndCaptureChecksUnchanged=True, failureArchive=archive, failureArchiveSha256=sha256(ROOT / archive),
        generatorSha256=sha256(__file__)))
    package_name = 'cohort165-parallel-wave20261105-j-package.json'
    package = read_json(ROOT / package_name)
    for name in [__file__.split('\\')[-1], receipt, missing, archive]:
        if name not in package['extra']:
            package['extra'].append(name)
    write_json(ROOT / package_name, package)
    subprocess.run([sys.executable, str(ROOT / 'finish_source_package_v17_20261105.py'), '--cohort', '165',
        '--stage', 'stage_parallel_packet_wave165_v2_20261106.py',
        '--document', 'docs/2026-11-06-parallel-wave-j-acceptance.md', '--label', 'parallel-wave-j'], cwd=ROOT, check=True)


if __name__ == '__main__':
    main()
