from project import ROOT, read_json, write_json, sha256


def main():
    name = 'evidence/lanes/parallel-wave20261102/dispatch.json'
    before = (ROOT / name).read_text(encoding='utf-8')
    board = read_json(ROOT / name)
    assert board['acceptedContinuationCheckpoint']['cohort'] == 167
    unchanged = {n: sha256(ROOT / n) for n in ['recovery.json', 'source-preferences.json']}
    claims = board['currentClaims']
    archive = 'evidence/attempts/closed167-dispatch-status-refresh-20261106/verbatim-inputs.json'
    assert not (ROOT / archive).exists()
    write_json(ROOT / archive, dict(sourceCredit=0, path=name, sha256=sha256(ROOT / name), text=before))
    board['currentExecution'] = 'Closed167;168 growing. WCM/CPS and SOC/SSL source work, GP character-data private routing, coordinator intake and original14-control pure-index qualification.'
    board['integrationQueueFrozenThroughCohort'] = 167
    for row in board['active']:
        if row['id'] == 'integration':
            row['state'] = 'closed167-coordinating168-and-private-index-qualification'
        elif row['id'] in ['dwc-http-next', 'dwc-match-next']:
            row['state'] = 'historical-handoffs-residual-reserved'
        elif row['id'] == 'itcm-reset-next':
            row['state'] = 'frozen-intaken-awaiting-itcm-reference-qualification'
    for row in board['currentDataInvestigations']:
        if row['id'] in ['sdk-constant-data', 'sdk-sound-data']:
            row.update(state='accepted-by-closed-cohort166',
                acceptedInitializedBytes=row['initializedCandidateBytes'],
                closure='evidence/verification/cohort166-expanded-source-closure-20261101.json')
    claim = 'evidence/lanes/parallel-wave20261106/gamespy-gp-character-data/data-claim.json'
    ready = 'evidence/lanes/parallel-wave20261106/gamespy-gp-character-data/ready.json'
    assert sha256(ROOT / ready) == '43edfab835b5248ce4bffa24ae5a92c994f15b217343d881582e21ca764a74ac'
    assert not any(r['id'] == 'gamespy-gp-character-data' for r in board['currentDataInvestigations'])
    board['currentDataInvestigations'].append(dict(id='gamespy-gp-character-data', owner='workflow_research',
        state='frozen-ready-private-registration-and-placement-qualification', claim=claim,
        claimSha256=sha256(ROOT / claim), ready=ready, readySha256=sha256(ROOT / ready),
        dataObjects=259, initializedCandidateBytes=3696, sourceCredit=0))
    board['currentDataClaims'] = [dict(id='gamespy-gp-character-data', owner='workflow_research',
        claim=claim, claimSha256=sha256(ROOT / claim))]
    for row in board['currentZeroByteInterfaceMigrations']:
        row.update(state='selected-and-preserved-by-closed-cohort167',
            closure='evidence/verification/cohort167-expanded-source-closure-20261101.json')
    board['currentInfrastructureInvestigation'].update(owner='coordinator',
        state='actual-root-original14-control-pure-index-qualification-running',
        captureV9QualifiedAndAdoptedFor=[164, 165, 166, 167],
        selectionSnapshotAdoptedFor=[165, 166, 167], productionIndexAdopted=False,
        evidenceIndexFullFourteenCaseQualification=False)
    assert board['currentClaims'] == claims and board['sourceCreditGrantedByDispatch'] == 0
    assert all(sha256(ROOT / n) == h for n, h in unchanged.items())
    write_json(ROOT / name, board)
    write_json(ROOT / 'evidence/verification/closed167-dispatch-status-refresh-20261106.json',
        dict(passed=True, sourceCredit=0, historicalClaimsAndAllCurrentFunctionOwnershipUnchanged=True,
            registeredSourceAndPreferencesUnchanged=True, previousDispatchArchive=archive,
            refreshedDispatchSha256=sha256(ROOT / name), generatorSha256=sha256(__file__)))
    print(dict(passed=True, sourceCredit=0, currentFunctions=11247, currentSourceBytes=1155781))


if __name__ == '__main__':
    main()
