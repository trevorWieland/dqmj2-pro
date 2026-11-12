"""Verify the main-module Thumb rows authored for batch 1.

Every row in ``src/main/t1_main_thumb`` is recompiled here with the real
source-unit rule (module main, mode thumb, profile p032, mwccarm 2.0/base), its
relocations are patched with :func:`ops.form_search.relocate` and the mode-aware
:class:`ops.form_search.TargetModes`, and the whole measured extent is compared
byte for byte with ``extract/arm9/arm9.bin`` at base 0x02000000.

For each row the check also proves:

* the object's relocation table is exactly the pinned one -- same offsets, same
  kinds, same externals -- so a match cannot come from a hard-coded literal that
  happens to equal an address;
* every ``R_ARM_ABS32`` slot has addend 0 or 1; a +1 addend (a Thumb-tagged
  function address) must resolve to a Thumb function in the ledger and a plain
  data address needs no mode evidence;
* every ``R_ARM_THM_CALL`` whose target resolves to ARM is encoded as a BLX
  immediate in the image, and every Thumb target as a BL;
* one whole-C negative control per function compiles and fails at the pinned
  offset(s), so a match is not vacuous.

    python ops/verify_main_thumb_1.py
    python ops/verify_main_thumb_1.py --pin    # reprint the ROWS table

Exit status 0 only when every positive check and every negative control passes.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / 'public_tools'))

import form_search  # noqa: E402
import source_units  # noqa: E402

LANE = 'src/main/t1_main_thumb'

# address -> (token in the body, replacement) for the whole-C negative control.
CONTROLS = {
    0x0208ba68: ('0x44', '0x48'),
    0x020a3d9c: ('node[3]', 'node[4]'),
    0x0208ed2c: ('~0x30', '~0x31'),
    0x020a8bc4: ('remaining = 8', 'remaining = 9'),
}

SIZES = {
    0x0208ba68: 56,
    0x020a3d9c: 60,
    0x0208ed2c: 44,
    0x020a8bc4: 42,
}

# address, bytes, source, relocations, control diff -- measured by --pin.
ROWS = (
    (0x0208ba68, 56, 'native_main_0208ba68.c',
     ((0x02, 10, 'native_fn_02007ff4'), (0x0a, 10, 'native_fn_020068c0'),
      (0x20, 10, 'native_fn_0200698c'), (0x26, 10, 'native_fn_02008008'),
      (0x30, 2, 'native_data_021cfea0'), (0x34, 2, 'native_data_021cfcf8')),
     [28]),
    (0x020a3d9c, 60, 'native_main_020a3d9c.c',
     ((0x18, 10, 'native_fn_0209aa64'), (0x22, 10, 'native_fn_0209aa64'),
      (0x38, 2, 'native_data_021d2300')),
     [14, 15]),
    (0x0208ed2c, 44, 'native_main_0208ed2c.c',
     ((0x02, 10, 'native_fn_0208edb0'), (0x16, 10, 'native_fn_0208ebd8'),
      (0x1e, 10, 'native_fn_0208ecbc'), (0x28, 2, 'native_fn_0208ed58')),
     [10]),
    (0x020a8bc4, 42, 'native_main_020a8bc4.c',
     ((0x1a, 10, 'native_fn_02090310'), (0x22, 10, 'native_fn_020a8b4c')),
     [6]),
)


def compile_unit(root, config, work, address, source_path, rule_path=None, tag='unit'):
    relative = (rule_path or source_path).relative_to(root).as_posix()
    rule = source_units.resolve(config, relative)
    if rule['module'] != 'main' or rule['mode'] != 'thumb':
        raise SystemExit(f'{relative}: resolved module/mode is {rule["module"]}/{rule["mode"]}')
    flags = [flag for flag in rule['compilerFlags'] if flag != '-thumb']
    compiler = root / rule['compiler']['path'] if 'compiler' in rule else form_search.default_compiler(root)
    obj = work / f'{address:08x}-{tag}.o'
    result = form_search.compile_source(compiler, source_path, obj, root, flags=flags)
    if result.returncode != 0:
        raise SystemExit(f'{relative}: compile failed\n{result.stderr[-800:]}')
    return form_search.read_object(obj)


def measure(root, config, work, address, size, name, control):
    """Compile one row and return (relocations, control diff, detail)."""
    source = root / LANE / name
    text, defined, relocations = compile_unit(root, config, work, address, source)
    image, _, base = form_search.module_image(root, 'main')
    want = image[address - base:address - base + size]
    modes = form_search.TargetModes(root, 'main')
    got = form_search.relocate(text, address, relocations, defined, modes=modes)

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
        'source': source, 'size': size, 'want': want, 'got': got,
        'relocations': table, 'defined': defined, 'control_diff': cdiff,
        'control_size': len(cgot),
        'addends': {offset: addend for offset, kind, symbol, addend in relocations},
    }


def check(root, config, work, address, size, name, expected_relocations, control,
          expected_control, modes, failures):
    result = measure(root, config, work, address, size, name, control)
    want, got = result['want'], result['got']
    table = result['relocations']

    if table != expected_relocations:
        failures.append(f'{name}: relocations {table} != pinned {expected_relocations}')
    diff = [i for i, (a, b) in enumerate(zip(got, want)) if a != b]
    if len(got) != size or diff:
        failures.append(f'{name}: patched {len(got)} B, diff {diff}')

    for offset, kind, symbol in table:
        target = result['defined'].get(symbol) or form_search.symbol_address(symbol)
        mode, _evidence = modes.resolve(target, symbol)
        if kind in (10, 30):
            first = int.from_bytes(want[offset:offset + 2], 'little')
            second = int.from_bytes(want[offset + 2:offset + 4], 'little')
            if first & 0xF800 != 0xF000:
                failures.append(f'{name}: +{offset:#x} is not a Thumb call')
            elif mode == 'arm':
                if second & 0xD000 != 0xC000:
                    failures.append(f'{name}: +{offset:#x} ARM target is not a BLX ({second:04x})')
            elif second & 0xD000 == 0xC000:
                failures.append(f'{name}: +{offset:#x} Thumb target is encoded as BLX')
        elif kind == 2:
            addend = result['addends'][offset]
            if addend not in (0, 1):
                failures.append(f'{name}: +{offset:#x} ABS32 addend {addend} is not a '
                                f'plain or Thumb-tagged address')
            elif addend == 1 and mode != 'thumb':
                failures.append(f'{name}: +{offset:#x} Thumb-tagged {target:#010x} resolves '
                                f'to mode {mode}')

    if result['control_diff'] != expected_control:
        failures.append(f'{name}: control diff {result["control_diff"]}, '
                        f'expected {expected_control}')
    print(f'{name}: exact {size}/{size} B, {len(table)} relocation(s), '
          f'control diff {result["control_diff"]}')
    return result


def pin(root, config, work):
    """Print the ROWS table with the measured relocations and control diffs."""
    lines = []
    for address in sorted(CONTROLS):
        name = f'native_main_{address:08x}.c'
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
    work = root / 'build/main_thumb_1'
    work.mkdir(parents=True, exist_ok=True)
    modes = form_search.TargetModes(root, 'main')
    if '--pin' in argv:
        return pin(root, config, work)
    if not ROWS:
        raise SystemExit('ROWS is empty; run --pin and paste the measured table')
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
