#!/usr/bin/env python3
"""Spot-check scanner-exact rows against the repository build.

A scanner can be self-consistent and still wrong. This tool takes rows the fixed
scanner calls exact, compiles the same sources through ``public_tools/repo_build``
and checks that repo_build's per-address measurement agrees. The ten
``utility-child-arm7-wram`` rows are always selected; the remaining slots go to
rows the baseline scanner did **not** call exact, so the check covers the fix
rather than only long-standing exact rows.

    python ops/verify_scanner_module_fix.py --scan work/census/after-*.json \\
        --baseline work/census/before-*.json

Exit status 0 only when every selected row is exact through repo_build.
"""
import argparse
import glob
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'public_tools'))

import repo_build  # noqa: E402

UTILITY = (
    ('utility-child-arm7-wram', 0x038029F4),
    ('utility-child-arm7-wram', 0x037FF3A8),
    ('utility-child-arm7-wram', 0x03802AC0),
    ('utility-child-arm7-wram', 0x037FF6E4),
    ('utility-child-arm7-wram', 0x037FF454),
    ('utility-child-arm7-wram', 0x03801BF8),
    ('utility-child-arm7-wram', 0x03802B88),
    ('utility-child-arm7-wram', 0x038018E0),
    ('utility-child-arm7-wram', 0x03802BD0),
    ('utility-child-arm7-wram', 0x03804C8C),
)


def expand(patterns):
    paths = []
    for pattern in patterns:
        paths.extend(glob.glob(pattern))
    return sorted(set(paths))


def exact_entries(patterns):
    entries = {}
    for name in expand(patterns):
        data = json.loads(Path(name).read_text(encoding='utf-8'))
        for entry in data['buckets'].get('exact', []):
            entries[(entry['module'], int(entry['address'], 0))] = entry
    return entries


def choose(entries, baseline, limit):
    chosen = []
    for key in UTILITY:
        if key in entries:
            chosen.append(entries[key])
    skipped = set(UTILITY)
    candidates = [entry for key, entry in sorted(entries.items()) if key not in skipped]
    if baseline:
        candidates = [entry for entry in candidates
                      if (entry['module'], int(entry['address'], 0)) not in baseline]
    for entry in candidates:
        if len(chosen) >= limit:
            break
        chosen.append(entry)
    return chosen[:limit]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--scan', nargs='+', required=True)
    parser.add_argument('--baseline', nargs='*')
    parser.add_argument('--limit', type=int, default=20)
    parser.add_argument('--work', default=None)
    args = parser.parse_args(argv)

    entries = exact_entries(args.scan)
    baseline = set(exact_entries(args.baseline)) if args.baseline else set()
    selected = choose(entries, baseline, args.limit)
    if len(selected) < args.limit:
        print(f'only {len(selected)} scanner-exact rows available', file=sys.stderr)
    sources = [entry['path'] for entry in selected]
    out = Path(args.work) if args.work else ROOT / 'work/scanner_verify'
    compilation = repo_build.compile_all(ROOT, ROOT, out, jobs=4, sources=sources)
    if compilation['status'] != 'source-compilation-passed':
        print('compile failed: ' + json.dumps(compilation['failures'][:3], indent=1))
        return 1
    selections, stats, unused_report = repo_build.compiled_selections(
        ROOT, ROOT, out / 'report.json')
    exact = {(item['module'], item['start'])
             for values in selections.values()
             for item in values if item['exact']}
    failures = []
    for entry in selected:
        key = (entry['module'], int(entry['address'], 0))
        if key not in exact:
            failures.append(f"{key[0]} {key[1]:#010x} ({entry['path']}) is not exact through repo_build")
    print(f"scanner-exact rows checked: {len(selected)}; repo_build exactFunctions: "
          f"{stats['exactFunctions']}; unresolved relocations: {stats['unresolvedRelocations']}")
    for entry in selected:
        print(f"  {entry['module']:24s} {int(entry['address'], 0):#010x} "
              f"{entry['bytes']:4d} B  {entry['path']}")
    if failures:
        print('\nFAIL')
        for failure in failures:
            print('  ' + failure)
        return 1
    print(f'\nPASS: all {len(selected)} scanner-exact rows are exact through repo_build')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
