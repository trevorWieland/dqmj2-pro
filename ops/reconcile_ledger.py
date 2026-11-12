"""Reconcile the private ledger against the public src/ tree.

The ledger's ``states.functionMatched`` flag is the input to the duplicate check, the
harvest filter and the permuter queue, so a stale flag silently misleads all three.
This tool answers one question per ledger row: does the public tree actually *define*
a symbol for that row's address?

Evidence lives in :mod:`ops/unclaimed.py` so the two tools cannot drift apart. A row is
claimed when either the definition's identifier encodes the address, or a source file's
stem does (``native_main_020685bc.c`` may define ``saved_identity_profile_pointer``).
Claims are module-scoped: every overlay loads at ``0x021d7240``, so a definition in
``src/ov000`` must not claim an ``ov004`` row that shares the address.

It reports four buckets:

* **stale** — a claim exists in ``src/`` but the ledger says ``functionMatched`` is
  false (merged work the ledger has not absorbed);
* **inverse** — the ledger says matched but no claim exists (a renamed or lost
  source; every one of these rows still carries a ``sourceUnit``, so the source is
  renamed rather than missing);
* **genuinely unmatched** — neither;
* **consistent** — claim and ledger agree.

Nothing tracked is modified. The proposed ledger patch is a copy written under ``work/``
so a coordinator can review it before touching the private tree.

    python ops/reconcile_ledger.py
    python ops/reconcile_ledger.py --json work/ledger-reconciliation.json \\
        --patch work/ledger-proposed.jsonl
"""
import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import unclaimed


def buckets(root, rows=None):
    """Classify ledger rows into the four buckets plus the proposed patch."""
    root = Path(root)
    rows = rows if rows is not None else unclaimed.load_rows(root)
    index = unclaimed.scan_sources(root, wanted={unclaimed.address_key(row) for row in rows})
    result = {'stale': [], 'inverse': [], 'unmatched': [], 'consistent': [],
              'dataClaimed': [], 'proposals': []}
    for row in rows:
        address = unclaimed.address_key(row)
        claims = index.claims_for(address, row['module'])
        strong = [claim for claim in claims if claim.kind != 'data']
        matched = bool(row['states'].get('functionMatched'))
        record = {'address': row['address'], 'module': row['module'],
                  'bytes': row['bytes'], 'mode': row['mode'],
                  'symbol': row.get('symbol'),
                  'source': strong[0].source if strong else None}
        if strong and not matched:
            result['stale'].append(record)
            result['proposals'].append(dict(row, **{
                'states': dict(row['states'], functionMatched=True),
                'sourceUnit': strong[0].source,
                'sourceLanguage': row.get('sourceLanguage') or
                                  ('assembly' if strong[0].source.endswith('.s') else 'c'),
            }))
        elif strong:
            result['consistent'].append(record)
        elif claims:
            result['dataClaimed'].append(record)
        elif matched:
            result['inverse'].append(record)
        else:
            result['unmatched'].append(record)
    result['totals'] = {
        name: {'rows': len(result[name]),
               'bytes': sum(record['bytes'] for record in result[name])}
        for name in ('stale', 'inverse', 'unmatched', 'consistent', 'dataClaimed')}
    result['files'] = index.files
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--root', default=str(ROOT))
    parser.add_argument('--json', dest='json_path', default=None)
    parser.add_argument('--patch', dest='patch_path', default=None)
    args = parser.parse_args(argv)

    started = time.perf_counter()
    root = Path(args.root).resolve()
    result = buckets(root)
    totals = result['totals']
    elapsed = time.perf_counter() - started
    print(f'ledger rows with bytes: {sum(t["rows"] for t in totals.values())} '
          f'({result["files"]} source files with a ledger address)')
    for name, label in (('stale', 'stale (claim exists, ledger says unmatched)'),
                        ('inverse', 'inverse (ledger says matched, no claim)'),
                        ('unmatched', 'genuinely unmatched'),
                        ('consistent', 'consistent (claim and ledger agree)'),
                        ('dataClaimed', 'data-symbol claim only')):
        print(f'  {label:46s} {totals[name]["rows"]:5d} rows '
              f'{totals[name]["bytes"]:9d} bytes')
    print('\nfirst 10 stale rows:')
    for record in result['stale'][:10]:
        print(f"  {record['address']:>10s} {record['module']:18s} {record['bytes']:5d} B "
              f"{record['source']}")
    print(f'\nruntime: {elapsed:.2f} s')

    counts = {name: totals[name]['rows']
              for name in ('stale', 'inverse', 'unmatched', 'consistent', 'dataClaimed')}
    byte_counts = {name: totals[name]['bytes']
                   for name in ('stale', 'inverse', 'unmatched', 'consistent', 'dataClaimed')}
    if args.json_path:
        Path(args.json_path).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json_path).write_text(json.dumps({
            'counts': counts, 'bytes': byte_counts,
            'stale': result['stale'], 'inverse': result['inverse'],
            'runtimeSeconds': round(elapsed, 2),
        }, indent=1) + '\n', encoding='utf-8')
        print(f'report written: {args.json_path}')
    if args.patch_path:
        Path(args.patch_path).parent.mkdir(parents=True, exist_ok=True)
        with Path(args.patch_path).open('w', encoding='utf-8') as stream:
            for row in result['proposals']:
                stream.write(json.dumps(row) + '\n')
        print(f'proposed patch written: {args.patch_path} ({len(result["proposals"])} rows, '
              f'{totals["stale"]["bytes"]} bytes)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
