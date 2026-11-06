import subprocess
import sys
from project import ROOT, read_json, write_json, sha256
import finish_source_package_v17_20261105 as original


def main():
    driver = read_json(ROOT / 'evidence/verification/cohort163-validation-driver.json')
    assert driver['state'] == 'build-and-regression-checks-passed' and len(driver['steps']) == 16
    for step in driver['steps']:
        assert sha256(ROOT / step['log']) == step['logSha256']
        if step['exitCode']:
            assert step['command'] == ['verify_workspace.py'] and step['externalApplicationSnapshotDifferences'] is True
            workspace = read_json(ROOT / 'evidence/verification/workspace.json')
            assert workspace['sourcePolicy']['passed'] and workspace['isolation']['baselineAndInputsUnchanged'] is True
            assert workspace['isolation']['auditAvailable'] and not workspace['gitRemotes']
            assert workspace['isolation']['applicationObservedUnchanged'] is False
    assert read_json(ROOT / 'evidence/verification/cohort163-continuation-driver-v23-20261105.json')['state'] == 'failed'
    plan = read_json(ROOT / 'evidence/verification/cohort-2026-10-29-163.json')
    assert not plan['linksPending'] and sha256(ROOT / 'recovery.json') == plan['sourceRegistrySha256']
    original_run = original.run

    def verified_stage(command, log):
        if len(command) != 2 or command[1] != str(ROOT / 'stage_parallel_packet_wave163.py'):
            return original_run(command, log)
        capture_path = ROOT / 'evidence/verification/cohort163-captured-oracle-closure-20261031.json'
        capture = read_json(capture_path)
        assert not capture['missingRequiredPaths'] and capture['registrySha256'] == plan['sourceRegistrySha256']
        changed = [path for path, expected in capture['sourceAndEvidenceHashes'].items()
                   if not (ROOT / path).is_file() or sha256(ROOT / path) != expected]
        assert not changed, changed
        raw_name = 'evidence/attempts/cohort162-missing-arm7-summary-bindings-20261106/logs__integration__cohort162-validation-03.txt'
        expected = '2bcdb8e3b92f942f9c8d0bd6be41a5419d27feecbab70b7f6eca973177e7642f'
        assert sha256(ROOT / raw_name) == expected
        assert raw_name not in capture['sourceAndEvidenceHashes']
        assert raw_name not in {path for batch in read_json(ROOT / 'recovery.json')['batches'] for path in batch['sourceHashes']}
        assert "'closurePaths': 23519" in (ROOT / log).read_text()
        directory = ROOT / 'evidence/attempts/cohort163-verbatim-diagnostic-packaging-20261106'
        directory.mkdir(parents=True, exist_ok=False)
        archive_name = (directory / 'original-log-verbatim.json').relative_to(ROOT).as_posix()
        raw = (ROOT / raw_name).read_bytes()
        write_json(ROOT / archive_name, dict(sourceCredit=0, path=raw_name, sha256=expected,
            exactUtf8Text=raw.decode('utf-8'), role='Verbatim original failed ARM7 link diagnostic; no source or oracle input'))
        assert read_json(ROOT / archive_name)['exactUtf8Text'].encode('utf-8') == raw
        for name in ['logs/integration/cohort163-expanded-v23-continuation-04-20261101.txt',
                     'logs/integration/cohort163-whitespace-20261101.txt']:
            data = (ROOT / name).read_bytes()
            write_json(directory / (name.split('/')[-1] + '.json'),
                       dict(sourceCredit=0, path=name, sha256=sha256(ROOT / name), exactUtf8Text=data.decode('utf-8')))
        package_name = 'cohort163-parallel-wave20261105-h-package.json'
        config_name = 'provenance/parallel-wave20261105-h-packets.json'
        for name in [package_name, config_name]:
            assert name not in capture['sourceAndEvidenceHashes']
            (directory / name.split('/')[-1]).write_bytes((ROOT / name).read_bytes())
        package = read_json(ROOT / package_name)
        assert raw_name in package['traces']
        package['traces'] = [archive_name if name == raw_name else name for name in package['traces']]
        config = read_json(ROOT / config_name)
        config['opaqueMetadata'] = [archive_name if name == raw_name else name for name in config['opaqueMetadata']]
        receipt_name = 'evidence/verification/cohort163-archived-failure-log-stage-resumption-20261106.json'
        for name in [receipt_name, 'resume_cohort163_captured_finish_20261106.py']:
            if name not in package['extra']:
                package['extra'].append(name)
        write_json(ROOT / package_name, package)
        write_json(ROOT / config_name, config)
        subprocess.run(['git', 'restore', '--staged', '--source=HEAD', '--', raw_name], cwd=ROOT, check=True)
        assert (ROOT / raw_name).read_bytes() == raw
        write_json(ROOT / receipt_name, dict(passed=True, sourceCredit=0, preservedOriginalSharedStages=16,
            existingCapturedSourcePathsVerified=len(capture['sourceAndEvidenceHashes']), capturedClosureSha256=sha256(capture_path),
            originalDiagnosticBytesPreserved=True, originalDiagnostic=raw_name, originalDiagnosticSha256=expected,
            exactCommittedArchive=archive_name, archiveSha256=sha256(ROOT / archive_name),
            sourceObjectsModelsRegistryAndCapturedInputsUnchanged=True,
            packageTraceRedirectedToLosslessJsonArchive=True, originalFinisherAndWhitespaceGuardsUnchanged=True,
            duplicateCaptureSkippedAfterFullHashVerification=True, generatorSha256=sha256(__file__)))
        files = [path.relative_to(ROOT).as_posix() for path in directory.iterdir()]
        subprocess.run(['git', 'add', '--', *files, receipt_name, package_name, config_name,
                        'resume_cohort163_captured_finish_20261106.py'], cwd=ROOT, check=True)
    original.run = verified_stage
    sys.argv = [sys.argv[0], '--cohort', '163', '--stage', 'stage_parallel_packet_wave163.py',
                '--document', 'docs/2026-11-06-parallel-wave-h-acceptance.md',
                '--label', 'parallel-wave-h']
    original.main()


if __name__ == '__main__':
    main()
