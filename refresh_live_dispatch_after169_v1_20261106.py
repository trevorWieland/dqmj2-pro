import subprocess
import sys
import runpy
from unittest.mock import patch
import project
from pathlib import Path
from project import ROOT, read_json, write_json, sha256


def main():
    driver = read_json(ROOT / 'evidence/verification/cohort169-continuation-driver-v39-20261105.json')
    assert driver['state'] == 'packaged' and driver.get('acceptedAtlasRefreshed')
    closure_name = 'evidence/verification/cohort169-expanded-source-closure-20261101.json'
    closure = read_json(ROOT / closure_name); assert closure['passed']
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    assert subprocess.check_output(['git', 'show', revision + ':' + closure_name], cwd=ROOT) == (ROOT / closure_name).read_bytes()
    name = 'evidence/lanes/parallel-wave20261102/dispatch.json'
    pins = read_json(ROOT / 'evidence/verification/cohort169-captured-oracle-closure-20261031.json')['sourceAndEvidenceHashes']
    assert sha256(ROOT / name) == pins[name]
    frozen_board_sha = sha256(ROOT / name)
    live_name = 'work/parallel-wave20261102/dispatch-live.json'
    board = read_json(ROOT / name)
    archive = 'evidence/attempts/closed169-live-dispatch-refresh-20261106/verbatim-dispatch.json'
    if (ROOT / archive).exists():
        assert read_json(ROOT / archive)['sha256'] == frozen_board_sha
    else:
        write_json(ROOT / archive, dict(sourceCredit=0, path=name, sha256=sha256(ROOT / name),
            verbatimUtf8=(ROOT / name).read_bytes().decode('utf-8')))
    current = {}
    for lane in ['ov006-md5-helper-next', 'auth-core-next', 'g2d-canvas-next', 'arm7-wm-residual-next']:
        folder = f'evidence/lanes/parallel-wave20261106/{lane}'
        admission_name = folder + '/coordinator-admission.json'; admission = read_json(ROOT / admission_name)
        assert admission['passed'] and admission['sourceCredit'] == 0
        claim_name = admission['claim']; assert sha256(ROOT / claim_name) == admission['claimSha256']
        claim = read_json(ROOT / claim_name); assert claim['status'] == 'coordinator-admitted-source-scope-no-credit'
        matches = [row for row in board['active'] if row['id'] == lane]
        assert len(matches) <= 1
        if matches:
            assert matches[0]['claim'] == claim_name
        else:
            board['active'].append(dict(id=lane, owner=claim['owner'], state='admitted-source-and-investigation',
                claim=claim_name, sourceRoot=claim['exclusiveSourceRoot'],
                nativeOpportunityBytes=sum(row['bytes'] for row in claim['claimedFunctions']), handedOffReports=[]))
        current[lane] = dict(id=lane, owner=claim['owner'], claim=claim_name, claimSha256=sha256(ROOT / claim_name))
    board['currentClaims'] = [current[lane] for lane in ['g2d-canvas-next', 'arm7-wm-residual-next', 'auth-core-next']]
    for row in board['active']:
        if row['id'] in ['auth-resume-next', 'ov006-crypto-utility-next']:
            row['state'] = 'frozen-checkpoint-residuals-reserved'
    board['acceptedDataClaims169'] = [dict(row, state='accepted169') for row in board.get('currentDataClaims', [])]
    board['currentDataClaims'] = []
    plan = read_json(ROOT / 'evidence/verification/cohort-2026-10-29-169.json')
    following = read_json(ROOT / 'cohort170-parallel-wave20261105-o-specification.json')
    board['currentExecution'] = dict(acceptedCohort=169, acceptedFunctions=plan['sourceMatchedFunctions'],
        acceptedBytes=plan['sourceLinkedBytes'], closedRevision=revision, sourceCommit=closure['sourceCommit'],
        nextCohort=170, nextFunctions=len(following['expectedAdditions']),
        nextBytes=sum(row['bytes'] for row in following['expectedAdditions']),
        sourceAndInvestigationWorkers=3, coordinator=1, pendingSourceCredit=0)
    write_json(ROOT / live_name, board)
    original_reader, original_writer, original_hash = project.read_json, project.write_json, project.sha256
    protected = (ROOT / name).resolve()
    def redirect(path):
        return ROOT / live_name if Path(path).resolve() == protected else path
    with patch.object(project, 'read_json', side_effect=lambda path: original_reader(redirect(path))), \
         patch.object(project, 'write_json', side_effect=lambda path, value: original_writer(redirect(path), value)), \
         patch.object(project, 'sha256', side_effect=lambda path: original_hash(redirect(path))), \
         patch.object(sys, 'argv', ['merge_closed_cohort_handoffs_v2_20261106.py', '--cohort', '169', '--revision', revision]):
        runpy.run_path(str(ROOT / 'merge_closed_cohort_handoffs_v2_20261106.py'), run_name='__main__')
    assert sha256(ROOT / name) == frozen_board_sha == pins[name]
    live = read_json(ROOT / live_name)
    assert live['acceptedContinuationCheckpoint']['cohort'] == 169
    assert live['pendingAggregate170']['bytes'] == sum(row['bytes'] for row in following['expectedAdditions'])
    snapshot = 'evidence/lanes/parallel-wave20261102/dispatch-closed169-20261106.json'
    assert not (ROOT / snapshot).exists()
    write_json(ROOT / snapshot, live)
    write_json(ROOT / 'evidence/verification/closed169-live-dispatch-refresh-20261106.json',
        dict(passed=True, sourceCredit=0, priorBoardPreservedVerbatim=archive, acceptedClosureRevision=revision,
            addedAndCurrentClaimsVerified=current, capturedSourceInputsUnchanged=True,
            originalCapturedDispatchUnchangedSha256=frozen_board_sha,
            liveProjection=live_name, liveProjectionSha256=sha256(ROOT / live_name),
            immutableDispatchSnapshot=snapshot, immutableDispatchSnapshotSha256=sha256(ROOT / snapshot),
            originalFullMergerExecutedWithOnlyExactBoardReadWriteHashPathRedirected=True,
            generatorSha256=sha256(__file__)))


if __name__ == '__main__':
    main()
