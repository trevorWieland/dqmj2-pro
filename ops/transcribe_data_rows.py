"""Emit one data-bearing row as a split-extent translation unit.

Some measured rows are code with data inside the extent: an inline switch table,
a reciprocal table, or literal pools the compiler would deduplicate.  The
ordinary transcription form (one ``asm`` body of instructions plus ``ldr =word``
pool loads) cannot express them.  This generator emits the extent as an ordered
sequence of code and data segments instead, in one of two carriers:

``c``
    An ``asm`` function whose data runs are ``dcd`` directives (the only data
    spelling mwccarm's inline assembler accepts) and whose literal-pool loads
    stay the measured ``ldr rX, [pc, #imm]`` instruction.  This is the carrier
    for ARM rows: ARM data is 32-bit aligned.

``s``
    A mwasmarm ``.s`` unit: instructions plus ``.hword``/``.byte``/``.word``
    data.  This is the carrier for Thumb rows: their switch tables are 16-bit
    entries that begin at 2-mod-4 addresses, which no 32-bit directive can
    express.

Both carriers keep the project's source-form rules: a branch is a named symbol
or a local label, a pool word that names an address is a relocation with its
measured addend, and the data bytes are the image's bytes.

    python ops/transcribe_data_rows.py --module ov006 --address 0x21ee600 --form s
    python ops/transcribe_data_rows.py --module main --address 0x2025578 --form c
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / 'public_tools'))

import disasm  # noqa: E402
import source_units  # noqa: E402
import transcribe_chunk  # noqa: E402

TYPES = transcribe_chunk.TYPES


# ---------------------------------------------------------------------------
# Row input


def ledger_row(module, address):
    for line in (ROOT / 'ledger/functions.jsonl').open(encoding='utf-8'):
        if not line.strip():
            continue
        row = json.loads(line)
        if row['module'] == module and int(row['address'], 16) == address:
            return row
    raise SystemExit('row %s:%s not in the ledger' % (module, hex(address)))


def module_functions(module):
    functions = set()
    for line in (ROOT / 'ledger/functions.jsonl').open(encoding='utf-8'):
        if not line.strip():
            continue
        row = json.loads(line)
        if row['module'] == module:
            functions.add(int(row['address'], 16))
    return functions


def load_row(module, address):
    config = source_units.load_config(ROOT)
    entry = config['modules'][module]
    image = (ROOT / entry['originalImage']).read_bytes()
    row = ledger_row(module, address)
    offset = int(row['binaryOffset'])
    return dict(row=row, data=image[offset:offset + int(row['bytes'])],
                address=int(row['address'], 16), bytes=int(row['bytes']),
                base=int(entry['loadAddressBase'], 16), image_size=len(image),
                functions=module_functions(module))


# ---------------------------------------------------------------------------
# Decode


def instructions(row, start, length, mode):
    text = disasm.disassemble(ROOT, row['row']['module'], start, length, mode)
    result = []
    for line in text.splitlines():
        match = transcribe_chunk.INSTRUCTION.match(
            transcribe_chunk.ANNOTATION.sub('', line))
        if not match:
            continue
        result.append((int(match.group(1), 16), match.group(2),
                       match.group(3).strip()))
    width = 2 if mode == 'thumb' else 4
    if not result or result[0][0] != start:
        raise SystemExit('%s region %08x+%d: no instruction at the region start'
                         % (mode, start, length))
    for index, (at, unused_mnemonic, unused_operands) in enumerate(result):
        following = result[index + 1][0] if index + 1 < len(result) else start + length
        if following <= at:
            raise SystemExit('%s region %08x+%d: overlapping decode' % (mode, start, length))
    if result[-1][0] + width > start + length:
        raise SystemExit('%s region %08x+%d: decode overruns the region'
                         % (mode, start, length))
    return result


def translate(row, start, length, mode):
    result = []
    for at, mnemonic, operands in instructions(row, start, length, mode):
        if mnemonic == '<unknown>':
            if mode == 'thumb':
                raise SystemExit('undecodable Thumb halfwords at %08x' % at)
            word = int.from_bytes(
                row['data'][at - row['address']:at - row['address'] + 4], 'little')
            decoded = transcribe_chunk.decode_dataproc(word, at)
            if decoded is None:
                raise SystemExit('undecodable ARM word %08x at %08x' % (word, at))
            mnemonic, operands = decoded
        if mode == 'thumb':
            spelled, spelled_operands = transcribe_chunk.thumb_mnemonic(mnemonic, operands)
        elif mnemonic.startswith(('push', 'pop')):
            root, condition = transcribe_chunk.split_condition(mnemonic)
            registers = operands.strip('{} ')
            spelled = ('stm%sdb' if root == 'push' else 'ldm%sia') % condition
            spelled_operands = 'sp!, {%s}' % registers
        else:
            spelled, spelled_operands = transcribe_chunk.mwcc_mnemonic(mnemonic), operands
            if mnemonic in ('lsl', 'lsr', 'asr', 'ror',
                            'lsls', 'lsrs', 'asrs', 'rors'):
                # LLVM prints a standalone shift; mwcc spells it as a MOV.
                shift = mnemonic[:-1] if mnemonic.endswith('s') else mnemonic
                set_s = 's' if mnemonic.endswith('s') else ''
                left, rest = operands.split(',', 1)
                source = rest.split(',', 1)[0].strip()
                spelled = 'mov' + set_s
                spelled_operands = '%s, %s, %s %s' % (
                    left.strip(), source, shift, rest.split(',', 1)[1].strip())
            else:
                shift_root, shift_condition = transcribe_chunk.split_condition(mnemonic)
                if shift_condition and shift_root in ('lsl', 'lsr', 'asr', 'ror',
                                                      'lsls', 'lsrs', 'asrs', 'rors'):
                    shift = shift_root[:-1] if shift_root.endswith('s') else shift_root
                    set_s = 's' if shift_root.endswith('s') else ''
                    left, rest = operands.split(',', 1)
                    source = rest.split(',', 1)[0].strip()
                    spelled = 'mov%s%s' % (shift_condition, set_s)
                    spelled_operands = '%s, %s, %s %s' % (
                        left.strip(), source, shift, rest.split(',', 1)[1].strip())
        result.append(dict(at=at, mnemonic=spelled, operands=spelled_operands,
                           target=transcribe_chunk.branch_target(mnemonic, operands)))
    return result


# ---------------------------------------------------------------------------
# Pool and layout


def pool_slots(row, mode):
    data, address = row['data'], row['address']
    slots = transcribe_chunk.thumb_literal_slots(data, address) if mode == 'thumb' \
        else transcribe_chunk.arm_literal_slots(data, address)
    return {address + at: slot for at, slot in slots.items()
            if address <= slot < address + row['bytes']}


def run_lengths(offsets):
    runs = []
    for offset in sorted(set(offsets)):
        if runs and offset == runs[-1][0] + 4 * runs[-1][1]:
            runs[-1] = (runs[-1][0], runs[-1][1] + 1)
        else:
            runs.append((offset, 1))
    return runs


def word_expression(row, value):
    span = (row['base'], row['base'] + row['image_size'])
    name, addend = transcribe_chunk.symbol_for(value, row['functions'], span)
    if name is None:
        return '0x%08x' % value
    return '%s+%d' % (name, addend) if addend else name


def externs_for(expressions):
    lines = []
    for expression in expressions:
        name = expression.partition('+')[0]
        if not name.startswith('native_'):
            continue
        line = ('extern void %s(void);' % name) if name.startswith('native_fn') \
            else ('extern u8 %s[];' % name)
        if line not in lines:
            lines.append(line)
    return lines


def header(module, row, purpose, unknowns, carrier):
    return '\n'.join([
        '/* %s row 0x%08x: %d bytes.' % (module, row['address'], row['bytes']),
        ' *',
        ' * What it does: %s' % purpose,
        ' *',
        ' * Carrier: %s.' % carrier,
        ' * The measured extent is code plus data inside the function. The data',
        ' * runs are emitted as data, not decoded as instructions; every',
        ' * instruction, branch target, pool word and table entry is read from',
        ' * the image.',
        ' *',
        ' * Unknowns: %s' % unknowns,
        ' */'])


def split(row, tables, mode):
    """Ordered code and data segments of one measured extent.

    ``tables`` is ``[(start, length)]``.  Every literal-pool slot read by a
    pc-relative load inside the extent is data too, whether it trails the code
    or sits between two code bodies; a row may have several pools.
    """
    address, size = row['address'], row['bytes']
    end = address + size
    width = 4 if mode == 'arm' else 2
    table_ranges = [(start, start + length) for start, length in tables]
    if any(start % width or length % width for start, length in tables):
        raise SystemExit('table extent is not %d-byte aligned' % width)
    slots = pool_slots(row, mode)
    inside = {at: slot for at, slot in slots.items()
              if not any(start <= slot < stop for start, stop in table_ranges)}
    data = [(start, stop, 'table', width) for start, stop in table_ranges]
    data.extend((start, start + count * 4, 'pool', 4)
                for start, count in run_lengths(inside.values()))
    data.sort()
    for index, item in enumerate(data):
        if item[0] < address or item[1] > end:
            raise SystemExit('data run %08x-%08x leaves the extent' % item[:2])
        if index and item[0] < data[index - 1][1]:
            raise SystemExit('data runs overlap at %08x' % item[0])
    code = []
    cursor = address
    for start, stop, unused_kind, unused_width in data:
        if start > cursor:
            code.append((cursor, start))
        cursor = stop
    if cursor < end:
        code.append((cursor, end))
    return dict(code=code, data=data, inside=inside)


# ---------------------------------------------------------------------------
# Carriers


def arm_c(module, row, tables, purpose, unknowns):
    """Emit the row as a mwccarm ``asm`` body with ``dcd`` data runs."""
    address = row['address']
    layout = split(row, tables, 'arm')
    labels = {}
    for first, last in layout['code']:
        for item in translate(row, first, last - first, 'arm'):
            target = item['target']
            if target is not None and address <= target < address + row['bytes']:
                labels[target] = 'L_%08x' % target
    body, expressions = [], []

    def emit_code(first, last):
        if last <= first:
            return
        for item in translate(row, first, last - first, 'arm'):
            if item['at'] in labels:
                body.append('%s:' % labels[item['at']])
            target = item['target']
            if item['at'] in layout['inside']:
                body.append('    %s %s' % (item['mnemonic'], item['operands']))
            elif target is not None:
                name = labels.get(target) or 'native_fn_%08x' % target
                if not name.startswith('L_'):
                    expressions.append(name)
                body.append('    %s %s' % (item['mnemonic'], name))
            else:
                body.append('    %s %s' % (item['mnemonic'], item['operands']))

    cursor = address
    for start, stop, kind, width in layout['data']:
        emit_code(cursor, start)
        if kind == 'table':
            for offset in range(start, stop, 4):
                value = int.from_bytes(
                    row['data'][offset - address:offset - address + 4], 'little')
                expression = word_expression(row, value)
                expressions.append(expression)
                body.append('    dcd %s' % expression)
        else:
            for offset in range(start, stop, 4):
                if offset in labels:
                    body.append('%s:' % labels[offset])
                value = int.from_bytes(
                    row['data'][offset - address:offset - address + 4], 'little')
                expression = word_expression(row, value)
                expressions.append(expression)
                body.append('    dcd %s' % expression)
        cursor = stop
    emit_code(cursor, address + row['bytes'])
    symbol = 'native_%s_%08x' % (module.replace('-', '_'), address)
    return (header(module, row, purpose, unknowns,
                   'mwccarm asm with dcd data runs') + '\n' + TYPES + '\n'
            + '\n'.join(externs_for(expressions)) + '\n\n\n'
            + 'asm u32 %s (register u32 a0)\n{\n' % symbol
            + '\n'.join(body) + '\n}\n')


def thumb_s(module, row, tables, purpose, unknowns):
    """Emit the row as a mwasmarm ``.s`` unit with halfword table data."""
    address = row['address']
    layout = split(row, tables, 'thumb')
    labels = {}
    for first, last in layout['code']:
        for item in translate(row, first, last - first, 'thumb'):
            target = item['target']
            if target is not None and address <= target < address + row['bytes']:
                labels[target] = '.L_%08x' % target
    body, expressions = [], []

    def emit_code(first, last):
        if last <= first:
            return
        for item in translate(row, first, last - first, 'thumb'):
            if item['at'] in labels:
                body.append('%s:' % labels[item['at']])
            target = item['target']
            if item['at'] in layout['inside']:
                destination = item['operands'].split(',')[0].strip()
                body.append('    %s %s, .L_pool_%08x' % (
                    item['mnemonic'], destination, layout['inside'][item['at']]))
            elif target is not None:
                name = labels.get(target) or 'native_fn_%08x' % target
                if not name.startswith('.L_'):
                    expressions.append(name)
                body.append('    %s %s' % (item['mnemonic'], name))
            else:
                body.append('    %s %s' % (item['mnemonic'], item['operands']))

    cursor = address
    for start, stop, kind, width in layout['data']:
        emit_code(cursor, start)
        if kind == 'table':
            for offset in range(start, stop, 2):
                value = int.from_bytes(
                    row['data'][offset - address:offset - address + 2], 'little')
                body.append('    .hword 0x%04x' % value)
        else:
            for offset in range(start, stop, 4):
                body.append('.L_pool_%08x:' % offset)
                value = int.from_bytes(
                    row['data'][offset - address:offset - address + 4], 'little')
                expression = word_expression(row, value)
                expressions.append(expression)
                body.append('    .word %s' % expression)
        cursor = stop
    emit_code(cursor, address + row['bytes'])
    symbol = 'native_%s_%08x' % (module.replace('-', '_'), address)
    lines = ['.section .text', '.thumb']
    for expression in expressions:
        name = expression.partition('+')[0]
        if name.startswith('native_'):
            line = '.extern ' + name
            if line not in lines:
                lines.append(line)
    lines.append('.global ' + symbol)
    lines.append('.type %s, @function' % symbol)
    lines.append(symbol + ':')
    lines.extend(body)
    lines.append('.size %s, .-%s' % (symbol, symbol))
    return header(module, row, purpose, unknowns,
                  'mwasmarm .s with .hword table data') + '\n' + '\n'.join(lines) + '\n'


# ---------------------------------------------------------------------------
# Table discovery


def dispatch_sites(row):
    """Every inline dispatch site and the table extent its entries prove.

    A Thumb table entry is a signed halfword offset to a target inside the row;
    the first entry that does not resolve inside the row is the first code
    halfword after the table.  An ARM table entry is a ``b`` word whose target
    is inside the row.  The byte comparison in ``ops/verify_data_rows.py`` is
    the final proof of the boundary: a wrong split cannot assemble back to the
    measured bytes.
    """
    import scan_jump_tables as scan
    address, size, data = row['address'], row['bytes'], row['data']
    end = address + size
    found = []
    if row['row']['mode'] == 'arm':
        offset, unused_word = scan.arm_dispatch_offset(data)
        if offset is None:
            return found
        site = address + offset
        table = site + 8
        entries = 0
        while table + entries * 4 + 4 <= end:
            value = int.from_bytes(
                data[table + entries * 4 - address:table + entries * 4 - address + 4],
                'little')
            target = scan.arm_branch_target(value, table + entries * 4)
            if target is None or not (address <= target < end):
                break
            entries += 1
        if entries:
            found.append(dict(site=site, table=table, width=4,
                              entries=entries, length=entries * 4))
        return found
    halfwords = scan.thumb_halfwords(data)
    for index, halfword in enumerate(halfwords):
        if scan.thumb_pc_write(halfword) is None:
            continue
        site = address + index * 2
        source = scan.thumb_pc_write(halfword)
        table, width = None, 2
        for back in range(index - 1, max(-1, index - 10) - 1, -1):
            base = scan.thumb_pc_base(halfwords[back], address + back * 2)
            if base is None or base[0] != source:
                continue
            table = base[1]
            for look in range(back + 1, index):
                load = halfwords[look]
                if (load & 0xF800) == 0x8800 and ((load >> 3) & 0x7) == source:
                    table = base[1] + ((load >> 6) & 0x1F) * 2
                    width = 2
                    break
                if (load & 0xF800) == 0x7800 and ((load >> 3) & 0x7) == source:
                    table = base[1] + ((load >> 6) & 0x1F)
                    width = 1
                    break
            break
        if table is None or not (address <= table < end):
            continue
        entries = 0
        while table + entries * width + width <= end:
            at = table + entries * width
            value = int.from_bytes(data[at - address:at - address + width], 'little')
            if width == 2 and value & 0x8000:
                value -= 0x10000
            if not (address <= site + 4 + value < end):
                break
            entries += 1
        if entries:
            found.append(dict(site=site, table=table, width=width,
                              entries=entries, length=entries * width))
    unique = {}
    for item in found:
        unique[(item['table'], item['site'])] = item
    return sorted(unique.values(), key=lambda item: item['table'])


def tables_for(module, row):
    return [(item['table'], item['length']) for item in dispatch_sites(row)]


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--module', required=True)
    parser.add_argument('--address', required=True)
    parser.add_argument('--form', choices=('c', 's'), required=True)
    parser.add_argument('--tables', nargs='*', default=None,
                        help='explicit table extents as address:length,address:length')
    parser.add_argument('--purpose', default=None)
    parser.add_argument('--unknowns', default='the field roles and the meaning of the '
                                               'table entries are not established by '
                                               'byte identity.')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    address = int(args.address, 0)
    row = load_row(args.module, address)
    if args.tables:
        tables = []
        for value in ','.join(args.tables).split(','):
            if not value:
                continue
            start, length = value.split(':')
            tables.append((int(start, 0), int(length, 0)))
    else:
        tables = tables_for(args.module, row)
    if args.form == 'c':
        text = arm_c(args.module, row, tables, args.purpose or 'switch dispatch',
                     args.unknowns)
    else:
        text = thumb_s(args.module, row, tables, args.purpose or 'switch dispatch',
                       args.unknowns)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding='ascii')
        print('written %s' % args.output)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == '__main__':
    sys.exit(main())
