"""Verify every ov000 row authored in ``src/ov000/pass2_20261111``.

Each row is recompiled with its resolved source-unit rule (module ``ov000``,
profile ``p001``, mwccarm 2.0/base, ARM mode), its relocations are patched with
the same formulas the repository build uses (``R_ARM_PC24`` from
``public_tools/repo_build.py``, everything else from ``ops/form_search.py``), and
the whole measured extent is compared byte for byte with the ``ov000`` image at
the row's ``binaryOffset``.

For each row the check also proves:

* the object's relocation table is exactly the pinned one -- same offsets, same
  kinds, same externals -- so a match cannot come from a hard-coded literal that
  happens to equal an address;
* every ``R_ARM_ABS32`` slot in the *image* holds exactly the target the object
  asks for, i.e. the pool target was read from the image word rather than
  trusted from a symbol name;
* one whole-C negative control per function compiles and differs from the image
  at the pinned offsets, so a match is not vacuous.

    python ops/verify_ov000_pass2.py

Exit status 0 only when every positive check and every negative control passes.
"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / 'public_tools'))

import form_search  # noqa: E402
import source_units  # noqa: E402

LANE = 'src/ov000/pass2_20261111'
MODULE = 'ov000'
PROFILE = 'p001'
COMPILER = '7150fa4f'

# address, bytes, source, pinned relocations, (control old, control new, diff).
ROWS = (
    (0x021e60a8, 56, 'native_ov000_021e60a8.c',
     ((52, 2, 'native_data_ov000_02232668'),),
     ('4', '5', [44])),
    (0x021e61c0, 56, 'native_ov000_021e61c0.c',
     ((52, 2, 'native_data_ov000_02232568'),),
     ('4', '5', [44])),
    (0x021ef4d8, 64, 'native_ov000_021ef4d8.c',
     ((56, 2, 'native_data_ov000_02236c04'), (60, 2, 'native_data_02101ae8')),
     ('0x7c', '0x7d', [16, 28])),
    (0x021ef57c, 64, 'native_ov000_021ef57c.c',
     ((56, 2, 'native_data_ov000_02236bec'), (60, 2, 'native_data_02101ae8')),
     ('0x7c', '0x7d', [16, 28])),
    (0x021f2764, 60, 'native_ov000_021f2764.c',
     ((48, 2, 'native_data_ov000_02236d94'), (52, 2, 'native_data_ov000_02236d95'), (56, 2, 'native_data_ov000_02236d96')),
     ('4', '5', [8])),
    (0x021f8398, 72, 'native_ov000_021f8398.c',
     ((36, 1, 'native_fn_0202a498'), (68, 2, 'native_data_ov000_02236f20')),
     ('2', '3', [56])),
    (0x0220201c, 84, 'native_ov000_0220201c.c',
     ((68, 1, 'native_fn_0204a574'), (80, 2, 'native_data_ov000_0222b9f0')),
     ('5', '6', [56])),
    (0x0220552c, 84, 'native_ov000_0220552c.c',
     ((68, 1, 'native_fn_ov000_02202938'), (76, 2, 'native_data_ov000_0222f548'), (80, 2, 'native_data_ov000_02238190')),
     ('3', '4', [68])),
    (0x02209100, 60, 'native_ov000_02209100.c',
     (),
     ('4', '5', [48])),
    (0x02210b98, 60, 'native_ov000_02210b98.c',
     ((56, 2, 'native_data_ov000_02238634'),),
     ('0x2b8', '0x2b9', [44])),
    (0x02212480, 52, 'native_ov000_02212480.c',
     ((28, 1, 'native_fn_ov000_02211104'),),
     ('9', '10', [40])),
    (0x022124b4, 52, 'native_ov000_022124b4.c',
     ((28, 1, 'native_fn_ov000_02211104'),),
     ('0xc', '0xd', [40])),
    (0x022124e8, 48, 'native_ov000_022124e8.c',
     ((24, 1, 'native_fn_ov000_02211104'),),
     ('7', '8', [32])),
    (0x02212518, 48, 'native_ov000_02212518.c',
     ((24, 1, 'native_fn_ov000_02211104'),),
     ('8', '9', [32])),
    (0x02215048, 28, 'native_ov000_02215048.c',
     ((24, 2, 'native_data_ov000_0222bb18'),),
     ('12', '13', [12])),
    (0x02216350, 84, 'native_ov000_02216350.c',
     ((68, 1, 'native_fn_020499a8'), (80, 2, 'native_data_ov000_0224536c')),
     ('0x10', '0x11', [44])),
    (0x0221f39c, 36, 'native_ov000_0221f39c.c',
     ((4, 1, 'native_fn_ov000_0221c658'), (32, 2, 'native_data_ov000_022463a0')),
     ('0xc', '0xd', [16])),
    (0x02223328, 88, 'native_ov000_02223328.c',
     (),
     ('0x14bf', '0x14c0', [28, 30, 31])),
    (0x02223d88, 80, 'native_ov000_02223d88.c',
     ((76, 2, 'native_data_ov000_02246594'),),
     ('3', '4', [64])),
    (0x02223df0, 80, 'native_ov000_02223df0.c',
     ((76, 2, 'native_data_ov000_0224659a'),),
     ('3', '4', [64])),
    (0x02223e70, 80, 'native_ov000_02223e70.c',
     ((76, 2, 'native_data_ov000_022465a0'),),
     ('3', '4', [64])),
    (0x0222a1dc, 68, 'native_ov000_0222a1dc.c',
     ((64, 2, 'native_data_ov000_0224754c'),),
     ('8', '9', [8])),
    (0x0222b0c8, 92, 'native_ov000_0222b0c8.c',
     ((32, 1, 'native_fn_0205f98c'), (88, 2, 'native_data_ov000_022476f0')),
     ('0xc', '0xd', [20])),
)


def compile_unit(root, rule, work, source_path, tag):
    """Compile one source with its resolved rule flags (ARM: no -thumb)."""
    compiler = root / root_config(root)['compilers'][rule['compilerSha256']]
    flags = [flag for flag in rule['compilerFlags'] if flag not in ('-thumb', '-c')]
    flags.append('-c')
    obj = work / f'{source_path.stem}-{tag}.o'
    env = dict(os.environ, LM_LICENSE_FILE=str(root / 'tools/mwccarm/mwccarm/license.dat'))
    result = subprocess.run([str(compiler), *flags, source_path.name, '-o', obj.name],
                            cwd=str(source_path.parent), env=env,
                            capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(f'{source_path.name}: compile failed\n{result.stdout[-800:]}')
    return form_search.read_object(obj)


def patch_pc24(text, base, relocations, defined, modes):
    """form_search.relocate plus R_ARM_PC24 (1), using repo_build's formula.

    ``repo_build.patch_function`` encodes ``(target + addend - absolute) >> 2``;
    mwcc writes addend -8 for a BL, so the branch lands on the symbol.
    """
    import struct

    out = bytearray(text)
    rest = []
    for offset, kind, symbol, addend in relocations:
        if kind == 1:
            target = defined.get(symbol) or form_search.symbol_address(symbol)
            immediate = (target + addend - (base + offset)) >> 2
            word = struct.unpack_from('<I', out, offset)[0]
            struct.pack_into('<I', out, offset,
                             (word & 0xFF000000) | (immediate & 0xFFFFFF))
        else:
            rest.append((offset, kind, symbol, addend))
    if rest:
        out = bytearray(form_search.relocate(bytes(out), base, rest, defined, modes=modes))
    return bytes(out)


_ROOT_CONFIG = {}


def root_config(root):
    if 'config' not in _ROOT_CONFIG:
        _ROOT_CONFIG['config'] = source_units.load_config(root)
    return _ROOT_CONFIG['config']


def check(root, work, modes, failures):
    config = root_config(root)
    image, _, base = form_search.module_image(root, MODULE)
    total = 0
    for address, size, name, expected_relocations, control in ROWS:
        rule = source_units.resolve(config, f'{LANE}/{name}')
        if (rule['module'], rule['mode']) != (MODULE, 'arm'):
            failures.append(f'{name}: rule resolved {rule["module"]}/{rule["mode"]}')
        if rule['compilerFlags'] != config['profiles'][PROFILE]:
            failures.append(f'{name}: profile is not {PROFILE}')
        if not rule['compilerSha256'].startswith(COMPILER):
            failures.append(f'{name}: compiler is not {COMPILER}')
        source = root / LANE / name
        body = source.read_text(encoding='utf-8')
        plain = work / name
        plain.write_text(body, encoding='utf-8')
        old_value, new_value, expected_control = control
        index = body.rfind(old_value)
        if index < 0:
            failures.append(f'{name}: control token {old_value!r} not in source')
            continue
        control_path = work / f'{address:08x}-control.c'
        control_path.write_text(body[:index] + new_value + body[index + len(old_value):],
                                encoding='utf-8')

        text, defined, relocations = compile_unit(root, rule, work, plain, 'unit')
        want = image[address - base:address - base + size]
        got = patch_pc24(text, address, relocations, defined, modes)
        table = tuple((offset, kind, symbol) for offset, kind, symbol, _ in relocations)
        if table != expected_relocations:
            failures.append(f'{name}: relocations {table} != pinned {expected_relocations}')
        diff = [i for i, (a, b) in enumerate(zip(got, want)) if a != b]
        if len(got) != size or diff:
            failures.append(f'{name}: patched {len(got)} B, diff {diff}')
        words = []
        for offset, kind, symbol in table:
            if kind != 2:
                continue
            target = defined.get(symbol) or form_search.symbol_address(symbol)
            word = int.from_bytes(want[offset:offset + 4], 'little')
            words.append(word)
            if word != target:
                failures.append(f'{name}: +{offset:#x} image word {word:#010x} != '
                                f'target {target:#010x}')
        ctext, cdefined, crelocations = compile_unit(root, rule, work, control_path,
                                                     'control')
        cgot = patch_pc24(ctext, address, crelocations, cdefined, modes)
        cdiff = [i for i, (a, b) in enumerate(zip(cgot, want)) if a != b]
        if not cdiff:
            failures.append(f'{name}: negative control still matches the image')
        elif cdiff != expected_control:
            failures.append(f'{name}: control diff {cdiff} != pinned {expected_control}')
        print(f'{address:#010x} {size:3d} B {name:30s} relocs={len(table)} '
              f'bytes=EXACT control_diff={cdiff}')
        total += size
    return total


def main():
    failures = []
    work = Path(tempfile.mkdtemp(prefix='ov000-pass2-'))
    modes = form_search.TargetModes(ROOT, MODULE)
    total = check(ROOT, work, modes, failures)
    print(f'\n{len(ROWS)} rows, {total} bytes, {len(failures)} failure(s)')
    for failure in failures:
        print('  FAIL', failure)
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
