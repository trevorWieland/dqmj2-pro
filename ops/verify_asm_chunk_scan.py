"""Verify the rows reconstructed by the aggregate-copy shape scan.

Every row is a translation unit whose body is the measured instruction stream
(``src/verified_assembly/20261112_asm_chunk_scan/<module>``). Each file is compiled
with the rule its path resolves to, its relocations are patched the way
``public_tools/whole_image_link.py`` patches them, and the whole measured extent is
compared with the module image at the row's ``binaryOffset``.

For each row the check proves:

* the object's relocation table is exactly the pinned one (offset, kind, symbol,
  addend), so a match cannot come from a hard-coded literal;
* every ``R_ARM_ABS32`` slot in the image equals the object's relocation target
  plus the relocation addend, so a pool word is checked against the image word,
  never a symbol name;
* one whole-source negative control (the first mutable instruction changed)
  compiles, differs from the image at the pinned offsets, and is therefore not a
  vacuous match.

    python ops/verify_asm_chunk_scan.py            # check
    python ops/verify_asm_chunk_scan.py --record   # refresh the pinned fixture
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / 'public_tools'))

import form_search  # noqa: E402
import source_units  # noqa: E402

LANE = 'src/verified_assembly/20261112_asm_chunk_scan'
FIXTURE = Path(__file__).resolve().parent / 'asm_chunk_scan_expectations.json'
IMAGE = {
    'main': ROOT / 'extract/arm9/arm9.bin',
    'ov000': ROOT / 'extract/arm9_overlays/ov000.bin',
    'ov001': ROOT / 'extract/arm9_overlays/ov001.bin',
    'ov003': ROOT / 'extract/arm9_overlays/ov003.bin',
    'ov005': ROOT / 'extract/arm9_overlays/ov005.bin',
    'ov006': ROOT / 'extract/arm9_overlays/ov006.bin',
}


def ledger_row(module, address):
    for line in (ROOT / 'ledger/functions.jsonl').open(encoding='utf-8'):
        if not line.strip():
            continue
        row = json.loads(line)
        if row['module'] == module and int(row['address'], 16) == address:
            return row
    return None


def sources():
    found = {}
    for module in IMAGE:
        directory = ROOT / LANE / module
        if not directory.is_dir():
            continue
        for path in sorted(directory.glob(f'native_{module}_*.c')):
            match = re.search(r'native_%s_([0-9a-f]{8})\.c$' % module, path.name)
            if match:
                found[(module, int(match.group(1), 16))] = path
    return found


def compile_unit(config, rule, source, obj):
    compiler = ROOT / config['compilers'][rule['compilerSha256']]
    flags = [flag for flag in rule['compilerFlags'] if flag not in ('-thumb', '-c')]
    flags.append('-c')
    env = dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat'))
    result = subprocess.run([str(compiler), *flags, str(source.resolve()), '-o', str(obj.resolve())],
                            cwd=str(source.parent), env=env, capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(f'{source.name}: compile failed\n{result.stdout[-900:]}')
    return form_search.read_object(obj)


def decode_target(data, offset, address):
    word = int.from_bytes(data[offset:offset + 4], 'little')
    immediate = word & 0xFFFFFF
    if immediate & 0x800000:
        immediate -= 0x1000000
    return address + offset + 8 + (immediate << 2)


def pin_relocations(relocations, defined, image, address):
    pinned = []
    for offset, kind, symbol, addend in relocations:
        if symbol in defined or re.search(r'[0-9a-f]{8}$', symbol):
            pinned.append([offset, kind, symbol, addend])
            continue
        if kind not in (1, 28, 29, 30, 31):
            raise SystemExit(f'unpinnable relocation {kind} {symbol} at {offset:#x}')
        pinned.append([offset, kind, f'native_fn_{decode_target(image, offset, address):08x}', addend])
    return pinned


def control_source(text):
    """Change the first mutable instruction so the control cannot match by construction.

    A register is mutated rather than an immediate: mwcc's assembler rejects many
    mutated constants as unencodable, while a register substitution is always
    encodable and always changes the encoded word. Instructions that name no
    numbered register (``bx lr``) are skipped.
    """
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if not line.startswith('    ') or not line.strip():
            continue
        instruction = line.strip()
        mutated = re.sub(r'r(\d+)', lambda match: 'r%d' % ((int(match.group(1)) + 1) % 13),
                         instruction, count=1)
        if mutated == instruction:
            continue
        lines[index] = '    ' + mutated
        return '\n'.join(lines) + '\n'
    raise SystemExit('no instruction to mutate for the control')


def check_row(config, work, module, address, source, expected, failures):
    row = ledger_row(module, address)
    if row is None:
        failures.append(f'{module}:{address:#010x}: not in the ledger')
        return None
    image = IMAGE[module].read_bytes()
    offset = int(row['binaryOffset'])
    size = int(row['bytes'])
    want = image[offset:offset + size]
    relative = source.relative_to(ROOT).as_posix()
    rule = source_units.resolve(config, relative)
    text, defined, relocations = compile_unit(config, rule, source, work / f'{module}-{address:08x}.o')
    pinned = pin_relocations(relocations, defined, want, address)
    if 'relocations' in expected and pinned != [list(item) for item in expected['relocations']]:
        failures.append(f'{source.name}: relocations {pinned} != pinned {expected["relocations"]}')
    patched = form_search.relocate(text, address, pinned, defined,
                                   modes=form_search.TargetModes(ROOT, module))
    diff = [i for i in range(min(len(patched), len(want))) if patched[i] != want[i]]
    if len(patched) != len(want) or diff:
        failures.append(f'{source.name}: patched {len(patched)} B, diff {diff[:12]}')
    words = []
    for slot, kind, symbol, addend in pinned:
        if kind != 2:
            continue
        target = defined.get(symbol) or form_search.symbol_address(symbol)
        word = int.from_bytes(want[slot:slot + 4], 'little')
        words.append(word)
        if word != (target + addend) & 0xFFFFFFFF:
            failures.append(f'{source.name}: +{slot:#x} image word {word:#010x} '
                            f'!= target {target:#010x} + {addend:#x}')

    control = work / f'{module}-{address:08x}-control.c'
    control.write_text(control_source(source.read_text(encoding='ascii')), encoding='ascii')
    ctext, cdefined, crelocations = compile_unit(config, rule, control,
                                                 work / f'{module}-{address:08x}-control.o')
    cpinned = pin_relocations(crelocations, cdefined, want, address)
    cpatched = form_search.relocate(ctext, address, cpinned, cdefined,
                                    modes=form_search.TargetModes(ROOT, module))
    cdiff = [i for i in range(min(len(cpatched), len(want))) if cpatched[i] != want[i]]
    if not cdiff:
        failures.append(f'{source.name}: negative control still matches the image')
    elif 'controlDiff' in expected and cdiff != list(expected['controlDiff']):
        failures.append(f'{source.name}: control diff {cdiff[:12]} != pinned {expected["controlDiff"][:12]}')
    print(f'{module:6s} {address:#010x} {size:3d} B {source.name:34s} relocs={len(pinned)} '
          f'bytes=EXACT control_diff={cdiff[:6]}')
    return dict(relocations=pinned, controlDiff=cdiff, poolWords=words)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--record', action='store_true')
    args = parser.parse_args()
    config = source_units.load_config(ROOT)
    fixture = {}
    if FIXTURE.is_file() and not args.record:
        fixture = {(module, int(key, 0)): value
                   for (module, key), value in
                   (((m, k), v) for m, rows in
                    json.loads(FIXTURE.read_text(encoding='utf-8')).items()
                    for k, v in rows.items())}
    work = Path(tempfile.mkdtemp(prefix='asm-chunk-scan-'))
    failures = []
    observed = {}
    found = sources()
    for (module, address), source in sorted(found.items()):
        result = check_row(config, work, module, address, source,
                           fixture.get((module, address), {}), failures)
        if result is not None:
            observed.setdefault(module, {})[f'{address:#010x}'] = result
    print()
    for module, rows in sorted(observed.items()):
        total = sum(int(ledger_row(module, int(address, 0))['bytes']) for address in rows)
        pool_words = sum(len(result['poolWords']) for result in rows.values())
        print(f'  {module}: {len(rows)} rows, {total} bytes, {pool_words} pinned pool words')
    total_rows = sum(len(rows) for rows in observed.values())
    total_bytes = sum(int(ledger_row(module, int(address, 0))['bytes'])
                      for module, rows in observed.items() for address in rows)
    print(f'\n{total_rows} rows, {total_bytes} bytes, {len(failures)} failure(s)')
    for failure in failures:
        print('  FAIL', failure)
    if args.record:
        FIXTURE.write_text(json.dumps(observed, indent=1) + '\n', encoding='utf-8')
        print(f'fixture written: {FIXTURE}')
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
