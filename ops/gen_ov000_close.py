"""Generate the ov000 close lane: one address-named translation unit per row.

``--scan`` rebuilds the plan from the live screen and the image; ``--write`` emits
one file per planned row.  This is the ov000 instance of the round-12
``ops/gen_ov006_sweep3.py`` method: the population is the live screen, and the
image decides every bucket.

``ov000`` is an all-ARM module, so the two forms are:

* ``asmTranscribed`` — one instruction run with the literal pool at the end,
  expressible by ``ops/transcribe_chunk.py`` with ``constant_aliases`` and
  ``unique_pool_slots`` on;
* ``asmDataCarrier`` — the row dispatches by writing ``pc`` and its extent contains a
  provable inline table, so it is emitted by ``ops/transcribe_data_rows.arm_c``
  (the ``dcd`` carrier);
* ``deferredJumpTable`` / ``refused`` — recorded with the reason, never guessed.

Two screen corrections are inherited from round 12 and re-checked here, because
both cost the ov006 population rows: ``add rD, pc, #imm`` is an ADR *read* of pc,
not a dispatch, and a pool word must not be decoded as code when deciding the class
(a literal that reads as a branch would condemn its row).

    python ops/gen_ov000_close.py --scan     # refresh the plan from the screen and the image
    python ops/gen_ov000_close.py --list
    python ops/gen_ov000_close.py --write
    python ops/gen_ov000_close.py --write --only 0x21d72cc
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

MODULE = 'ov000'
LANE = Path('src/ov000/g1_ov000_close')
PLAN = Path(__file__).resolve().parent / 'ov000_close_plan.json'
UNCLAIMED = Path('work/ov000-close/unclaimed-ov000.json')
JUMP_TABLES = Path('work/ov000-close/jump-tables.json')
IMAGE = Path('extract/arm9_overlays/ov000.bin')
UNKNOWNS = ('byte identity fixes the instruction stream, not the field, block and callee '
            'semantics behind the addresses and strides it touches.')
CARRIER_UNKNOWNS = ('the field roles, the meaning of the table entries and every callee '
                    'contract are not established by byte identity; the dispatch range and '
                    'the table bounds are measured.')


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


def _code_end(row):
    """The end of the code, at the row's first in-row literal slot.

    A pool word decoded as code is what condemned four ordinary ov006 rows, so the
    class screen must stop here rather than read the whole measured extent.
    """
    address = int(row['address'], 16)
    size = int(row['bytes'])
    image = (ROOT / IMAGE).read_bytes()
    code = image[int(row['binaryOffset']):int(row['binaryOffset']) + size]
    slots = (transcribe_chunk.arm_literal_slots(code, address)
             if row['mode'] == 'arm'
             else transcribe_chunk.thumb_literal_slots(code, address))
    inside = {at: slot for at, slot in slots.items() if address <= slot < address + size}
    return (min(inside.values()) if inside else address + size), inside


def purpose(row):
    """A one-line purpose read off the measured stream: calls, back edge, exit."""
    address = int(row['address'], 16)
    size = int(row['bytes'])
    instructions = transcribe_chunk.parse(
        disasm.disassemble(ROOT, MODULE, address, size, row['mode']))
    code_end, inside = _code_end(row)
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


def table_sites(row):
    """The row's inline dispatch tables, shared bounder first, measured fallback second."""
    import transcribe_data_rows as data_rows
    sites = data_rows.dispatch_sites(data_rows.load_row(MODULE, int(row['address'], 16)))
    if sites:
        return sites
    return _arm_table_fallback(row)


def carrier_purpose(address):
    """Purpose for a table row, measured: the dispatch, its range and its table."""
    row = ledger_row(MODULE, address)
    sites = table_sites(row)
    if not sites:
        return 'dispatching row whose inline table could not be bounded'
    site = sites[0]
    instructions = transcribe_chunk.parse(
        disasm.disassemble(ROOT, MODULE, address, int(row['bytes']), row['mode']))
    code_end, unused = _code_end(row)
    body = [item for item in instructions if item[0] < code_end]
    calls = [transcribe_chunk.branch_target(mnemonic, operands)
             for at, mnemonic, operands in body
             if mnemonic.startswith(('bl', 'blx'))]
    calls = [call for call in calls if call is not None]
    return ('%d instructions and %d call(s), then a %d-entry dispatch through an inline '
            'branch table at 0x%08x (dispatch word at 0x%08x)'
            % (len(body), len(calls), site['entries'], site['table'], site['site']))


def asm_source(address):
    _installed()
    row = ledger_row(MODULE, address)
    return transcribe_chunk.emit(MODULE, row, purpose(row), UNKNOWNS,
                                 constant_aliases=True, unique_pool_slots=True)


def carrier_source(address):
    """A row whose measured extent is code plus an inline table (the `dcd` carrier)."""
    _installed()
    import transcribe_data_rows as data_rows
    key = '%08x' % address
    tables = [tuple(int(value, 0) for value in item.split(':'))
              for item in plan()['carrierTables'][key]]
    return data_rows.arm_c(MODULE, data_rows.load_row(MODULE, address), tables,
                           carrier_purpose(address), CARRIER_UNKNOWNS)


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
    print('%d rows, %d bytes' % (len(data['asmTranscribed'])
                                 + len(data.get('asmDataCarrier', [])), total))
    print('deferredJumpTable: %d, refused: %d'
          % (len(data['deferredJumpTable']), len(data['refused'])))


def has_pc_write(row):
    """True when the row dispatches by writing ``pc``, not when it reads ``pc``.

    Only a *write* to pc is the dispatch class: the ARM ``add pc, pc, rN, lsl #2``
    table jump, a ``mov pc, rN`` computed jump, and a pc load.  ``bx``, ``pop {.., pc}``
    and ``ldm ..{pc}`` are returns.  ``add rD, pc, #imm`` is the ADR *read* of pc and
    is fully transcribable, so it must not defer a row.
    """
    address = int(row['address'], 16)
    size = int(row['bytes'])
    mode = row['mode']
    image = (ROOT / IMAGE).read_bytes()
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


def _arm_table_fallback(row):
    """Bound an ARM dispatch table whose entries are not all branches.

    ``ops/transcribe_data_rows.dispatch_sites`` accepts an ARM table only while every
    entry is a ``b`` word into the row.  A switch arm that *returns early* stores a
    ``pop {.., pc}`` word in the table instead, so those rows bound to zero entries
    and fall out of the carrier bucket — measured on two rows of this population
    (0x0221c0c4, 0x02224e38), where the first entry is a ``pop``.

    The extension is measured, not guessed: an entry counts when the word is a
    branch into the row *or* an instruction that writes ``pc`` as a return
    (``pop``/``ldm``/``bx``/``mov pc, ..``), and the run ends at the first word that
    is neither.  The byte gate is still the proof — a wrong bound cannot assemble
    back to the measured extent.
    """
    address = int(row['address'], 16)
    size = int(row['bytes'])
    end = address + size
    image = (ROOT / IMAGE).read_bytes()
    code = image[int(row['binaryOffset']):int(row['binaryOffset']) + size]
    decoded = {at: (mnemonic, operands) for at, mnemonic, operands
               in transcribe_chunk.parse(disasm.disassemble(ROOT, MODULE, address, size, 'arm'))}
    sites = []
    for at, (mnemonic, operands) in sorted(decoded.items()):
        if not mnemonic.startswith('add') or not mnemonic.endswith('ls'):
            continue
        destination, unused, shift = operands.split(',', 2)
        if destination.strip() != 'pc' or 'pc' not in operands or 'lsl' not in shift:
            continue
        sites.append(at)
    found = []
    for site in sites:
        table = site + 8
        entries = 0
        while table + entries * 4 + 4 <= end:
            slot = table + entries * 4
            word = int.from_bytes(code[slot - address:slot - address + 4], 'little')
            target = None
            immediate = word & 0xFFFFFF
            if immediate & 0x800000:
                immediate -= 0x1000000
            if (word >> 24) & 0x0F == 0x0A:  # b / bl
                target = slot + 8 + (immediate << 2)
            instruction = decoded.get(slot)
            if instruction is not None:
                name = instruction[0].split('.')[0]
                operands_i = instruction[1]
                destination = operands_i.split(',')[0].strip().rstrip('!')
                # A ``pop``/``ldm`` keeps ``pc`` inside the register list, so the
                # first operand is not the destination; a ``mov pc, ..`` and a
                # ``bx`` name it directly.
                if name in ('pop', 'ldm', 'ldmia', 'ldmfd'):
                    returns = 'pc' in operands_i
                elif name == 'mov':
                    returns = destination == 'pc'
                else:
                    returns = name == 'bx'
            else:
                returns = False
            if target is not None and address <= target < end:
                entries += 1
                continue
            if instruction is not None and returns:
                entries += 1
                continue
            break
        if entries:
            found.append(dict(site=site, table=table, width=4, entries=entries,
                              length=entries * 4))
    return found


def scan(unclaimed=UNCLAIMED, jump_tables=JUMP_TABLES):
    """Rebuild the plan from the live screen; the image decides every bucket."""
    _installed()
    import transcribe_data_rows as data_rows
    report = json.loads((ROOT / unclaimed).read_text())
    live = sorted(int(row['address'], 16) for row in report['rows']
                  if row['status'] == 'unclaimed')
    jump = {int(item['address'], 16)
            for item in json.loads((ROOT / jump_tables).read_text())}
    rows = {address: ledger_row(MODULE, address) for address in live}
    data = {'asmTranscribed': [], 'asmDataCarrier': [], 'deferredJumpTable': [],
            'refused': {}, 'sizes': {}, 'carrierTables': {}}
    for address in live:
        row = rows[address]
        key = '%08x' % address
        if address in jump or has_pc_write(row):
            sites = table_sites(row)
            if not sites:
                data['deferredJumpTable'].append(key)
                continue
            data['asmDataCarrier'].append(key)
            data['carrierTables'][key] = ['0x%08x:%d' % (item['table'], item['length'])
                                          for item in sites]
            data['sizes'][key] = {'bytes': int(row['bytes']), 'mode': row['mode']}
            continue
        try:
            transcribe_chunk.emit(MODULE, row, None, UNKNOWNS,
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
    print('  refused            %3d rows' % len(data['refused']))
    for key, reason in list(data['refused'].items())[:10]:
        print('    %s %s' % (key, reason))


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
