"""Census: which functions in the measured images contain ARM swp/swpb.

Scans every module image named in ``manifest.json`` for the ARM encodings of
``swp``/``swpb`` (mask 0x0FB00FF0 against 0x01000090 / 0x01400090), converts each hit to
an absolute address, and reports which ledger rows contain one — split by whether the
row is already matched.

This is the census behind the `-avoid_byte strb` hypothesis: if a TU was compiled with a
byte-store mode that lowers a member read-modify-write to ``swp``, the functions it built
will contain one, and they are candidates for a flag-specific match.

    python ops/swp_census.py
    python ops/swp_census.py --json build/swp-census.json
"""
import argparse
import json
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MASK = 0x0FB00FF0
SWP = 0x01000090
SWPB = 0x01400090


def swp_hits(data):
    hits = []
    for offset in range(0, len(data) - 3, 4):
        word = struct.unpack_from('<I', data, offset)[0]
        masked = word & MASK
        if masked in (SWP, SWPB):
            hits.append((offset, 'swpb' if masked == SWPB else 'swp', word))
    return hits


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--root', default=str(ROOT))
    parser.add_argument('--json', dest='json_path')
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()

    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8-sig'))
    ledger = [json.loads(line) for line in
              (root / 'ledger/functions.jsonl').read_text(encoding='utf-8').splitlines() if line]
    by_module = {}
    for row in ledger:
        if not row.get('bytes'):
            continue
        by_module.setdefault(row.get('module'), []).append(row)

    report = {}
    for module in manifest['modules']:
        name = module['name']
        path = root / module['binary']
        if not path.is_file():
            continue
        base = int(str(module['base']), 0)
        hits = swp_hits(path.read_bytes())
        if not hits:
            continue
        rows = by_module.get(name, [])
        inside = []
        for offset, kind, word in hits:
            address = base + offset
            row = next((entry for entry in rows
                        if int(entry['address'], 16) <= address < int(entry['address'], 16) + entry['bytes']),
                       None)
            inside.append({
                'address': f'{address:#010x}',
                'kind': kind,
                'word': f'{word:#010x}',
                'function': row['address'] if row else None,
                'bytes': row['bytes'] if row else None,
                'matched': bool(row and row['states'].get('functionMatched')) if row else None,
            })
        report[name] = inside
        print(f'{name}: {len(hits)} swp hit(s), base {base:#x}')
        for entry in inside:
            function = entry['function'] or '(outside any ledger row)'
            state = ('matched' if entry['matched'] else 'unmatched') if entry['matched'] is not None else 'n/a'
            print(f"  {entry['address']} {entry['kind']:5s} word={entry['word']} "
                  f"fn={function} {entry['bytes'] or ''} {state}")

    total_functions = {entry['function'] for entries in report.values() for entry in entries
                       if entry['function']}
    print(f'\nmodules with swp: {len(report)}; distinct functions containing swp: {len(total_functions)}')
    if args.json_path:
        Path(args.json_path).write_text(json.dumps(report, indent=1) + '\n', encoding='utf-8')
        print(f'report written: {args.json_path}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
