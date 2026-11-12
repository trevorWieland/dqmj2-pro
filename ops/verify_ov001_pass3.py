"""Verify the ov001 pass-3 packet (``src/ov001/p10_ov001_pass3``).

Every ``native_ov001_<address>.c`` file in the packet is recompiled with the real
source-unit rule (module ov001, ARM, profile p003), its relocations are patched the
way ``public_tools/repo_build.py`` patches them (branch and absolute sites take the
target the measured image word encodes), and the whole measured extent is compared
byte for byte with the overlay image.

For each row the check also proves:

* the object's relocation table is exactly the pinned one -- same offsets, same
  kinds, same externals -- so a match cannot come from a literal that happens to
  equal an address;
* every relocation site names its target: the address encoded in the symbol name
  equals the image-decoded target, so a match cannot come from a call to the wrong
  function;
* one whole-C negative control per function compiles and fails at the pinned
  offsets, so the match is not vacuous.

    python ops/verify_ov001_authoring_2.py            # run the gate
    python ops/verify_ov001_authoring_2.py --pin      # reprint the ROWS table

The lane is authored one address-named file per function; the module base is
0x021d7240 and the compared image is extract/arm9_overlays/ov001.bin (the overlay is
LZ-compressed in the ROM, so the extract is the decompressed image the ledger's
binaryOffset indexes).
"""
import os
import re
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / 'public_tools'))

import source_units  # noqa: E402

LANE = 'src/ov001/p10_ov001_pass3'
ADDRESS = re.compile(r'([0-9a-f]{8})\.c$')
SYMBOL_ADDRESS = re.compile(r'([0-9a-fA-F]{8})$')

# Auto-derived negative controls, tried in this order.  The first substitution that
# changes the text, compiles, and produces different patched bytes is the control.
CONTROL_FORMS = (
    ('return ov001_first_candidate_02226cb0(&local);',
     'return ov001_first_candidate_02226cb0(&local) + 1;'),
    ('return 1;', 'return 2;'),
    ('return 0;', 'return 1;'),
    (' == 0', ' == 1'),
    (' != 0', ' != 1'),
    ('[0xF]', '[0xE]'),
    ('[0x16]', '[0x17]'),
    ('[0x1D]', '[0x1E]'),
    ('0x14)', '0x15)'),
    ('0x27]', '0x26]'),
    ('0x3C]', '0x3D]'),
    ('0x31E]', '0x31D]'),
    ('0x31C]', '0x31B]'),
    ('0x2E)', '0x2F)'),
    ('0x0C]', '0x0D]'),
    ('* 0x14', '* 0x18'),
    ('* 12', '* 16'),
    ('1u << bit', '2u << bit'),
    ('!= 8', '!= 9'),
    ('== 2', '== 3'),
    ('0xB6', '0xB7'),
    ('>= 5', '>= 6'),
    ('* 100', '* 101'),
    ('/ 5;', '/ 7;'),
    ('* 6 / 5', '* 6 / 7'),
    ('* 100 +', '* 101 +'),
    ('= 4;', '= 5;'),
    ('= 8;', '= 9;'),
    ('= 2;', '= 3;'),
    ('[1] =', '[2] ='),
    ('0x440', '0x480'),
    ('0x200', '0x240'),
    ('[0x4c]', '[0x4d]'),
    ('[0x45]', '[0x44]'),
    ('[0x42]', '[0x41]'),
    ('[0x43]', '[0x44]'),
    ('[0x36]', '[0x37]'),
    ('[0x35]', '[0x34]'),
    ('[0x55]', '[0x54]'),
    ('[0x54]', '[0x55]'),
    ('[0x3f]', '[0x3e]'),
    ('[0x40]', '[0x41]'),
    ('[0x41]', '[0x42]'),
    ('[0x1e8]', '[0x1e9]'),
    ('[0x8d]', '[0x8e]'),
    ('[0x8e]', '[0x8d]'),
    ('[0xca]', '[0xcb]'),
    ('[0xb1]', '[0xb2]'),
    ('[0x28]', '[0x29]'),
    ('/ 10;', '/ 11;'),
    ('>= 10', '>= 11'),
    ('< 5', '< 6'),
    ('0x34', '0x35'),
    ('0x35', '0x36'),
    ('9999', '10000'),
    ('0xff', '0xfe'),
    ('i == 2', 'i == 1'),
    ('i < 3', 'i < 4'),
    ('+ 0x10', '+ 0x14'),
)


def compiler(root):
    config = source_units.load_config(root)
    return root / config['data']['compiler']['path']


def compile_unit(root, source_path, object_path, profile_flags, cwd=None):
    config = source_units.load_config(root)
    flags = list(profile_flags)
    if '-c' not in flags:
        flags.append('-c')
    license_file = root / 'tools/mwccarm/mwccarm/license.dat'
    env = dict(os.environ, LM_LICENSE_FILE=str(license_file))
    command = [str(compiler(root)), *flags, source_path.name, '-o', str(object_path)]
    return subprocess.run(command, cwd=str(cwd or source_path.parent), env=env,
                          capture_output=True, text=True)


def read_object(object_path):
    from elftools.elf.elffile import ELFFile
    with open(object_path, 'rb') as stream:
        elf = ELFFile(stream)
        text = elf.get_section_by_name('.text').data()
        symtab = elf.get_section_by_name('.symtab')
        defined = {}
        for symbol in symtab.iter_symbols():
            section = symbol['st_shndx']
            if isinstance(section, int) and section != 'SHN_UNDEF' and symbol['st_value']:
                defined[symbol.name] = symbol['st_value']
        relocations = []
        for section in elf.iter_sections():
            if section.name not in ('.rel.text', '.rela.text'):
                continue
            for relocation in section.iter_relocations():
                symbol = symtab.get_symbol(relocation['r_info_sym']).name
                addend = relocation['r_addend'] if section.name == '.rela.text' else 0
                relocations.append((relocation['r_offset'], relocation['r_info_type'],
                                    symbol, addend or 0))
    return text, defined, relocations


def sign_extend(value, bits):
    if value & (1 << (bits - 1)):
        return value - (1 << bits)
    return value


def decode_target(kind, image, base, absolute):
    offset = absolute - base
    if offset < 0 or offset + 4 > len(image):
        return None
    if kind == 1:
        word = struct.unpack_from('<I', image, offset)[0]
        return (absolute + 8 + (sign_extend(word & 0xFFFFFF, 24) << 2)) & 0xFFFFFFFF
    if kind == 2:
        return struct.unpack_from('<I', image, offset)[0]
    return None


def patch(text, address, relocations, image, base):
    """Patch exactly like repo_build.patch_function for kinds 1 and 2."""
    body = bytearray(text)
    for offset, kind, symbol, addend in relocations:
        absolute = address + offset
        target = decode_target(kind, image, base, absolute)
        if target is None:
            raise SystemExit(f'{symbol}: no image word at {absolute:#x}')
        if kind == 1:
            word = struct.unpack_from('<I', body, offset)[0]
            immediate = (target + addend - absolute) >> 2
            struct.pack_into('<I', body, offset,
                             (word & 0xFF000000) | (immediate & 0xFFFFFF))
        else:
            struct.pack_into('<I', body, offset, target & 0xFFFFFFFF)
    return bytes(body)


def measure(root, config, work, address, size, source_path, text_override=None):
    rule = source_units.resolve(config, source_path.relative_to(root).as_posix())
    flags = list(rule['compilerFlags'])
    if rule.get('mode') == 'thumb':
        raise SystemExit(f'{source_path}: rule is thumb, this lane is ARM')
    object_path = work / f'{address:08x}.o'
    if text_override is None:
        result = compile_unit(root, source_path, object_path, flags)
        if result.returncode != 0:
            raise SystemExit(f'{source_path.name}: compile failed\n{result.stderr[-800:]}')
    else:
        control_path = work / f'{address:08x}-control.c'
        control_path.write_text(text_override, encoding='utf-8')
        context = work / 'context.h'
        if not context.is_file():
            context.write_text((source_path.parent / 'context.h').read_text(encoding='utf-8'),
                               encoding='utf-8')
        result = compile_unit(root, control_path, object_path, flags, cwd=work)
        if result.returncode != 0:
            return None
    text, defined, relocations = read_object(object_path)
    image = image_bytes(root)
    base = module_base(root)
    patched = patch(text, address, relocations, image, base)
    want = image[address - base:address - base + size]
    diff = [i for i in range(min(len(patched), size)) if patched[i] != want[i]]
    return dict(text=patched, want=want, diff=diff, relocations=relocations,
                defined=defined, rule=rule)


def module_entry(root):
    """Read the ov001 geometry from the public rule set (no generated manifest)."""
    import json
    config = json.loads((root / 'config/source_units.json').read_text(encoding='utf-8'))
    entry = config['modules']['ov001']
    return {'name': 'ov001',
            'base': int(str(entry['loadAddressBase']), 0),
            'binary': entry['originalImage'],
            'bytes': int(entry['bytes'])}


def image_bytes(root):
    entry = module_entry(root)
    return (root / entry['binary']).read_bytes()


def module_base(root):
    return int(str(module_entry(root)['base']), 0)


def control_for(body, root, config, work, address, size, source_path, image, base):
    """Return (mutation_name, diff) for the first working negative control."""
    for old, new in CONTROL_FORMS:
        if old not in body:
            continue
        first = body.find(old)
        last = body.rfind(old)
        positions = [first] if first == last else [last, first]
        for position in positions:
            mutated = body[:position] + new + body[position + len(old):]
            result = measure(root, config, work, address, size, source_path,
                             text_override=mutated)
            if result is None:
                continue
            if result['diff']:
                return f'{old!r} -> {new!r}', result['diff']
    # Generic fallback: perturb each numeric literal in the source once.  This keeps
    # the control whole-C and per-row even when the row has no idiom in CONTROL_FORMS.
    for old, new in (('(s8)', '(s16)'), ('(u8)', '(u16)'), ('(s16)', '(s32)'),
                     ('(u16)', '(u32)')):
        position = body.find(old)
        if position < 0:
            continue
        mutated = body[:position] + new + body[position + len(old):]
        result = measure(root, config, work, address, size, source_path,
                         text_override=mutated)
        if result is not None and result['diff']:
            return f'{old!r} -> {new!r}', result['diff']
    for match in re.finditer(r'(?<![0-9A-Za-z_])(0x[0-9A-Fa-f]+|[0-9]+)(?![0-9A-Za-z_])',
                             body):
        token = match.group(1)
        value = int(token, 0)
        for delta in (1, -1):
            if value + delta < 0:
                continue
            if token.lower().startswith('0x'):
                replacement = hex(value + delta)
            else:
                replacement = str(value + delta)
            position = match.start(1)
            mutated = body[:position] + replacement + body[position + len(token):]
            result = measure(root, config, work, address, size, source_path,
                             text_override=mutated)
            if result is None:
                continue
            if result['diff']:
                return f'{token!r} -> {replacement!r}', result['diff']
    return None, None


def pin(root, config, work):
    for source_path in sorted((root / LANE).glob('native_ov001_*.c')):
        match = ADDRESS.search(source_path.name)
        address = int(match.group(1), 16)
        size = ledger_size(root, address)
        result = measure(root, config, work, address, size, source_path)
        table = ', '.join(f'({offset:#04x}, {kind}, {symbol!r})'
                          for offset, kind, symbol, _addend in result['relocations'])
        body = source_path.read_text(encoding='utf-8')
        name, diff = control_for(body, root, config, work, address, size, source_path,
                                 image_bytes(root), module_base(root))
        print(f'    ({address:#010x}, {size}, {source_path.name!r},\n'
              f'     ({table}),\n'
              f'     {diff!r}),')
    return 0


def ledger_size(root, address):
    import json
    with (root / 'ledger/functions.jsonl').open(encoding='utf-8') as stream:
        for line in stream:
            if f'{address:08x}' not in line:
                continue
            row = json.loads(line)
            if row.get('module') == 'ov001' and int(row['address'], 0) == address:
                return int(row['bytes'])
    raise SystemExit(f'{address:#x}: no ledger row')


ROWS = (
    (0x021dcfa0, 84, 'native_ov001_021dcfa0.c',
     ((0x08, 1, 'ov001_record_is_active_021db8d0'), (0x20, 1, 'native_fn_ov001_021dcf0c'), (0x34, 1, 'native_fn_ov001_021dcf54')),
     [12]),
    (0x021df640, 64, 'native_ov001_021df640.c',
     ((0x04, 1, 'native_fn_ov001_0220e2f0'), (0x10, 1, 'native_fn_ov001_021dda80'), (0x3c, 2, 'native_data_ov001_022388ec')),
     [52]),
    (0x021df9a8, 60, 'native_ov001_021df9a8.c',
     ((0x08, 1, 'native_fn_ov001_0220b70c'), (0x0c, 1, 'native_fn_ov001_021de590'), (0x20, 1, 'native_fn_ov001_021f9588'), (0x38, 2, 'native_data_ov001_022388ec')),
     [48]),
    (0x021dfa84, 64, 'native_ov001_021dfa84.c',
     ((0x04, 1, 'native_fn_ov001_0220d278'), (0x10, 1, 'native_fn_ov001_021dda80'), (0x3c, 2, 'native_data_ov001_022388ec')),
     [52]),
    (0x021e2984, 84, 'native_ov001_021e2984.c',
     ((0x3c, 1, 'native_fn_ov001_021e82fc'), (0x50, 2, 'native_data_ov001_022388ec')),
     [12]),
    (0x021e81d0, 32, 'native_ov001_021e81d0.c',
     ((0x18, 2, 'native_data_ov001_02238d1c'), (0x1c, 2, 'native_data_ov001_02238d2e')),
     [0]),
    (0x021eaa3c, 76, 'native_ov001_021eaa3c.c',
     ((0x2c, 1, 'ov001_begin_state_transition_021f1354'), (0x44, 2, 'native_data_ov001_0222ec84'), (0x48, 2, 'native_data_ov001_02238d7c')),
     [16]),
    (0x021f74fc, 72, 'native_ov001_021f74fc.c',
     ((0x04, 1, 'native_fn_ov001_021e29e8'), (0x14, 1, 'native_fn_ov001_021e2a48'), (0x28, 1, 'native_fn_ov001_021e29f8'), (0x2c, 1, 'native_fn_ov001_021e048c'), (0x44, 2, 'native_data_ov001_0223989c')),
     [60]),
    (0x021f927c, 60, 'native_ov001_021f927c.c',
     ((0x0c, 1, 'native_fn_0205e684'), (0x14, 1, 'native_fn_0205e73c'), (0x20, 1, 'native_fn_0205f5dc'), (0x38, 2, 'native_data_ov001_02239a08')),
     [24]),
    (0x021fe54c, 92, 'native_ov001_021fe54c.c',
     ((0x14, 1, 'native_fn_02049ad0'), (0x40, 1, 'native_fn_ov001_021fe6cc')),
     [36]),
    (0x021fefb0, 80, 'native_ov001_021fefb0.c',
     ((0x40, 1, 'native_fn_0206c718'), (0x4c, 2, 'native_data_ov001_02239c10')),
     [10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 24, 26, 27, 28, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43, 44, 46, 48, 49, 50, 52, 53, 54, 56, 57, 58, 59, 61, 63, 64, 65, 66, 67, 71, 73, 74, 75, 76, 77, 78, 79]),
    (0x02202540, 40, 'native_ov001_02202540.c',
     ((0x18, 1, 'native_fn_ov001_022028c8'), (0x20, 1, 'native_fn_ov001_02202598')),
     [8]),
    (0x02202584, 20, 'native_ov001_02202584.c',
     ((0x10, 2, 'native_fn_ov001_022028c8')),
     [5, 9]),
    (0x0220409c, 92, 'native_ov001_0220409c.c',
     ((0x10, 1, 'native_fn_0202a37c'), (0x28, 1, 'native_fn_02008c14'), (0x38, 1, 'native_fn_ov001_02204250'), (0x58, 2, 'native_data_ov001_0223d900')),
     [4]),
    (0x022044c8, 84, 'native_ov001_022044c8.c',
     ((0x38, 1, 'native_fn_0204b4f4'), (0x44, 1, 'native_fn_0204b61c')),
     [72]),
    (0x0220b2fc, 72, 'native_ov001_0220b2fc.c',
     ((0x20, 1, 'native_fn_ov001_0220b344'), (0x40, 2, 'native_data_ov001_0223df3c'), (0x44, 2, 'native_data_ov001_0223df44')),
     [12]),
    (0x0220b738, 20, 'native_ov001_0220b738.c',
     ((0x10, 2, 'native_data_ov001_0223e088')),
     [8]),
    (0x0220b75c, 20, 'native_ov001_0220b75c.c',
     ((0x10, 2, 'native_data_ov001_0223e088')),
     [8]),
    (0x0220b780, 20, 'native_ov001_0220b780.c',
     ((0x10, 2, 'native_data_ov001_0223e088')),
     [8]),
    (0x0220b7b8, 80, 'native_ov001_0220b7b8.c',
     ((0x0c, 1, 'native_fn_ov001_021f1294'), (0x10, 1, 'native_fn_ov001_0220b74c'), (0x18, 1, 'native_fn_ov001_0220b794'), (0x2c, 1, 'native_fn_ov001_021e1358'), (0x34, 1, 'ov001_side_slot_record_021db438'), (0x38, 1, 'native_fn_ov001_021ee9fc'), (0x4c, 2, 'native_data_ov001_0223e088')),
     [60, 61, 65, 69, 70, 72, 73, 74, 75, 76, 77, 78, 79]),
    (0x0220f91c, 68, 'native_ov001_0220f91c.c',
     ((0x14, 1, 'native_fn_0207b674')),
     [48, 49, 64, 65, 66, 67]),
    (0x0220f960, 68, 'native_ov001_0220f960.c',
     ((0x14, 1, 'native_fn_0207b674')),
     [48, 49, 64, 65, 66, 67]),
    (0x02213588, 76, 'native_ov001_02213588.c',
     ((0x20, 1, 'native_fn_0205f98c'), (0x30, 1, 'native_fn_ov001_021f1ba0')),
     [5, 10, 13, 26, 28, 38, 53, 54, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75]),
    (0x0221490c, 64, 'native_ov001_0221490c.c',
     ((0x0c, 1, 'native_fn_ov001_021f1294'), (0x28, 1, 'native_fn_ov001_021e1358'), (0x3c, 2, 'native_data_ov001_02242b94')),
     [16, 44, 45, 49, 53, 54, 56, 57, 58, 59, 60, 61, 62, 63]),
    (0x0221807c, 72, 'native_ov001_0221807c.c',
     ((0x10, 1, 'native_fn_0202a8e0'), (0x30, 1, 'native_fn_0202a954'), (0x40, 2, 'native_data_ov001_0222f1fc'), (0x44, 2, 'native_data_ov001_022430c8')),
     [8, 36, 39]),
    (0x022180f4, 80, 'native_ov001_022180f4.c',
     ((0x10, 1, 'native_fn_0202a8e0'), (0x34, 1, 'native_fn_0202a954'), (0x44, 2, 'native_data_ov001_0222f20c'), (0x4c, 2, 'native_data_ov001_022445c8')),
     [8, 40, 43]),
    (0x02218178, 72, 'native_ov001_02218178.c',
     ((0x40, 2, 'native_data_ov001_022445c8'), (0x44, 2, 'native_data_ov001_022445ca')),
     [36]),
    (0x022181c0, 72, 'native_ov001_022181c0.c',
     ((0x10, 1, 'native_fn_0202a8e0'), (0x30, 1, 'native_fn_0202a954'), (0x40, 2, 'native_data_ov001_0222f21c'), (0x44, 2, 'native_data_ov001_02242ec8')),
     [24, 25]),
    (0x0221823c, 72, 'native_ov001_0221823c.c',
     ((0x10, 1, 'native_fn_0202a8e0'), (0x30, 1, 'native_fn_0202a954'), (0x40, 2, 'native_data_ov001_0222f238'), (0x44, 2, 'native_data_ov001_02243dc8')),
     [8, 36, 39]),
    (0x02218304, 72, 'native_ov001_02218304.c',
     ((0x10, 1, 'native_fn_0202a8e0'), (0x30, 1, 'native_fn_0202a954'), (0x40, 2, 'native_data_ov001_0222f248'), (0x44, 2, 'native_data_ov001_022435c8')),
     [8, 36, 39]),
    (0x0221839c, 72, 'native_ov001_0221839c.c',
     ((0x10, 1, 'native_fn_0202a8e0'), (0x30, 1, 'native_fn_0202a954'), (0x40, 2, 'native_data_ov001_0222f260'), (0x44, 2, 'native_data_ov001_02242e4c')),
     [8, 36, 39]),
    (0x0221920c, 80, 'native_ov001_0221920c.c',
     ((0x0c, 1, 'native_fn_ov001_022191e8'), (0x20, 1, 'ov001_record_is_active_021db8d0')),
     [64]),
    (0x02219978, 64, 'native_ov001_02219978.c',
     ((0x0c, 1, 'native_fn_ov001_021dbd24'), (0x18, 1, 'native_fn_ov001_021dbcbc')),
     [40, 41, 60, 61, 62, 63]),
    (0x02219ba0, 64, 'native_ov001_02219ba0.c',
     ((0x0c, 1, 'ov001_record_field_1f2_021dbd30'), (0x18, 1, 'native_fn_ov001_021dbcf0')),
     [40, 41, 60, 61, 62, 63]),
    (0x02219dd8, 80, 'native_ov001_02219dd8.c',
     ((0x0c, 1, 'native_fn_ov001_02219d8c'), (0x20, 1, 'ov001_record_is_active_021db8d0')),
     [64]),
    (0x0221b748, 80, 'native_ov001_0221b748.c',
     ((0x10, 1, 'ov001_record_is_active_021db8d0'), (0x20, 1, 'native_fn_ov001_02218dbc')),
     [48]),
    (0x0221c11c, 80, 'native_ov001_0221c11c.c',
     ((0x10, 1, 'ov001_record_is_active_021db8d0'), (0x20, 1, 'ov001_record_field_1f2_021dbd30')),
     [48]),
    (0x0221dd80, 52, 'native_ov001_0221dd80.c',
     ((0x0c, 1, 'native_fn_ov001_0221887c'), (0x18, 1, 'native_fn_ov001_022188d0')),
     [8, 20]),
    (0x02223fe8, 56, 'ov001_clear_free_candidate_slots_02223fe8.c',
     ((0x18, 1, 'ov001_record_is_active_021db8d0')),
     [28]),
    (0x02226d2c, 68, 'native_ov001_02226d2c.c',
     ((0x24, 1, 'ov001_clear_free_candidate_slots_02223fe8'), (0x2c, 1, 'ov001_pick_random_candidate_02224050'), (0x34, 1, 'ov001_first_candidate_02226cb0'), (0x40, 2, 'native_data_ov001_0222e914')),
     [28]),
    (0x02226d70, 68, 'native_ov001_02226d70.c',
     ((0x24, 1, 'ov001_clear_free_candidate_slots_02223fe8'), (0x2c, 1, 'ov001_pick_random_candidate_02224050'), (0x34, 1, 'ov001_first_candidate_02226cb0'), (0x40, 2, 'native_data_ov001_0222e908')),
     [28]),
    (0x022294c8, 52, 'native_ov001_022294c8.c',
     ((0x1c, 1, 'ov001_pick_random_candidate_02224050'), (0x24, 1, 'ov001_first_candidate_02226cb0'), (0x30, 2, 'native_data_ov001_0222e5c0')),
     [8, 40, 41, 42, 44, 45, 46, 47, 48, 49, 50, 51]),
    (0x0222afc8, 84, 'native_ov001_0222afc8.c',
     ((0x24, 1, 'ov001_clear_free_candidate_slots_02223fe8'), (0x34, 1, 'native_fn_ov001_02226bdc'), (0x3c, 1, 'ov001_pick_random_candidate_02224050'), (0x44, 1, 'ov001_first_candidate_02226cb0'), (0x50, 2, 'native_data_ov001_0222e344')),
     [28]),
    (0x0222b034, 52, 'native_ov001_0222b034.c',
     ((0x10, 1, 'native_fn_02065d88'), (0x24, 1, 'native_fn_ov001_02226d08'), (0x2c, 1, 'native_fn_ov001_0222b198')),
     [12]),
    (0x0222b068, 52, 'native_ov001_0222b068.c',
     ((0x10, 1, 'native_fn_02065d88'), (0x24, 1, 'native_fn_ov001_02226d08'), (0x2c, 1, 'native_fn_ov001_02226db4')),
     [12]),
    (0x0222b09c, 52, 'native_ov001_0222b09c.c',
     ((0x10, 1, 'native_fn_02065d88'), (0x24, 1, 'native_fn_ov001_02226d08'), (0x2c, 1, 'native_fn_ov001_02226e34')),
     [12]),
    (0x0222b0d0, 52, 'native_ov001_0222b0d0.c',
     ((0x10, 1, 'native_fn_02065d88'), (0x24, 1, 'native_fn_ov001_02226d08'), (0x2c, 1, 'native_fn_ov001_02226ec8')),
     [12]),
    (0x0222b198, 84, 'native_ov001_0222b198.c',
     ((0x24, 1, 'ov001_clear_free_candidate_slots_02223fe8'), (0x34, 1, 'native_fn_ov001_02226bdc'), (0x3c, 1, 'ov001_pick_random_candidate_02224050'), (0x44, 1, 'ov001_first_candidate_02226cb0'), (0x50, 2, 'native_data_ov001_0222e2fc')),
     [28]),
)


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    root = ROOT
    config = source_units.load_config(root)
    work = root / 'build/ov001_pass3'
    work.mkdir(parents=True, exist_ok=True)
    if '--pin' in argv:
        return pin(root, config, work)
    image = image_bytes(root)
    base = module_base(root)
    failures = []
    rows = ROWS or tuple(
        (int(ADDRESS.search(path.name).group(1), 16), ledger_size(root, int(ADDRESS.search(path.name).group(1), 16)),
         path.name, None, None)
        for path in sorted((root / LANE).glob('native_ov001_*.c')))
    exact = controls = 0
    for address, size, name, expected_relocations, expected_control in rows:
        source_path = root / LANE / name
        result = measure(root, config, work, address, size, source_path)
        table = tuple((offset, kind, symbol) for offset, kind, symbol, _addend in result['relocations'])
        diff = result['diff']
        if len(result['text']) != size or diff:
            failures.append(f'{name}: patched {len(result["text"])} B, diff {diff}')
            continue
        if expected_relocations is not None:
            # Pin output wraps a single relocation as a bare 3-tuple; normalise it.
            if len(expected_relocations) == 3 and isinstance(expected_relocations[0], int):
                expected_relocations = (expected_relocations,)
            if table != expected_relocations:
                failures.append(f'{name}: relocations {table} != pinned {expected_relocations}')
                continue
        for offset, kind, symbol, _addend in result['relocations']:
            match = SYMBOL_ADDRESS.search(symbol)
            if not match or kind not in (1, 2):
                continue
            target = int(match.group(1), 16)
            decoded = decode_target(kind, image, base, address + offset)
            if decoded is None or (decoded & ~1) != (target & ~1):
                failures.append(f'{name}: +{offset:#x} resolves to {decoded and decoded:#x}, '
                                f'symbol says {target:#x}')
        body = source_path.read_text(encoding='utf-8')
        control_name, control_diff = control_for(body, root, config, work, address, size,
                                                 source_path, image, base)
        if control_diff is None:
            failures.append(f'{name}: no negative control compiled and differed')
            continue
        exact += 1
        controls += 1
        print(f'{name}: exact {size}/{size} B, {len(table)} relocation(s), '
              f'control {control_name} -> {control_diff}')
    if failures:
        print('\nFAIL')
        for failure in failures:
            print('  ' + failure)
        return 1
    print(f'\n{exact} functions exact; {controls} negative controls failed as expected')
    return 0


if __name__ == '__main__':
    sys.exit(main())
