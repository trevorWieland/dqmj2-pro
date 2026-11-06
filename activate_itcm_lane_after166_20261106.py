import subprocess
from project import ROOT, read_json, write_json, sha256


def main():
    closure = 'evidence/verification/cohort166-expanded-source-closure-20261101.json'
    assert subprocess.check_output(['git', 'show', 'cfbac6c94de7d69bd70c92e81e652726cdb3c603:' + closure], cwd=ROOT) == (ROOT / closure).read_bytes()
    assert read_json(ROOT / closure)['passed']
    for path in (ROOT / 'evidence/verification').glob('cohort*-continuation-driver-v*-20261105.json'):
        value = read_json(path)
        assert not (value.get('state') == 'running' and value.get('currentCommand', [''])[0].startswith('finish_source_'))
    folder = ROOT / 'evidence/lanes/parallel-wave20261105/itcm-reset-next'
    admission = read_json(folder / 'coordinator-admission.json')
    assert admission['passed'] and admission['sourceCredit'] == 0
    assert sha256(ROOT / admission['claim']) == admission['claimSha256']
    subset = read_json(folder / 'canonical-subset-admission.json')
    assert subset['allOriginalCommittedPendingClaimAndStorageGuardsRetained']
    claim = read_json(ROOT / admission['claim'])
    assert len(claim['claimedFunctions']) == 1 and claim['claimedFunctions'][0]['bytes'] == 168
    path = ROOT / 'evidence/lanes/parallel-wave20261102/dispatch.json'
    board = read_json(path)
    before = sha256(path)
    archive = ROOT / 'evidence/attempts/closed166-itcm-lane-activation-20261106/dispatch-before.json'
    assert not archive.exists()
    write_json(archive, board)
    assert not any(row['id'] == 'itcm-reset-next' for row in board['active'])
    row = read_json(folder / 'deferred-dispatch-admission.json')['proposedLane']
    assert row['owner'] == 'workflow_research' and row['id'] == 'itcm-reset-next'
    row['state'] = 'coordinator-admitted-exclusive-source-work'
    board['active'].append(row)
    old = next(row for row in board['active'] if row['id'] == 'dwc-auth-next')
    old.update(state='reserved-residual-checkpoint', reservedResidualFunctions=55, reservedResidualBytes=8382,
               residualOwnershipRetained=True)
    board['currentClaims'] = [r for r in board['currentClaims'] if r['owner'] != 'workflow_research']
    board['currentClaims'].append(dict(id='itcm-reset-next', owner='workflow_research', claim=admission['claim'],
                                      claimSha256=admission['claimSha256']))
    write_json(path, board)
    write_json(ROOT / 'evidence/verification/closed166-itcm-lane-activation-20261106.json', dict(passed=True,
        sourceCredit=0, previousDispatchSha256=before, newDispatchSha256=sha256(path),
        actualUnclaimedFunctionsActivated=1, initializedOpportunityBytes=168,
        oldAuthResidualOwnershipPreserved=True, generatorSha256=sha256(ROOT / 'activate_itcm_lane_after166_20261106.py')))
    print(dict(passed=True, sourceCredit=0, activeLane='itcm-reset-next'))


if __name__ == '__main__':
    main()
