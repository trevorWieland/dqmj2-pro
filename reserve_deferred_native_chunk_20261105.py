import argparse
import json
import subprocess
import sys
from unittest.mock import patch
import parallel_status
import reserve_native_parallel_chunk_20261105 as original
from project import ROOT, read_json, write_json, sha256


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--chunk', required=True)
    parser.add_argument('--lane', required=True)
    parser.add_argument('--owner', required=True, choices=['repo_audit', 'ds_tooling_research', 'workflow_research'])
    parser.add_argument('--accepted-revision', required=True)
    parser.add_argument('--pending-specification', action='append', default=[])
    options = parser.parse_args()
    revision = subprocess.check_output(['git', 'rev-parse', options.accepted_revision + '^{commit}'], cwd=ROOT, text=True).strip()
    def committed(name):
        return subprocess.check_output(['git', 'show', revision + ':' + name], cwd=ROOT).decode('utf-8')
    with patch.object(parallel_status, 'committed', side_effect=committed):
        baseline = parallel_status.snapshot()
    assert not baseline['conflicts'] and not baseline['missingClaims']
    proposal = next(r for r in read_json(ROOT / 'evidence/lanes/parallel-wave20261102/native-backlog/partition.json')['chunks'] if r['id'] == options.chunk)
    additions = []
    for name in options.pending_specification:
        additions.extend(read_json(ROOT / name)['expectedAdditions'])
    for row in proposal['functionIdentities']:
        span = parallel_status.interval(row)
        assert not any(span[0] == v[0] and span[1] < v[2] and v[1] < span[2] for v in map(parallel_status.interval, additions))
    board = ROOT / parallel_status.DISPATCH
    board_sha = sha256(board)
    deferred = {}
    def write(path, value):
        if path == board:
            deferred.update(value)
        else:
            write_json(path, value)
    argv = [original.__file__, '--chunk', options.chunk, '--lane', options.lane, '--owner', options.owner]
    with patch.object(parallel_status, 'committed', side_effect=committed), patch.object(original, 'committed', side_effect=committed), patch.object(original, 'write_json', side_effect=write), patch.object(sys, 'argv', argv):
        original.main()
    assert sha256(board) == board_sha and deferred
    folder = ROOT / 'evidence/lanes/parallel-wave20261105' / options.lane
    path = folder / 'deferred-dispatch-admission.json'
    write_json(path, dict(passed=True, sourceCredit=0, acceptedEvidenceRevision=revision,
        acceptedCohort=baseline['acceptedCohort'], actualDispatchUnchanged=True, dispatchSha256=board_sha,
        proposedLane=deferred['active'][-1], pendingSpecificationPins=[dict(path=n, sha256=sha256(ROOT / n)) for n in options.pending_specification],
        originalAdmissionGuardsRetained=True, nativeClaimSha256=sha256(folder / 'claim.json'),
        ownershipActiveByCoordinatorInstruction=True, generatorSha256=sha256(__file__)))
    print(dict(passed=True, deferredDispatch=path.relative_to(ROOT).as_posix(), actualDispatchUnchanged=True))


if __name__ == '__main__':
    main()
