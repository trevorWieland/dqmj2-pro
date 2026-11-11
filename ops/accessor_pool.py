"""Measure the pool-cluster shape of a module's ready rows.

The accessor pool question — "does one pool word group a reusable family of rows?"
— cannot be answered by row count alone: a word shared by thirty rows is often a
memory-mapped register every row touches, not a family with one shape. This tool
measures the sharing and emits an ordered worklist so the next pass starts from
evidence instead of size alone.

Ordering: rows with no BL/BLX first, then rows whose pool words belong to a cluster
of three or more, then ascending size.

    python ops/accessor_pool.py --module ov006
    python ops/accessor_pool.py --module ov006 --json build/accessor-pool.json

It reads the screen report (`ops/screen_candidates.py --json`) to know which rows
are ready, then disassembles each with `ops/disasm.py --resolve-pools`.
"""
import argparse
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CALL = re.compile(r'\b(?:bl|blx)\s+(?:0x[0-9a-f]+|r\d+)')
POOL = re.compile(r'pool 0x[0-9a-f]+ -> 0x([0-9a-f]+)')


def pool_rows(root, module, ready):
    rows = []
    for entry in ready:
        address, size = int(entry['address'], 0), entry['bytes']
        result = subprocess.run(
            [sys.executable, str(root / 'ops/disasm.py'), '--module', module,
             '--address', hex(address), '--bytes', str(size), '--mode', entry['mode'],
             '--resolve-pools', '--root', str(root)],
            capture_output=True, text=True)
        if result.returncode != 0:
            continue
        listing = result.stdout
        rows.append({
            'address': address,
            'bytes': size,
            'calls': len(CALL.findall(listing)),
            'words': sorted({f'0x{value}' for value in POOL.findall(listing)}),
        })
    return rows


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--module', required=True)
    parser.add_argument('--root', default=str(ROOT))
    parser.add_argument('--json', dest='json_path')
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    screen_path = root / 'build' / 'screen' / f'{args.module}.json'
    if not screen_path.is_file():
        print(f'run the screen first: python ops/screen_candidates.py --module {args.module} '
              f'--json {screen_path}', file=sys.stderr)
        return 2
    screen = json.loads(screen_path.read_text())
    ready = [entry for entry in screen['ready'] if entry['mode'] == 'thumb']
    rows = pool_rows(root, args.module, ready)

    sizes = Counter()
    for row in rows:
        sizes['<64 B' if row['bytes'] < 64 else ('64-127 B' if row['bytes'] < 128 else '>=128 B')] += 1
    by_word = defaultdict(list)
    for row in rows:
        for word in row['words']:
            by_word[word].append(row['address'])
    clusters = {word: sorted(addrs) for word, addrs in by_word.items() if len(addrs) >= 3}
    in_cluster = sum(len(addrs) for addrs in clusters.values())
    no_call = [row for row in rows if row['calls'] == 0]

    print(f'ready {args.module} thumb rows analysed: {len(rows)}')
    print(f'  size buckets: {dict(sizes)}')
    print(f'  distinct pool words: {len(by_word)}; clusters of 3+: {len(clusters)}')
    print(f'  row/word incidences inside 3+ clusters: {in_cluster}')
    print(f'  no-call rows: {len(no_call)}')
    for word, addrs in sorted(clusters.items(), key=lambda item: -len(item[1]))[:8]:
        print(f'    {word} x{len(addrs)}')

    worklist = [row for row in rows
                if row['calls'] == 0 and any(len(by_word[word]) >= 3 for word in row['words'])]
    worklist.sort(key=lambda row: (row['bytes'], row['address']))
    print(f'\nno-call rows inside a 3+ cluster: {len(worklist)}')
    for row in worklist[:20]:
        shared = [word for word in row['words'] if len(by_word[word]) >= 3]
        print(f"  {row['address']:08x} {row['bytes']:4d} B shared={shared}")
    if args.json_path:
        Path(args.json_path).write_text(json.dumps({
            'module': args.module,
            'analysed': len(rows),
            'sizeBuckets': dict(sizes),
            'distinctPoolWords': len(by_word),
            'clustersOfThreeOrMore': len(clusters),
            'rowWordIncidencesInClusters': in_cluster,
            'noCallRows': len(no_call),
            'worklist': [{'address': f'{row["address"]:#010x}', 'bytes': row['bytes'],
                          'words': row['words']} for row in worklist],
        }, indent=1) + '\n')
        print(f'report written: {args.json_path}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
