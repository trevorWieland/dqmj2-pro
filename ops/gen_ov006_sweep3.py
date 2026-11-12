"""Generate the sweep-3 lane: one address-named translation unit per ov006 row.

``--scan`` rebuilds the plan from the live screen and the image; ``--write`` emits
one file per planned row.

The plan has three buckets, each decided by measurement:

* ``asmTranscribed`` — one instruction run with the literal pool at the end,
  expressible by ``ops/transcribe_chunk.py`` with ``constant_aliases`` and
  ``unique_pool_slots`` on (so a shared literal slot or a repeated non-address
  constant is expressed rather than refused);
* ``asmDataCarrier`` — the row dispatches by writing ``pc`` and its extent contains a
  provable inline table, so it is emitted by ``ops/transcribe_data_rows.arm_c``
  (the ``dcd`` carrier);
* ``deferredJumpTable`` / ``refused`` — recorded with the reason, never guessed.

Two screen corrections the scan makes, because the earlier sweeps' screen cost this
population rows: ``add rD, pc, #imm`` is an ADR *read* of pc, not a dispatch, and a
pool word must not be decoded as code (a literal that reads as
``eoreq pc, r0, #244, #4`` would condemn its row).

The header's purpose line is derived from the measurement, not invented: the calls
the body makes, whether it has a back edge, and how it returns.  Byte identity
proves the instruction stream; the ``Unknowns`` line says so per file.

Regeneration is deterministic (the plan pins the addresses and the image is the only
other input).  When the pinned LLVM objdump archive is absent, the renderer falls
back to ``ops/disasm_capstone.py``; that fallback is calibrated by regenerating
every committed sweep-1/sweep-2 row and re-verifying it against those lanes'
fixtures (247 rows, 0 failures).

    python ops/gen_ov006_sweep3.py --scan     # refresh the plan from src/ and the image
    python ops/gen_ov006_sweep3.py --list
    python ops/gen_ov006_sweep3.py --write
    python ops/gen_ov006_sweep3.py --write --only 0x21f2890
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / 'public_tools'))

import transcribe_chunk  # noqa: E402
import disasm  # noqa: E402

LANE = Path('src/ov006/g1_ov006_sweep3')
PLAN = Path(__file__).resolve().parent / 'ov006_sweep3_plan.json'
UNCLAIMED = Path('work/ov006-sweep3/unclaimed-ov006.json')
JUMP_TABLES = Path('work/ov006-sweep3/jump-tables.json')
UNKNOWNS = ('byte identity fixes the instruction stream, not the field, block and callee '
            'semantics behind the addresses and strides it touches.')
CARRIER_UNKNOWNS = ('the field roles, the meaning of the table entries and every callee '
                    'contract are not established by byte identity; the dispatch range and '
                    'the table bounds are measured.')
# Measured purpose for the one row whose extent is code plus an inline table.  Stated
# from the stream: 24 call sites and the display/engine control writes, then the
# seven-way dispatch, whose entries are branch words at 0x021d7330.
CARRIER_PURPOSE = {
    '021d7240': 'first row of the overlay: 24 helper calls and display/engine control '
                'writes, then a seven-way dispatch on a value in 28..34 through an inline '
                'branch table at 0x021d7330',
}


def _installed():
    """Make ``transcribe_chunk`` able to decode without the pinned LLVM archive."""
    if (ROOT / 'tools/android-ndk').is_dir():
        return
    import disasm_capstone
    disasm_capstone.install()


def ledger_row(module, address):
    for line in (ROOT / 'ledger/functions.jsonl').open(encoding='utf-8'):
        if not line.strip():
            continue
        row = json.loads(line)
        if row['module'] == module and int(row['address'], 16) == address:
            return row
    raise SystemExit('row %s:%s not in the ledger' % (module, hex(address)))


def purpose(row):
    """A one-line purpose read off the measured stream: calls, back edge, exit."""
    address = int(row['address'], 16)
    size = int(row['bytes'])
    instructions = transcribe_chunk.parse(
        disasm.disassemble(ROOT, 'ov006', address, size, row['mode']))
    # The code ends at the first literal slot inside the row; a pool word is not an
    # instruction and must not be counted as one.
    image_path, base = disasm.module_image(ROOT, 'ov006')
    image = image_path.read_bytes()
    code = image[int(row['binaryOffset']):int(row['binaryOffset']) + size]
    slots = (transcribe_chunk.arm_literal_slots(code, address) if row['mode'] == 'arm'
             else transcribe_chunk.thumb_literal_slots(code, address))
    inside = {at: slot for at, slot in slots.items() if address <= slot < address + size}
    code_end = min(inside.values()) if inside else address + size
    body = [item for item in instructions if item[0] < code_end]
    calls = [transcribe_chunk.branch_target(mnemonic, operands)
             for at, mnemonic, operands in body
             if mnemonic.startswith(('bl', 'blx'))]
    calls = [call for call in calls if call is not None]
    loops = [at for at, mnemonic, operands in body
             if transcribe_chunk.branch_target(mnemonic, operands) is not None
             and transcribe_chunk.branch_target(mnemonic, operands) < at]
    exits = [item for item in body if item[1] in ('pop', 'bx') or item[1].startswith('pop')]
    parts = ['%d instructions' % len(body)]
    if calls:
        named = ', '.join('0x%08x' % call for call in calls[:3])
        if len(calls) > 3:
            named += ', +%d more' % (len(calls) - 3)
        parts.append('%d call(s) to %s' % (len(calls), named))
    else:
        parts.append('no calls')
    if loops:
        parts.append('loops (back edge at +0x%02x)' % (loops[0] - address))
    else:
        parts.append('no back edge')
    if exits:
        parts.append('returns through %s' % ' '.join(exits[-1][1:]).strip())
    if inside:
        parts.append('%d literal slot(s) in the extent' % len(set(inside.values())))
    return '; '.join(parts)


def asm_source(address):
    _installed()
    row = ledger_row('ov006', address)
    return transcribe_chunk.emit('ov006', row, purpose(row), UNKNOWNS,
                                 constant_aliases=True, unique_pool_slots=True)


def carrier_source(address):
    """A row whose measured extent is code plus an inline table (the `dcd` carrier)."""
    _installed()
    import transcribe_data_rows as data_rows
    tables = [tuple(int(value, 0) for value in item.split(':'))
              for item in plan()['carrierTables']['%08x' % address]]
    return data_rows.arm_c('ov006', data_rows.load_row('ov006', address), tables,
                           CARRIER_PURPOSE['%08x' % address], CARRIER_UNKNOWNS)


def lane_path(address, mode):
    return ROOT / LANE / mode / 'ov006' / ('native_ov006_%08x.c' % address)


def plan():
    return json.loads(PLAN.read_text())


def write(only=None):
    data = plan()
    written = 0
    for key in data['asmTranscribed']:
        address = int(key, 16)
        if only and address not in only:
            continue
        row = ledger_row('ov006', address)
        path = lane_path(address, row['mode'])
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(asm_source(address), encoding='ascii')
        written += 1
    for key in data.get('asmDataCarrier', []):
        address = int(key, 16)
        if only and address not in only:
            continue
        row = ledger_row('ov006', address)
        path = lane_path(address, row['mode'])
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(carrier_source(address), encoding='ascii')
        written += 1
    print('written %d files under %s' % (written, LANE))


def listing():
    data = plan()
    total = 0
    for form, key in (('transcribed', 'asmTranscribed'), ('carrier', 'asmDataCarrier')):
        for address in data.get(key, []):
            row = ledger_row('ov006', int(address, 16))
            total += int(row['bytes'])
            print('%-11s 0x%s %4d B %s' % (form, address, int(row['bytes']), row['mode']))
    print('%d rows, %d bytes' % (len(data['asmTranscribed']) + len(data.get('asmDataCarrier', [])),
                                 total))
    print('deferredJumpTable: %d' % len(data['deferredJumpTable']))


def has_pc_write(row):
    """True when the row dispatches by writing ``pc``, not when it reads ``pc``.

    The earlier sweeps' screen also matched ``add rD, pc, #imm``, which is the ADR
    form of an address computation and completely transcribable; it deferred four
    rows of this population that are ordinary C/asm rows.  Two corrections matter:

    * only a *write* to pc is the dispatch class: the ARM ``add pc, pc, rN, lsl #2``
      table jump, a ``mov pc, rN`` computed jump, and a pc load.  ``bx`` and
      ``pop {.., pc}`` are returns.
    * the scan must stop at the row's first literal slot.  A pool word decoded as
      code reads as ``eoreq pc, r0, #244, #4`` and would condemn an ordinary row;
      that is the decode-the-whole-extent artefact the sweeps already recorded.
    """
    address = int(row['address'], 16)
    size = int(row['bytes'])
    mode = row['mode']
    image = (ROOT / 'extract/arm9_overlays/ov006.bin').read_bytes()
    code = image[int(row['binaryOffset']):int(row['binaryOffset']) + size]
    slots = (transcribe_chunk.arm_literal_slots(code, address) if mode == 'arm'
             else transcribe_chunk.thumb_literal_slots(code, address))
    inside = {at: slot for at, slot in slots.items() if address <= slot < address + size}
    code_end = min(inside.values()) if inside else address + size
    for at, mnemonic, operands in transcribe_chunk.parse(
            disasm.disassemble(ROOT, 'ov006', address, size, mode)):
        if at >= code_end:
            break
        destination = operands.split(',')[0].strip().rstrip('!')
        if destination == 'pc' and mnemonic not in ('pop', 'bx', 'ldm', 'ldmia'):
            return True
    return False


def scan(unclaimed=UNCLAIMED, jump_tables=JUMP_TABLES):
    """Rebuild the plan from the live screen; the image decides every bucket."""
    _installed()
    import transcribe_data_rows as data_rows
    report = json.loads((ROOT / unclaimed).read_text())
    live = sorted(int(row['address'], 16) for row in report['rows']
                  if row['status'] == 'unclaimed')
    jump = {int(item['address'], 16)
            for item in json.loads((ROOT / jump_tables).read_text())}
    rows = {address: ledger_row('ov006', address) for address in live}
    data = {'asmTranscribed': [], 'asmDataCarrier': [], 'deferredJumpTable': [],
            'refused': {}, 'sizes': {}, 'carrierTables': {}}
    for address in live:
        row = rows[address]
        key = '%08x' % address
        if address in jump or has_pc_write(row):
            sites = data_rows.dispatch_sites(data_rows.load_row('ov006', address))
            if not sites:
                data['deferredJumpTable'].append(key)
                continue
            data['asmDataCarrier'].append(key)
            data['carrierTables'][key] = ['0x%08x:%d' % (item['table'], item['length'])
                                          for item in sites]
            data['sizes'][key] = {'bytes': int(row['bytes']), 'mode': row['mode']}
            continue
        try:
            transcribe_chunk.emit('ov006', row, None, UNKNOWNS,
                                  constant_aliases=True, unique_pool_slots=True)
        except SystemExit as error:
            data['refused'][key] = str(error)
            continue
        data['asmTranscribed'].append(key)
        data['sizes'][key] = {'bytes': int(row['bytes']), 'mode': row['mode']}
    data['totalUnclaimed'] = len(live)
    data['unclaimedBytes'] = sum(int(rows[address]['bytes']) for address in live)
    PLAN.write_text(json.dumps(data, indent=1) + '\n')
    print('plan written: %d rows, %d bytes' % (len(live), data['unclaimedBytes']))
    for label in ('asmTranscribed', 'asmDataCarrier', 'deferredJumpTable'):
        keys = data[label]
        print('  %-18s %3d rows %6d B %s' % (
            label, len(keys), sum(int(rows[int(key, 16)]['bytes']) for key in keys),
            {mode: sum(1 for key in keys if rows[int(key, 16)]['mode'] == mode)
             for mode in ('arm', 'thumb')}))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--scan', action='store_true')
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--unclaimed', default=str(UNCLAIMED))
    parser.add_argument('--jump-tables', default=str(JUMP_TABLES))
    parser.add_argument('--only', nargs='*', default=None)
    args = parser.parse_args(argv)
    if args.scan:
        scan(args.unclaimed, args.jump_tables)
    if args.write:
        write({int(value, 0) for value in args.only} if args.only else None)
    if args.list or not (args.scan or args.write):
        listing()
    return 0


if __name__ == '__main__':
    sys.exit(main())
