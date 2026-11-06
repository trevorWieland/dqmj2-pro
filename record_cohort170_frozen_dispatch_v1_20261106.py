from project import ROOT, read_json, write_json, sha256


def main():
    base = read_json(ROOT / 'evidence/verification/closed169-live-dispatch-refresh-20261106.json')
    assert base['passed'] and sha256(ROOT / base['immutableDispatchSnapshot']) == base['immutableDispatchSnapshotSha256']
    assert sha256(ROOT / 'evidence/lanes/parallel-wave20261102/dispatch.json') == base['originalCapturedDispatchUnchangedSha256']
    live_name = base['liveProjection']; assert sha256(ROOT / live_name) == base['liveProjectionSha256']
    cfg_name = 'provenance/parallel-wave20261105-o-packets.json'
    cfg = read_json(ROOT / cfg_name); assert cfg['membershipFrozen']
    spec_name = cfg['name'] + '-specification.json'; spec = read_json(ROOT / spec_name)
    freeze_name = 'evidence/verification/cohort170-frozen-ordinary-union-20261106.json'
    freeze = read_json(ROOT / freeze_name)
    assert freeze['passed'] and freeze['functions'] == len(spec['expectedAdditions']) == 58
    assert freeze['ordinaryCBytes'] == sum(row['bytes'] for row in spec['expectedAdditions']) == 14964
    for pin in freeze['readys']:
        assert sha256(ROOT / pin['path']) == pin['sha256']
    board = read_json(ROOT / live_name)
    assert board['acceptedContinuationCheckpoint']['cohort'] == 169
    board['pendingAggregate170']['membershipFrozen'] = True
    board['currentExecution'].update(runningCohort=170, nextFunctions=58, nextBytes=14964,
        nextMembershipFrozen=True, sourceAndInvestigationWorkers=3, coordinator=1)
    for row in board['active']:
        if row['id'] == 'arm7-wm-residual-next':
            row.update(state='all16-frozen-selected170; fresh-read-only-scout', reservedResidualFunctions=0, reservedResidualBytes=0)
        elif row['id'] == 'auth-core-next':
            row.update(state='11-frozen-selected170; fresh-read-only-scout', reservedResidualFunctions=2, reservedResidualBytes=516)
        elif row['id'] == 'g2d-canvas-next':
            row.update(state='3-frozen-selected170; fresh-read-only-scout', reservedResidualFunctions=13, reservedResidualBytes=3024)
    snapshot = 'evidence/lanes/parallel-wave20261102/dispatch-closed169-frozen170-20261106.json'
    assert not (ROOT / snapshot).exists()
    write_json(ROOT / live_name, board); write_json(ROOT / snapshot, board)
    write_json(ROOT / 'evidence/verification/closed169-frozen170-dispatch-20261106.json',
        dict(passed=True, sourceCredit=0, previousSnapshotUnchanged=base['immutableDispatchSnapshot'],
            originalCapturedDispatchUnchanged=True, currentSnapshot=snapshot, currentSnapshotSha256=sha256(ROOT / snapshot),
            liveProjection=live_name, liveProjectionSha256=sha256(ROOT / live_name),
            configuration=dict(path=cfg_name, sha256=sha256(ROOT / cfg_name)),
            frozenUnion=dict(path=freeze_name, sha256=sha256(ROOT / freeze_name)), generatorSha256=sha256(__file__)))
    print(dict(passed=True, acceptedCohort=169, pendingFunctions=58, pendingBytes=14964, sourceCredit=0))


if __name__ == '__main__':
    main()
