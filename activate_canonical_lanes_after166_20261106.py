import hashlib
import json
import subprocess
from project import ROOT, read_json, write_json, sha256
from parallel_status import finalized


def main():
    closure_name = 'evidence/verification/cohort166-expanded-source-closure-20261101.json'
    raw = subprocess.check_output(['git', 'show', 'HEAD:' + closure_name], cwd=ROOT)
    assert raw == (ROOT / closure_name).read_bytes()
    closure = json.loads(raw)
    assert finalized(read_json(ROOT / 'evidence/verification/cohort-2026-10-29-166.json'), closure)
    for path in (ROOT / 'evidence/verification').glob('cohort*-continuation-driver-v*-20261105.json'):
        state = read_json(path)
        assert not (state.get('state') == 'running' and state.get('currentCommand', [''])[0].startswith('finish_source_'))
    board_path = ROOT / 'evidence/lanes/parallel-wave20261102/dispatch.json'
    board = read_json(board_path)
    archive = ROOT / 'evidence/attempts/closed166-canonical-lane-activation-20261106/dispatch-before.json'
    assert not archive.exists()
    write_json(archive, board)
    before = sha256(board_path)
    activated = []
    for lane, owner, old_lane, old_remaining_functions, old_remaining_bytes in [
        ('wcm-manager-next', 'ds_tooling_research', 'dwc-match-tail-next', 11, 4406),
        ('socl-continuation-next', 'repo_audit', 'game-main-arm-next', 20, 13044)]:
        folder = ROOT / 'evidence/lanes/parallel-wave20261105' / lane
        admission = read_json(folder / 'coordinator-admission.json')
        claim = read_json(ROOT / admission['claim'])
        subset = read_json(folder / 'canonical-subset-admission.json')
        assert admission['passed'] and admission['sourceCredit'] == 0 and admission['sharedDispatchUnchanged']
        assert sha256(ROOT / admission['claim']) == admission['claimSha256'] == subset['claimSha256']
        assert subset['allOriginalCommittedPendingClaimAndStorageGuardsRetained']
        assert claim['status'] == 'coordinator-admitted-source-scope-no-credit'
        images = {}
        for row in claim['claimedFunctions']:
            binary = row['binary']
            if binary not in images:
                images[binary] = (ROOT / binary).read_bytes()
            image = images[binary]
            assert hashlib.sha256(image).hexdigest() == row['inputModuleSha256']
            start = int(row['address'], 0) - row['base']
            assert hashlib.sha256(image[start:start + row['bytes']]).hexdigest() == row['targetSha256']
        assert not any(row['id'] == lane for row in board['active'])
        row = read_json(folder / 'deferred-dispatch-admission.json')['proposedLane']
        assert row['id'] == lane and row['owner'] == owner
        row['state'] = 'coordinator-admitted-exclusive-source-work'
        board['active'].append(row)
        old = next(row for row in board['active'] if row['id'] == old_lane)
        old.update(state='reserved-residual-checkpoint', reservedResidualFunctions=old_remaining_functions,
                   reservedResidualBytes=old_remaining_bytes, residualOwnershipRetained=True)
        board['currentClaims'] = [r for r in board['currentClaims'] if r['owner'] != owner]
        board['currentClaims'].append(dict(id=lane, owner=owner, claim=admission['claim'], claimSha256=admission['claimSha256']))
        activated.append(dict(lane=lane, claim=admission['claim'], claimSha256=admission['claimSha256'],
            functions=len(claim['claimedFunctions']), bytes=sum(r['bytes'] for r in claim['claimedFunctions']),
            sourceCredit=0, publicSourceCorrespondenceProvenOnlyForMeasuredSubsets=True))
    write_json(board_path, board)
    write_json(ROOT / 'evidence/verification/closed166-canonical-lane-activation-20261106.json',
        dict(passed=True, sourceCredit=0, previousDispatchSha256=before, newDispatchSha256=sha256(board_path),
             activated=activated, oldResidualOwnershipPreserved=True, allNativeTargetsFreshlyRechecked=True,
             generatorSha256=sha256(ROOT / 'activate_canonical_lanes_after166_20261106.py')))
    print(dict(passed=True, activatedLanes=2, sourceCredit=0))


if __name__ == '__main__':
    main()
