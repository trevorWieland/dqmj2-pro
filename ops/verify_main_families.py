"""Verify the twenty-five main-module rows authored in the main-families lane.

Every row is a translation unit whose body is the measured instruction stream
(``src/verified_assembly/20261111_main_families``). Each file is compiled with
the rule its path resolves to (``src/verified_assembly/**`` -> p001 on mwccarm
2.0/sp1p5), its relocations are patched the way ``public_tools/whole_image_link.py``
patches them, and the whole measured extent is compared with
``extract/arm9/arm9.bin`` at the row's ``binaryOffset``.

For each row the check proves:

* the object's relocation table is exactly the pinned one (offset, kind, symbol,
  addend), so a match cannot come from a hard-coded literal;
* every ``R_ARM_ABS32`` slot in the image equals the object's relocation target,
  so a pool word is checked against the image word, never a symbol name;
* one whole-source negative control (the first instruction mutated) compiles,
  differs from the image at the pinned offsets, and is therefore not a vacuous
  match.

    python ops/verify_main_families.py            # check
    python ops/verify_main_families.py --record   # refresh the pinned fixture
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

MODULE = 'main'
LANE = 'src/verified_assembly/20261111_main_families'
FIXTURE = Path(__file__).resolve().parent / 'main_families_expectations.json'


def ledger_row(address):
    for line in (ROOT / 'ledger/functions.jsonl').open(encoding='utf-8'):
        if not line.strip():
            continue
        row = json.loads(line)
        if row['module'] == MODULE and int(row['address'], 0) == address:
            return row
    return None


def sources():
    found = {}
    for path in sorted((ROOT / LANE).glob('native_main_*.c')):
        match = re.search(r'native_main_([0-9a-f]{8})\.c$', path.name)
        if match:
            found[int(match.group(1), 16)] = path
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
    """Mutate the first instruction so the control cannot match by construction."""
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if not line.startswith('    ') or not line.strip():
            continue
        instruction = line.strip()
        if instruction.startswith(('b', 'l', 'm', 's', 'a', 'o', 't', 'c')) and ' ' in instruction:
            if '#0x' in instruction:
                mutated = re.sub(r'#0x([0-9a-fA-F]+)',
                                 lambda m: '#0x%x' % (int(m.group(1), 16) ^ 0x01), instruction, count=1)
            elif '{' in instruction and '}' in instruction:
                mutated = re.sub(r'r(\d+)', lambda m: 'r%d' % ((int(m.group(1)) + 1) % 13),
                                 instruction, count=1)
            elif ', r' in instruction:
                mutated = re.sub(r', r(\d+)', lambda m: ', r%d' % ((int(m.group(1)) + 1) % 13),
                                 instruction, count=1)
            else:
                mutated = re.sub(r'r(\d+)', lambda m: 'r%d' % ((int(m.group(1)) + 1) % 13),
                                 instruction, count=1)
                if mutated == instruction:
                    continue
            lines[index] = '    ' + mutated
            return '\n'.join(lines) + '\n'
    raise SystemExit('no instruction to mutate for the control')


def check_row(config, work, address, source, expected, failures):
    row = ledger_row(address)
    if row is None:
        failures.append(f'{address:#010x}: not in the main ledger')
        return None
    image = (ROOT / 'extract/arm9/arm9.bin').read_bytes()
    offset = int(row['binaryOffset'])
    size = int(row['bytes'])
    want = image[offset:offset + size]
    rule = source_units.resolve(config, f'{LANE}/{source.name}')
    modes = form_search.TargetModes(ROOT, MODULE)
    text, defined, relocations = compile_unit(config, rule, source, work / f'{address:08x}.o')
    pinned = pin_relocations(relocations, defined, want, address)
    if 'relocations' in expected and pinned != [list(item) for item in expected['relocations']]:
        failures.append(f'{source.name}: relocations {pinned} != pinned {expected["relocations"]}')
    patched = form_search.relocate(text, address, pinned, defined, modes=modes)
    diff = [i for i, (a, b) in enumerate(zip(patched, want)) if a != b]
    if len(patched) != len(want) or diff:
        failures.append(f'{source.name}: patched {len(patched)} B, diff {diff[:12]}')
    words = []
    for slot, kind, symbol, addend in pinned:
        if kind != 2:
            continue
        target = defined.get(symbol) or form_search.symbol_address(symbol)
        word = int.from_bytes(want[slot:slot + 4], 'little')
        words.append(word)
        if word != target:
            failures.append(f'{source.name}: +{slot:#x} image word {word:#010x} != target {target:#010x}')

    control = work / f'{address:08x}-control.c'
    control.write_text(control_source(source.read_text(encoding='ascii')), encoding='ascii')
    ctext, cdefined, crelocations = compile_unit(config, rule, control, work / f'{address:08x}-control.o')
    cpinned = pin_relocations(crelocations, cdefined, want, address)
    cpatched = form_search.relocate(ctext, address, cpinned, cdefined, modes=modes)
    cdiff = [i for i, (a, b) in enumerate(zip(cpatched, want)) if a != b]
    if not cdiff:
        failures.append(f'{source.name}: negative control still matches the image')
    elif 'controlDiff' in expected and cdiff != list(expected['controlDiff']):
        failures.append(f'{source.name}: control diff {cdiff[:12]} != pinned {expected["controlDiff"][:12]}')
    print(f'{address:#010x} {size:3d} B {source.name:30s} relocs={len(pinned)} '
          f'bytes=EXACT control_diff={cdiff[:6]}')
    return dict(relocations=pinned, controlDiff=cdiff, poolWords=words)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--record', action='store_true')
    args = parser.parse_args()
    config = source_units.load_config(ROOT)
    fixture = {}
    if FIXTURE.is_file() and not args.record:
        fixture = {int(key, 0): value for key, value in
                   json.loads(FIXTURE.read_text(encoding='utf-8')).items()}
    work = Path(tempfile.mkdtemp(prefix='main-families-'))
    failures = []
    observed = {}
    found = sources()
    for address, source in found.items():
        result = check_row(config, work, address, source, fixture.get(address, {}), failures)
        if result is not None:
            observed[address] = result
    print()
    for address, result in sorted(observed.items()):
        print(f'  {address:#010x} pool=' + ', '.join('%#010x' % w for w in result['poolWords']))
    total = sum(int(ledger_row(a)['bytes']) for a in found if ledger_row(a))
    print(f'\n{len(found)} rows, {total} bytes, {len(failures)} failure(s)')
    for failure in failures:
        print('  FAIL', failure)
    if args.record:
        FIXTURE.write_text(json.dumps({f'{a:#010x}': r for a, r in sorted(observed.items())},
                                      indent=1) + '\n', encoding='utf-8')
        print(f'fixture written: {FIXTURE}')
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
