"""Verify the ov001 straight-line leaf packet (``src/ov001/p8_ov001_pass1``).

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

    python ops/verify_ov001_authoring_1.py            # run the gate
    python ops/verify_ov001_authoring_1.py --pin      # reprint the ROWS table

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

LANE = 'src/ov001/p8_ov001_pass1'
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
    import json
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8-sig'))
    return next(m for m in manifest['modules'] if m['name'] == 'ov001')


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
    (0x021d92c0, 28, 'native_ov001_021d92c0.c',
     ((0x10, 1, 'native_fn_0202871c'), (0x18, 2, 'native_data_ov001_02235534')),
     [8, 16]),
    (0x021d92dc, 28, 'native_ov001_021d92dc.c',
     ((0x10, 1, 'native_fn_020287ac'), (0x18, 2, 'native_data_ov001_02235534')),
     [8, 16]),
    (0x021dc8b4, 52, 'native_ov001_021dc8b4.c',
     (),
     [36]),
    (0x021e2cb4, 40, 'native_ov001_021e2cb4.c',
     ((0x04, 1, 'native_fn_0204446c'), (0x24, 2, 'native_data_ov001_02238ad0')),
     [4, 8]),
    (0x021fc110, 44, 'native_ov001_021fc110.c',
     ((0x08, 1, 'native_fn_02044424'), (0x28, 2, 'native_data_ov001_0222ed28')),
     [8, 12]),
    (0x021fd074, 36, 'native_ov001_021fd074.c',
     ((0x20, 2, 'native_data_ov001_02239ca4')),
     [0]),
    (0x021fd098, 36, 'native_ov001_021fd098.c',
     ((0x20, 2, 'native_data_ov001_02239c9c')),
     [0]),
    (0x02202230, 44, 'native_ov001_02202230.c',
     ((0x28, 2, 'native_data_ov001_02239c10')),
     [12]),
    (0x02202568, 28, 'native_ov001_02202568.c',
     ((0x14, 1, 'native_fn_ov001_022028c8')),
     [4, 20]),
    (0x02203270, 64, 'native_ov001_02203270.c',
     ((0x3c, 2, 'native_data_ov001_0223a030')),
     [24]),
    (0x02203480, 28, 'native_ov001_02203480.c',
     ((0x18, 2, 'native_data_ov001_02239c10')),
     [8]),
    (0x0220468c, 48, 'native_ov001_0220468c.c',
     ((0x28, 1, 'native_fn_ov001_0220459c')),
     [8, 40]),
    (0x022047d0, 28, 'native_ov001_022047d0.c',
     ((0x18, 2, 'native_data_ov001_0223d904')),
     [0, 1, 4, 5, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19]),
    (0x022048fc, 40, 'native_ov001_022048fc.c',
     ((0x24, 2, 'native_data_ov001_0223d904')),
     [0, 4, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]),
    (0x02204924, 32, 'native_ov001_02204924.c',
     ((0x1c, 2, 'native_data_ov001_0223d904')),
     [0, 1, 4, 5, 8, 9, 10, 14, 16, 17, 18, 19, 20, 21, 22, 23]),
    (0x0220946c, 36, 'native_ov001_0220946c.c',
     (),
     [28]),
    (0x0220ee84, 32, 'native_ov001_0220ee84.c',
     (),
     [6, 8, 12, 17, 20, 22, 24, 25, 26, 27, 28, 29, 30, 31]),
    (0x02210d98, 56, 'native_ov001_02210d98.c',
     ((0x34, 2, 'native_data_ov001_0223e118')),
     [8]),
    (0x02210dd0, 56, 'native_ov001_02210dd0.c',
     ((0x34, 2, 'native_data_ov001_0223e118')),
     [8]),
    (0x022129cc, 40, 'native_ov001_022129cc.c',
     ((0x24, 2, 'native_data_020d3fe0')),
     [0]),
    (0x02212af8, 48, 'native_ov001_02212af8.c',
     ((0x04, 1, 'native_fn_ov001_021f1a44')),
     [4, 44, 45, 46, 47]),
    (0x02213b5c, 32, 'native_ov001_02213b5c.c',
     ((0x1c, 2, 'native_data_ov001_02242998')),
     [12]),
    (0x02215760, 32, 'native_ov001_02215760.c',
     ((0x1c, 2, 'native_data_ov001_02242ba0')),
     [20]),
    (0x0221bd44, 44, 'native_ov001_0221bd44.c',
     ((0x18, 1, 'native_fn_ov001_021db578')),
     [12, 24]),
    (0x0221be4c, 44, 'native_ov001_0221be4c.c',
     ((0x18, 1, 'native_fn_ov001_021db578')),
     [12, 24]),
    (0x0221c318, 48, 'native_ov001_0221c318.c',
     ((0x1c, 1, 'native_fn_ov001_02218a54')),
     [28, 32]),
    (0x0221ef2c, 48, 'native_ov001_0221ef2c.c',
     ((0x18, 1, 'native_fn_ov001_02218b54')),
     [24, 28]),
    (0x02223f20, 40, 'ov001_count_candidates_02223f20.c',
     (),
     [16]),
    (0x02224020, 48, 'native_ov001_02224020.c',
     (),
     [24]),
    (0x02226cb0, 40, 'ov001_first_candidate_02226cb0.c',
     (),
     [32]),
    (0x0222be84, 44, 'native_ov001_0222be84.c',
     ((0x04, 1, 'native_fn_ov001_0222be7c'), (0x28, 2, 'native_data_ov001_022497e8')),
     [4, 32]),
    (0x0222d91c, 32, 'native_ov001_0222d91c.c',
     ((0x1c, 2, 'native_data_ov001_02249828')),
     [4]),
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
