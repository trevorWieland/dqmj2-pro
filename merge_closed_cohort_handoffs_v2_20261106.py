import argparse
import hashlib
import json
import subprocess
from project import ROOT, read_json, write_json, sha256, now
from parallel_status import finalized


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cohort', type=int, required=True)
    parser.add_argument('--revision', required=True)
    parser.add_argument('--dry-run', action='store_true')
    options = parser.parse_args()
    revision = subprocess.check_output(['git', 'rev-parse', options.revision], cwd=ROOT, text=True).strip()
    def committed(name):
        return subprocess.check_output(['git', 'show', revision + ':' + name], cwd=ROOT)
    plan_name = f'evidence/verification/cohort-2026-10-29-{options.cohort}.json'
    closure_name = f'evidence/verification/cohort{options.cohort}-expanded-source-closure-20261101.json'
    plan_raw, closure_raw = committed(plan_name), committed(closure_name)
    plan, closure = json.loads(plan_raw), json.loads(closure_raw)
    assert finalized(plan, closure)
    assert subprocess.run(['git', 'merge-base', '--is-ancestor', closure['sourceCommit'], revision], cwd=ROOT).returncode == 0
    for path in (ROOT / 'evidence/verification').glob('cohort*-continuation-driver-v*-20261105.json'):
        state = read_json(path)
        if state.get('state') == 'running':
            command = state.get('currentCommand', [])
            assert not command or not command[0].startswith('finish_source_'), 'Committed capture is active'
    board_path = ROOT / 'evidence/lanes/parallel-wave20261102/dispatch.json'
    before = sha256(board_path)
    board = read_json(board_path)
    assert board['acceptedContinuationCheckpoint']['cohort'] <= options.cohort
    operations = []
    for path in sorted((ROOT / 'evidence/lanes/parallel-wave20261105/deferred-packet-intake').glob('*.json')):
        operation = read_json(path)
        if operation['cohort'] <= options.cohort:
            continue
        assert operation['passed'] and operation['sourceCredit'] == 0 and operation['sharedDispatchUnchanged']
        assert sha256(ROOT / operation['ready']) == operation['readySha256']
        config = read_json(ROOT / operation['configuration'])
        assert operation['ready'] in config['readyPackets']
        assert config['packetIds'][operation['ready']] == operation['packetId']
        board['pendingSpecifications'][str(operation['cohort'])] = operation['specification']
        if operation['cohort'] not in board['pendingAcceptedCohorts']:
            board['pendingAcceptedCohorts'].append(operation['cohort'])
        lane = next(row for row in board['active'] if row['id'] == operation['owner'])
        for report in operation['handedOffReports']:
            assert any(packet['report'] == report for packet in read_json(ROOT / operation['ready'])['packets'])
            if report not in lane.setdefault('handedOffReports', []):
                lane['handedOffReports'].append(report)
        operations.append(dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)))
    for key, name in list(board['pendingSpecifications'].items()):
        cohort = int(key)
        if cohort <= options.cohort:
            board['acceptedSpecifications'][key] = name
            del board['pendingSpecifications'][key]
            continue
        spec = read_json(ROOT / name)
        candidates = [read_json(path) for path in (ROOT / 'provenance').glob('parallel-wave20261105-*-packets.json')]
        configs = [value for value in candidates if value['cohort'] == cohort]
        assert len(configs) == 1
        config = configs[0]
        data = spec.get('expectedDataAdditions', [])
        board[f'pendingAggregate{cohort}'] = dict(functions=len(spec['expectedAdditions']),
            functionBytes=sum(row['bytes'] for row in spec['expectedAdditions']),
            initializedDataObjects=len(data), initializedDataBytes=sum(row['bytes'] for row in data),
            bytes=sum(row['bytes'] for row in spec['expectedAdditions'] + data),
            membershipFrozen=bool(config.get('membershipFrozen')), sourceCredit=0)
    board['pendingAcceptedCohorts'] = [c for c in board['pendingAcceptedCohorts'] if c > options.cohort]
    if options.cohort not in board['acceptedWaveCohorts']:
        board['acceptedWaveCohorts'].append(options.cohort)
    board['acceptedContinuationCheckpoint'] = dict(cohort=options.cohort, functions=plan['sourceMatchedFunctions'],
        bytes=plan['sourceLinkedBytes'], sourceCommit=closure['sourceCommit'], closureCommit=revision)
    board.setdefault(f'pendingAggregate{options.cohort}', {}).update(accepted=True, sourceCredit=plan['newSourceBytes'], closure=closure_name)
    board['aggregatePendingFunctions'] = sum(board[f'pendingAggregate{c}']['functions'] for c in board['pendingAcceptedCohorts'])
    board['aggregatePendingBytes'] = sum(board[f'pendingAggregate{c}']['bytes'] for c in board['pendingAcceptedCohorts'])
    if options.dry_run:
        assert sha256(board_path) == before
        print(dict(passed=True, dryRun=True, closedCohort=options.cohort, mergedOperations=len(operations),
                   pendingFunctions=board['aggregatePendingFunctions'], pendingBytes=board['aggregatePendingBytes'], sourceCredit=0))
        return
    write_json(board_path, board)
    output = ROOT / f'evidence/lanes/parallel-wave20261105/deferred-intake-merge-after{options.cohort}.json'
    write_json(output, dict(passed=True, sourceCredit=0, createdUtc=now(), mergedOperations=operations,
        previousDispatchSha256=before, mergedDispatchSha256=sha256(board_path), closedRevision=revision,
        committedPlanSha256=hashlib.sha256(plan_raw).hexdigest(), committedClosureSha256=hashlib.sha256(closure_raw).hexdigest(),
        generator=__file__.split('\\')[-1], generatorSha256=sha256(__file__)))
    print(dict(passed=True, closedCohort=options.cohort, mergedOperations=len(operations), sourceCredit=0))


if __name__ == '__main__':
    main()
