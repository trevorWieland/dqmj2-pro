"""Verify the nineteen ov006 Thumb rows authored for the BLX-mode packet.

Every row in ``src/ov006/p6_ov006_blx_auth`` is recompiled here with the real
source-unit rule (profile p004, module ov006, mode thumb), its relocations are
patched with :func:`ops.form_search.relocate` + :class:`ops.form_search.TargetModes`,
and the whole measured extent is compared byte for byte with the overlay image.

For each row the check also proves:

* at least one ``R_ARM_THM_CALL`` in the object resolves to an ARM target, i.e.
  the row exercises the BLX-immediate path this packet is about;
* the old placeholder-mode patcher (``modes=None``) does **not** reproduce the
  image, and every byte it gets wrong is in the second halfword of one of those
  ARM-target call sites — the measured regression the mode fix removes;
* one whole-C negative control per function compiles and fails at the expected
  offset(s), so the match is not vacuous.

    python ops/verify_blx_authoring_1.py

Exit status 0 only when every positive check and every negative control passes.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / 'public_tools'))

import form_search  # noqa: E402
import source_units  # noqa: E402

LANE = 'src/ov006/p6_ov006_blx_auth'

# address, size, source, negative-control substitution, expected control diff.
ROWS = (
    (0x021EF050, 40, 'native_ov006_021ef050.c', ('0x0C', '0x10'), [20, 21]),
    (0x02204268, 34, 'native_ov006_02204268.c', ('02005d50(1)', '02005d50(2)'), [4]),
    (0x0220428C, 30, 'native_ov006_0220428c.c', ('02005d50(1)', '02005d50(2)'), [4]),
    (0x021F1EF0, 28, 'native_ov006_021f1ef0.c', ('0x82EA', '0x82EB'), [24]),
    (0x021F2B3C, 40, 'native_ov006_021f2b3c.c', ('0xC0', '0xC4'), [20]),
    (0x021FEA78, 40, 'native_ov006_021fea78.c', ('02203c20', '02203c24'), [26]),
    (0x021FFF6C, 40, 'native_ov006_021fff6c.c', ('0x1374', '0x1378'), [36]),
    (0x02203C4C, 40, 'native_ov006_02203c4c.c', ('02005d50(1)', '02005d50(2)'), [4]),
    (0x021FEE00, 40, 'native_ov006_021fee00.c', ('0x4E7', '0x4E8'), [36]),
    (0x021FF440, 40, 'native_ov006_021ff440.c', ('0xEF', '0xF0'), [14]),
    (0x022041F0, 40, 'native_ov006_022041f0.c', ('0x04000208', '0x0400020A'), [8]),
    (0x021FEFD4, 44, 'native_ov006_021fefd4.c', ('0x4C0', '0x480'), [8]),
    (0x02203720, 44, 'native_ov006_02203720.c', ('(u32)arg6 << 3', '(u32)arg6 << 4'),
     [24, 25]),
    (0x02203B94, 44, 'native_ov006_02203b94.c', ('0x40000, 0)', '0x40000, 1)'), [20]),
    (0x02203C20, 44, 'native_ov006_02203c20.c', ('02005d50(1)', '02005d50(2)'), [4]),
    (0x02203148, 48, 'native_ov006_02203148.c', ('0x18, 4', '0x18, 5'), [4]),
    (0x02203BD8, 48, 'native_ov006_02203bd8.c', ('02005d50(1)', '02005d50(2)'), [4]),
    (0x022026A8, 48, 'native_ov006_022026a8.c', ('0xAB0', '0xAC0'), [36, 38]),
    (0x021FE510, 52, 'native_ov006_021fe510.c', ('0x40', '0x44'), [40]),
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


def main():
    root = ROOT
    config = source_units.load_config(root)
    work = root / 'build/blx_authoring_1'
    work.mkdir(parents=True, exist_ok=True)
    modes = form_search.TargetModes(root, 'ov006')
    image, _, base = form_search.module_image(root, 'ov006')
    failures = []

    for address, size, name, control, expected_control in ROWS:
        source = root / LANE / name
        text, defined, relocations = compile_unit(root, config, work, address, source)
        want = image[address - base:address - base + size]
        got = form_search.relocate(text, address, relocations, defined, modes=modes)
        old = form_search.relocate(text, address, relocations, defined, modes=None)
        diff = [i for i, (a, b) in enumerate(zip(got, want)) if a != b]
        if len(got) != size or diff:
            failures.append(f'{name}: patched {len(got)} B, diff {diff}')

        # Every ARM-target call site must exist and be a BLX immediate.
        arm_sites = []
        for offset, kind, symbol, addend in relocations:
            if kind not in (10, 30):
                continue
            target = defined.get(symbol) or form_search.symbol_address(symbol)
            mode, evidence = modes.resolve(target, symbol)
            if mode != 'arm':
                continue
            arm_sites.append(offset)
            first, second = want[offset:offset + 2], want[offset + 2:offset + 4]
            if int.from_bytes(first, 'little') & 0xF800 != 0xF000:
                failures.append(f'{name}: +{offset:#x} is not a Thumb call')
            elif int.from_bytes(second, 'little') & 0xD000 != 0xC000:
                failures.append(f'{name}: +{offset:#x} is not a BLX immediate '
                                f'({second.hex()})')
        if not arm_sites:
            failures.append(f'{name}: no ARM-target R_ARM_THM_CALL')

        old_diff = [i for i, (a, b) in enumerate(zip(old, want)) if a != b]
        allowed = {offset + half for offset in arm_sites for half in (2, 3)}
        if not old_diff:
            failures.append(f'{name}: old placeholder patcher unexpectedly exact')
        if any(i not in allowed for i in old_diff):
            failures.append(f'{name}: old diff outside an ARM call halfword: {old_diff}')

        # One whole-C negative control: mutate a body constant, not the comment.
        body = source.read_text(encoding='utf-8')
        old_value, new_value = control
        index = body.rfind(old_value)
        if index < 0:
            failures.append(f'{name}: control token {old_value} not in source')
            continue
        control_path = work / f'{address:08x}-control.c'
        control_path.write_text(body[:index] + new_value + body[index + len(old_value):],
                                encoding='utf-8')
        (work / 'context.h').write_text(
            (root / LANE / 'context.h').read_text(encoding='utf-8'), encoding='utf-8')
        ctext, cdefined, crelocations = compile_unit(
            root, config, work, address, control_path, rule_path=source, tag='control')
        cgot = form_search.relocate(ctext, address, crelocations, cdefined, modes=modes)
        cdiff = [i for i, (a, b) in enumerate(zip(cgot, want)) if a != b]
        if cdiff != expected_control:
            failures.append(f'{name}: control diff {cdiff}, expected {expected_control}')

        print(f'{name}: exact {size}/{size} B, {len(arm_sites)} ARM call site(s), '
              f'old-patcher diff {old_diff}, control diff {cdiff}')

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
