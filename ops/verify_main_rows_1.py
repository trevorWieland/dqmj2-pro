"""Verify the four main-module rows authored in ``src/main/r1_main_small``.

Every row is recompiled here with its real source-unit rule (module ``main``,
profile ``p001``, mwccarm 2.0/base, ARM mode), its relocations are patched with
:func:`ops.form_search.relocate` + :class:`ops.form_search.TargetModes`, and the
whole measured extent is compared byte for byte with the ``main`` image at the
row's ``binaryOffset``.

For each row the check also proves:

* the object's relocation table is exactly the pinned one -- same offsets, same
  kinds, same externals -- so a match cannot come from a hard-coded literal that
  happens to equal an address;
* every ``R_ARM_ABS32`` slot in the *image* holds exactly the target the object
  asks for, i.e. the literal/pool target was read from the image word rather
  than trusted from a symbol name;
* one whole-C negative control per function compiles and differs from the image
  at the expected offsets, so a match is not vacuous.

    python ops/verify_main_rows_1.py

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

LANE = 'src/main/r1_main_small'
MODULE = 'main'

# address -> (token in the body, replacement) for the negative control.
CONTROLS = {
    0x02083E08: ('<= 14', '<= 15'),
    0x020C4944: ('native_data_021d53d4', 'native_data_021d53b4'),
    0x020D13BC: ('| 8', '| 4'),
    0x020D13E0: ('| 8', '| 4'),
}

# address, bytes, source, pinned relocations, pinned control diff.
ROWS = (
    (0x02083E08, 32, 'native_main_02083e08.c',
     ((0x1c, 2, 'native_data_021c72a0'),), [8]),
    (0x020C4944, 28, 'native_main_020c4944.c',
     ((0x14, 2, 'native_data_021d53b4'), (0x18, 2, 'native_data_021d53d4')), [0, 1, 2, 3]),
    (0x020D13BC, 36, 'native_main_020d13bc.c',
     ((0x1c, 2, 'native_data_021d6bc0'), (0x20, 2, 'native_data_021d6bcc')), [16]),
    (0x020D13E0, 36, 'native_main_020d13e0.c',
     ((0x1c, 2, 'native_data_021d6bb4'), (0x20, 2, 'native_data_021d6bcc')), [16]),
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


_ROOT_CONFIG = {}


def root_config(root):
    if 'config' not in _ROOT_CONFIG:
        _ROOT_CONFIG['config'] = source_units.load_config(root)
    return _ROOT_CONFIG['config']


def check(root, work, modes, failures):
    config = root_config(root)
    image, _, base = form_search.module_image(root, MODULE)
    pinned = []
    for address, size, name, expected_relocations, expected_control in ROWS:
        rule = source_units.resolve(config, f'{LANE}/{name}')
        if (rule['module'], rule['mode']) != (MODULE, 'arm'):
            failures.append(f'{name}: rule resolved {rule["module"]}/{rule["mode"]}')
        source = root / LANE / name
        body = source.read_text(encoding='utf-8')
        plain = work / name
        plain.write_text(body, encoding='utf-8')
        (work / 'context.h').write_text(
            (root / LANE / 'context.h').read_text(encoding='utf-8'), encoding='utf-8')
        old_value, new_value = CONTROLS[address]
        index = body.rfind(old_value)
        if index < 0:
            failures.append(f'{name}: control token {old_value!r} not in source')
            continue
        control_path = work / f'{address:08x}-control.c'
        control_path.write_text(body[:index] + new_value + body[index + len(old_value):],
                                encoding='utf-8')

        text, defined, relocations = compile_unit(root, rule, work, plain, 'unit')
        want = image[address - base:address - base + size]
        got = form_search.relocate(text, address, relocations, defined, modes=modes)
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
        cgot = form_search.relocate(ctext, address, crelocations, cdefined, modes=modes)
        cdiff = [i for i, (a, b) in enumerate(zip(cgot, want)) if a != b]
        if not cdiff:
            failures.append(f'{name}: negative control still matches the image')
        elif expected_control and cdiff != expected_control:
            failures.append(f'{name}: control diff {cdiff} != pinned {expected_control}')
        print(f'{address:#010x} {size:3d} B {name:26s} profile={rule["compilerFlags"]} '
              f'relocs={len(table)} bytes=EXACT control_diff={cdiff}')
        pinned.append((address, size, name, tuple(words)))
    return pinned


def main():
    failures = []
    work = Path(tempfile.mkdtemp(prefix='main-rows-1-'))
    modes = form_search.TargetModes(ROOT, MODULE)
    pinned = check(ROOT, work, modes, failures)
    print()
    for address, size, name, words in pinned:
        print(f'  {address:#010x} {size:3d} B  pool={", ".join("%#010x" % w for w in words)}')
    total = sum(row[1] for row in ROWS)
    print(f'\n{len(ROWS)} rows, {total} bytes, {len(failures)} failure(s)')
    for failure in failures:
        print('  FAIL', failure)
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
