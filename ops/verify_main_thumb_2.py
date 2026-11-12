"""Verify the main-module Thumb form-search batch (round 2).

Every row authored through ``ops/form_search_thumb.py`` is recompiled here
with the resolved source-unit rule (module main, mode thumb, profile p032,
mwccarm 2.0/base), its relocations are patched through
:func:`ops.form_search.relocate` and the mode-aware
:class:`ops.form_search.TargetModes`, and the whole measured extent is
compared byte for byte with ``extract/arm9/arm9.bin`` at base 0x02000000.

For each row the check also proves:

* the object's relocation table is exactly the pinned one (offset, kind,
  external), so a match cannot come from a hard-coded literal that happens
  to equal an address;
* a Thumb call target is encoded BL and an ARM target BLX in the image;
* every ``R_ARM_ABS32`` slot has addend 0 or 1, and a +1 addend resolves to
  a Thumb function;
* one whole-C negative control compiles and differs at the pinned offsets.

The lane rule itself is asserted too: the source-unit resolution must still
report module main, mode thumb and the 2.0/base compiler hash, so a future
lane edit cannot silently move these rows to another profile.

    python ops/verify_main_thumb_2.py
    python ops/verify_main_thumb_2.py --pin    # reprint the ROWS table

Exit status 0 only when every positive check and every negative control passes.
"""
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / 'public_tools'))

import form_search  # noqa: E402
import source_units  # noqa: E402

LANE = 'src/main/t1_main_thumb'
COMPILER_SHA256 = '7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880'

# address -> (token in the body, replacement) for the whole-C negative control.
CONTROLS = {
    0x020b5890: ('0x67', '0x68'),
    0x02092c98: ('02008e0c(b, a, c)', '02008e0c(a, b, c)'),
    0x02092ca8: ('02008e0c(b, a, c)', '02008e0c(a, b, c)'),
    0x020973c8: ('native_fn_02096ffc(b, record->f24, c)',
                 'native_fn_02096ffc(c, record->f24, b)'),
    0x02092ba0: ('0x455', '0x451'),
    0x020900f4: ('0x12', '0x13'),
    0x020a2cf0: ('arg0 == 0', 'arg0 == 1'),
}

SIZES = {
    0x020b5890: 12,
    0x02092c98: 16,
    0x02092ca8: 16,
    0x020973c8: 16,
    0x02092ba0: 44,
    0x020900f4: 68,
    0x020a2cf0: 64,
}

# address, bytes, source, relocations, control diff -- measured by --pin.
ROWS = (
    (0x020900f4, 68, 'native_main_020900f4.c',
     ((0x16, 10, 'native_fn_02008058'), (0x20, 10, 'native_fn_02006b7c'),
      (0x38, 2, 'native_data_021cfd48'), (0x3c, 2, 'native_data_021d1548'),
      (0x40, 2, 'native_data_021d1544')),
     [26]),
    (0x02092ba0, 44, 'native_main_02092ba0.c',
     ((0x28, 2, 'native_data_021cfd38'),),
     [32]),
    (0x02092c98, 16, 'native_main_02092c98.c',
     ((0x0c, 2, 'native_fn_02008e0c'),),
     [0, 1, 2, 3, 8, 9, 10, 11, 12, 13, 15]),
    (0x02092ca8, 16, 'native_main_02092ca8.c',
     ((0x0c, 2, 'native_fn_02008e0c'),),
     [0, 1, 2, 3, 8, 9, 10, 11, 12, 13, 15]),
    (0x020973c8, 16, 'native_main_020973c8.c',
     ((0x0c, 2, 'native_fn_02096ffc'),),
     [0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]),
    (0x020a2cf0, 64, 'native_main_020a2cf0.c',
     ((0x1e, 10, 'native_fn_02007a9c'), (0x2e, 10, 'native_fn_02007a9c'),
      (0x3c, 2, 'native_data_021d1b88')),
     [36]),
    (0x020b5890, 12, 'native_main_020b5890.c',
     ((0x08, 2, 'native_fn_020b4108'),),
     [0]),
)


def compile_unit(root, config, work, address, source_path, rule_path=None, tag='unit'):
    relative = (rule_path or source_path).relative_to(root).as_posix()
    rule = source_units.resolve(config, relative)
    if rule['module'] != 'main' or rule['mode'] != 'thumb':
        raise SystemExit(f'{relative}: resolved {rule["module"]}/{rule["mode"]}')
    flags = [flag for flag in rule['compilerFlags'] if flag != '-thumb']
    compiler = root / rule['compilerPath']
    obj = work / f'{address:08x}-{tag}.o'
    result = form_search.compile_source(compiler, source_path, obj, root, flags=flags)
    if result.returncode != 0:
        raise SystemExit(f'{relative}: compile failed\n{(result.stdout or result.stderr)[-800:]}')
    return form_search.read_object(obj), rule


def measure(root, config, work, address, size, name, control):
    source = root / LANE / name
    (text, defined, relocations), rule = compile_unit(
        config=config, root=root, work=work, address=address, source_path=source)
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
    (ctext, cdefined, crelocations), _control_rule = compile_unit(
        config=config, root=root, work=work, address=address,
        source_path=control_path, rule_path=source, tag='control')
    cgot = form_search.relocate(ctext, address, crelocations, cdefined, modes=modes)
    if len(cgot) < len(want):
        cgot = cgot + bytes(len(want) - len(cgot))
    control_diff = [i for i, (a, b) in enumerate(zip(cgot, want)) if a != b]
    return {
        'source': source, 'size': size, 'want': want, 'got': got,
        'relocations': table, 'defined': defined, 'control_diff': control_diff,
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
            elif mode == 'arm' and second & 0xD000 != 0xC000:
                failures.append(f'{name}: +{offset:#x} ARM target is not a BLX')
            elif mode == 'thumb' and second & 0xD000 == 0xC000:
                failures.append(f'{name}: +{offset:#x} Thumb target is a BLX')
        elif kind == 2:
            addend = result['addends'][offset]
            if addend not in (0, 1):
                failures.append(f'{name}: +{offset:#x} ABS32 addend {addend}')
            elif addend == 1 and mode != 'thumb':
                failures.append(f'{name}: +{offset:#x} Thumb-tagged {target:#010x} '
                                f'resolves to {mode}')

    if result['control_diff'] != expected_control:
        failures.append(f'{name}: control diff {result["control_diff"]}, '
                        f'expected {expected_control}')
    print(f'{name}: exact {size}/{size} B, {len(table)} relocation(s), '
          f'control diff {result["control_diff"]}')
    return result


def pin(root, config, work):
    lines = []
    for address in sorted(CONTROLS):
        name = f'native_main_{address:08x}.c'
        result = measure(root, config, work, address, SIZES[address], name,
                         CONTROLS[address])
        table = ', '.join(f'({offset:#04x}, {kind}, {symbol!r})'
                          for offset, kind, symbol in result['relocations'])
        if len(table) == 1:
            table += ','
        lines.append(f'    ({address:#010x}, {SIZES[address]}, {name!r},\n'
                     f'     ({table}),\n'
                     f'     {result["control_diff"]!r}),')
    print('\n'.join(lines))
    return 0


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    root = ROOT
    config = source_units.load_config(root)
    work = root / 'build/main_thumb_2'
    work.mkdir(parents=True, exist_ok=True)
    (work / 'context.h').write_text(
        (root / LANE / 'context.h').read_text(encoding='utf-8'), encoding='utf-8')

    rule = source_units.resolve(config, f'{LANE}/native_main_020900f4.c')
    if rule.get('module') != 'main' or rule.get('mode') != 'thumb':
        raise SystemExit(f'lane rule is {rule.get("module")}/{rule.get("mode")}')
    compiler = root / rule['compilerPath']
    digest = hashlib.sha256(compiler.read_bytes()).hexdigest()
    if digest != COMPILER_SHA256:
        raise SystemExit(f'lane compiler {compiler} is {digest}, expected {COMPILER_SHA256}')

    if '--pin' in argv:
        return pin(root, config, work)
    if not ROWS:
        raise SystemExit('ROWS is empty; run --pin and paste the measured table')
    modes = form_search.TargetModes(root, 'main')
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
          f'{len(ROWS)} negative controls differed as expected')
    return 0


if __name__ == '__main__':
    sys.exit(main())
