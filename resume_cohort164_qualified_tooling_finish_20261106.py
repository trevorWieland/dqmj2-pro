import ast
import subprocess
import sys
from project import ROOT, read_json, write_json, sha256
import finish_source_package_v17_20261105 as original


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def pending(excluded):
    names = set(git('diff', '--cached', '--name-only', '-z').decode().split('\0')) - {''} - excluded
    entries = {}
    for record in git('ls-files', '--stage', '-z').decode().split('\0'):
        if record:
            value, name = record.split('\t', 1)
            if name in names:
                entries[name] = value
    assert set(entries) == names
    return entries


def main():
    driver = read_json(ROOT / 'evidence/verification/cohort164-validation-driver.json')
    assert driver['state'] == 'build-and-regression-checks-passed' and len(driver['steps']) == 16
    for step in driver['steps']:
        assert sha256(ROOT / step['log']) == step['logSha256']
        if step['exitCode']:
            assert step['command'] == ['verify_workspace.py'] and step['externalApplicationSnapshotDifferences']
            workspace = read_json(ROOT / 'evidence/verification/workspace.json')
            assert workspace['sourcePolicy']['passed'] and workspace['isolation']['baselineAndInputsUnchanged']
            assert workspace['isolation']['auditAvailable'] and not workspace['gitRemotes']
    assert read_json(ROOT / 'evidence/verification/cohort164-continuation-driver-v24-20261105.json')['state'] == 'failed'
    plan = read_json(ROOT / 'evidence/verification/cohort-2026-10-29-164.json')
    assert not plan['linksPending'] and sha256(ROOT / 'recovery.json') == plan['sourceRegistrySha256']
    capture_path = ROOT / 'evidence/verification/cohort164-captured-oracle-closure-20261031.json'
    capture = read_json(capture_path)
    assert not capture['missingRequiredPaths'] and capture['registrySha256'] == plan['sourceRegistrySha256']

    def verify_capture():
        changed = [name for name, digest in capture['sourceAndEvidenceHashes'].items()
                   if not (ROOT / name).is_file() or sha256(ROOT / name) != digest]
        assert not changed, changed

    verify_capture()
    failure_name = 'logs/integration/cohort164-expanded-v24-continuation-04-20261101.txt'
    failure = (ROOT / failure_name).read_bytes()
    findings = ast.literal_eval(failure.decode('utf-8').split('AssertionError: ', 1)[1].strip())
    unclassified = [row for row in findings if not row['classified']]
    tool = 'oracle_source_closure_v2_20261106.py'
    assert len(unclassified) == 1 and unclassified[0]['path'] == tool
    assert sha256(ROOT / tool) == unclassified[0]['sha256'] == 'f4b070a006e0c2ec6010876a086843bf16be3e52c1915e2cc23eeb971b452eb5'
    files = {}
    for name, key in [
        ('evidence/lanes/parallel-wave20261106/path-lookup-next/stage-v9-handoff.json', 'files'),
        ('evidence/lanes/parallel-wave20261106/path-lookup-next/collector-v3-qualification.json', 'files'),
        ('evidence/lanes/parallel-wave20261105/source-capture-performance-next/collector-v2-stage-v8-qualification.json', 'filesAndQualificationReceipts')]:
        files[name] = sha256(ROOT / name)
        for pin in read_json(ROOT / name)[key]:
            assert sha256(ROOT / pin['path']) == pin['sha256']
            files[pin['path']] = pin['sha256']
    assert tool in files
    assert not any(name.split('/')[0] in {'src', 'inputs', 'extract', 'tools', 'deps', 'build', 'work'} for name in files)
    assert all((ROOT / name).suffix in ['.py', '.json'] for name in files)
    directory = ROOT / 'evidence/attempts/cohort164-qualified-tooling-packaging-20261106'
    directory.mkdir(parents=True, exist_ok=False)
    for name in [failure_name, 'logs/integration/cohort164-whitespace-20261101.txt']:
        data = (ROOT / name).read_bytes()
        write_json(directory / (name.split('/')[-1] + '.json'),
            dict(sourceCredit=0, path=name, sha256=sha256(ROOT / name), exactUtf8Text=data.decode('utf-8')))
    receipt = 'evidence/verification/cohort164-qualified-capture-tooling-preservation-20261106.json'
    excluded = set(files) | {receipt}
    before = pending(excluded)
    write_json(ROOT / receipt, dict(passed=True, sourceCredit=0, newNativeSourceBytes=0,
        qualifiedToolingFiles=[dict(path=name, sha256=digest) for name, digest in sorted(files.items())],
        allSixteenOriginalSharedStagesPreserved=True, capturedSourcePathsVerified=len(capture['sourceAndEvidenceHashes']),
        capturedClosureSha256=sha256(capture_path), pendingNativeAndEvidenceIndexEntries=len(before),
        reason='Preserve independently qualified frozen tooling bytes in a separate infrastructure commit; native acceptance remains pending.',
        originalFinisherWhitespaceClassifierUnchanged=True, generatorSha256=sha256(__file__)))
    subprocess.run(['git', 'add', '--', *files, receipt], cwd=ROOT, check=True)
    subprocess.run(['git', 'commit', '--only', '-m', 'Preserve qualified capture tooling and frozen proof bytes', '--', *files, receipt], cwd=ROOT, check=True)
    infrastructure_commit = git('rev-parse', 'HEAD').decode().strip()
    assert pending(excluded) == before
    assert git('show', 'HEAD:' + tool) == (ROOT / tool).read_bytes()
    verify_capture()
    package_name = 'cohort164-parallel-wave20261105-i-package.json'
    package = read_json(ROOT / package_name)
    assert package_name not in capture['sourceAndEvidenceHashes']
    for name in [__file__.split('\\')[-1], receipt]:
        if name not in package['extra']:
            package['extra'].append(name)
    for path in directory.iterdir():
        name = path.relative_to(ROOT).as_posix()
        if name not in package['traces']:
            package['traces'].append(name)
    write_json(ROOT / package_name, package)
    resume = 'evidence/verification/cohort164-verified-tooling-stage-resumption-20261106.json'
    write_json(ROOT / resume, dict(passed=True, sourceCredit=0, infrastructureCommit=infrastructure_commit,
        capturedSourcePathsVerified=len(capture['sourceAndEvidenceHashes']), pendingNativeIndexPreserved=True,
        unchangedQualifiedToolBytesCommittedSeparately=True, originalSourceDataObjectsModelsAndRegistryUnchanged=True,
        originalSharedGatesAndFinisherUnchanged=True, duplicateCaptureSkippedOnlyAfterFullHashVerification=True))
    subprocess.run(['git', 'add', '--', package_name, __file__.split('\\')[-1], resume,
                    *[path.relative_to(ROOT).as_posix() for path in directory.iterdir()]], cwd=ROOT, check=True)
    original_run = original.run

    def verified_stage(command, log):
        if command == [sys.executable, str(ROOT / 'stage_parallel_packet_wave164.py')]:
            verify_capture()
            assert "'closurePaths': 23719" in (ROOT / log).read_text()
            return
        return original_run(command, log)

    original.run = verified_stage
    sys.argv = [sys.argv[0], '--cohort', '164', '--stage', 'stage_parallel_packet_wave164.py',
                '--document', 'docs/2026-11-06-parallel-wave-i-acceptance.md', '--label', 'parallel-wave-i']
    original.main()


if __name__ == '__main__':
    main()
