"""Verify the ov006 Thumb rows authored for the second BLX batch.

Every row in ``src/ov006/p7_ov006_blx_auth2`` is recompiled here with the real
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
* every ``R_ARM_ABS32`` slot in the image holds its target plus the object's
  addend (the two Thumb callback addresses in this batch carry a +1 addend);
* one whole-C negative control per function compiles and fails at the expected
  offset(s), so the match is not vacuous.

    python ops/verify_blx_authoring_2.py
    python ops/verify_blx_authoring_2.py --pin    # reprint the table below

Exit status 0 only when every positive check and every negative control passes.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / 'public_tools'))

import form_search  # noqa: E402
import source_units  # noqa: E402

LANE = 'src/ov006/p7_ov006_blx_auth2'

# address -> (token in the body, replacement) for the negative control.
CONTROLS = {
    0x021FED84: ('0xA001', '0xA003'),
    0x021FFE28: ('02204974(1, value)', '02204974(2, value)'),
    0x02204330: ('native_data_ov006_0221c1ac, 0x800', 'native_data_ov006_0221c1ac, 0xA00'),
    0x021F8B00: ('0x1C)', '0x1D)'),
    0x021FE544: ('0221c134 + 4), 0, 0x600)', '0221c134 + 4), 1, 0x600)'),
    0x021FEBC4: ('i < 0x14', 'i < 0x15'),
    0x022009C8: ('[0x1A] >= 0', '[0x1B] >= 0'),
    0x02202A0C: ('return 4', 'return 5'),
    0x021F2AD4: ('0xC0)', '0xC1)'),
    0x021FE49C: ('0x608', '0x609'),
    0x02200598: ('<= -12', '<= -11'),
    0x02200DF0: ('slot < 0x10', 'slot < 0x11'),
}

# address, bytes, source, relocations, control diff -- measured by --pin.
ROWS = (
    (0x021f2ad4, 64, 'native_ov006_021f2ad4.c',
     ((0x08, 10, 'native_ov006_021f2798'), (0x10, 10, 'native_ov006_02202a80'), (0x1c, 10, 'native_fn_02008ca4'), (0x22, 10, 'native_ov006_02202b24'), (0x2e, 10, 'native_ov006_0220490c'), (0x34, 2, 'native_data_ov006_0220d72c'), (0x38, 2, 'native_data_ov006_0221c054'), (0x3c, 2, 'native_ov006_021f2b3c')),
     [26]),
    (0x021f8b00, 60, 'native_ov006_021f8b00.c',
     ((0x12, 10, 'native_fn_020024bc'), (0x30, 2, 'native_data_ov006_0221c0d8')),
     [16]),
    (0x021fe49c, 64, 'native_ov006_021fe49c.c',
     ((0x08, 10, 'ov006_clear_buffer_02203c08'), (0x1a, 10, 'native_fn_02008ca4'), (0x26, 10, 'native_ov006_0220490c'), (0x38, 2, 'native_data_ov006_0221c134'), (0x3c, 2, 'native_ov006_021fe544')),
     [52]),
    (0x021fe544, 60, 'native_ov006_021fe544.c',
     ((0x12, 10, 'native_fn_02007308'), (0x22, 10, 'native_fn_02004cd8'), (0x34, 2, 'native_data_ov006_0221c134')),
     [28]),
    (0x021febc4, 60, 'native_ov006_021febc4.c',
     ((0x1c, 10, 'native_fn_0201b248'), (0x34, 2, 'native_data_ov006_0221c144'), (0x38, 2, 'native_data_ov006_0220b9a4')),
     [42]),
    (0x021fed84, 52, 'native_ov006_021fed84.c',
     ((0x06, 10, 'ov006_clear_buffer_02203c08'), (0x14, 10, 'native_fn_02019a58'), (0x1c, 10, 'native_fn_020a47cc'), (0x28, 2, 'native_data_ov006_0221c148')),
     [48]),
    (0x021ffe28, 52, 'native_ov006_021ffe28.c',
     ((0x0c, 10, 'native_fn_02007308'), (0x1a, 10, 'native_fn_02004c78'), (0x22, 10, 'native_ov006_02202b24'), (0x2a, 10, 'native_ov006_02204974'), (0x30, 2, 'native_data_ov006_0221c150')),
     [38]),
    (0x02200598, 64, 'native_ov006_02200598.c',
     ((0x16, 10, 'native_fn_02004308'), (0x2c, 10, 'native_ov006_02204970'), (0x34, 2, 'native_data_ov006_0221c15c'), (0x3c, 2, 'native_ov006_022005d8')),
     [34]),
    (0x022009c8, 60, 'native_ov006_022009c8.c',
     ((0x16, 10, 'native_fn_02004308'), (0x2a, 10, 'native_ov006_02204970'), (0x30, 2, 'native_data_ov006_0221c15c'), (0x38, 2, 'native_ov006_02200a04')),
     [30]),
    (0x02200df0, 64, 'native_ov006_02200df0.c',
     ((0x22, 10, 'native_fn_020143d0'), (0x3c, 2, 'native_data_ov006_0221c160')),
     [52]),
    (0x02202a0c, 60, 'native_ov006_02202a0c.c',
     ((0x18, 10, 'native_fn_020102c4'), (0x28, 10, 'native_fn_020102e0'), (0x38, 2, 'native_data_ov006_0221c170')),
     [48]),
    (0x02204330, 52, 'native_ov006_02204330.c',
     ((0x0a, 10, 'native_fn_02007308'), (0x18, 10, 'native_fn_020049fc'), (0x28, 10, 'native_fn_02004a50'), (0x30, 2, 'native_data_ov006_0221c1ac')),
     [4, 8]),
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
        mode, evidence = modes.resolve(target, symbol)
        if mode is None:
            failures.append(f'{name}: +{offset:#x} ABS32 target {target:#010x} has no '
                            f'mode evidence')
        if addend not in (0, 1):
            failures.append(f'{name}: +{offset:#x} ABS32 addend {addend} is not a '
                            f'plain or Thumb-tagged address')
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


SIZES = {
    0x021FED84: 52,
    0x021FFE28: 52,
    0x02204330: 52,
    0x021F8B00: 60,
    0x021FE544: 60,
    0x021FEBC4: 60,
    0x022009C8: 60,
    0x02202A0C: 60,
    0x021F2AD4: 64,
    0x021FE49C: 64,
    0x02200598: 64,
    0x02200DF0: 64,
}


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    root = ROOT
    config = source_units.load_config(root)
    work = root / 'build/blx_authoring_2'
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
