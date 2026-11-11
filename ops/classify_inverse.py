"""Classify the inverse set: ledger says matched, but no definition in src/.

For every row the ledger reports as matched while `src/` has no definition for its
address, this decides which of four things happened:

* **RENAMED** — a source file exists for the unit but does not carry the address in its
  file name or symbol (semantic naming or a different convention). Bookkeeping only.
* **MENTION-ONLY** — the address appears in `src/` only as an extern declaration, a call
  site or a data reference. Either the source was deleted or never committed.
* **DATA/ASM** — the row is data or an assembly unit whose source lives elsewhere (an
  `.s` file, a justified-assembly range, or a data blob).
* **GENUINELY LOST** — no trace in `src/`, `work/` or the git history.

Evidence for every row is written to ``work/inverse-504.json``; the summary lands in
``docs/acceptance/inverse-504.md``.

    python ops/classify_inverse.py
"""
import argparse
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ('.c', '.h', '.s', '.inc', '.cpp')


def address_key(row):
    return f"{int(row['address'], 16):08x}"


def src_index(root):
    """Every src file's text, lowercased, once."""
    index = {}
    for path in (root / 'src').rglob('*'):
        if path.suffix.lower() not in SOURCES or not path.is_file():
            continue
        try:
            index[path.relative_to(root).as_posix()] = path.read_text(
                encoding='utf-8', errors='replace').lower()
        except OSError:
            continue
    return index


def work_mentions(root, key):
    hits = []
    for path in (root / 'work').rglob('*'):
        if not path.is_file() or path.stat().st_size > 4_000_000:
            continue
        if path.suffix.lower() not in ('.json', '.jsonl', '.md', '.txt', '.py', '.c', '.s'):
            continue
        try:
            if key in path.read_text(encoding='utf-8', errors='replace').lower():
                hits.append(path.relative_to(root).as_posix())
        except OSError:
            continue
        if len(hits) >= 3:
            break
    return hits


def git_history(root, key, symbol):
    """Has any commit added a line mentioning the address or the ledger symbol?"""
    for needle in (key, (symbol or '').lower()):
        if not needle:
            continue
        try:
            result = subprocess.run(['git', 'log', '--oneline', '-S', needle, '--', 'src'],
                                    capture_output=True, text=True, cwd=str(root), timeout=120)
        except (OSError, subprocess.SubprocessError):
            return []
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip().splitlines()[:3]
    return []


def classify(row, index, root):
    key = address_key(row)
    symbol = (row.get('symbol') or '')
    source_unit = row.get('sourceUnit')

    if source_unit and (root / source_unit).is_file():
        body = (root / source_unit).read_text(encoding='utf-8', errors='replace').lower()
        strong = key in body or (symbol.lower() in body if symbol else False)
        return 'A', {'path': source_unit, 'strong': strong,
                     'why': ('sourceUnit exists and names the unit' if strong else
                             'sourceUnit exists but mentions neither the address nor the symbol')}

    named = [path for path in index if key in path.rsplit('/', 1)[-1].lower()]
    if named:
        return 'A', {'path': named[0], 'strong': True,
                     'why': 'file name carries the address'}

    mentions = [path for path, text in index.items() if key in text]
    if mentions:
        return 'B', {'mentions': mentions[:3], 'count': len(mentions)}

    if row.get('sourceLanguage') == 'assembly' or (row.get('justifiedAssemblyBytes') or 0) > 0:
        return 'C', {'why': 'assembly unit', 'ranges': row.get('justifiedAssemblyRanges')}

    work_hits = work_mentions(root, key)
    if work_hits:
        return 'C', {'work': work_hits, 'why': 'trace in work/'}

    history = git_history(root, key, symbol)
    if history:
        return 'B', {'history': history, 'why': 'appears in git history but not in the tree'}

    return 'D', {'object': row.get('object'), 'objectSha256': row.get('objectSha256')}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--root', default=str(ROOT))
    parser.add_argument('--report', default=None)
    parser.add_argument('--doc', default=None)
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()

    reconciliation = json.loads((root / 'work/ledger-reconciliation.json').read_text(
        encoding='utf-8'))
    inverse = reconciliation['inverse']
    ledger = {}
    for line in (root / 'ledger/functions.jsonl').read_text(encoding='utf-8').splitlines():
        if line.strip():
            row = json.loads(line)
            ledger[row['id']] = row

    index = src_index(root)
    buckets = defaultdict(list)
    for record in inverse:
        key = f"{int(record['address'], 16):08x}" 
        row = next((entry for entry in ledger.values()
                    if address_key(entry) == key), None)
        if row is None:
            continue
        bucket, evidence = classify(row, index, root)
        buckets[bucket].append({
            'address': row['address'], 'module': row['module'], 'bytes': row['bytes'],
            'mode': row['mode'], 'symbol': row.get('symbol'),
            'objectSha256': row.get('objectSha256'), 'evidence': evidence,
        })

    total_bytes = {bucket: sum(item['bytes'] for item in items)
                   for bucket, items in buckets.items()}
    print(f'inverse rows: {len(inverse)}')
    for bucket in sorted(buckets):
        weak = sum(1 for item in buckets[bucket] if item['evidence'].get('strong') is False)
        suffix = f' ({weak} weak: file present, address absent)' if weak else ''
        print(f'  {bucket}: {len(buckets[bucket]):3d} rows, {total_bytes[bucket]:6d} B{suffix}')
    for bucket in sorted(buckets):
        top = sorted(buckets[bucket], key=lambda item: -item['bytes'])[:3]
        print(f'  {bucket} largest: ' + ', '.join(
            f"{item['address']}({item['bytes']}B)" for item in top))

    report = {'counts': {bucket: len(items) for bucket, items in buckets.items()},
              'bytes': total_bytes,
              'buckets': {bucket: sorted(items, key=lambda item: -item['bytes'])
                          for bucket, items in buckets.items()}}
    if args.report:
        Path(args.report).parent.mkdir(parents=True, exist_ok=True)
        Path(args.report).write_text(json.dumps(report, indent=1) + '\n', encoding='utf-8')
        print(f'report written: {args.report}')

    if args.doc:
        lines = ['# Inverse set: 504 rows the ledger calls matched with no definition in `src/`',
                 '',
                 'Generated by `ops/classify_inverse.py` from `ops/reconcile_ledger.py`.',
                 'The ledger is not edited here; this classifies what is actually missing.',
                 '',
                 '| bucket | meaning | rows | bytes |', '| --- | --- | --- | --- |']
        meanings = {
            'A': 'renamed source (path does not carry the address)',
            'B': 'mention only (extern/call/data reference, or history but not tree)',
            'C': 'data or assembly unit (source elsewhere)',
            'D': 'genuinely lost (no trace anywhere)',
        }
        for bucket in ('A', 'B', 'C', 'D'):
            weak = sum(1 for item in buckets.get(bucket, [])
                       if item['evidence'].get('strong') is False)
            note = f' ({weak} weak)' if weak else ''
            lines.append(f"| {bucket}{note} | {meanings[bucket]} | "
                         f"{len(buckets.get(bucket, []))} | {total_bytes.get(bucket, 0)} |")
        for bucket in ('B', 'D'):
            lines += ['', f'## Top 20 by bytes — {bucket} ({meanings[bucket]})', '',
                      '| address | module | bytes | symbol | evidence |',
                      '| --- | --- | --- | --- | --- |']
            for item in sorted(buckets.get(bucket, []), key=lambda x: -x['bytes'])[:20]:
                evidence = item['evidence']
                detail = evidence.get('path') or evidence.get('mentions') or evidence.get('why') or ''
                lines.append(f"| `{item['address']}` | {item['module']} | {item['bytes']} | "
                             f"`{item['symbol']}` | {str(detail)[:60]} |")
        Path(args.doc).parent.mkdir(parents=True, exist_ok=True)
        Path(args.doc).write_text('\n'.join(lines) + '\n', encoding='utf-8')
        print(f'doc written: {args.doc}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
