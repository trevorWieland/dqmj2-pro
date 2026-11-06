import argparse
import copy
import json
import runpy
import sys
from pathlib import Path
from unittest.mock import patch
import project
from project import ROOT, read_json, write_json, sha256


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--chunk', required=True)
    parser.add_argument('--lane', required=True)
    options, unused = parser.parse_known_args()
    board_path = ROOT / 'evidence/lanes/parallel-wave20261102/dispatch.json'
    board_sha = sha256(board_path)
    projected = copy.deepcopy(read_json(board_path))
    operations = []
    for path in sorted((ROOT / 'evidence/lanes/parallel-wave20261105/deferred-packet-intake').glob('*.json')):
        operation = read_json(path)
        if operation['cohort'] <= projected['acceptedContinuationCheckpoint']['cohort']:
            continue
        assert operation['passed'] and operation['sourceCredit'] == 0 and operation['sharedDispatchUnchanged']
        assert sha256(ROOT / operation['ready']) == operation['readySha256']
        config = read_json(ROOT / operation['configuration'])
        assert operation['ready'] in config['readyPackets']
        assert config['packetIds'][operation['ready']] == operation['packetId']
        ready = read_json(ROOT / operation['ready'])
        lane = next(row for row in projected['active'] if row['id'] == operation['owner'])
        for report in operation['handedOffReports']:
            assert any(packet['report'] == report for packet in ready['packets'])
            if report not in lane.setdefault('handedOffReports', []):
                lane['handedOffReports'].append(report)
        projected['pendingSpecifications'][str(operation['cohort'])] = operation['specification']
        if operation['cohort'] not in projected['pendingAcceptedCohorts']:
            projected['pendingAcceptedCohorts'].append(operation['cohort'])
        operations.append(dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)))
    original_reader = project.read_json
    original_text_reader = Path.read_text

    def reader(path):
        if path.resolve() == board_path.resolve():
            return copy.deepcopy(projected)
        return original_reader(path)

    def text_reader(path, *args, **kwargs):
        if path.resolve() == board_path.resolve():
            return json.dumps(projected)
        return original_text_reader(path, *args, **kwargs)

    command = ['reserve_deferred_native_chunk_storage_v2_20261106.py', *sys.argv[1:]]
    with patch.object(project, 'read_json', side_effect=reader), patch.object(Path, 'read_text', text_reader), patch.object(sys, 'argv', command):
        runpy.run_path(str(ROOT / command[0]), run_name='__main__')
    assert sha256(board_path) == board_sha
    folder = ROOT / 'evidence/lanes/parallel-wave20261105' / options.lane
    claim_path = folder / 'claim.json'
    claim = read_json(claim_path)
    assert claim['proposal'] == options.chunk and claim['sourceCreditGranted'] == 0
    original_claim_sha = sha256(claim_path)
    claim['status'] = 'coordinator-admitted-source-scope-no-credit'
    claim['exclusiveSourceRoot'] = 'src/runtime/parallel_wave20261105/' + options.lane
    write_json(claim_path, claim)
    eligibility = read_json(folder / 'eligibility.json')
    assert eligibility['passed'] and eligibility['claimSha256'] == original_claim_sha
    eligibility.update(initialReservationClaimSha256=original_claim_sha, claimSha256=sha256(claim_path),
                       coordinatorStatusAndExclusiveSourceRootAddedOnly=True)
    write_json(folder / 'eligibility.json', eligibility)
    reservation = read_json(folder / 'deferred-dispatch-admission.json')
    assert reservation['passed'] and reservation['nativeClaimSha256'] == original_claim_sha
    reservation.update(initialReservationClaimSha256=original_claim_sha, nativeClaimSha256=sha256(claim_path))
    write_json(folder / 'deferred-dispatch-admission.json', reservation)
    write_json(folder / 'coordinator-admission.json', dict(passed=True, sourceCredit=0,
        claim=claim_path.relative_to(ROOT).as_posix(), claimSha256=sha256(claim_path),
        exclusiveSourceRoot=claim['exclusiveSourceRoot'], sharedDispatchUnchanged=True,
        actualDispatchSha256=board_sha, projectedVerifiedHandoffOperations=operations,
        originalNativeAndStorageAdmissionGuardsRetained=True,
        functions=len(claim['claimedFunctions']), initializedCandidateBytes=sum(r['bytes'] for r in claim['claimedFunctions']),
        generatorSha256=sha256(__file__)))
    print(dict(passed=True, functions=len(claim['claimedFunctions']), claimSha256=sha256(claim_path),
               sharedDispatchUnchanged=True, sourceCredit=0))


if __name__ == '__main__':
    main()
