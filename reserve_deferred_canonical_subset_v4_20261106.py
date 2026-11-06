import argparse
import copy
import runpy
import sys
from unittest.mock import patch
import project
from project import ROOT, read_json, write_json, sha256


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--selection', required=True)
    parser.add_argument('--selection-sha256', required=True)
    parser.add_argument('--chunk', required=True)
    parser.add_argument('--lane', required=True)
    options, unused = parser.parse_known_args()
    assert sha256(ROOT / options.selection) == options.selection_sha256
    selected = read_json(ROOT / options.selection)
    assert selected['sourceCredit'] == 0 and selected['sourceOwnershipGranted'] is False
    assert selected['backlogId'] == options.chunk
    partition_name = 'evidence/lanes/parallel-wave20261102/native-backlog/partition.json'
    partition_path = ROOT / partition_name
    partition_hash = sha256(partition_path)
    partition = read_json(partition_path)
    proposal = next(r for r in partition['chunks'] if r['id'] == options.chunk)
    wanted = {r['id']: r for r in selected['identities']}
    assert len(wanted) == selected['functions']
    canonical = {r['id']: r for r in proposal['functionIdentities']}
    assert wanted.keys() <= canonical.keys()
    rows = []
    for identifier, row in wanted.items():
        actual = canonical[identifier]
        for key in ['processor', 'module', 'mode', 'bytes']:
            assert row[key] == actual[key]
        assert (row.get('program') or '') == (actual.get('program') or '')
        assert int(row['address'], 0) == int(actual['address'], 0)
        assert row['inputModuleSha256'] == actual['inputModuleSha256']
        assert row.get('targetSha256', row.get('inputBytesSha256')) == actual['targetSha256']
        rows.append(copy.deepcopy(actual))
    rows.sort(key=lambda r: int(r['address'], 0))
    assert sum(r['bytes'] for r in rows) == selected['bytes']
    projected = copy.deepcopy(partition)
    scope = next(r for r in projected['chunks'] if r['id'] == options.chunk)
    scope.update(functionIdentities=rows, functions=len(rows), opportunityBytes=sum(r['bytes'] for r in rows))
    before_board = sha256(ROOT / 'evidence/lanes/parallel-wave20261102/dispatch.json')
    original_reader = project.read_json
    def reader(path):
        if path.resolve() == partition_path.resolve():
            return copy.deepcopy(projected)
        return original_reader(path)
    forwarded = []
    skip = False
    for arg in sys.argv[1:]:
        if skip:
            skip = False
            continue
        if arg in ['--selection', '--selection-sha256']:
            skip = True
            continue
        forwarded.append(arg)
    command = ['reserve_deferred_native_chunk_storage_v3_20261106.py', *forwarded]
    with patch.object(project, 'read_json', side_effect=reader), patch.object(sys, 'argv', command):
        runpy.run_path(str(ROOT / command[0]), run_name='__main__')
    assert sha256(partition_path) == partition_hash
    assert sha256(ROOT / 'evidence/lanes/parallel-wave20261102/dispatch.json') == before_board
    folder = ROOT / 'evidence/lanes/parallel-wave20261105' / options.lane
    claim = read_json(folder / 'claim.json')
    assert {r['id'] for r in claim['claimedFunctions']} == set(wanted)
    receipt_path = folder / 'canonical-subset-admission.json'
    write_json(receipt_path, dict(passed=True, sourceCredit=0,
        selection=options.selection, selectionSha256=options.selection_sha256,
        originalPartition=partition_name, originalPartitionSha256=partition_hash,
        originalBacklogFunctions=proposal['functions'], selectedCanonicalWholeFunctions=len(rows),
        selectedInitializedCandidateBytes=sum(r['bytes'] for r in rows),
        omittedRowsNotClaimedOrCredited=True, canonicalNativeIdentityAndEveryTargetHashUnchanged=True,
        allOriginalCommittedPendingClaimAndStorageGuardsRetained=True,
        actualSharedDispatchAndPartitionUnchanged=True, claimSha256=sha256(folder / 'claim.json'),
        generatorSha256=sha256(ROOT / 'reserve_deferred_canonical_subset_v4_20261106.py')))
    admission = read_json(folder / 'coordinator-admission.json')
    admission['canonicalSubsetSelection'] = dict(path=receipt_path.relative_to(ROOT).as_posix(), sha256=sha256(receipt_path))
    write_json(folder / 'coordinator-admission.json', admission)
    print(dict(passed=True, functions=len(rows), initializedCandidateBytes=sum(r['bytes'] for r in rows), sourceCredit=0))


if __name__ == '__main__':
    main()
