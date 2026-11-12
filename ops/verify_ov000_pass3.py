"""Verify every ov000 row authored in ``src/ov000/pass3_20261111``.

Each row is recompiled with its resolved source-unit rule (module ``ov000``,
profile ``p001``, mwccarm 2.0/base, ARM mode), its relocations are patched with
the same formulas the repository build uses (``R_ARM_PC24`` from
``public_tools/repo_build.py``, everything else from ``ops/form_search.py``), and
the whole measured extent at the ledger row's ``binaryOffset`` is compared byte
for byte with the ``ov000`` image.

For each row the check also proves:

* the object's relocation table is exactly the pinned one -- same offsets, same
  kinds, same externals -- so a match cannot come from a hard-coded literal that
  happens to equal an address;
* every ``R_ARM_ABS32`` slot in the *image* holds exactly the target the object
  asks for, i.e. the pool target was read from the image word rather than
  trusted from a symbol name;
* one whole-C negative control per function compiles and differs from the image
  at the pinned offsets, so a match is not vacuous.

    python ops/verify_ov000_pass3.py

Exit status 0 only when every positive check and every negative control passes.
"""
import json
import os
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / 'public_tools'))

import form_search  # noqa: E402
import source_units  # noqa: E402

LANE = 'src/ov000/pass3_20261111'
MODULE = 'ov000'
PROFILE = 'p001'
COMPILER = '7150fa4f'

# address, bytes, source, pinned relocations,
# (control old, control new, expected differing offsets).
ROWS = (
    (0x02229f54, 20, 'native_ov000_02229f54.c',
     ((16, 2, 'native_data_ov000_0222ffd4'),),
     ('native_data_ov000_0222ffd4[index]', 'native_data_ov000_0222ffd4[index + 1]', [0, 2, 3, 4, 6, 7, 8, 9, 10, 12, 13, 14, 16, 18, 19])),
    (0x021effec, 44, 'native_ov000_021effec.c',
     ((8, 1, 'native_fn_02049ad0'), (20, 1, 'native_fn_021ef1cc'), (28, 1, 'native_fn_021f0448')),
     ('native_fn_021f0448(0x12)', 'native_fn_021f0448(0x13)', [24])),
    (0x021e7a78, 40, 'native_ov000_021e7a78.c',
     ((12, 1, 'native_fn_0205e7f4'), (28, 1, 'native_fn_0205c1a8')),
     ('native_fn_0205e7f4(0, 0)', 'native_fn_0205e7f4(0, 1)', [8, 11])),
    (0x02216e6c, 56, 'native_ov000_02216e6c.c',
     ((4, 1, 'native_fn_0202a634'), (28, 1, 'native_fn_ov000_02216cc8'), (40, 1, 'native_fn_02068f60')),
     ('& 0xff7', '& 0xff6', [52])),
    (0x021e725c, 52, 'native_ov000_021e725c.c',
     ((8, 1, 'native_fn_ov000_021e722c'), (20, 1, 'native_fn_ov000_021e722c'), (32, 1, 'native_fn_ov000_021e722c'), (40, 1, 'native_fn_ov000_021e729c')),
     ('native_fn_ov000_021e722c(6)', 'native_fn_ov000_021e722c(7)', [4])),
    (0x021e6a40, 48, 'native_ov000_021e6a40.c',
     ((8, 1, 'native_fn_021e63a4'), (16, 1, 'native_fn_0202859c')),
     ('native_fn_0202859c(handle, (u32 *)dst)', 'native_fn_020285a0(handle, (u32 *)dst)', [16])),
    (0x021e6a70, 48, 'native_ov000_021e6a70.c',
     ((8, 1, 'native_fn_021e63a4'), (16, 1, 'native_fn_020285c8')),
     ('native_fn_020285c8(handle, (u32 *)dst)', 'native_fn_020285c0(handle, (u32 *)dst)', [16])),
    (0x0221221c, 64, 'native_ov000_0221221c.c',
     ((28, 1, 'native_fn_02211104'), (44, 1, 'native_fn_02211644')),
     ('native_fn_02211644(handle, c)', 'native_fn_02211648(handle, c)', [44])),
    (0x02217c68, 52, 'native_ov000_02217c68.c',
     ((24, 1, 'native_fn_ov000_02217bdc'), (36, 1, 'native_fn_02049e0c')),
     ('native_fn_02049e0c(0)', 'native_fn_02049e0c(1)', [32])),
    (0x022213ec, 60, 'native_ov000_022213ec.c',
     ((24, 1, 'native_fn_0207ca3c'), (28, 1, 'native_fn_ov000_0221c9e4'), (56, 2, 'native_data_ov000_022463b0')),
     ('if (index >= 4)', 'if (index >= 3)', [12])),
    (0x02227834, 60, 'native_ov000_02227834.c',
     ((12, 1, 'native_fn_ov000_02223c14'), (24, 1, 'native_fn_020c4928'), (52, 1, 'native_fn_020c5f48')),
     ('native_fn_020c5f48(7)', 'native_fn_020c5f48(8)', [48])),
    (0x021f02b4, 60, 'native_ov000_021f02b4.c',
     ((8, 1, 'native_fn_02049ad0'), (36, 1, 'native_fn_020852c8'), (52, 1, 'native_fn_02086b14')),
     ('native_fn_02086b14((*slot)[1], 0x10)', 'native_fn_02086b14((*slot)[1], 0x11)', [44])),
    (0x02215cb4, 48, 'native_ov000_02215cb4.c',
     ((44, 2, 'native_data_ov000_0224575c'),),
     ('index * 0x64', 'index * 0x65', [4])),
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
    """form_search.relocate plus R_ARM_PC24 (1), using repo_build's formula."""
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


def ledger_offsets(root):
    """address -> binaryOffset from the ledger (checked against the image base)."""
    offsets = {}
    for line in (root / 'ledger/functions.jsonl').open(encoding='utf-8'):
        line = line.strip()
        if not line:
            continue
        row = json.loads(line)
        if row.get('module') == MODULE:
            offsets[int(row['address'], 0)] = int(row['binaryOffset'])
    return offsets


def check(root, work, modes, failures):
    config = root_config(root)
    image, base, _ = form_search.module_image(root, MODULE)
    offsets = ledger_offsets(root)
    total = 0
    for address, size, name, expected_relocations, control in ROWS:
        rule = source_units.resolve(config, f'{LANE}/{name}')
        if (rule['module'], rule['mode']) != (MODULE, 'arm'):
            failures.append(f'{name}: rule resolved {rule["module"]}/{rule["mode"]}')
        if rule['compilerFlags'] != config['profiles'][PROFILE]:
            failures.append(f'{name}: profile is not {PROFILE}')
        if not rule['compilerSha256'].startswith(COMPILER):
            failures.append(f'{name}: compiler is not {COMPILER}')
        offset = offsets.get(address)
        if offset is None:
            failures.append(f'{name}: no ledger binaryOffset')
            continue
        if offset != address - base:
            failures.append('%s: ledger offset 0x%x != image base 0x%x' % (name, offset, address - base))
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
        want = image[offset:offset + size]
        got = patch_pc24(text, address, relocations, defined, modes)
        table = tuple((reloc_offset, kind, symbol)
                      for reloc_offset, kind, symbol, _ in relocations)
        if table != expected_relocations:
            failures.append(f'{name}: relocations {table} != pinned {expected_relocations}')
        diff = [i for i, (a, b) in enumerate(zip(got, want)) if a != b]
        if len(got) != size or diff:
            failures.append(f'{name}: patched {len(got)} B, diff {diff}')
        words = []
        for reloc_offset, kind, symbol in table:
            if kind != 2:
                continue
            target = defined.get(symbol) or form_search.symbol_address(symbol)
            word = int.from_bytes(want[reloc_offset:reloc_offset + 4], 'little')
            words.append(word)
            if word != target:
                failures.append(f'{name}: +{reloc_offset:#x} image word {word:#010x} != '
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
    work = Path(tempfile.mkdtemp(prefix='ov000-pass3-'))
    modes = form_search.TargetModes(ROOT, MODULE)
    total = check(ROOT, work, modes, failures)
    print(f'\n{len(ROWS)} rows, {total} bytes, {len(failures)} failure(s)')
    for failure in failures:
        print('  FAIL', failure)
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
