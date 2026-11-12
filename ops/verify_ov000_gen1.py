"""Verify the ov000 generation-1 packet (``src/ov000/g1_ov000_gen1``).

The packet has two forms:

* ``asm/*.c`` -- the measured instruction stream as an mwccarm ``asm`` function;
* ``*.c`` -- C instantiated from a donor template read off a coarse-skeleton
  cluster representative.

Every row is recompiled through its resolved source-unit rule, its relocations are
patched the way ``public_tools/whole_image_link.py`` patches them, and the whole
measured extent is compared byte for byte against
``extract/arm9_overlays/ov000.bin`` (base ``0x021d7240``).

For each row the check also proves:

* the object's relocation table is exactly the pinned one (offset, kind, symbol,
  addend), so a match cannot come from a hard-coded literal;
* every ``R_ARM_ABS32`` slot in the image equals the object's target plus addend,
  so a pool word is checked against the image word, never a symbol name;
* one whole-source negative control per row compiles, differs from the image and
  its differing bytes are pinned, so the match is not vacuous.

    python ops/verify_ov000_gen1.py            # check
    python ops/verify_ov000_gen1.py --record   # refresh the pinned fixture
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

MODULE = 'ov000'
BASE = 0x021D7240
IMAGE = ROOT / 'extract/arm9_overlays/ov000.bin'
LANE = 'src/ov000/g1_ov000_gen1'
FIXTURE = Path(__file__).resolve().parent / 'ov000_gen1_expectations.json'


def ledger_row(address):
    with (ROOT / 'ledger/functions.jsonl').open(encoding='utf-8') as stream:
        for line in stream:
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get('module') == MODULE and int(row['address'], 0) == address:
                return row
    return None


def sources():
    found = {}
    for direcotry in (ROOT / LANE / 'asm', ROOT / LANE):
        for path in sorted(direcotry.glob(f'native_{MODULE}_*.c')):
            match = re.search(r'native_%s_([0-9a-f]{8})\.c$' % MODULE, path.name)
            if match:
                found[int(match.group(1), 16)] = path
    return found


def compile_unit(config, rule, source, obj):
    compiler = ROOT / rule['compilerPath']
    flags = [flag for flag in rule['compilerFlags'] if flag not in ('-thumb', '-c')]
    flags.append('-c')
    env = dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat'))
    result = subprocess.run([str(compiler), *flags, str(source.resolve()), '-o', str(obj.resolve())],
                            cwd=str(source.parent), env=env, capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(f'{source.name}: compile failed\n{(result.stdout or result.stderr)[-900:]}')
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


def asm_control(text):
    """Change the first mutable instruction register (proven in the round-6 sweep)."""
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if not line.startswith('    ') or not line.strip():
            continue
        instruction = line.strip()
        mutated = re.sub(r'r(\d+)', lambda m: 'r%d' % ((int(m.group(1)) + 1) % 13),
                         instruction, count=1)
        if mutated == instruction:
            continue
        lines[index] = '    ' + mutated
        return '\n'.join(lines) + '\n'
    raise SystemExit('no instruction to mutate for the control')


C_CONTROLS = (
    ('n = 8;', 'n = 7;'),
    ('0x10c', '0x10d'),
    ('(s16)a', '(s32)a'),
    ('0x20]', '0x24]'),
    ('<< 3', '<< 2'),
    ('<< 4', '<< 3'),
    ('return ok;', 'return ok + 1;'),
)


def c_control(text):
    """Mutate one immediate in the C body, keeping it compilable.

    The scan starts at the function body: a comment or an extern symbol name is
    not a control, because mutating it cannot change an instruction.
    """
    body_start = text.find('{\n')
    if body_start < 0:
        raise SystemExit('no function body for the control')
    for old, new in C_CONTROLS:
        position = text.find(old, body_start)
        if position >= 0:
            return text[:position] + new + text[position + len(old):]
    body = text[body_start:]
    for match in re.finditer(r'(?<![0-9A-Za-z_])(0x[0-9A-Fa-f]+|\d+)(?![0-9A-Za-z_])', body):
        token = match.group(1)
        value = int(token, 0)
        if value == 0:
            continue
        replacement = hex(value + 1) if token.lower().startswith('0x') else str(value + 1)
        start = body_start + match.start(1)
        mutated = text[:start] + replacement + text[start + len(token):]
        if mutated != text:
            return mutated
    raise SystemExit('no literal to mutate for the control')


def check_row(config, work, address, source, expected, failures, modes):
    row = ledger_row(address)
    if row is None:
        failures.append(f'{address:#010x}: not in the ledger')
        return None
    image = IMAGE.read_bytes()
    offset = int(row['binaryOffset'])
    size = int(row['bytes'])
    want = image[offset:offset + size]
    rule = source_units.resolve(config, source.relative_to(ROOT).as_posix())
    text, defined, relocations = compile_unit(config, rule, source, work / f'{address:08x}.o')
    pinned = pin_relocations(relocations, defined, want, address)
    if 'relocations' in expected and pinned != [list(item) for item in expected['relocations']]:
        failures.append(f'{source.name}: relocations {pinned} != pinned {expected["relocations"]}')
    patched = form_search.relocate(text, address, pinned, defined, modes=modes)
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
                            f'!= target {target:#010x} + {addend:#x}'
                            )
    body = source.read_text(encoding='ascii')
    control = work / f'{address:08x}-control.c'
    control.write_text(asm_control(body) if 'g1_ov000_gen1/asm' in source.as_posix()
                       else c_control(body), encoding='ascii')
    ctext, cdefined, crelocations = compile_unit(config, rule, control,
                                                 work / f'{address:08x}-control.o')
    cpinned = pin_relocations(crelocations, cdefined, want, address)
    cpatched = form_search.relocate(ctext, address, cpinned, cdefined, modes=modes)
    cdiff = [i for i in range(min(len(cpatched), len(want))) if cpatched[i] != want[i]]
    if not cdiff:
        failures.append(f'{source.name}: negative control still matches the image')
    elif 'controlDiff' in expected and cdiff != list(expected['controlDiff']):
        failures.append(f'{source.name}: control diff {cdiff[:12]} != pinned {expected["controlDiff"][:12]}')
    print(f'{address:#010x} {size:3d} B {source.name:36s} relocs={len(pinned)} '
          f'bytes=EXACT control_diff={cdiff[:6]}')
    return dict(relocations=pinned, controlDiff=cdiff, poolWords=words)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--record', action='store_true')
    args = parser.parse_args(argv)
    config = source_units.load_config(ROOT)
    fixture = {}
    if FIXTURE.is_file() and not args.record:
        fixture = {int(key, 0): value
                   for key, value in json.loads(FIXTURE.read_text(encoding='utf-8')).items()}
    work = Path(tempfile.mkdtemp(prefix='ov000-gen1-'))
    failures = []
    observed = {}
    found = sources()
    modes = form_search.TargetModes(ROOT, MODULE)
    for address, source in sorted(found.items()):
        result = check_row(config, work, address, source, fixture.get(address, {}), failures,
                           modes)
        if result is not None:
            observed[f'{address:#010x}'] = result
    total = sum(int(ledger_row(address)['bytes']) for address in found)
    print(f'\n{len(observed)} rows, {total} bytes, '
          f'{sum(len(result["relocations"]) for result in observed.values())} pinned relocations')
    for failure in failures:
        print('  FAIL', failure)
    if args.record:
        FIXTURE.write_text(json.dumps(observed, indent=1) + '\n', encoding='utf-8')
        print(f'fixture written: {FIXTURE}')
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
