"""Verify the ov006 Thumb rows authored for the third BLX batch.

Every row in ``src/ov006/p8_ov006_blx_auth3`` is recompiled here with the real
source-unit rule (profile p004, module ov006, mode thumb), its relocations are
patched with :func:`ops.form_search.relocate` + :class:`ops.form_search.TargetModes`,
and the whole measured extent is compared byte for byte with the overlay image.

For each row the check also proves:

* the object's relocation table is exactly the pinned one -- same offsets, same
  kinds, same externals -- so a match cannot come from a hard-coded literal that
  happens to equal an address;
* at least one ``R_ARM_THM_CALL`` resolves to an ARM target, that site is a Thumb
  call in the image, and its second halfword is a BLX immediate;
* the old placeholder-mode patcher (``modes=None``) does **not** reproduce the
  image, and every byte it gets wrong is in the second halfword of one of those
  ARM-target call sites -- the measured regression the mode fix removes;
* every ``R_ARM_ABS32`` slot has addend 0 or 1; a +1 addend (a Thumb-tagged
  function address) must resolve to a Thumb function in the ledger, and a plain
  data address needs no mode evidence;
* one whole-C negative control per function compiles and fails at the expected
  offset(s), so the match is not vacuous.

    python ops/verify_blx_authoring_3.py
    python ops/verify_blx_authoring_3.py --pin    # reprint the table below

Exit status 0 only when every positive check and every negative control passes.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / 'public_tools'))

import form_search  # noqa: E402
import source_units  # noqa: E402

LANE = 'src/ov006/p8_ov006_blx_auth3'

# address -> (token in the body, replacement) for the negative control.
CONTROLS = {
    0x021FB474: ('0x44', '0x45'),
    0x021EDB00: ('100', '101'),
    0x021F56D8: ('0x0F', '0x0E'),
    0x021F6984: ('0221c0a8 + 2', '0221c0a8 + 3'),
    0x022019D0: ('0x5C', '0x5D'),
    0x022029AC: ('0x88', '0x89'),
    0x02203644: ('0x28', '0x2C'),
    0x02204150: ('0x8000', '0x4000'),
    0x022041A0: ('0x00040018', '0x0004001A'),
    0x0220491C: ('0x11', '0x12'),
    0x022035D8: ('0x638', '0x63C'),
    0x02201F54: ('0x40', '0x44'),
    0x021FE86C: ('0x7F', '0x7E'),
    0x021F8050: ('0x1C', '0x1D'),
    0x022042C4: ('0xC8', '0xC9'),
    0x02201C84: ('0x13E0', '0x13E4'),
    0x021FEB5C: ('0x168C', '0x168E'),
}

SIZES = {
    0x021EDB00: 88,
    0x021F56D8: 76,
    0x021F6984: 92,
    0x021FB474: 88,
    0x021FEB5C: 104,
    0x021FE86C: 100,
    0x021F8050: 116,
    0x022019D0: 80,
    0x02201C84: 112,
    0x02201F54: 104,
    0x022029AC: 96,
    0x022035D8: 108,
    0x02203644: 76,
    0x02204150: 80,
    0x022041A0: 80,
    0x022042C4: 108,
    0x0220491C: 84,
}

# address, bytes, source, relocations, control diff -- measured by --pin.
ROWS = (
    (0x021edb00, 88, 'native_ov006_021edb00.c',
     ((0x06, 10, 'native_ov006_021edc50'), (0x10, 10, 'native_ov006_021edc50'), (0x1a, 10, 'native_ov006_021edc50'), (0x24, 10, 'native_fn_0209063c'), (0x3e, 10, 'native_fn_02006b7c'), (0x4c, 2, 'native_data_ov006_0220d3dc'), (0x50, 2, 'native_data_ov006_0220d3e4'), (0x54, 2, 'native_data_ov006_021cfd48')),
     [58]),
    (0x021f56d8, 76, 'native_ov006_021f56d8.c',
     ((0x0a, 10, 'native_ov006_02203c08'), (0x24, 10, 'native_ov006_021f1fa8'), (0x2c, 10, 'native_fn_02008430'), (0x32, 10, 'native_fn_02006b7c'), (0x3c, 2, 'native_data_ov006_0221c094'), (0x40, 2, 'native_ov006_021f57cc'), (0x44, 2, 'native_ov006_021f57ec'), (0x48, 2, 'native_ov006_021f57e0')),
     [32]),
    (0x021f6984, 92, 'native_ov006_021f6984.c',
     ((0x0e, 10, 'native_fn_020024bc'), (0x1e, 10, 'native_fn_020024bc'), (0x28, 10, 'native_ov006_021ff6d4'), (0x42, 10, 'native_ov006_021f29bc'), (0x48, 2, 'native_data_ov006_0221c0a8'), (0x4c, 2, 'native_data_ov006_0220b5be'), (0x50, 2, 'native_data_ov006_0220b5bc'), (0x54, 2, 'native_data_ov006_0220b5c0'), (0x58, 2, 'native_data_ov006_0220b5ba')),
     [12]),
    (0x021f8050, 116, 'native_ov006_021f8050.c',
     ((0x5a, 10, 'native_fn_02002480'), (0x68, 10, 'native_ov006_021fe60c'), (0x70, 2, 'native_data_ov006_0221c0d8')),
     [20]),
    (0x021fb474, 88, 'native_ov006_021fb474.c',
     ((0x12, 10, 'native_fn_02002480'), (0x1e, 10, 'native_fn_020024bc'), (0x48, 2, 'native_data_ov006_0221c0ec'), (0x54, 2, 'native_data_ov006_0220b7f0')),
     [66]),
    (0x021fe86c, 100, 'native_ov006_021fe86c.c',
     ((0x20, 10, 'native_fn_02002480'), (0x28, 10, 'native_ov006_021ff6ec'), (0x42, 10, 'native_fn_02002480'), (0x54, 10, 'native_ov006_021ff700'), (0x5c, 2, 'native_data_ov006_0221c140')),
     [38]),
    (0x021feb5c, 104, 'native_ov006_021feb5c.c',
     ((0x12, 10, 'native_fn_02012030'), (0x24, 10, 'native_fn_020127ec'), (0x3a, 10, 'native_fn_02012030'), (0x48, 10, 'native_fn_02012824'), (0x58, 2, 'native_data_ov006_0221c144'), (0x64, 2, 'native_ov006_021fec00')),
     [52]),
    (0x022019d0, 80, 'native_ov006_022019d0.c',
     ((0x0c, 10, 'native_fn_02008430'), (0x12, 10, 'native_ov006_02201270'), (0x1e, 10, 'native_ov006_02201a20'), (0x48, 2, 'native_data_ov006_0221c164'), (0x4c, 2, 'native_data_ov006_0220e7d0')),
     [66]),
    (0x02201c84, 112, 'native_ov006_02201c84.c',
     ((0x12, 10, 'native_fn_020136fc'), (0x46, 10, 'native_ov006_022012c0'), (0x52, 10, 'native_ov006_022012c0'), (0x60, 2, 'native_data_ov006_0221c164'), (0x68, 2, 'native_data_ov006_0220e804'), (0x6c, 2, 'native_data_ov006_0220e834')),
     [100]),
    (0x02201f54, 104, 'native_ov006_02201f54.c',
     ((0x0a, 10, 'native_ov006_02201804'), (0x1a, 10, 'native_fn_020125bc'), (0x32, 10, 'native_fn_02008e0c'), (0x54, 2, 'native_data_ov006_0221c16c')),
     [48]),
    (0x022029ac, 96, 'native_ov006_022029ac.c',
     ((0x04, 10, 'native_fn_0200c1fc'), (0x0e, 10, 'native_fn_0200baa0'), (0x18, 10, 'native_fn_0200b8bc'), (0x22, 10, 'native_fn_0200b7c8'), (0x2e, 10, 'native_fn_0200613c'), (0x3e, 10, 'native_ov006_02203c20'), (0x4c, 10, 'native_ov006_02203c20'), (0x54, 2, 'native_data_ov006_0220e8d0'), (0x58, 2, 'native_data_ov006_0221c170')),
     [32]),
    (0x022035d8, 108, 'native_ov006_022035d8.c',
     ((0x1e, 10, 'native_fn_02007308'), (0x30, 10, 'native_fn_02004e58'), (0x3e, 10, 'native_fn_02007308'), (0x50, 10, 'native_fn_02004eb8'), (0x5c, 2, 'native_data_ov006_0221c184')),
     [100]),
    (0x02203644, 76, 'native_ov006_02203644.c',
     ((0x08, 10, 'native_ov006_0220498c'), (0x1a, 10, 'native_fn_020040ec'), (0x26, 10, 'native_fn_02008be0'), (0x2c, 10, 'native_fn_020040ec'), (0x38, 10, 'native_fn_02008be0'), (0x40, 10, 'native_ov006_02203c20'), (0x48, 2, 'native_data_ov006_0221c184')),
     [60]),
    (0x02204150, 80, 'native_ov006_02204150.c',
     ((0x1a, 10, 'native_fn_0200f0a4'), (0x38, 10, 'native_fn_0200f0a4')),
     [44]),
    (0x022041a0, 80, 'native_ov006_022041a0.c',
     ((0x0c, 10, 'native_fn_02005cf4'), (0x12, 10, 'native_fn_02005d20'), (0x18, 10, 'native_fn_02005bd8'), (0x24, 10, 'native_fn_02005b50'), (0x2a, 10, 'native_fn_02005d80'), (0x36, 10, 'native_fn_02007fe0'), (0x40, 2, 'native_data_ov006_0221c1a4'), (0x48, 2, 'native_ov006_02204218')),
     [68]),
    (0x022042c4, 108, 'native_ov006_022042c4.c',
     ((0x06, 10, 'native_ov006_02203c08'), (0x16, 10, 'native_fn_02008c58'), (0x2a, 10, 'native_ov006_022030a4'), (0x4c, 10, 'native_ov006_0220490c'), (0x60, 2, 'native_data_ov006_0221c1ac'), (0x64, 2, 'native_ov006_02204330')),
     [74]),
    (0x0220491c, 84, 'native_ov006_0220491c.c',
     ((0x10, 10, 'native_ov006_02203114'), (0x26, 10, 'native_fn_02005d50'), (0x3c, 10, 'native_ov006_0220428c'), (0x48, 10, 'native_fn_02005d20'), (0x50, 2, 'native_data_ov006_0221c1e8')),
     [34]),
)


def compile_unit(root, config, work, address, source_path, rule_path=None, tag='unit'):
    relative = (rule_path or source_path).relative_to(root).as_posix()
    rule = source_units.resolve(config, relative)
    if rule['module'] != 'ov006' or rule['mode'] != 'thumb':
        raise SystemExit(f'{relative}: resolved module/mode is {rule["module"]}/{rule["mode"]}')
    flags = [flag for flag in rule['compilerFlags'] if flag != '-thumb']
    obj = work / f'{address:08x}-{tag}.o'
    result = form_search.compile_source(form_search.default_compiler(root), source_path,
                                        obj, root, flags=flags)
    if result.returncode != 0:
        raise SystemExit(f'{relative}: compile failed\n{result.stderr[-800:]}')
    return form_search.read_object(obj)


def measure(root, config, work, address, size, name, control):
    """Compile one row and return (relocations, control diff, detail)."""
    source = root / LANE / name
    text, defined, relocations = compile_unit(root, config, work, address, source)
    image, _, base = form_search.module_image(root, 'ov006')
    want = image[address - base:address - base + size]
    modes = form_search.TargetModes(root, 'ov006')
    got = form_search.relocate(text, address, relocations, defined, modes=modes)
    old = form_search.relocate(text, address, relocations, defined, modes=None)

    table = tuple((offset, kind, symbol) for offset, kind, symbol, _addend in relocations)
    body = source.read_text(encoding='utf-8')
    old_value, new_value = control
    index = body.rfind(old_value)
    if index < 0:
        raise SystemExit(f'{name}: control token {old_value!r} not in source')
    control_path = work / f'{address:08x}-control.c'
    control_path.write_text(body[:index] + new_value + body[index + len(old_value):],
                            encoding='utf-8')
    (work / 'context.h').write_text((root / LANE / 'context.h').read_text(encoding='utf-8'),
                                    encoding='utf-8')
    ctext, cdefined, crelocations = compile_unit(root, config, work, address, control_path,
                                                 rule_path=source, tag='control')
    cgot = form_search.relocate(ctext, address, crelocations, cdefined, modes=modes)
    cdiff = [i for i, (a, b) in enumerate(zip(cgot, want)) if a != b]
    if len(cgot) != len(want):
        cdiff = cdiff + [len(want), len(cgot)]
    return {
        'source': source, 'size': size, 'want': want, 'got': got, 'old': old,
        'relocations': table, 'defined': defined, 'control_diff': cdiff,
        'control_size': len(cgot),
        'addends': {offset: addend for offset, kind, symbol, addend in relocations},
    }


def check(root, config, work, address, size, name, expected_relocations, control,
          expected_control, modes, failures):
    result = measure(root, config, work, address, size, name, control)
    want, got, old = result['want'], result['got'], result['old']
    table = result['relocations']

    if table != expected_relocations:
        failures.append(f'{name}: relocations {table} != pinned {expected_relocations}')
    diff = [i for i, (a, b) in enumerate(zip(got, want)) if a != b]
    if len(got) != size or diff:
        failures.append(f'{name}: patched {len(got)} B, diff {diff}')

    arm_sites = []
    for offset, kind, symbol in table:
        if kind not in (10, 30):
            continue
        target = result['defined'].get(symbol) or form_search.symbol_address(symbol)
        mode, _evidence = modes.resolve(target, symbol)
        if mode != 'arm':
            continue
        arm_sites.append(offset)
        first = int.from_bytes(want[offset:offset + 2], 'little')
        second = int.from_bytes(want[offset + 2:offset + 4], 'little')
        if first & 0xF800 != 0xF000:
            failures.append(f'{name}: +{offset:#x} is not a Thumb call')
        elif second & 0xD000 != 0xC000:
            failures.append(f'{name}: +{offset:#x} is not a BLX immediate ({second:04x})')
    if not arm_sites:
        failures.append(f'{name}: no ARM-target R_ARM_THM_CALL')

    for offset, kind, symbol in table:
        if kind != 2:
            continue
        target = result['defined'].get(symbol) or form_search.symbol_address(symbol)
        addend = result['addends'][offset]
        mode, _evidence = modes.resolve(target, symbol)
        if addend not in (0, 1):
            failures.append(f'{name}: +{offset:#x} ABS32 addend {addend} is not a '
                            f'plain or Thumb-tagged address')
        elif addend == 1 and mode != 'thumb':
            failures.append(f'{name}: +{offset:#x} Thumb-tagged {target:#010x} resolves '
                            f'to mode {mode}')

    old_diff = [i for i, (a, b) in enumerate(zip(old, want)) if a != b]
    allowed = {offset + half for offset in arm_sites for half in (2, 3)}
    if not old_diff:
        failures.append(f'{name}: old placeholder patcher unexpectedly exact')
    if any(i not in allowed for i in old_diff):
        failures.append(f'{name}: old diff outside an ARM call halfword: {old_diff}')

    if result['control_diff'] != expected_control:
        failures.append(f'{name}: control diff {result["control_diff"]}, '
                        f'expected {expected_control}')
    print(f'{name}: exact {size}/{size} B, {len(arm_sites)} ARM call site(s), '
          f'{len(table)} relocation(s), old-patcher diff {old_diff}, '
          f'control diff {result["control_diff"]}')
    return result


def pin(root, config, work):
    """Print the ROWS table with the measured relocations and control diffs."""
    lines = []
    for address in sorted(CONTROLS):
        name = f'native_ov006_{address:08x}.c'
        size = SIZES[address]
        result = measure(root, config, work, address, size, name, CONTROLS[address])
        table = ', '.join(f'({offset:#04x}, {kind}, {symbol!r})'
                          for offset, kind, symbol in result['relocations'])
        lines.append(f'    ({address:#010x}, {size}, {name!r},\n'
                     f'     ({table}),\n'
                     f'     {result["control_diff"]!r}),')
    print('\n'.join(lines))
    return 0


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    root = ROOT
    config = source_units.load_config(root)
    work = root / 'build/blx_authoring_3'
    work.mkdir(parents=True, exist_ok=True)
    modes = form_search.TargetModes(root, 'ov006')
    if '--pin' in argv:
        return pin(root, config, work)
    failures = []
    for address, size, name, relocations, expected in ROWS:
        check(root, config, work, address, size, name, relocations,
              CONTROLS[address], expected, modes, failures)
    if failures:
        print('\nFAIL')
        for failure in failures:
            print('  ' + failure)
        return 1
    print(f'\n{len(ROWS)} functions exact with mode-aware relocation; '
          f'{len(ROWS)} negative controls failed as expected')
    return 0


if __name__ == '__main__':
    sys.exit(main())

