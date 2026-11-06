import sys
import subprocess
from project import ROOT, read_json, write_json, sha256
import finish_source_package_v17_20261105 as original


def main():
    cohort = 161
    driver = read_json(ROOT / 'evidence/verification/cohort161-validation-driver.json')
    assert driver['state'] == 'build-and-regression-checks-passed'
    assert len(driver['steps']) == 16
    for row in driver['steps']:
        assert sha256(ROOT / row['log']) == row['logSha256']
        if row['exitCode']:
            assert row['command'] == ['verify_workspace.py'] and row['externalApplicationSnapshotDifferences'] is True
            workspace = read_json(ROOT / 'evidence/verification/workspace.json')
            assert workspace['sourcePolicy']['passed'] and workspace['isolation']['baselineAndInputsUnchanged'] is True
            assert workspace['isolation']['auditAvailable'] and not workspace['gitRemotes']
            assert workspace['isolation']['applicationObservedUnchanged'] is False
    assert not read_json(ROOT / 'evidence/verification/cohort-2026-10-29-161.json')['linksPending']
    run_original = original.run
    def preserved_stage(command, log):
        if len(command) != 2 or command[1] != str(ROOT / 'stage_parallel_packet_wave161.py'):
            return run_original(command, log)
        closure_path = ROOT / 'evidence/verification/cohort161-captured-oracle-closure-20261031.json'
        closure = read_json(closure_path)
        assert not closure['missingRequiredPaths']
        source = 'src/runtime/parallel_wave20261105/browser-query-next/query-start/020a58dc/match.c'
        archive_name = 'evidence/attempts/cohort161-headerless-c-source-20261105/original-source-text.json'
        archive = read_json(ROOT / archive_name)
        assert archive['sourceCredit'] == 0 and archive['path'] == source
        assert archive['sha256'] == 'f66aa0954800b668127bb579d6b7df155c478908e446cdd2988ee3bd2e190780'
        verbatim = (ROOT / source).read_bytes()
        assert verbatim.decode('utf-8').replace('\r\n', '\n') == archive['exactUtf8Text']
        assert sha256(ROOT / source) == archive['sha256'] and source not in closure['sourceAndEvidenceHashes']
        verbatim_archive = 'evidence/attempts/cohort161-headerless-c-source-20261105/original-source-verbatim-20261106.json'
        write_json(ROOT / verbatim_archive, dict(sourceCredit=0, path=source, sha256=sha256(ROOT / source),
            exactUtf8Text=verbatim.decode('utf-8'), originalNormalizedTextArchive=archive_name,
            originalNormalizedArchiveUnchanged=True, role='Unselected failed-attempt authored C; not accepted reconstruction'))
        assert read_json(ROOT / verbatim_archive)['exactUtf8Text'].encode('utf-8') == verbatim
        registered = {name for batch in read_json(ROOT / 'recovery.json')['batches'] for name in batch['sourceHashes']}
        assert source not in registered
        changed = [name for name, expected in closure['sourceAndEvidenceHashes'].items()
                   if not (ROOT / name).is_file() or sha256(ROOT / name) != expected]
        assert not changed, changed
        original_stage_log = ROOT / log
        assert "'closurePaths': 22541" in original_stage_log.read_text()
        subprocess.run(['git', 'restore', '--staged', '--source=HEAD', '--', source], cwd=ROOT, check=True)
        assert (ROOT / source).read_bytes() == verbatim
        assert archive_name in subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT, text=True).splitlines()
        receipt_name = 'evidence/verification/cohort161-archived-unselected-source-stage-resumption-20261106.json'
        write_json(ROOT / receipt_name, dict(passed=True, sourceCredit=0, preservedOriginalSharedStages=16,
            existingCapturedSourcePathsVerified=len(closure['sourceAndEvidenceHashes']), capturedClosureSha256=sha256(closure_path),
            unstagedUnselectedSource=source, originalSourceBytesPreserved=True, sourceSha256=sha256(ROOT / source),
            exactCommittedArchive=verbatim_archive, archiveSha256=sha256(ROOT / verbatim_archive),
            originalFinisherAndWhitespaceGuardsUnchanged=True, duplicateCaptureSkippedAfterFullHashVerification=True,
            generatorSha256=sha256(__file__)))
        subprocess.run(['git', 'add', '--', receipt_name, verbatim_archive, 'resume_cohort161_captured_finish_20261106.py'], cwd=ROOT, check=True)
    original.run = preserved_stage
    sys.argv = [sys.argv[0], '--cohort', str(cohort), '--stage', 'stage_parallel_packet_wave161.py',
                '--document', 'docs/2026-11-05-parallel-wave-f-acceptance.md',
                '--label', 'disjoint GP UDP negotiation and socket C']
    original.main()


if __name__ == '__main__':
    main()
