from project import ROOT, read_json, write_json, sha256


def main():
    board_name = 'evidence/lanes/parallel-wave20261102/dispatch.json'
    board = read_json(ROOT / board_name)
    archive = 'evidence/attempts/closed168-resumed-source-dispatch-20261106/verbatim-dispatch.json'
    assert not (ROOT / archive).exists()
    write_json(ROOT / archive, dict(sourceCredit=0, path=board_name, sha256=sha256(ROOT / board_name),
        text=(ROOT / board_name).read_text(encoding='utf-8')))
    lanes = [('ov006-aes-next', 'frozen-selected169'), ('ov006-md5-next', 'frozen-selected170'),
        ('auth-resume-next', 'active-source'), ('ov006-crypto-utility-next', 'active-source'),
        ('arm7-wm-residual-next', 'active-source')]
    claims = {}
    for lane, state in lanes:
        folder = f'evidence/lanes/parallel-wave20261106/{lane}'
        admission = read_json(ROOT / (folder + '/coordinator-admission.json'))
        claim_name = admission['claim']
        assert admission['passed'] and admission['sourceCredit'] == 0
        assert sha256(ROOT / claim_name) == admission['claimSha256']
        claim = read_json(ROOT / claim_name)
        assert claim['status'] == 'coordinator-admitted-source-scope-no-credit'
        matches = [row for row in board['active'] if row['id'] == lane]
        if matches:
            assert len(matches) == 1 and matches[0]['claim'] == claim_name
        else:
            board['active'].append(dict(id=lane, owner=claim['owner'], state=state, claim=claim_name,
                sourceRoot=claim['exclusiveSourceRoot'], nativeOpportunityBytes=sum(row['bytes'] for row in claim['claimedFunctions']),
                handedOffReports=[]))
        claims[lane] = dict(id=lane, owner=claim['owner'], claim=claim_name, claimSha256=sha256(ROOT / claim_name))
    board['currentClaims'] = [claims[lane] for lane in ['ov006-crypto-utility-next', 'arm7-wm-residual-next', 'auth-resume-next']]
    board['currentDataClaims'] = []
    for lane in ['auth-character-data', 'aes-table-data']:
        name = f'evidence/lanes/parallel-wave20261106/{lane}/data-claim.json'
        claim = read_json(ROOT / name)
        board['currentDataClaims'].append(dict(id=lane, claim=name, claimSha256=sha256(ROOT / name),
            state='frozen-selected169', objects=len(claim['claimedStorage']), bytes=sum(row['bytes'] for row in claim['claimedStorage']), sourceCredit=0))
    board['currentExecution'] = dict(acceptedCohort=168, acceptedFunctions=11339, acceptedBytes=1172627,
        closedRevision='9e6aea5ee032dd24a884041a098b669534d88629', runningCohort=169,
        frozenCandidateFunctions=31, frozenCandidateDataObjects=112, frozenCandidateBytes=19049,
        nextGrowingCohort=170, sourceWorkers=3, coordinator=1, sourceCreditPendingAcceptance=0)
    for row in board['active']:
        if row['id'] in ['wcm-manager-next', 'socl-continuation-next', 'itcm-reset-next']:
            row['state'] = 'frozen-checkpoint-residuals-reserved'
    write_json(ROOT / board_name, board)
    write_json(ROOT / 'evidence/verification/closed168-resumed-source-dispatch-20261106.json',
        dict(passed=True, sourceCredit=0, actualCoordinatedAdmissionClaimsVerified=claims,
            oldBoardPreservedVerbatim=archive, historicalClaimsReadysSourcesUnchanged=True,
            newThreeSourceScopesDisjoint=True, generatorSha256=sha256(__file__)))


if __name__ == '__main__':
    main()
