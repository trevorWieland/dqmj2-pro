import argparse
import hashlib
import json
import subprocess
from project import ROOT, read_json, write_json, sha256, now
from parallel_status import interval, committed, snapshot
from prepare_parallel_packet_wave import reserved_storage


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--chunk', required=True)
    parser.add_argument('--lane', required=True)
    parser.add_argument('--owner', choices=['repo_audit', 'workflow_research', 'ds_tooling_research'], required=True)
    options = parser.parse_args()
    assert options.lane and all(c in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in options.lane)
    boardpath = ROOT / 'evidence/lanes/parallel-wave20261102/dispatch.json'
    board = read_json(boardpath)
    accepted = snapshot()
    assert not accepted['conflicts'] and not accepted['missingClaims']
    partition = ROOT / 'evidence/lanes/parallel-wave20261102/native-backlog/partition.json'
    proposal = next(r for r in read_json(partition)['chunks'] if r['id'] == options.chunk)
    reserved = [('accepted', interval(r)) for r in map(json.loads, committed('ledger/functions.jsonl').splitlines())
                if r['states']['functionMatched']]
    reserved += reserved_storage(ROOT, read_json(ROOT / 'ledger/data.json')['buildSha256'])
    pins = {}
    for path in (ROOT / 'evidence/lanes').rglob('claim.json'):
        claim = read_json(path)
        rows = claim.get('claimedFunctions', claim.get('functions', []))
        rows = rows if isinstance(rows, list) else []
        reserved.extend((path.relative_to(ROOT).as_posix(), interval(r, claim)) for r in rows)
        pins[path.relative_to(ROOT).as_posix()] = sha256(path)
    for pending in accepted['pending']:
        path = ROOT / pending['specification']
        reserved.extend((path.name, interval(r)) for r in read_json(path)['expectedAdditions'])
        pins[path.name] = sha256(path)
    base = 'evidence/lanes/parallel-wave20261105/' + options.lane
    path = ROOT / (base + '/claim.json')
    assert not path.exists() and not any(r['id'] == options.lane for r in board['active'])
    rows, images = [], {}
    for original in proposal['functionIdentities']:
        row = dict(original)
        span = interval(row)
        assert not any(span[0] == r[0] and span[1] < r[2] and r[1] < span[2] for _, r in reserved), row['id']
        if row['binary'] not in images:
            images[row['binary']] = (ROOT / row['binary']).read_bytes()
        image = images[row['binary']]
        assert hashlib.sha256(image).hexdigest() == row['inputModuleSha256']
        offset = int(row['address'], 0) - row['base']
        assert hashlib.sha256(image[offset:offset + row['bytes']]).hexdigest() == row['targetSha256']
        row['sourceTarget'] = 'src/runtime/parallel_wave20261105/' + options.lane + '/' + f'{span[1]:08x}.c'
        rows.append(row)
        reserved.append((options.lane, span))
    assert len(rows) == proposal['functions'] and sum(r['bytes'] for r in rows) == proposal['opportunityBytes']
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    write_json(path, dict(schemaVersion=1, owner=options.owner + '/' + options.lane,
        status='reserved-awaiting-checkpoint', createdUtc=now(), discoveryCommit=head,
        acceptedBaselineCohort=accepted['acceptedCohort'], acceptedFinalizedReceipt=accepted['acceptedReceipt'],
        coordinatorOwnershipAuthorized=True, proposal=options.chunk, claimedFunctions=rows, sourceCreditGranted=0))
    write_json(ROOT / (base + '/eligibility.json'), dict(passed=True, createdUtc=now(), functions=len(rows),
        bytes=sum(r['bytes'] for r in rows), sourceCredit=0, claimSha256=sha256(path), partitionSha256=sha256(partition),
        acceptedCommit=head, exclusionInputs=pins, physicalNamespaceModeAliasesExcluded=True,
        nativeModuleAndEveryTargetHashVerified=True, overlaps=0, generatorSha256=sha256(__file__)))
    board['active'].append(dict(id=options.lane, owner=options.owner, state='reserved-awaiting-checkpoint',
        claim=path.relative_to(ROOT).as_posix(), sourceRoot='src/runtime/parallel_wave20261105/' + options.lane,
        nativeOpportunityBytes=proposal['opportunityBytes'], handedOffReports=[]))
    write_json(boardpath, board)
    print(dict(claim=path.relative_to(ROOT).as_posix(), sha256=sha256(path), functions=len(rows),
               bytes=sum(r['bytes'] for r in rows)))


if __name__ == '__main__':
    main()
