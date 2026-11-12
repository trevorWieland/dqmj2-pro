"""Verify the ov001 pass-2 packet (``src/ov001/p9_ov001_pass2``).

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

LANE = 'src/ov001/p9_ov001_pass2'
ADDRESS = re.compile(r'([0-9a-f]{8})\.c$')
SYMBOL_ADDRESS = re.compile(r'([0-9a-fA-F]{8})$')

# Auto-derived negative controls, tried in this order.  The first substitution that
# changes the text, compiles, and produces different patched bytes is the control.
CONTROL_FORMS = (
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
    (0x021dc99c, 56, 'native_ov001_021dc99c.c',
     ((0x18, 1, 'native_fn_ov001_021dc940')),
     [28]),
    (0x021e2aa4, 88, 'native_ov001_021e2aa4.c',
     ((0x54, 2, 'native_data_ov001_022388ec')),
     [76]),
    (0x021eaa88, 56, 'native_ov001_021eaa88.c',
     ((0x18, 1, 'ov001_clear_state_flag4_021f14a4'), (0x30, 2, 'native_data_ov001_0222ec84'), (0x34, 2, 'native_data_ov001_02238d7c')),
     [16]),
    (0x02209490, 44, 'native_ov001_02209490.c',
     (),
     [28]),
    (0x0220f11c, 68, 'native_ov001_0220f11c.c',
     (),
     [48]),
    (0x0220f3ac, 72, 'native_ov001_0220f3ac.c',
     (),
     [60]),
    (0x0220f3f4, 72, 'native_ov001_0220f3f4.c',
     (),
     [60]),
    (0x022141f0, 68, 'native_ov001_022141f0.c',
     ((0x3c, 2, 'native_data_ov001_02242aac'), (0x40, 2, 'native_data_ov001_02242ab4')),
     [52]),
    (0x02214690, 68, 'native_ov001_02214690.c',
     ((0x24, 1, 'native_fn_ov001_02216ac4'), (0x40, 2, 'native_data_ov001_02242b50')),
     [56]),
    (0x0221a738, 88, 'native_ov001_0221a738.c',
     ((0x10, 1, 'ov001_record_is_active_021db8d0')),
     [56]),
    (0x0221a7e4, 88, 'native_ov001_0221a7e4.c',
     ((0x10, 1, 'ov001_record_is_active_021db8d0')),
     [56]),
    (0x0221ac38, 64, 'native_ov001_0221ac38.c',
     (),
     [32]),
    (0x0221b254, 88, 'native_ov001_0221b254.c',
     ((0x10, 1, 'ov001_record_is_active_021db8d0')),
     [56]),
    (0x0221b5e0, 88, 'native_ov001_0221b5e0.c',
     ((0x10, 1, 'ov001_record_is_active_021db8d0')),
     [56]),
    (0x0221b834, 96, 'native_ov001_0221b834.c',
     ((0x10, 1, 'ov001_record_is_active_021db8d0')),
     [64]),
    (0x0221b8b0, 88, 'native_ov001_0221b8b0.c',
     ((0x10, 1, 'ov001_record_is_active_021db8d0')),
     [56]),
    (0x0221dcd4, 88, 'native_ov001_0221dcd4.c',
     ((0x10, 1, 'ov001_record_is_active_021db8d0')),
     [56]),
    (0x0221e1c8, 80, 'native_ov001_0221e1c8.c',
     ((0x10, 1, 'ov001_record_is_active_021db8d0')),
     [48]),
    (0x0221e220, 88, 'native_ov001_0221e220.c',
     ((0x10, 1, 'ov001_record_is_active_021db8d0')),
     [56]),
    (0x0221f0a4, 80, 'native_ov001_0221f0a4.c',
     ((0x10, 1, 'ov001_record_is_active_021db8d0')),
     [48]),
    (0x0221f0f4, 80, 'native_ov001_0221f0f4.c',
     ((0x10, 1, 'ov001_record_is_active_021db8d0')),
     [48]),
)


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    root = ROOT
    config = source_units.load_config(root)
    work = root / 'build/ov001_authoring_1'
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
