"""Emit one transcribed ``asm`` translation unit from a measured row in the image.

The aggregate-copy class is transcribed, not guessed: the body is the measured
instruction stream of the row, decoded from the module image, with the literal
pool and every branch target read from the image. This generator does the
mechanical half (decode, rename, spelling) and leaves the two judgement halves to
the caller: ``--purpose`` and ``--unknowns`` become the header prose.

mwccarm's assembler is not gas and not capstone; the spellings that matter here are:

* a standalone shift is ``mov rX, rY, lsl #n``, never ``lsl rX, rY, #n``;
* a block transfer with a condition needs the addressing mode spelled out
  (``ldmltia``, not ``ldmlt``);
* ``push``/``pop`` are ``stmdb sp!``/``ldmia sp!``;
* a conditional width suffix follows the condition (``ldreqsb``, not ``ldrsbeq``);
* two pool slots holding the same value need distinct symbols (``native_data2_``),
  because the assembler deduplicates one expression used twice.

    python ops/transcribe_chunk.py --module main --address 0x2008ca4 \
        --purpose "Copies in 32-byte blocks then words." --unknowns "none"
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / 'public_tools'))

import disasm  # noqa: E402

CONDITIONS = ('eq', 'ne', 'cs', 'hs', 'cc', 'lo', 'mi', 'pl', 'vs', 'vc',
              'hi', 'ls', 'ge', 'lt', 'gt', 'le', 'al')
WIDTH_SUFFIX = ('sb', 'sh', 'h', 'b', 'd')
ADDRESSING = ('ia', 'db', 'ib', 'da')
INSTRUCTION = re.compile(r'^\s*([0-9a-f]+):\s+(\S+)\s*(.*?)\s*$')
ANNOTATION = re.compile(r'\s*@.*$')
BRANCH = re.compile(r'^0x([0-9a-f]+)')
CONDITIONS_FULL = ('eq', 'ne', 'cs', 'cc', 'mi', 'pl', 'vs', 'vc',
                   'hi', 'ls', 'ge', 'lt', 'gt', 'le', 'al', 'nv')
TYPES = ('typedef unsigned int u32;\ntypedef signed int s32;\n'
         'typedef unsigned short u16;\ntypedef signed short s16;\n'
         'typedef unsigned char u8;\ntypedef signed char s8;\n')


def split_condition(mnemonic):
    """Split a trailing condition code off a mnemonic, if there is one."""
    for condition in CONDITIONS:
        if mnemonic.endswith(condition) and len(mnemonic) > len(condition) + 1:
            return mnemonic[:-len(condition)], condition
    return mnemonic, ''


def mwcc_mnemonic(mnemonic):
    """Rewrite one LLVM mnemonic into the spelling mwccarm's assembler accepts."""
    if mnemonic in ('push', 'pop', 'nop'):
        return mnemonic
    root, condition = split_condition(mnemonic)
    if root in ('ldm', 'stm'):
        return root + condition + 'ia'
    if root.startswith(('ldm', 'stm')) and root[3:] in ADDRESSING:
        # ``ldmiaeq`` (addressing mode before the condition) is the spelling the
        # disassembler prints; mwccarm wants the condition first: ``ldmeqia``.
        return root[:3] + condition + root[3:]
    for suffix in WIDTH_SUFFIX:
        if root.endswith(suffix) and not root.startswith(('ldm', 'stm')):
            base = root[:-len(suffix)]
            if base in ('ldr', 'str'):
                return base + condition + suffix
    return mnemonic


def arm_literal_slots(code, address):
    """Map instruction offset -> literal slot address for ARM pc-relative loads."""
    slots = {}
    for offset in range(0, len(code) - 3, 4):
        word = int.from_bytes(code[offset:offset + 4], 'little')
        if (word & 0x0F7F0000) != 0x051F0000:
            continue
        immediate = word & 0xFFF
        slots[offset] = address + offset + 8 + (immediate if word & 0x00800000 else -immediate)
    return slots


def thumb_literal_slots(code, address):
    slots = {}
    offset = 0
    while offset < len(code) - 1:
        halfword = int.from_bytes(code[offset:offset + 2], 'little')
        if (halfword & 0xF800) == 0x4800:
            slots[offset] = ((address + offset + 4) & ~3) + (halfword & 0xFF) * 4
            offset += 2
        elif (halfword & 0xE000) == 0xE000:
            offset += 4
        else:
            offset += 2
    return slots


def describe(instructions, address, code_end):
    """Describe the copy shape of a row in one sentence (the header's 'what it does')."""
    blocks = [(at, mnemonic, operands) for at, mnemonic, operands in instructions
              if at < code_end and mnemonic.startswith(('ldm', 'stm'))
              and 'sp!' not in operands]
    predicated = [item for item in blocks
                  if item[1][-2:] in CONDITIONS_FULL[:-2]]
    loads = [item for item in blocks if item[1].startswith('ldm')]
    stores = [item for item in blocks if item[1].startswith('stm')]
    body = [item for item in instructions if item[0] < code_end]

    def width(operands):
        inside = operands[operands.find('{'):]
        return len([item for item in inside.strip('{} ').split(',') if item.strip()])

    def plural(count, noun):
        return ('one %s' % noun) if count == 1 else ('%d %ss' % (count, noun))

    if predicated:
        return ('predicated block copy',
                'Copies a %d-register block to an optional destination under a condition '
                'in %s.' % (width(predicated[0][2]), plural(len(predicated), 'predicated move')))
    if loads and stores:
        return ('chunk loop',
                'Moves %d-register chunks between two pointers with writeback block moves '
                '(%s, %s).' % (width(stores[0][2]), plural(len(loads), 'load'),
                               plural(len(stores), 'store')))
    if stores:
        return ('block fill',
                'Writes %s of %d registers through a writeback base pointer.' % (
                    plural(len(stores), 'block'), width(stores[0][2])))
    if loads:
        return ('block load',
                'Reads %s of %d registers through a writeback base pointer.' % (
                    plural(len(loads), 'block'), width(loads[0][2])))
    return ('aggregate copy', 'Copies a measured block.')


def parse(text):
    """Parse objdump output into (offset, mnemonic, operands) triples."""
    instructions = []
    for line in text.splitlines():
        match = INSTRUCTION.match(ANNOTATION.sub('', line))
        if not match:
            continue
        instructions.append((int(match.group(1), 16), match.group(2), match.group(3).strip()))
    return instructions


DATAPROC = ('and', 'eor', 'sub', 'rsb', 'add', 'adc', 'sbc', 'rsc',
            'tst', 'teq', 'cmp', 'cmn', 'orr', 'mov', 'bic', 'mvn')
SHIFTS = ('lsl', 'lsr', 'asr', 'ror')


def decode_dataproc(word, address):
    """Spell a data-processing word LLVM's objdump leaves as ``<unknown>``.

    The pinned objdump declines two plain ARMv5 encodings in this population: the
    register-shifted-register data-processing forms (``and r1, r1, r0, lsl r2``)
    and the multiply family (``mla r1, r0, r2, r1``). Both are ordinary ARM words
    and the assembler accepts the spelling, so decode them here rather than
    dropping a row that is otherwise transcribable.
    """
    condition = CONDITIONS_FULL[word >> 28]
    sets = bool(word & 0x00100000)
    if (word & 0x0F000000) == 0 and (word & 0x0F0) == 0x90:
        if word & 0x00800000:
            mnemonic = ('s' if word & 0x00400000 else 'u') + \
                ('mlal' if word & 0x00200000 else 'mull')
            if condition != 'al':
                mnemonic += condition
            return mnemonic, 'r%d, r%d, r%d, r%d' % (
                (word >> 12) & 0xF, (word >> 16) & 0xF, word & 0xF, (word >> 8) & 0xF)
        mnemonic = 'mla' if word & 0x00200000 else 'mul'
        if sets:
            mnemonic += 's'
        if condition != 'al':
            mnemonic += condition
        if mnemonic.startswith('mla'):
            return mnemonic, 'r%d, r%d, r%d, r%d' % (
                (word >> 16) & 0xF, word & 0xF, (word >> 8) & 0xF, (word >> 12) & 0xF)
        return mnemonic, 'r%d, r%d, r%d' % (
            (word >> 16) & 0xF, word & 0xF, (word >> 8) & 0xF)
    if (word & 0x0C000000) != 0:
        return None
    opcode = (word >> 21) & 0xF
    rn = (word >> 16) & 0xF
    rd = (word >> 12) & 0xF
    mnemonic = DATAPROC[opcode]
    if sets and mnemonic not in ('tst', 'teq', 'cmp', 'cmn'):
        mnemonic += 's'
    if condition != 'al':
        mnemonic += condition
    if opcode in (13, 15) or opcode in (8, 9, 10, 11):
        left = 'r%d' % rd
    else:
        left = 'r%d, r%d' % (rd, rn)
    if word & 0x02000000:
        rotate = ((word >> 8) & 0xF) * 2
        value = word & 0xFF
        value = ((value >> rotate) | (value << (32 - rotate))) & 0xFFFFFFFF if rotate else value
        operand = '#0x%x' % value
    elif word & 0x10:
        shift = SHIFTS[(word >> 5) & 3]
        operand = 'r%d, %s r%d' % (word & 0xF, shift, (word >> 8) & 0xF)
    else:
        shift = SHIFTS[(word >> 5) & 3]
        amount = (word >> 7) & 0x1F
        if shift == 'ror' and amount == 0:
            operand = 'r%d, rrx' % (word & 0xF)
        elif amount:
            operand = 'r%d, %s #%d' % (word & 0xF, shift, amount)
        else:
            operand = 'r%d' % (word & 0xF)
    if left:
        return mnemonic, '%s, %s' % (left, operand)
    return mnemonic, operand


def branch_target(mnemonic, operands):
    if not mnemonic.startswith('b'):
        return None
    match = BRANCH.match(ANNOTATION.sub('', operands).strip())
    return int(match.group(1), 16) if match else None


def symbol_for(value, functions, span):
    """Name a pool word by what it points at (the image word is the evidence).

    Only a word that lands inside the module image is an address. A magic
    constant (``0x88888889``, a division multiplier) stays a numeric literal: it
    would be a lie to call it ``native_data_88888889``.
    """
    if value & 1 and (value - 1) in functions:
        return 'native_fn_%08x' % (value - 1), 1
    if value in functions:
        return 'native_fn_%08x' % value, 0
    if span[0] <= value < span[1]:
        return 'native_data_%08x' % value, 0
    return None, 0


def ledger_rows():
    for line in (ROOT / 'ledger/functions.jsonl').open(encoding='utf-8'):
        if line.strip():
            yield json.loads(line)


def row_for(module, address):
    for candidate in ledger_rows():
        if candidate['module'] == module and int(candidate['address'], 16) == address:
            return candidate
    return None


def emit(module, row, purpose, unknowns):
    image_path, base = disasm.module_image(ROOT, module)
    image = image_path.read_bytes()
    offset = int(row['binaryOffset'])
    size = int(row['bytes'])
    address = int(row['address'], 16)
    code = image[offset:offset + size]
    mode = row['mode']
    slots = arm_literal_slots(code, address) if mode == 'arm' else thumb_literal_slots(code, address)
    inside = {address + at: slot for at, slot in slots.items()
              if address <= slot < address + size}
    code_end = min(inside.values()) if inside else address + size
    code_size = code_end - address
    instructions = parse(disasm.disassemble(ROOT, module, address, code_size, mode))
    if not instructions:
        raise SystemExit('no instructions decoded')
    functions = {int(item['address'], 16) for item in ledger_rows()
                 if item['module'] == module}
    labels = {}
    for at, mnemonic, operands in instructions:
        target = branch_target(mnemonic, operands)
        if target is not None and address <= target < code_end:
            labels.setdefault(target, '%s_%08x_L%x' % (module.replace('-', '_'), address,
                                                       target - address))
    # Two pool slots holding the same value need distinct symbols: the assembler
    # would otherwise deduplicate one expression into a single slot.
    occurrences = {}
    for at in sorted(inside):
        value = int.from_bytes(image[inside[at] - base:inside[at] - base + 4], 'little')
        occurrences.setdefault(value, []).append(inside[at])
    slot_alias = {}
    for value, slots_for_value in occurrences.items():
        for index, slot in enumerate(slots_for_value):
            slot_alias[slot] = index
    body = []
    symbols = []
    for at, mnemonic, operands in instructions:
        if at >= code_end:
            break
        if at in labels:
            body.append('%s:' % labels[at])
        if at in inside:
            slot = inside[at]
            value = int.from_bytes(image[slot - base:slot - base + 4], 'little')
            name, addend = symbol_for(value, functions, (base, base + len(image)))
            if name is None:
                expression = '0x%08x' % value
            else:
                index = slot_alias[slot]
                if index:
                    name = name.replace('native_data_', 'native_data%d_' % (index + 1), 1) \
                        if name.startswith('native_data') else \
                        name.replace('native_fn_', 'native_fn%d_' % (index + 1), 1)
                expression = '%s+%d' % (name, addend) if addend else name
            if expression not in symbols:
                symbols.append(expression)
            destination = operands.split(',')[0].strip()
            body.append('    %s %s, =%s' % (mwcc_mnemonic(mnemonic), destination, expression))
            continue
        if mnemonic == '<unknown>':
            word = int.from_bytes(image[offset + (at - address):][:4], 'little')
            decoded = decode_dataproc(word, address)
            if decoded is None:
                raise SystemExit('undecodable word %08x at %08x' % (word, at))
            mnemonic, operands = decoded
        if mnemonic.startswith(('push', 'pop')):
            root, condition = split_condition(mnemonic)
            registers = operands.strip('{} ')
            if root == 'push':
                body.append('    stm%sdb sp!, {%s}' % (condition, registers))
            else:
                body.append('    ldm%sia sp!, {%s}' % (condition, registers))
            continue
        if mnemonic in ('lsl', 'lsr', 'asr', 'ror',
                        'lsls', 'lsrs', 'asrs', 'rors'):
            shift = mnemonic[:-1] if mnemonic.endswith('s') else mnemonic
            set_s = 's' if mnemonic.endswith('s') else ''
            left, rest = operands.split(',', 1)
            source = rest.split(',', 1)[0].strip()
            body.append('    mov%s %s, %s, %s %s' % (set_s, left, source, shift,
                                                     rest.split(',', 1)[1].strip()))
            continue
        spelled = mwcc_mnemonic(mnemonic)
        target = branch_target(mnemonic, operands)
        if target is not None:
            destination = labels.get(target, 'native_fn_%08x' % target)
            body.append('    %s %s' % (spelled, destination))
            if not destination.startswith('native_fn'):
                continue
            symbols.append('native_fn_%08x' % target)
            continue
        body.append('    %s %s' % (spelled, operands))
    stores = sum(1 for at, mnemonic, _operands in instructions
                 if mnemonic.startswith('str') and at < code_end)
    shape, described = describe(parse(disasm.disassemble(ROOT, module, address, size, mode)),
                                address, address + size)
    if purpose is None:
        purpose = described
    header = ['/* %s row 0x%08x: %d bytes.' % (module, address, size), ' *',
              ' * What it does: %s' % purpose, ' *',
              ' * Decoded shape: %s.' % shape, ' *']
    seen_slots = set()
    for at in sorted(inside):
        slot = inside[at]
        if slot in seen_slots:
            continue
        seen_slots.add(slot)
        value = int.from_bytes(image[slot - base:slot - base + 4], 'little')
        name, addend = symbol_for(value, functions, (base, base + len(image)))
        labelled = 'constant 0x%08x' % value if name is None else \
            name + ('+%d' % addend if addend else '')
        header.append(' *   pool +0x%02x -> %s (image word 0x%08x)' % (
            slot - address, labelled, value))
    for at, mnemonic, operands in instructions:
        target = branch_target(mnemonic, operands)
        if target is not None and address <= target < code_end:
            header.append(' *   %s +0x%02x -> +0x%02x' % (
                'back edge' if target < at else 'branch', at - address, target - address))
    for at, mnemonic, operands in instructions:
        if at >= code_end:
            continue
        if mnemonic.startswith(('cmp', 'tst')):
            header.append(' *   test +0x%02x %s %s' % (at - address, mnemonic, operands))
    header.append(' *   %d store instruction(s)' % stores)
    header.append(' *')
    header.append(' * Body: the measured instruction stream transcribed from')
    header.append(' * %s at 0x%08x; the literal pool and' % (image_path.name, address))
    header.append(' * every branch target are read from the image, not guessed.')
    header.append(' *')
    header.append(' * Unknowns: %s' % unknowns)
    header.append(' */')
    externs = []
    for expression in symbols:
        name = expression.partition('+')[0]
        if not name.startswith('native_'):
            continue
        line = ('extern void %s(void);' % name) if name.startswith('native_fn') \
            else ('extern u8 %s[];' % name)
        if line not in externs:
            externs.append(line)
    signature = 'asm u32 native_%s_%08x (register u32 a0)' % (module.replace('-', '_'), address)
    return ('\n'.join(header) + '\n' + TYPES + '\n' + '\n'.join(externs) +
            ('\n\n\n' if externs else '\n\n') + signature + '\n{\n' +
            '\n'.join(body) + '\n}\n')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--module', required=True)
    parser.add_argument('--address', required=True)
    parser.add_argument('--purpose', default='Copies a measured block.')
    parser.add_argument('--unknowns', default='the meaning of the fields, blocks and callee '
                                              'contracts the body touches is not established '
                                              'by byte identity.')
    parser.add_argument('--output', type=Path, default=None)
    args = parser.parse_args(argv)
    address = int(args.address, 0)
    row = row_for(args.module, address)
    if row is None:
        raise SystemExit('row not in the ledger')
    text = emit(args.module, row, args.purpose, args.unknowns)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding='ascii')
        print('written %s' % args.output)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == '__main__':
    sys.exit(main())
