"""Generate the ov001 closing lane: one address-named translation unit per unclaimed row.

This is the completion-sweep generator the ov006 sweeps established, retargeted at
``ov001``: ``--scan`` rebuilds the plan from the live screen and the image, ``--write``
emits one file per planned row.

The plan has three buckets, each decided by measurement:

* ``asmTranscribed`` -- one instruction run with the literal pool at the end,
  expressible by ``ops/transcribe_chunk.py`` with ``constant_aliases`` and
  ``unique_pool_slots`` on;
* ``asmDataCarrier`` -- a row whose extent is code plus a measured inline table, so it
  is emitted by ``ops/transcribe_data_rows.arm_c`` (the ``dcd`` carrier);
* ``refused`` -- recorded with the reason, never guessed.

The renderer falls back to ``ops/disasm_capstone.py`` when the pinned LLVM archive is
absent (this replay has no ``tools/android-ndk``); the fallback is calibrated by
``ops/verify_capstone_parity.py``.

    python ops/gen_ov001_close.py --scan
    python ops/gen_ov001_close.py --list
    python ops/gen_ov001_close.py --write
    python ops/gen_ov001_close.py --write --only 0x21d73e4
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

MODULE = 'ov001'
LANE = Path('src/ov001/p12_ov001_close')
PLAN = Path(__file__).resolve().parent / 'ov001_close_plan.json'
UNCLAIMED = Path('work/ov001-close/unclaimed-ov001.json')
JUMP_TABLES = Path('work/ov001-close/jump-tables.json')
UNKNOWNS = ('byte identity fixes the instruction stream, not the field, block and callee '
            'semantics behind the addresses and strides it touches.')
CARRIER_UNKNOWNS = ('the field roles, the meaning of the table entries and every callee '
                    'contract are not established by byte identity; the dispatch range and '
                    'the table bounds are measured.')

_ROWS = None


def ledger_rows():
    """Every ledger row, parsed once (the file is 32 MB; one pass, not one per row)."""
    global _ROWS
    if _ROWS is None:
        _ROWS = [json.loads(line) for line in
                 (ROOT / 'ledger/functions.jsonl').open(encoding='utf-8') if line.strip()]
        # transcribe_chunk rebuilds the callee set from the ledger on every emit;
        # hand it the cached list so generation is linear instead of quadratic.
        transcribe_chunk.ledger_rows = lambda: iter(_ROWS)
    return _ROWS


def ledger_row(module, address):
    for row in ledger_rows():
        if row['module'] == module and int(row['address'], 16) == address:
            return row
    raise SystemExit('row %s:%s not in the ledger' % (module, hex(address)))


def _installed():
    """Make ``transcribe_chunk`` able to decode without the pinned LLVM archive."""
    if (ROOT / 'tools/android-ndk').is_dir():
        return
    import disasm_capstone
    disasm_capstone.install()


def purpose(row):
    """A one-line purpose read off the measured stream: calls, back edge, exit."""
    address = int(row['address'], 16)
    size = int(row['bytes'])
    instructions = transcribe_chunk.parse(
        disasm.disassemble(ROOT, MODULE, address, size, row['mode']))
    image_path, base = disasm.module_image(ROOT, MODULE)
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


def measure(row):
    """Decode one row's extent once: (body instructions, code end, literal slots)."""
    address = int(row['address'], 16)
    size = int(row['bytes'])
    image_path, base = disasm.module_image(ROOT, MODULE)
    image = image_path.read_bytes()
    code = image[int(row['binaryOffset']):int(row['binaryOffset']) + size]
    slots = (transcribe_chunk.arm_literal_slots(code, address) if row['mode'] == 'arm'
             else transcribe_chunk.thumb_literal_slots(code, address))
    inside = {at: slot for at, slot in slots.items() if address <= slot < address + size}
    code_end = min(inside.values()) if inside else address + size
    instructions = transcribe_chunk.parse(
        disasm.disassemble(ROOT, MODULE, address, size, row['mode']))
    body = [item for item in instructions if item[0] < code_end]
    return body, code_end, inside


def shape_line(row):
    """A measured shape phrase for the header, from the code part of the extent.

    ``ops/transcribe_chunk.describe`` names a row from its block transfers only and
    falls back to "aggregate copy" otherwise, which is a false description for a
    straight-line scalar or a call sequence.  This lane states what the measurement
    shows instead of inheriting that fallback.
    """
    body, code_end, inside = measure(row)
    blocks = [item for item in body if item[1].startswith(('ldm', 'stm'))
              and 'sp!' not in item[2]]
    loads = [item for item in blocks if item[1].startswith('ldm')]
    stores = [item for item in blocks if item[1].startswith('stm')]
    calls = [item for item in body if item[1].startswith(('bl', 'blx'))]
    branches = [item for item in body if item[1].startswith('b')
                and not item[1].startswith(('bl', 'bx'))]
    back = []
    for at, mnemonic, operands in body:
        target = transcribe_chunk.branch_target(mnemonic, operands)
        if target is not None and target < at:
            back.append(at)
    if loads and stores:
        shape = 'block copy loop'
    elif stores:
        shape = 'block fill'
    elif loads:
        shape = 'block load'
    elif back and calls:
        shape = 'loop with %d call%s' % (len(calls), '' if len(calls) == 1 else 's')
    elif back:
        shape = 'loop'
    elif calls and not branches:
        shape = 'call sequence'
    elif branches:
        shape = 'branched body'
    else:
        shape = 'straight-line scalar'
    return '%s (%d instructions, %d call%s, %d branch%s, %d back edge%s, %d literal slot%s)' % (
        shape, len(body), len(calls), '' if len(calls) == 1 else 's',
        len(branches), '' if len(branches) == 1 else 'es',
        len(back), '' if len(back) == 1 else 's',
        len(set(inside.values())), '' if len(set(inside.values())) == 1 else 's')


def asm_source(address):
    _installed()
    row = ledger_row(MODULE, address)
    text = transcribe_chunk.emit(MODULE, row, purpose(row), UNKNOWNS,
                                 constant_aliases=True, unique_pool_slots=True)
    lines = text.splitlines()
    shape = shape_line(row)
    for index, line in enumerate(lines):
        if line.startswith(' * Decoded shape:'):
            lines[index] = ' * Decoded shape: %s.' % shape
            break
    return '\n'.join(lines) + '\n'


def carrier_source(address):
    """A row whose measured extent is code plus an inline table (the `dcd` carrier)."""
    _installed()
    import transcribe_data_rows as data_rows
    tables = [tuple(int(value, 0) for value in item.split(':'))
              for item in plan()['carrierTables']['%08x' % address]]
    return data_rows.arm_c(MODULE, data_rows.load_row(MODULE, address), tables,
                           plan()['carrierPurpose']['%08x' % address], CARRIER_UNKNOWNS)


def lane_path(address, mode):
    return ROOT / LANE / mode / MODULE / ('native_%s_%08x.c' % (MODULE, address))


def plan():
    return json.loads(PLAN.read_text())


def write(only=None):
    data = plan()
    written = 0
    for key in data['asmTranscribed']:
        address = int(key, 16)
        if only and address not in only:
            continue
        row = ledger_row(MODULE, address)
        path = lane_path(address, row['mode'])
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(asm_source(address), encoding='ascii')
        written += 1
    for key in data.get('asmDataCarrier', []):
        address = int(key, 16)
        if only and address not in only:
            continue
        row = ledger_row(MODULE, address)
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
            row = ledger_row(MODULE, int(address, 16))
            total += int(row['bytes'])
            print('%-11s 0x%s %4d B %s' % (form, address, int(row['bytes']), row['mode']))
    print('%d rows, %d bytes' % (len(data['asmTranscribed']) + len(data.get('asmDataCarrier', [])),
                                 total))
    print('refused: %d' % len(data['refused']))


def has_pc_write(row):
    """True when the row dispatches by writing ``pc``, not when it reads ``pc``.

    Only a *write* to pc is the dispatch class: the ARM ``add pc, pc, rN, lsl #2``
    table jump, a ``mov pc, rN`` computed jump and a pc load.  ``bx`` and
    ``pop {.., pc}`` are returns, and ``add rD, pc, #imm`` is the ADR form of an
    address computation, not a dispatch.  The scan stops at the row's first literal
    slot, because a pool word decoded as code can read as a pc write.
    """
    address = int(row['address'], 16)
    size = int(row['bytes'])
    mode = row['mode']
    image = (ROOT / 'extract/arm9_overlays/%s.bin' % MODULE).read_bytes()
    code = image[int(row['binaryOffset']):int(row['binaryOffset']) + size]
    slots = (transcribe_chunk.arm_literal_slots(code, address) if mode == 'arm'
             else transcribe_chunk.thumb_literal_slots(code, address))
    inside = {at: slot for at, slot in slots.items() if address <= slot < address + size}
    code_end = min(inside.values()) if inside else address + size
    for at, mnemonic, operands in transcribe_chunk.parse(
            disasm.disassemble(ROOT, MODULE, address, size, mode)):
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
    jump_path = ROOT / jump_tables
    jump = {int(item['address'], 16)
            for item in json.loads(jump_path.read_text())} if jump_path.is_file() else set()
    rows = {address: ledger_row(MODULE, address) for address in live}
    data = {'asmTranscribed': [], 'asmDataCarrier': [], 'refused': {},
            'refusedJumpTable': [], 'sizes': {}, 'carrierTables': {},
            'carrierPurpose': {}}
    for address in live:
        row = rows[address]
        key = '%08x' % address
        try:
            transcribe_chunk.emit(MODULE, row, None, UNKNOWNS,
                                  constant_aliases=True, unique_pool_slots=True)
        except SystemExit as error:
            if address in jump or has_pc_write(row):
                sites = data_rows.dispatch_sites(data_rows.load_row(MODULE, address))
                if not sites:
                    data['refusedJumpTable'].append(key)
                    data['refused'][key] = str(error)
                    continue
                data['asmDataCarrier'].append(key)
                data['carrierTables'][key] = ['0x%08x:%d' % (item['table'], item['length'])
                                              for item in sites]
                data['carrierPurpose'][key] = purpose(row)
                data['sizes'][key] = {'bytes': int(row['bytes']), 'mode': row['mode']}
                continue
            data['refused'][key] = str(error)
            continue
        data['asmTranscribed'].append(key)
        data['sizes'][key] = {'bytes': int(row['bytes']), 'mode': row['mode']}
    data['totalUnclaimed'] = len(live)
    data['unclaimedBytes'] = sum(int(rows[address]['bytes']) for address in live)
    PLAN.write_text(json.dumps(data, indent=1) + '\n')
    print('plan written: %d rows, %d bytes' % (len(live), data['unclaimedBytes']))
    for label in ('asmTranscribed', 'asmDataCarrier'):
        keys = data[label]
        print('  %-18s %3d rows %6d B %s' % (
            label, len(keys), sum(int(rows[int(key, 16)]['bytes']) for key in keys),
            {mode: sum(1 for key in keys if rows[int(key, 16)]['mode'] == mode)
             for mode in ('arm', 'thumb')}))
    print('  %-18s %3d rows' % ('refused', len(data['refused'])))
    for key, reason in list(data['refused'].items())[:20]:
        print('    %s  %s' % (key, reason))


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
