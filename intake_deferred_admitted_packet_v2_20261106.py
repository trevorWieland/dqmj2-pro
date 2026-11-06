import argparse
import copy
import runpy
import sys
from unittest.mock import patch
import project
from project import ROOT, read_json, write_json, sha256


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--admission', required=True)
    options, forwarded = parser.parse_known_args()
    owner = forwarded[forwarded.index('--owner') + 1]
    ready_name = forwarded[forwarded.index('--ready') + 1]
    ready = read_json(ROOT / ready_name)
    admission = read_json(ROOT / options.admission)
    assert admission['passed'] and admission['sourceCredit'] == 0 and admission['sharedDispatchUnchanged']
    assert sha256(ROOT / admission['claim']) == admission['claimSha256']
    claim = read_json(ROOT / admission['claim'])
    assert claim['status'] == 'coordinator-admitted-source-scope-no-credit'
    assert claim['exclusiveSourceRoot'] == admission['exclusiveSourceRoot']
    def identity(row):
        return row.get('program') or '', row['processor'], row['module'], row['mode'], int(row['address'], 0), row['bytes']
    scope = {identity(row) for row in claim['claimedFunctions']}
    for packet in ready['packets']:
        for row in read_json(ROOT / packet['report'])['matches']:
            assert identity(row) in scope
            assert row['source'].startswith(claim['exclusiveSourceRoot'] + '/')
    board_path = ROOT / 'evidence/lanes/parallel-wave20261102/dispatch.json'
    before = sha256(board_path)
    original_reader = project.read_json
    board = copy.deepcopy(read_json(board_path))
    existing = [row for row in board['active'] if row['id'] == owner]
    if existing:
        assert len(existing) == 1 and existing[0]['claim'] == admission['claim']
    else:
        board['active'].append(dict(id=owner, owner=claim['owner'], state='independently-admitted-source-ready',
            claim=admission['claim'], sourceRoot=claim['exclusiveSourceRoot'],
            nativeOpportunityBytes=sum(row['bytes'] for row in claim['claimedFunctions']), handedOffReports=[]))
    def projected_reader(path):
        if path.resolve() == board_path.resolve():
            return copy.deepcopy(board)
        return original_reader(path)
    sys.argv = ['intake_deferred_ready_packet_20261106.py', *forwarded]
    with patch.object(project, 'read_json', side_effect=projected_reader):
        runpy.run_path(str(ROOT / sys.argv[0]), run_name='__main__')
    assert sha256(board_path) == before
    config = read_json(ROOT / forwarded[0])
    packet_id = forwarded[forwarded.index('--packet-id') + 1]
    write_json(ROOT / f'evidence/lanes/parallel-wave20261105/deferred-admission-intakes/cohort{config["cohort"]}-{packet_id}.json',
        dict(passed=True, sourceCredit=0, actualDispatchUnchanged=True, originalDispatchSha256=before,
             admission=options.admission, admissionSha256=sha256(ROOT / options.admission),
             claim=admission['claim'], claimSha256=sha256(ROOT / admission['claim']), ready=ready_name,
             readySha256=sha256(ROOT / ready_name), originalIntakeAndNativeGuardsRetained=True,
             generatorSha256=sha256(__file__)))


if __name__ == '__main__':
    main()
