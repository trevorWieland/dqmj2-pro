"""Generate exact ov000 sources from the measured instruction stream.

The generator has two modes, both driven by the ledger row and the overlay image
rather than by any hand transcription:

``asm``
    Emit the measured instruction stream as an mwccarm ``asm`` function (the
    verified-assembly form).  Every literal-pool address becomes a
    ``native_fn_<addr>`` / ``native_data_<addr>`` symbol, every call target a
    named symbol and every intra-row branch a label.  This is the fallback the
    round-6 assembly sweep proved: when C resists a row, transcribe the measured
    stream instead of guessing another source form.

``c``
    Instantiate a donor template read from one representative of a
    coarse-skeleton cluster.  The template is stored in :data:`TEMPLATES` and is
    filled with image-decoded immediates, symbols and call targets.  A template
    is only used for a row whose instruction skeleton the representative
    established (see ``docs/authoring/2026-11-12-ov000-gen1.md``).

Nothing in either mode is allowed to guess an address: pool words, call targets
and branch destinations are read from ``extract/arm9_overlays/ov000.bin``.

    python ops/gen_ov000_gen1.py --list
    python ops/gen_ov000_gen1.py --write
    python ops/gen_ov000_gen1.py --write --only 0x21dfd80
"""
import argparse
import json
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'public_tools'))

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM  # noqa: E402

MODULE = 'ov000'
BASE = 0x021D7240
IMAGE_PATH = ROOT / 'extract/arm9_overlays/ov000.bin'
LANE = 'src/ov000/g1_ov000_gen1'
ASM_DIR = LANE + '/asm'

CONDITIONS = ('eq', 'ne', 'cs', 'cc', 'hs', 'lo', 'mi', 'pl', 'vs', 'vc',
              'hi', 'ls', 'ge', 'lt', 'gt', 'le')
BRANCH = re.compile(r'^#(0x[0-9a-fA-F]+)$')
PC_LITERAL = re.compile(r'\[pc, #(-?0x[0-9a-fA-F]+)\]')
MEMORY = re.compile(r'\[[^\]]+\]')

MD = Cs(CS_ARCH_ARM, CS_MODE_ARM)
MD.detail = False


# --------------------------------------------------------------------------- data


def load_ledger():
    rows = {}
    for line in (ROOT / 'ledger/functions.jsonl').open(encoding='utf-8'):
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get('module') == MODULE:
            rows[int(row['address'], 0)] = row
    return rows


LEDGER = load_ledger()
IMAGE = IMAGE_PATH.read_bytes()
# Function addresses per module.  Every overlay loads at 0x021d7240, so a global
# address set would call an ov000 data word a function whenever a different
# overlay has code there; the pool symbol is resolved in the module whose range
# contains the word instead.
MODULE_FUNCTIONS = {}
for _line in (ROOT / 'ledger/functions.jsonl').open(encoding='utf-8'):
    if _line.strip():
        _row = json.loads(_line)
        if _row.get('bytes'):
            MODULE_FUNCTIONS.setdefault(_row['module'], set()).add(int(_row['address'], 0))


def row_bytes(row):
    offset = int(row['binaryOffset'])
    return IMAGE[offset:offset + int(row['bytes'])]


def instructions(row):
    address = int(row['address'], 0)
    data = row_bytes(row)
    decoded = list(MD.disasm(data, address))
    if sum(item.size for item in decoded) != len(data):
        raise SystemExit(f'{address:#x}: instruction stream does not cover the row')
    return decoded


# ------------------------------------------------------------------- asm emitter


def address_like(value):
    return (0x01FF8000 <= value < 0x02000000          # ITCM
            or 0x02000000 <= value < 0x02400000        # main RAM / overlays
            or 0x027C0000 <= value < 0x027E4000        # DTCM
            or 0x037F8000 <= value < 0x03810000        # ARM7 WRAM
            or 0x04000000 <= value < 0x05000000        # MMIO
            or 0x06000000 <= value < 0x07000000)       # VRAM


def pool_expression(value, row_address):
    """Render a measured literal word as the strongest expression we can verify."""
    if BASE <= value < BASE + 0x100000:
        functions = MODULE_FUNCTIONS.get(MODULE, set())
        if value in functions:
            return f'native_fn_{value:08x}'
        if value & 1 and (value & ~1) in functions:
            return f'native_fn_{value & ~1:08x} + 1'
        if value & 1:
            return f'0x{value:08x}'
        return f'native_data_{value:08x}'
    if 0x02000000 <= value < BASE:
        functions = MODULE_FUNCTIONS.get('main', set())
        if value in functions:
            return f'native_fn_{value:08x}'
        return f'native_data_{value:08x}'
    if value & 1:
        return f'0x{value:08x}'
    if address_like(value):
        return f'native_data_{value:08x}'
    return f'0x{value:08x}'


# Mnemonics whose trailing ``s`` is the flag-setting suffix, not the VS condition.
FLAG_SET_MNEMONICS = frozenset((
    'movs', 'adds', 'subs', 'rsbs', 'adcs', 'sbcs', 'rscs', 'ands', 'orrs',
    'eors', 'bics', 'muls', 'mlas', 'umulls', 'smulls', 'tsts', 'cmps', 'cmns',
    'mvns',
))


def split_condition(mnemonic):
    if mnemonic in FLAG_SET_MNEMONICS:
        return mnemonic, ''
    if len(mnemonic) > 2 and mnemonic[-2:] in CONDITIONS:
        return mnemonic[:-2], mnemonic[-2:]
    return mnemonic, ''


def reorder_ldm(mnemonic):
    """``ldmiane`` -> ``ldmneia``; mwccarm wants the condition before the mode."""
    base, cond = split_condition(mnemonic)
    match = re.match(r'^(ldm|stm)(ia|ib|da|db)?$', base)
    if not match:
        return None
    root, mode = match.group(1), match.group(2) or 'ia'
    return f'{root}{cond}{mode}'


def reorder_width(mnemonic):
    """``ldrbeq`` -> ``ldreqb``; mwccarm wants the condition before the width."""
    base, cond = split_condition(mnemonic)
    match = re.match(r'^(ldr|str)(b|h|sb|sh|d)?$', base)
    if not match or not cond:
        return None
    return f'{match.group(1)}{cond}{match.group(2) or ""}'


def translate(insn, row_address, row_size, labels):
    """Return (text, symbols) for one instruction."""
    mnemonic = insn.mnemonic
    operands = insn.op_str
    address = insn.address
    base, cond = split_condition(mnemonic)

    # pop/push aliases: mwccarm spells them as block transfers.
    if base == 'pop':
        symbols = set()
        return f'ldm{cond}ia sp!, {operands}', symbols
    if base == 'push':
        return f'stm{cond}db sp!, {operands}', set()

    # ldm/stm: condition belongs between the root and the addressing mode.
    grouped = reorder_ldm(mnemonic)
    if grouped is not None:
        return f'{grouped} {operands}', set()

    # byte/halfword/signed loads and stores: condition belongs before the width.
    width_form = reorder_width(mnemonic)
    if width_form is not None and not (base in ('ldr',) and '[pc' in operands):
        return f'{width_form} {operands}', set()

    # branches (check bl/bx before the b<cond> case: ``bls`` is b+ls, not bl+s).
    if mnemonic in ('bl', 'blx'):
        match = BRANCH.match(operands)
        if not match:
            raise SystemExit(f'{address:#x}: indirect {mnemonic}')
        target = int(match.group(1), 16)
        return f'{mnemonic} native_fn_{target:08x}', {f'native_fn_{target:08x}'}
    if mnemonic == 'bx' or (base == 'bx' and cond):
        return f'{mnemonic} {operands}', set()
    if mnemonic == 'b':
        return _branch('b', operands, address, row_address, row_size, labels)
    if mnemonic.startswith('b') and mnemonic[1:] in CONDITIONS:
        return _branch(mnemonic, operands, address, row_address, row_size, labels)

    # PC-relative literal loads: name the measured pool word.
    if base in ('ldr', 'ldrb', 'ldrh', 'ldrsb', 'ldrsh') and '[pc' in operands:
        match = PC_LITERAL.search(operands)
        if not match:
            raise SystemExit(f'{address:#x}: unparsed pc literal {operands!r}')
        literal_address = address + 8 + int(match.group(1), 0)
        literal_offset = literal_address - BASE
        offset = literal_address - row_address
        if not 0 <= offset <= row_size - 4:
            raise SystemExit(f'{address:#x}: pool word {literal_address:#x} is outside the row')
        value = int.from_bytes(IMAGE[literal_offset:literal_offset + 4], 'little')
        expression = pool_expression(value, row_address)
        symbols = set()
        if not expression.startswith('0x'):
            symbol = expression.split(' ')[0]
            symbols.add(symbol)
        return f'{mnemonic} {operands[:match.start()]}={expression}', symbols

    # Standalone shifts are not mwccarm mnemonics; spell them as mov.
    shifts = ('lsl', 'lsr', 'asr', 'ror', 'rrx')
    shift = base
    flag = ''
    if shift not in shifts and shift.endswith('s') and shift[:-1] in shifts:
        shift, flag = shift[:-1], 's'
    if shift in shifts:
        parts = [part.strip() for part in operands.split(',')]
        if len(parts) == 3:
            return f'mov{cond}{flag} {parts[0]}, {parts[1]}, {shift} {parts[2]}', set()
        if len(parts) == 2:
            return f'mov{cond}{flag} {parts[0]}, {parts[0]}, {shift} {parts[1]}', set()

    return f'{mnemonic} {operands}'.rstrip(), set()


def _branch(mnemonic, operands, address, row_address, row_size, labels):
    match = BRANCH.match(operands)
    if not match:
        raise SystemExit(f'{address:#x}: indirect branch')
    target = int(match.group(1), 16)
    if row_address <= target < row_address + row_size:
        labels.add(target)
        return f'{mnemonic} ov000_{row_address:08x}_L{target - row_address:03x}', set()
    return f'{mnemonic} native_fn_{target:08x}', {f'native_fn_{target:08x}'}


def pool_slots(decoded, address, size):
    """Byte ranges of the row that are literal-pool data, not instructions."""
    slots = set()
    for insn in decoded:
        if '[pc' not in insn.op_str:
            continue
        match = PC_LITERAL.search(insn.op_str)
        if not match:
            continue
        literal = insn.address + 8 + int(match.group(1), 0)
        if address <= literal < address + size:
            slots.add(literal)
    return slots


def branch_labels(decoded, address, size):
    labels = set()
    for insn in decoded:
        mnemonic = insn.mnemonic
        if mnemonic in ('bl', 'blx', 'bx'):
            continue
        if not (mnemonic == 'b' or (mnemonic.startswith('b')
                                    and mnemonic[1:] in CONDITIONS)):
            continue
        match = BRANCH.match(insn.op_str)
        if match:
            target = int(match.group(1), 16)
            if address <= target < address + size:
                labels.add(target)
    return labels


def emit_asm(row):
    address = int(row['address'], 0)
    size = int(row['bytes'])
    decoded = instructions(row)
    slots = pool_slots(decoded, address, size)
    decoded = [insn for insn in decoded if insn.address not in slots]
    labels = branch_labels(decoded, address, size)
    body = []
    symbols = set()
    for insn in decoded:
        if insn.address in labels:
            body.append(f'ov000_{address:08x}_L{insn.address - address:03x}:')
        text, used = translate(insn, address, size, labels)
        symbols |= used
        body.append('    ' + text)
    externs = []
    for symbol in sorted(symbols):
        if symbol.startswith('native_data_'):
            externs.append(f'extern u8 {symbol}[];')
        else:
            externs.append(f'extern void {symbol}(void);')
    header = [
        f'/* ov000 row 0x{address:08x}: {size} bytes.',
        ' *',
        f' * What it does: {describe(row, decoded)}',
        ' *',
        ' * Body: the measured instruction stream transcribed from',
        f' * extract/arm9_overlays/ov000.bin at 0x{address:08x}; every literal pool',
        ' * word and branch target is read from the image, not guessed.',
        ' *',
        ' * Unknowns: the meaning of the fields, blocks and callee contracts',
        ' * the body touches is not established by byte identity.',
        ' */',
        'typedef unsigned int u32;',
        'typedef signed int s32;',
        'typedef unsigned short u16;',
        'typedef signed short s16;',
        'typedef unsigned char u8;',
        'typedef signed char s8;',
        '',
    ]
    if externs:
        header += externs + ['']
    header += ['', f'asm u32 native_{MODULE}_{address:08x} (register u32 a0)', '{']
    return '\n'.join(header + body + ['}', ''])


def describe(row, decoded):
    calls = sum(1 for item in decoded if item.mnemonic in ('bl', 'blx'))
    loads = sum(1 for item in decoded if item.mnemonic.startswith('ldr'))
    stores = sum(1 for item in decoded if item.mnemonic.startswith('str'))
    branches = sum(1 for item in decoded if item.mnemonic.startswith('b')
                   and item.mnemonic not in ('bl', 'bx', 'blx'))
    parts = [f'{len(decoded)} instructions']
    if calls:
        parts.append(f'{calls} call(s)')
    if loads or stores:
        parts.append(f'{loads} load(s), {stores} store(s)')
    if branches:
        parts.append(f'{branches} branch(es)')
    return ', '.join(parts) + '.'


# --------------------------------------------------------------------- assembly


# Rows emitted as assembly: the parked backlog that C has not matched.  The
# skeletons in this set are the small straight-line and simple-loop bodies; the
# C clusters live in C_ROWS below.
ASM_ROWS = (
    0x021DFD80, 0x0222B7B4, 0x0220A4B4, 0x021F65E4, 0x02215984,
    0x021F83E0, 0x02204CF0, 0x02212148, 0x02227E80, 0x02227EBC,
    0x021E96CC, 0x021E7AA8, 0x021E6B64,
    0x021E6BF4, 0x021F3D2C, 0x02222F70, 0x02222FB8, 0x021F95C8,
    0x021FB8A8, 0x0221F3F4, 0x02223190, 0x02225738, 0x02227648,
    0x021FDF44, 0x021FF478, 0x021E70B0, 0x021EB720, 0x021F7278,
    0x021FDED0, 0x02210C34, 0x021E7108, 0x022163A4, 0x021F8D28,
)

# C clusters: representatives read from the measured stream, then instantiated
# from the image-decoded parameters.  Five skeletons were found; four converged
# to exact C.  The 144-byte nested-guard scan (F3) did not reproduce the
# original allocation and is parked in the report, not guessed at.  F4 ships two
# of three rows: the source-first screen found 0x0221221c already defined.
C_ROWS = (
    (0x021EBD88, 'f1'), (0x021EF620, 'f1'), (0x021F2CBC, 'f1'),
    (0x0221C6F0, 'f1'), (0x0222B1E4, 'f1'),
    (0x021EB654, 'f2'), (0x021ECF88, 'f2'), (0x021F1018, 'f2'), (0x0222ABF4, 'f2'),
    (0x0221225C, 'f4'), (0x0221229C, 'f4'),
    (0x02213E10, 'f7'), (0x02213E7C, 'f7'), (0x02213EE4, 'f7'),
)

C_HEADER = '''typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

'''


def code_instructions(row):
    decoded = instructions(row)
    slots = pool_slots(decoded, int(row['address'], 0), int(row['bytes']))
    return [insn for insn in decoded if insn.address not in slots]


def bl_targets(row):
    return [int(BRANCH.match(insn.op_str).group(1), 16)
            for insn in code_instructions(row) if insn.mnemonic == 'bl']


def pool_words(row):
    values = []
    for insn in code_instructions(row):
        match = PC_LITERAL.search(insn.op_str)
        if match:
            literal = insn.address + 8 + int(match.group(1), 0)
            offset = literal - BASE
            values.append(int.from_bytes(IMAGE[offset:offset + 4], 'little'))
    return values


def first_pool_word(row):
    values = pool_words(row)
    return values[0] if values else None


def immediate_after(decoded, mnemonic):
    values = []
    for insn in decoded:
        if insn.mnemonic == mnemonic:
            match = re.search(r'#(0x[0-9a-fA-F]+|\d+)', insn.op_str)
            if match:
                values.append(int(match.group(1), 0))
    return values


def offset_in(decoded, pattern):
    regex = re.compile(pattern)
    for insn in decoded:
        match = regex.search(insn.mnemonic + ' ' + insn.op_str)
        if match:
            return int(match.group(1), 0)
    raise SystemExit('template parameter not found: ' + pattern)


def render_f1(row):
    """Table-driven stat update over 0x15 three-byte configuration rows; 104 bytes."""
    address = int(row['address'], 0)
    decoded = code_instructions(row)
    calls = bl_targets(row)
    if len(calls) != 1:
        raise SystemExit(f'{address:#x}: f1 expects 1 call, saw {len(calls)}')
    cfg, stride = pool_words(row)
    bound = offset_in(decoded, r'cmp r4, #(0x[0-9a-fA-F]+|\d+)')
    cfg_step = offset_in(decoded, r'add r5, r5, #(0x[0-9a-fA-F]+|\d+)')
    stride_step = offset_in(decoded, r'add r6, r6, #(0x[0-9a-fA-F]+|\d+)') // 4
    externs = [f'extern u8 native_data_{cfg:08x}[];',
               f'extern u8 native_data_{stride:08x}[];',
               f'extern s32 native_fn_{calls[0]:08x}(u32 *, s32, u32, u32, u32);']
    body = f'''void native_ov000_{address:08x}(u32 *table)
{{
    s32 i = 0;
    u8 *cfg = native_data_{cfg:08x};
    u32 *stride = (u32 *)native_data_{stride:08x};

    do {{
        u32 idx = cfg[2];

        table[idx] += native_fn_{calls[0]:08x}(stride, (s8)cfg[0], cfg[1], idx, table[idx]);
        cfg += {cfg_step};
        stride += {stride_step};
    }} while (++i < 0x{bound:x});
}}
'''
    return comment(address, row, 'table-driven stat update over three-byte configuration rows.') + \
        C_HEADER + '\n'.join(externs) + '\n\n' + body


def render_f2(row):
    """32-byte buffer clear, then seven fixed calls; 104 bytes."""
    address = int(row['address'], 0)
    decoded = code_instructions(row)
    calls = bl_targets(row)
    if len(calls) != 7:
        raise SystemExit(f'{address:#x}: f2 expects 7 calls, saw {len(calls)}')
    pool = first_pool_word(row)
    size = offset_in(decoded, r'sub sp, sp, #(0x[0-9a-fA-F]+)')
    count = immediate_after(decoded, 'mov')[0]
    externs = [f'extern u8 native_data_{pool:08x}[];',
               f'extern void native_fn_{calls[0]:08x}(u8 *, u8 *);',
               f'extern void native_fn_{calls[1]:08x}(u8 *);']
    externs += [f'extern void native_fn_{target:08x}(void);' for target in calls[2:6]]
    externs += [f'extern void native_fn_{calls[6]:08x}(u32);']
    body = f'''void native_ov000_{address:08x}(void)
{{
    u8 buf[0x{size:x}];
    s32 n;
    u8 *p = buf;

    n = {count};
    do {{
        p[0] = 0;
        p[1] = 0;
        p[2] = 0;
        p[3] = 0;
        p += 4;
    }} while (--n != 0);
    native_fn_{calls[0]:08x}(buf, native_data_{pool:08x});
    native_fn_{calls[1]:08x}(buf);
    native_fn_{calls[2]:08x}();
    native_fn_{calls[3]:08x}();
    native_fn_{calls[4]:08x}();
    native_fn_{calls[5]:08x}();
    native_fn_{calls[6]:08x}(2);
}}
'''
    return comment(address, row, '32-byte clear loop plus seven fixed calls.') + C_HEADER + \
        '\n'.join(externs) + '\n\n' + body


def render_f4(row):
    """Two signed-16 arguments narrowed, then two guard calls; 64 bytes."""
    address = int(row['address'], 0)
    calls = bl_targets(row)
    if len(calls) != 2:
        raise SystemExit(f'{address:#x}: f4 expects 2 calls, saw {len(calls)}')
    externs = [f'extern s32 native_fn_{calls[0]:08x}(s32, s32);',
               f'extern s32 native_fn_{calls[1]:08x}(s32, u32);']
    body = f'''u32 native_ov000_{address:08x}(u32 a, u32 b, u32 c)
{{
    s32 ok = 0;
    s32 t = native_fn_{calls[0]:08x}((s16)a, (s16)b);

    if (t != 0) {{
        if (native_fn_{calls[1]:08x}(t, c) != 0) {{
            ok = 1;
        }}
    }}
    return ok;
}}
'''
    return comment(address, row, 'narrow two signed halves, then two guard calls.') + \
        C_HEADER + '\n'.join(externs) + '\n\n' + body


def render_f7(row):
    """Strided record lookup, one guard call, one helper and a byte store; 104/108 B."""
    address = int(row['address'], 0)
    decoded = code_instructions(row)
    calls = bl_targets(row)
    if len(calls) != 3:
        raise SystemExit(f'{address:#x}: f7 expects 3 calls, saw {len(calls)}')
    pool = first_pool_word(row)
    field = offset_in(decoded, r'ldrb r0, \[r6, #(0x[0-9a-fA-F]+)\]')
    store = offset_in(decoded, r'strb r0, \[r6, #(0x[0-9a-fA-F]+)\]')
    dst = offset_in(decoded, r'add r1, r4, #(0x[0-9a-fA-F]+)')
    word = offset_in(decoded, r'ldr r0, \[r0, #(0x[0-9a-fA-F]+)\]')
    shift = offset_in(decoded, r'lsl #(0x[0-9a-fA-F]+|\d+)')
    four_arguments = any(insn.mnemonic == 'mov' and insn.op_str.replace(' ', '') == 'r3,r2'
                         for insn in decoded)
    proto = f'extern void native_fn_{calls[2]:08x}(u8 *, u8 *, u32, u32);' if four_arguments \
        else f'extern void native_fn_{calls[2]:08x}(u8 *, u8 *, u32);'
    call = f'native_fn_{calls[2]:08x}(e, p + 0x{dst:x} + (slot << {shift}), 0, 0);' \
        if four_arguments else f'native_fn_{calls[2]:08x}(e, p + 0x{dst:x} + (slot << {shift}), 0);'
    externs = [f'extern u8 native_data_{pool:08x}[];',
               f'extern u8 *native_fn_{calls[0]:08x}(u32);',
               f'extern s32 native_fn_{calls[1]:08x}(u8 *, u32);', proto]
    body = f'''u32 native_ov000_{address:08x}(u32 index, u32 slot)
{{
    u32 ok = 0;
    u8 *e = native_data_{pool:08x} + index * 0x10c;
    u8 *p = native_fn_{calls[0]:08x}(e[0x{field:x}]);

    if (native_fn_{calls[1]:08x}(p, slot) != 0) {{
        {call}
        e[0x{store:x}] = *(u32 *)(p + 0x{word:x} + (slot << {shift}));
        ok = 1;
    }} else {{
        e[0x{store:x}] = 0;
    }}
    return ok;
}}
'''
    return comment(address, row, 'strided record lookup, guard call, helper and byte store.') + \
        C_HEADER + '\n'.join(externs) + '\n\n' + body


C_TEMPLATES = {'f1': render_f1, 'f2': render_f2, 'f4': render_f4, 'f7': render_f7}


def comment(address, row, what):
    return (f'/* ov000 row 0x{address:08x}: {int(row["bytes"])} bytes.\n'
            ' *\n'
            f' * What it does: {what}\n'
            ' *\n'
            ' * Generated by ops/gen_ov000_gen1.py from the measured instruction\n'
            f' * stream at 0x{address:08x}; every call target, pool word and immediate\n'
            ' * is decoded from extract/arm9_overlays/ov000.bin, not guessed.\n'
            ' *\n'
            ' * Unknowns: the meaning of the fields and callee contracts is not\n'
            ' * established by byte identity.\n'
            ' */\n')


def write_all(only=None):
    written = []
    for address in ASM_ROWS:
        if only and address not in only:
            continue
        row = LEDGER.get(address)
        if row is None:
            raise SystemExit(f'{address:#x}: no ledger row')
        text = emit_asm(row)
        path = ROOT / ASM_DIR / f'native_{MODULE}_{address:08x}.c'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='ascii')
        written.append(path)
    for address, template_id in C_ROWS:
        if only and address not in only:
            continue
        row = LEDGER.get(address)
        if row is None:
            raise SystemExit(f'{address:#x}: no ledger row')
        text = C_TEMPLATES[template_id](row)
        path = ROOT / LANE / f'native_{MODULE}_{address:08x}.c'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='ascii')
        written.append(path)
    return written


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--only', nargs='*', default=None)
    args = parser.parse_args(argv)
    only = {int(value, 0) for value in args.only} if args.only else None
    if args.list:
        for address in ASM_ROWS:
            row = LEDGER[address]
            print(f'{address:#010x} {row["bytes"]:4d} B asm')
        for address, template_id in C_ROWS:
            row = LEDGER[address]
            print(f'{address:#010x} {row["bytes"]:4d} B c:{template_id}')
        return 0
    if args.write:
        for path in write_all(only):
            print(path.relative_to(ROOT).as_posix())
        return 0
    parser.print_help()
    return 1


if __name__ == '__main__':
    sys.exit(main())
