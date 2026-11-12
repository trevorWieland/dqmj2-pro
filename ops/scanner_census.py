#!/usr/bin/env python3
"""Join scanner output against the ledger and report the exact-census delta.

The unit of the census is a *ledger row*, not a source unit: several sources can
measure the same address, and a row is exact when any declared source reproduces
it. A scanner scan (``ops/permuter_candidates.py --json``) supplies the exact
set; the ledger supplies the row population and the matched flag.

    python ops/scanner_census.py --scan build/after-*.json \\
        --baseline build/before-*.json --out-json build/census.json

The four buckets are the ones used by the 2026-11-11 exact census:

* ``a`` exact + matched
* ``b`` exact + unmatched
* ``c`` not-exact + matched
* ``d`` not-exact + unmatched

``movedToExact`` is the set of rows the repaired scanner now measures exact but
the baseline did not: these are measurement artifacts, not source changes.
"""
import argparse
import collections
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUCKETS = ('a', 'b', 'c', 'd')


def load_scans(paths):
    exact = {}
    units = 0
    skips = collections.Counter()
    for name in paths:
        data = json.loads(Path(name).read_text(encoding='utf-8'))
        units += data.get('units', 0)
        for entry in data['buckets'].get('exact', []):
            exact[(entry['module'], int(entry['address'], 0))] = entry
        for kind, count in (data.get('relocationSkips') or {}).items():
            skips[int(kind)] += count
    return dict(exact=exact, units=units, relocationSkips=dict(sorted(skips.items())))


def load_ledger(root):
    rows = []
    with (root / 'ledger/functions.jsonl').open(encoding='utf-8') as stream:
        for line in stream:
            if not line.strip():
                continue
            row = json.loads(line)
            size = row.get('bytes')
            if type(size) is int and size > 0:
                rows.append(row)
    return rows


def buckets(rows, exact):
    cells = {key: dict(rows=0, bytes=0) for key in BUCKETS}
    index = {(True, True): 'a', (True, False): 'b', (False, True): 'c', (False, False): 'd'}
    for row in rows:
        key = (row['module'], int(row['address'], 0))
        matched = bool((row.get('states') or {}).get('functionMatched'))
        cell = cells[index[(key in exact, matched)]]
        cell['rows'] += 1
        cell['bytes'] += row['bytes']
    return cells


def summarize(scan_paths, rows):
    scan = load_scans(scan_paths)
    return dict(scan=scan, buckets=buckets(rows, scan['exact']))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--scan', nargs='+', required=True, help='after-fix scan JSON(s)')
    parser.add_argument('--baseline', nargs='+', help='before-fix scan JSON(s)')
    parser.add_argument('--root', default=str(ROOT))
    parser.add_argument('--out-json')
    parser.add_argument('--out-md')
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    rows = load_ledger(root)
    after = summarize(args.scan, rows)
    before = summarize(args.baseline, rows) if args.baseline else None

    moved = []
    if before:
        for key in sorted(set(after['scan']['exact']) - set(before['scan']['exact'])):
            entry = after['scan']['exact'][key]
            row = next((item for item in rows
                        if item['module'] == key[0] and int(item['address'], 0) == key[1]), None)
            if row is not None:
                moved.append(dict(address=f'{key[1]:#010x}', module=key[0], bytes=row['bytes'],
                                  path=entry.get('path'), score=entry.get('score')))
    by_module = collections.defaultdict(lambda: dict(rows=0, bytes=0))
    for item in moved:
        by_module[item['module']]['rows'] += 1
        by_module[item['module']]['bytes'] += item['bytes']

    report = dict(
        after=dict(units=after['scan']['units'], buckets=after['buckets'],
                   relocationSkips=after['scan']['relocationSkips']),
        before=(dict(units=before['scan']['units'], buckets=before['buckets'],
                     relocationSkips=before['scan']['relocationSkips'])
                if before else None),
        delta=({key: dict(rows=after['buckets'][key]['rows'] - before['buckets'][key]['rows'],
                          bytes=after['buckets'][key]['bytes'] - before['buckets'][key]['bytes'])
                for key in BUCKETS} if before else None),
        movedToExact=dict(rows=len(moved),
                          bytes=sum(item['bytes'] for item in moved),
                          byModule=dict(sorted(by_module.items())),
                          rowsDetail=moved),
        trueNonExact=dict(rows=after['buckets']['c']['rows'] + after['buckets']['d']['rows'],
                          bytes=after['buckets']['c']['bytes'] + after['buckets']['d']['bytes']),
    )
    if args.out_json:
        destination = Path(args.out_json)
        if not destination.is_absolute():
            destination = root / destination
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(report, indent=1) + '\n', encoding='utf-8')
        print(f'json: {destination}')

    if args.out_md:
        lines = ['# Exact-census scanner delta', '',
                 f"after units: {after['scan']['units']}" +
                 (f"; before units: {before['scan']['units']}" if before else ''), '',
                 '| bucket | before rows | before bytes | after rows | after bytes | delta rows | delta bytes |',
                 '| --- | ---: | ---: | ---: | ---: | ---: | ---: |']
        labels = dict(a='a exact + matched', b='b exact + unmatched',
                      c='c not-exact + matched', d='d not-exact + unmatched')
        for key in BUCKETS:
            now = after['buckets'][key]
            if before:
                then = before['buckets'][key]
                lines.append(f"| {labels[key]} | {then['rows']} | {then['bytes']} | "
                             f"{now['rows']} | {now['bytes']} | "
                             f"{now['rows'] - then['rows']:+d} | {now['bytes'] - then['bytes']:+d} |")
            else:
                lines.append(f"| {labels[key]} | - | - | {now['rows']} | {now['bytes']} | - | - |")
        lines += ['', f"Rows moved from not-exact to exact: **{report['movedToExact']['rows']}** "
                      f"({report['movedToExact']['bytes']} B).",
                  f"True non-exact after the fix: **{report['trueNonExact']['rows']} rows / "
                  f"{report['trueNonExact']['bytes']} B** (buckets c + d).", '']
        if by_module:
            lines += ['| module moved to exact | rows | bytes |', '| --- | ---: | ---: |']
            for module, cell in sorted(by_module.items()):
                lines.append(f"| {module} | {cell['rows']} | {cell['bytes']} |")
            lines.append('')
            lines += ['## Rows moved to exact', '',
                      '| address | bytes | module | source |', '| --- | ---: | --- | --- |']
            for item in moved:
                lines.append(f"| `{item['address']}` | {item['bytes']} | {item['module']} | "
                             f"`{item['path']}` |")
            lines.append('')
        if after['scan']['relocationSkips']:
            lines += ['## Remaining unsupported relocation kinds', '',
                      '| kind | units skipped |', '| ---: | ---: |']
            for kind, count in after['scan']['relocationSkips'].items():
                lines.append(f'| {kind} | {count} |')
            lines.append('')
        destination = Path(args.out_md)
        if not destination.is_absolute():
            destination = root / destination
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text('\n'.join(lines) + '\n', encoding='utf-8')
        print(f'md: {destination}')
    print(f"moved to exact {report['movedToExact']['rows']} rows / "
          f"{report['movedToExact']['bytes']} B; true non-exact "
          f"{report['trueNonExact']['rows']} rows / {report['trueNonExact']['bytes']} B")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
