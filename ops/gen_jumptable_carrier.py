"""Generate the jump-table carrier lane from the measured rows.

The plan is the enumeration: every row that
``ops/scan_jump_tables.py`` proves dispatches through a table inside its own
measured extent, plus the two main-module rows that carry the 256-byte
reciprocal table between two code bodies.  The generator is deterministic: the
plan pins the addresses and table extents, and the image is the only other
input, so ``--write`` always recreates the identical lane.

    python ops/gen_jumptable_carrier.py --scan     # refresh the plan
    python ops/gen_jumptable_carrier.py --write    # write the lane sources
    python ops/gen_jumptable_carrier.py --list
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / 'public_tools'))

import transcribe_data_rows as rows  # noqa: E402

LANE = Path('src/verified_assembly/20261112_jumptable_carrier')
PLAN = Path(__file__).resolve().parent / 'jumptable_carrier_plan.json'
MAIN_ROWS = [
    dict(module='main', address='0x2025578',
         tables=['0x202562c:256'],
         purpose='normalises a soft-float quotient through a 256-byte reciprocal table',
         unknowns='the reciprocal table\'s producer and every call-site contract; the '
                  'table content and bounds are measured.'),
    dict(module='main', address='0x202654c',
         tables=['0x2026684:256'],
         purpose='normalises a soft-float quotient through a 256-byte reciprocal table',
         unknowns='the reciprocal table\'s producer and every call-site contract; the '
                  'table content and bounds are measured.'),
]


def ov006_rows(unclaimed):
    """Every unclaimed ov006 row whose extent contains a provable inline table."""
    report = json.loads(Path(unclaimed).read_text())
    wanted = {int(row['address'], 16) for row in report['rows']
              if row['status'] == 'unclaimed'}
    found = []
    for line in (ROOT / 'ledger/functions.jsonl').open(encoding='utf-8'):
        if not line.strip():
            continue
        ledger = json.loads(line)
        if ledger['module'] != 'ov006':
            continue
        address = int(ledger['address'], 16)
        if address not in wanted:
            continue
        row = rows.load_row('ov006', address)
        sites = rows.dispatch_sites(row)
        if not sites:
            continue
        tables = ','.join('0x%08x:%d' % (item['table'], item['length'])
                          for item in sites)
        found.append(dict(module='ov006', address=ledger['address'],
                          form='c' if ledger['mode'] == 'arm' else 's',
                          tables=[tables],
                          purpose='switch dispatch through an inline table',
                          unknowns='the field roles and the meaning of the table '
                                   'entries are not established by byte identity.'))
    return found


def plan():
    return json.loads(PLAN.read_text())


def write(only=None):
    written = 0
    for entry in plan()['rows']:
        module = entry['module']
        address = int(entry['address'], 16)
        if only and address not in only:
            continue
        row = rows.load_row(module, address)
        tables = []
        for value in (','.join(entry['tables'])).split(','):
            if not value:
                continue
            start, length = value.split(':')
            tables.append((int(start, 0), int(length, 0)))
        form = entry.get('form') or ('c' if module == 'main' else 's')
        symbol = 'native_%s_%08x' % (module.replace('-', '_'), address)
        if form == 'c':
            text = rows.arm_c(module, row, tables, entry['purpose'], entry['unknowns'])
            path = ROOT / LANE / module / 'arm' / (symbol + '.c')
        else:
            text = rows.thumb_s(module, row, tables, entry['purpose'], entry['unknowns'])
            path = ROOT / LANE / module / 'thumb' / (symbol + '.s')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='ascii')
        written += 1
    print('written %d files under %s' % (written, LANE))


def listing():
    total = 0
    for entry in plan()['rows']:
        row = rows.load_row(entry['module'], int(entry['address'], 16))
        total += row['bytes']
        print('%-6s %-10s %4d B form=%s tables=%s' % (
            entry['module'], entry['address'], row['bytes'],
            entry.get('form', 's' if entry['module'] != 'main' else 'c'),
            ','.join(entry['tables'])))
    print('%d rows, %d bytes' % (len(plan()['rows']), total))


def scan(unclaimed):
    entries = ov006_rows(unclaimed) + [
        dict(item, form='c') for item in MAIN_ROWS]
    for entry in entries:
        entry.setdefault('form', 'c' if entry['module'] == 'main' else 's')
    entries.sort(key=lambda item: (item['module'], int(item['address'], 16)))
    PLAN.write_text(json.dumps(dict(rows=entries), indent=1) + '\n', encoding='utf-8')
    print('plan written: %d rows' % len(entries))


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--scan', action='store_true')
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--unclaimed', default='work/unclaimed-ov006.json')
    parser.add_argument('--only', nargs='*', default=None)
    args = parser.parse_args()
    if args.scan:
        scan(args.unclaimed)
    if args.write:
        write({int(value, 0) for value in args.only} if args.only else None)
    if args.list or not (args.scan or args.write):
        listing()
    return 0


if __name__ == '__main__':
    sys.exit(main())
