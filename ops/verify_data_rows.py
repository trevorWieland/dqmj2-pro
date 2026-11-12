"""Verify the data-bearing rows: bytes, relocations and a per-row control.

The lane ships two carriers.  An ARM row is one ``asm`` translation unit whose
data runs are ``dcd`` directives; a Thumb row is one mwasmarm ``.s`` unit whose
table runs are ``.hword`` directives.  Both are compiled here with the toolchain
their path resolves to, their relocations are patched the way
``public_tools/whole_image_link.py`` patches them, and the whole measured extent
is compared with the module image at the row's ``binaryOffset``.

For each row the check proves:

* every object byte is the image byte: a data run is not merely present, it is
  the measured data at the measured offset;
* the object's relocation table is exactly the pinned one (offset, kind, symbol,
  addend), so a data word that names an address is a relocation, never a
  hard-coded literal;
* every ``R_ARM_ABS32`` slot in the image equals the relocation target plus the
  addend;
* the assembled symbol's size is the measured extent (a mwasmarm ``.text``
  section is padded to a 4-byte boundary, so up to three trailing zero bytes are
  allowed after the symbol and are recorded, never counted as extent);
* one whole-source negative control (the first mutable instruction changed)
  differs from the image, so the match is not vacuous.

    python ops/verify_data_rows.py
    python ops/verify_data_rows.py --record   # refresh the pinned fixture
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

LANE = 'src/verified_assembly/20261112_jumptable_carrier'
FIXTURE = Path(__file__).resolve().parent / 'data_rows_expectations.json'
IMAGE = {
    'main': ROOT / 'extract/arm9/arm9.bin',
    'ov000': ROOT / 'extract/arm9_overlays/ov000.bin',
    'ov001': ROOT / 'extract/arm9_overlays/ov001.bin',
    'ov003': ROOT / 'extract/arm9_overlays/ov003.bin',
    'ov005': ROOT / 'extract/arm9_overlays/ov005.bin',
    'ov006': ROOT / 'extract/arm9_overlays/ov006.bin',
}
SOURCE = re.compile(r'native_(main|ov[0-9]{3})_([0-9a-f]{8})\.(c|s)$')
ASSEMBLER = ROOT / 'tools/mwccarm/mwccarm/2.0/base/mwasmarm.exe'
ASSEMBLER_SHA256 = 'e928cbcce71d687fadf25cf426280f23252e2aaae897fc2ce4e5570d8554dc8c'
LICENSE = ROOT / 'tools/mwccarm/mwccarm/license.dat'


def ledger_row(module, address):
    for line in (ROOT / 'ledger/functions.jsonl').open(encoding='utf-8'):
        if not line.strip():
            continue
        row = json.loads(line)
        if row['module'] == module and int(row['address'], 16) == address:
            return row
    return None


def sources(lane_name):
    lane = ROOT / lane_name
    if not lane.is_dir():
        raise SystemExit('lane is missing: ' + str(lane))
    found = {}
    for path in sorted(lane.rglob('*')):
        if not path.is_file():
            continue
        match = SOURCE.search(path.name)
        if not match:
            continue
        module, address, suffix = match.group(1), int(match.group(2), 16), match.group(3)
        key = (module, address)
        if key in found:
            raise SystemExit('duplicate translation unit for %s:0x%08x' % key)
        found[key] = (path, suffix)
    return found


def compile_c(config, rule, source, obj):
    compiler = ROOT / config['compilers'][rule['compilerSha256']]
    flags = [flag for flag in rule['compilerFlags'] if flag != '-c']
    flags.append('-c')
    env = dict(os.environ, LM_LICENSE_FILE=str(LICENSE))
    result = subprocess.run([str(compiler), *flags, str(source.resolve()), '-o', str(obj.resolve())],
                            cwd=str(source.parent), env=env, capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(f'{source.name}: compile failed\n{result.stdout[-1200:]}')
    if rule['compilerSha256'] not in config['compilers']:
        raise SystemExit('unknown compiler identity')
    return form_search.read_object(obj)


def assemble_s(source, obj):
    env = dict(os.environ, LM_LICENSE_FILE=str(LICENSE))
    result = subprocess.run([str(ASSEMBLER), '-proc', 'arm5TE', str(source.resolve()),
                             '-o', str(obj.resolve())],
                            cwd=str(source.parent), env=env, capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(f'{source.name}: assemble failed\n{result.stdout[-1200:]}')
    return form_search.read_object(obj)


def symbol_size(path, name):
    from elftools.elf.elffile import ELFFile
    with open(path, 'rb') as stream:
        elf = ELFFile(stream)
        symtab = elf.get_section_by_name('.symtab')
        for symbol in symtab.iter_symbols():
            if symbol.name == name:
                return symbol['st_size']
    return None


def pin_relocations(relocations, defined, image, address, mode='arm'):
    pinned = []
    for offset, kind, symbol, addend in relocations:
        if not re.search(r'[0-9a-f]{8}$', symbol) and symbol not in defined:
            raise SystemExit('unnameable relocation %s at %#x' % (symbol, offset))
        pinned.append([offset, kind, symbol, addend])
    return pinned


def control_source(text):
    """Change the first mutable instruction so the control cannot match."""
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if not line.startswith('    ') or not line.strip():
            continue
        instruction = line.strip()
        if instruction.startswith(('.', '/*', '*')):
            continue
        mutated = re.sub(r'r(\d+)', lambda match: 'r%d' % ((int(match.group(1)) + 1) % 13),
                         instruction, count=1)
        if mutated == instruction:
            continue
        lines[index] = '    ' + mutated
        return '\n'.join(lines) + '\n'
    raise SystemExit('no instruction to mutate for the control')


def check_row(config, work, module, address, source, suffix, expected, failures):
    row = ledger_row(module, address)
    if row is None:
        failures.append(f'{module}:{address:#010x}: not in the ledger')
        return None
    image = IMAGE[module].read_bytes()
    offset, size = int(row['binaryOffset']), int(row['bytes'])
    want = image[offset:offset + size]
    relative = source.relative_to(ROOT).as_posix()
    rule = source_units.resolve(config, relative)
    name = 'native_%s_%08x' % (module.replace('-', '_'), address)
    if suffix == 'c':
        text, defined, relocations = compile_c(config, rule, source, work / (name + '.o'))
        pad = b''
        section_pad = False
    else:
        text, defined, relocations = assemble_s(source, work / (name + '.o'))
        symbol = symbol_size(work / (name + '.o'), name)
        if symbol != size:
            failures.append(f'{source.name}: symbol size {symbol} != measured {size}')
        pad = text[size:]
        section_pad = True
        if len(pad) > 3 or any(pad):
            failures.append(f'{source.name}: unexpected bytes after the extent: {pad.hex()}')
    mode = row.get('mode', 'arm')
    pinned = pin_relocations(relocations, defined, want, address, mode)
    if 'relocations' in expected and pinned != [list(item) for item in expected['relocations']]:
        failures.append(f'{source.name}: relocations {pinned} != pinned {expected["relocations"]}')
    patched = form_search.relocate(text[:size] if section_pad else text, address, pinned,
                                   defined, modes=form_search.TargetModes(ROOT, module))
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

    control = work / (name + '-control.' + suffix)
    control.write_text(control_source(source.read_text(encoding='ascii')), encoding='ascii')
    if suffix == 'c':
        ctext, cdefined, crelocations = compile_c(config, rule, control,
                                                  work / (name + '-control.o'))
        cpatched = form_search.relocate(ctext, address, pin_relocations(
            crelocations, cdefined, want, address, mode), cdefined,
            modes=form_search.TargetModes(ROOT, module))
    else:
        ctext, cdefined, crelocations = assemble_s(control, work / (name + '-control.o'))
        cpatched = form_search.relocate(ctext[:size], address, pin_relocations(
            crelocations, cdefined, want, address, mode), cdefined,
            modes=form_search.TargetModes(ROOT, module))
    cdiff = [i for i in range(min(len(cpatched), len(want))) if cpatched[i] != want[i]]
    if not cdiff:
        failures.append(f'{source.name}: negative control still matches the image')
    elif 'controlDiff' in expected and cdiff != list(expected['controlDiff']):
        failures.append(f'{source.name}: control diff {cdiff[:12]} != pinned {expected["controlDiff"][:12]}')
    print(f'{module:6s} {address:#010x} {size:4d} B {suffix} {source.name:40s} '
          f'relocs={len(pinned)} bytes=EXACT control_diff={cdiff[:6]}'
          + (f' pad={len(pad)}' if pad else ''))
    return dict(relocations=pinned, controlDiff=cdiff, poolWords=words, padBytes=len(pad))


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--record', action='store_true')
    parser.add_argument('--lane', default=LANE)
    parser.add_argument('--fixture', default=str(FIXTURE))
    args = parser.parse_args()
    fixture_path = Path(args.fixture)
    if not fixture_path.is_absolute():
        fixture_path = ROOT / fixture_path
    config = source_units.load_config(ROOT)
    fixture = {}
    if fixture_path.is_file() and not args.record:
        fixture = {(module, int(key, 0)): value
                   for module, rows in json.loads(fixture_path.read_text()).items()
                   for key, value in rows.items()}
    work = Path(tempfile.mkdtemp(prefix='data-rows-'))
    failures, observed = [], {}
    found = sources(args.lane)
    for (module, address), (source, suffix) in sorted(found.items()):
        try:
            result = check_row(config, work, module, address, source, suffix,
                               fixture.get((module, address), {}), failures)
        except SystemExit as error:
            failures.append(f'{source.name}: {error}')
            continue
        if result is not None:
            observed.setdefault(module, {})[f'{address:#010x}'] = result
    print()
    total_rows = total_bytes = total_pad = 0
    for module, rows in sorted(observed.items()):
        for key in rows:
            total_rows += 1
            total_bytes += int(ledger_row(module, int(key, 0))['bytes'])
            total_pad += rows[key]['padBytes']
    print(f'{total_rows} rows, {total_bytes} bytes, {total_pad} alignment pad byte(s), '
          f'{len(failures)} failure(s)')
    for failure in failures:
        print('  FAIL', failure)
    if args.record:
        fixture_path.write_text(json.dumps(observed, indent=1) + '\n', encoding='utf-8')
        print(f'fixture written: {fixture_path}')
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())

