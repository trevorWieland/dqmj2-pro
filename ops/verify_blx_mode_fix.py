"""Verify the four shipped ov006 BLX-mode rows end to end.

For each function this checks, with the real source-unit rule from
``config/source_units.json`` (profile p004, module ov006, mode thumb) and the
pinned mwccarm:

* the unit resolves to Thumb and compiles;
* the function's compiled text has the expected ``R_ARM_THM_CALL`` at the call
  site, resolving to the measured ARM target with addend -4;
* :func:`ops.form_search.relocate` with :class:`ops.form_search.TargetModes`
  reproduces the measured image byte for byte (full extent, not masked);
* the old placeholder-mode patcher does **not** reproduce the BLX word, which is
  the regression this packet exists to prevent;
* one ordinary-C negative control per function compiles and fails at the
  expected byte (a constant change in the function body).

    python ops/verify_blx_mode_fix.py

Exit status 0 only when every positive and every negative control passes.
"""
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / 'public_tools'))

import form_search  # noqa: E402
import source_units  # noqa: E402

LANE = 'src/ov006/p5_ov006_blx_mode'
ROWS = (
    # address, size, source, branch offset, ARM target, expected image word,
    # negative-control old/new constant, expected control diff offsets
    dict(address=0x021FB384, size=24, source='native_ov006_021fb384.c', branch=0x0A,
         target=0x02002480, word='07f678e8', control=('0x1D', '0x1E'), diff=[6]),
    dict(address=0x021FF02C, size=48, source='native_ov006_021ff02c.c', branch=0x1A,
         target=0x0200616C, word='07f692e8', control=('0x4C4', '0x4C8'), diff=[40]),
    dict(address=0x021FF05C, size=48, source='native_ov006_021ff05c.c', branch=0x1A,
         target=0x0200616C, word='07f67ae8', control=('0x4C8', '0x4C4'), diff=[40]),
    dict(address=0x021FF08C, size=48, source='native_ov006_021ff08c.c', branch=0x1A,
         target=0x0200616C, word='07f662e8', control=('0x4CC', '0x4C8'), diff=[40]),
)


def compile_unit(root, config, work, row, source_path, rule_path=None, tag='unit'):
    relative = (rule_path or source_path).relative_to(root).as_posix()
    rule = source_units.resolve(config, relative)
    if rule['module'] != 'ov006' or rule['mode'] != 'thumb':
        raise SystemExit(f'{relative}: resolved module/mode is {rule["module"]}/{rule["mode"]}')
    flags = [flag for flag in rule['compilerFlags'] if flag != '-thumb']
    obj = work / f'{row["address"]:08x}-{tag}.o'
    result = form_search.compile_source(form_search.default_compiler(root), source_path,
                                        obj, root, flags=flags)
    if result.returncode != 0:
        raise SystemExit(f'{relative}: compile failed\n{result.stderr[-800:]}')
    return form_search.read_object(obj)


def main():
    root = ROOT
    config = source_units.load_config(root)
    work = root / 'build/blx_verify'
    work.mkdir(parents=True, exist_ok=True)
    modes = form_search.TargetModes(root, 'ov006')
    image, _, base = form_search.module_image(root, 'ov006')
    failures = []

    for row in ROWS:
        address = row['address']
        source = root / LANE / row['source']
        text, defined, relocations = compile_unit(root, config, work, row, source)
        want = image[address - base:address - base + row['size']]
        got = form_search.relocate(text, address, relocations, defined, modes=modes)
        old = form_search.relocate(text, address, relocations, defined, modes=None)
        diff = [i for i, (a, b) in enumerate(zip(got, want)) if a != b]

        branch = [item for item in relocations if item[0] == row['branch']]
        if len(branch) != 1 or branch[0][1] != 10:
            failures.append(f'{source.name}: no single R_ARM_THM_CALL at +{row["branch"]:#x}')
        else:
            _, kind, symbol, addend = branch[0]
            measured = form_search.symbol_address(symbol)
            if (measured, addend) != (row['target'], -4):
                failures.append(f'{source.name}: branch {symbol} -> {measured:#x} addend {addend}')
        if want[row['branch']:row['branch'] + 4].hex() != row['word']:
            failures.append(f'{source.name}: image word is '
                            f'{want[row["branch"]:row["branch"] + 4].hex()}')
        if len(got) != row['size'] or diff:
            failures.append(f'{source.name}: patched {len(got)} B, diff {diff}')
        old_diff = [i for i, (a, b) in enumerate(zip(old, want)) if a != b]
        if not old_diff:
            failures.append(f'{source.name}: old placeholder patcher unexpectedly exact')
        if any(i not in (row['branch'] + 2, row['branch'] + 3) for i in old_diff):
            failures.append(f'{source.name}: old diff outside BLX halfword: {old_diff}')

        # One whole-C negative control: mutate the body constant, not the comment.
        body = source.read_text(encoding='utf-8')
        old_value, new_value = row['control']
        index = body.rfind(old_value)
        if index < 0:
            failures.append(f'{source.name}: control constant {old_value} not in source')
        else:
            control = work / f'{address:08x}-control.c'
            control.write_text(body[:index] + new_value + body[index + len(old_value):],
                               encoding='utf-8')
            # The lane's context.h must be visible to the control source.
            (work / 'context.h').write_text(
                (root / LANE / 'context.h').read_text(encoding='utf-8'), encoding='utf-8')
            ctext, cdefined, crelocations = compile_unit(
                root, config, work, row, control, rule_path=source, tag='control')
            cgot = form_search.relocate(ctext, address, crelocations, cdefined, modes=modes)
            cdiff = [i for i, (a, b) in enumerate(zip(cgot, want)) if a != b]
            if cdiff != row['diff']:
                failures.append(f'{source.name}: control diff {cdiff}, expected {row["diff"]}')

        print(f'{source.name}: exact {row["size"]}/{row["size"]} B, '
              f'BLX @+{row["branch"]:#x} -> {row["target"]:#010x}, '
              f'control diff {row["diff"]}, old patcher diff {old_diff}')

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
