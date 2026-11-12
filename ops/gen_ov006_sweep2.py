"""Generate the sweep-2 lane: one address-named translation unit per ov006 row.

Two populations, both transcribed from the measured instruction stream with
``ops/transcribe_chunk.py``:

* ``asmSingleton`` - the 96 zero-shape singleton rows the sweep-1 lane left
  behind (the sweep-1 plan kept the 85 largest of 181; this is the rest).
* ``asmDuplicatePool`` - 40 of the 60 rows whose literal pool holds the same
  non-address constant in two slots.  mwcc folds an equal numeric literal into
  one slot, so each slot is given its own alias symbol
  (``native_const_<value>``, ``native_const2_<value>``); the alias name carries
  the measured value and the fixture pins both image words.  The 13 rows that
  write ``pc`` (inline jump table) are another lane's class and the 7 rows the
  chunk lane already defines are recorded, not shipped.

The generator is deterministic: the plan pins the addresses and the image is the
only other input, so ``--write`` always recreates the identical lane.

    python ops/gen_ov006_sweep2.py --list
    python ops/gen_ov006_sweep2.py --write
    python ops/gen_ov006_sweep2.py --write --only 0x21f2f60
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / 'public_tools'))

import transcribe_chunk  # noqa: E402

LANE = Path('src/ov006/g1_ov006_sweep2')
PLAN = Path(__file__).resolve().parent / 'ov006_sweep2_plan.json'
UNKNOWNS = ('byte identity proves the instruction stream, not the meaning of the fields, '
            'blocks and callee contracts it touches.')


def ledger_row(module, address):
    for line in (ROOT / 'ledger/functions.jsonl').open(encoding='utf-8'):
        if not line.strip():
            continue
        row = json.loads(line)
        if row['module'] == module and int(row['address'], 16) == address:
            return row
    raise SystemExit('row %s:%s not in the ledger' % (module, hex(address)))


def asm_source(address):
    row = ledger_row('ov006', address)
    return transcribe_chunk.emit('ov006', row, None, UNKNOWNS, constant_aliases=True,
                                 unique_pool_slots=True)


def lane_path(address, mode):
    return ROOT / LANE / mode / 'ov006' / ('native_ov006_%08x.c' % address)


def plan():
    return json.loads(PLAN.read_text())


def rows(data=None):
    data = data or plan()
    for key in data['asmSingleton'] + data['asmDuplicatePool']:
        yield key, int(key, 16)


def write(only=None):
    written = 0
    for key, address in rows():
        if only and address not in only:
            continue
        row = ledger_row('ov006', address)
        path = lane_path(address, row['mode'])
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(asm_source(address), encoding='ascii')
        written += 1
    print('written %d files under %s' % (written, LANE))


def listing():
    data = plan()
    total = 0
    for key, address in rows(data):
        row = ledger_row('ov006', address)
        form = 'duplicate' if key in data['asmDuplicatePool'] else 'singleton'
        total += int(row['bytes'])
        print('%-10s 0x%s %4d B %s' % (form, key, int(row['bytes']), row['mode']))
    print('%d rows, %d bytes' % (len(data['asmSingleton']) + len(data['asmDuplicatePool']),
                                 total))
    for label in ('deferredJumpTable', 'droppedAlreadyDefined'):
        print('%s: %d' % (label, len(data[label])))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--only', nargs='*', default=None)
    args = parser.parse_args(argv)
    if args.write:
        write({int(value, 0) for value in args.only} if args.only else None)
    if args.list or not args.write:
        listing()
    return 0


if __name__ == '__main__':
    sys.exit(main())
