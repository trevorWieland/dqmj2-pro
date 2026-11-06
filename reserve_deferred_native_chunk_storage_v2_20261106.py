import argparse
import runpy
import sys
from project import ROOT, read_json, sha256
from parallel_status import interval


def storage_claims():
    values = []
    for path in sorted((ROOT / 'evidence/lanes').rglob('data-claim.json')):
        claim = read_json(path)
        assert claim['functionCount'] == 0 and not claim['functionOwnershipGranted']
        for row in claim['claimedStorage']:
            assert row['kind'] == 'data' and row['mode'] == 'data' and row['bytes'] > 0
            assert sha256(ROOT / row['semanticSource']) == row['semanticSourceSha256']
            scope = (row.get('program') or '', row['processor'], row['module'])
            assert scope[1] in ('arm9', 'arm7') and scope[2]
            begin = int(row['address'], 0)
            values.append((path.relative_to(ROOT).as_posix(), (scope, begin, begin + row['bytes'], 'data')))
    return values


def check(functions, storage):
    for row in functions:
        own = interval(row)
        for name, reserved in storage:
            if own[0] == reserved[0] and max(own[1], reserved[1]) < min(own[2], reserved[2]):
                raise ValueError('Native source proposal overlaps admitted initialized storage: ' + name)


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--chunk', required=True)
    options, unused = parser.parse_known_args()
    partition = read_json(ROOT / 'evidence/lanes/parallel-wave20261102/native-backlog/partition.json')
    matches = [row for row in partition['chunks'] if row['id'] == options.chunk]
    assert len(matches) == 1
    check(matches[0]['functionIdentities'], storage_claims())
    sys.argv[0] = str(ROOT / 'reserve_deferred_native_chunk_20261105.py')
    runpy.run_path(sys.argv[0], run_name='__main__')


if __name__ == '__main__':
    main()
