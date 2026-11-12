"""Compile one plausible C body for an unmatched row and diff it against the image.

This is the C-attempt half of the aggregate-copy triage: before a row is
transcribed as assembly, a plausible C form has to be written, compiled with the
row's rule and compared with the measured bytes at the row's ``binaryOffset``. A
row whose C form matches is shipped as C; the rest are transcribed.

    python ops/probe_c.py --module main --address 0x2008ca4 --bytes 56 --source probe.c
    python ops/probe_c.py --batch work/asm-chunk-scan/probes

A batch file is named ``probe_<module>_<address:08x>.c``; the ledger supplies the
size. A trailing ``_<n>`` is allowed so several plausible bodies can be probed per
row. The row's ledger mode adds ``-thumb`` and the relocation patcher decodes the
Thumb ``BL``/``BLX`` pair, so a Thumb probe is compared on the same terms as ARM.
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

IMAGE = {
    'main': 'extract/arm9/arm9.bin',
    'itcm': 'extract/arm9/itcm.bin',
    'dtcm': 'extract/arm9/dtcm.bin',
    'ov000': 'extract/arm9_overlays/ov000.bin',
    'ov001': 'extract/arm9_overlays/ov001.bin',
    'ov002': 'extract/arm9_overlays/ov002.bin',
    'ov003': 'extract/arm9_overlays/ov003.bin',
    'ov004': 'extract/arm9_overlays/ov004.bin',
    'ov005': 'extract/arm9_overlays/ov005.bin',
    'ov006': 'extract/arm9_overlays/ov006.bin',
    'ov007': 'extract/arm9_overlays/ov007.bin',
}


def ledger_rows(root):
    rows = {}
    for line in (root / 'ledger/functions.jsonl').open(encoding='utf-8'):
        if not line.strip():
            continue
        row = json.loads(line)
        rows[(row['module'], int(row['address'], 16))] = row
    return rows


def decode_target(data, offset, address, mode='arm'):
    """Decode a call's measured target, ARM or Thumb, from the image bytes."""
    if mode == 'thumb':
        first = int.from_bytes(data[offset:offset + 2], 'little')
        second = int.from_bytes(data[offset + 2:offset + 4], 'little')
        base = ((address + offset + 4) & ~3) if (second & 0xD000) == 0xC000 \
            else (address + offset + 4)
        sign = (first >> 10) & 1
        i1 = (((second >> 13) & 1) ^ sign) ^ 1
        i2 = (((second >> 11) & 1) ^ sign) ^ 1
        delta = (sign << 24) | (i1 << 23) | (i2 << 22) | ((first & 0x3FF) << 12) \
            | ((second & 0x7FF) << 1)
        if delta & (1 << 24):
            delta -= 1 << 25
        return base + delta
    word = int.from_bytes(data[offset:offset + 4], 'little')
    immediate = word & 0xFFFFFF
    if immediate & 0x800000:
        immediate -= 0x1000000
    return address + offset + 8 + (immediate << 2)


def pin_relocations(relocations, defined, image, address, mode='arm'):
    pinned = []
    for offset, kind, symbol, addend in relocations:
        if symbol in defined or re.search(r'[0-9a-f]{8}$', symbol):
            pinned.append([offset, kind, symbol, addend])
            continue
        if kind not in (1, 10, 16, 28, 29, 30, 31):
            raise SystemExit(f'unpinnable relocation {kind} {symbol} at {offset:#x}')
        pinned.append([offset, kind,
                       f'native_fn_{decode_target(image, offset, address, mode):08x}', addend])
    return pinned


def compile_unit(config, flags, source, obj):
    compiler = ROOT / config['compilers'][flags['compilerSha256']]
    arguments = [flag for flag in flags['compilerFlags'] if flag != '-c']
    arguments.append('-c')
    env = dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat'))
    result = subprocess.run([str(compiler), *arguments, str(source.resolve()), '-o', str(obj.resolve())],
                            cwd=str(source.parent), env=env, capture_output=True, text=True)
    return result


def probe(config, module, address, source, extra_flags=None):
    rule = source_units.resolve(config, 'src/verified_assembly/20260601_probe/x.c')
    flags = {'compilerSha256': rule['compilerSha256'],
             'compilerFlags': list(rule['compilerFlags'])}
    if extra_flags:
        flags['compilerFlags'] = list(extra_flags)
    rows = ledger_rows(ROOT)
    row = rows.get((module, address))
    if row is None:
        raise SystemExit(f'{module}:{address:#x}: not in the ledger')
    mode = row.get('mode', 'arm')
    if mode == 'thumb' and '-thumb' not in flags['compilerFlags']:
        flags['compilerFlags'] = list(flags['compilerFlags']) + ['-thumb']
    image = (ROOT / IMAGE[module]).read_bytes()
    offset = int(row['binaryOffset'])
    want = image[offset:offset + int(row['bytes'])]
    with tempfile.TemporaryDirectory(prefix='probe-c-') as work:
        obj = Path(work) / 'probe.o'
        result = compile_unit(config, flags, source, obj)
        if result.returncode != 0:
            print(result.stdout[-1200:])
            raise SystemExit(f'{source.name}: compile failed')
        text, defined, relocations = form_search.read_object(obj)
    pinned = pin_relocations(relocations, defined, want, address, mode)
    patched = form_search.relocate(text, address, pinned, defined,
                                   modes=form_search.TargetModes(ROOT, module))
    diff = [index for index in range(min(len(patched), len(want)))
            if patched[index] != want[index]]
    return {'module': module, 'address': address, 'bytes': len(want),
            'source': source.name, 'length': len(patched), 'relocations': len(pinned),
            'diff': diff, 'patched': patched, 'want': want}


def report(result, verbose=True):
    exact = result['length'] == result['bytes'] and not result['diff']
    if verbose:
        print('%s %s %s %d/%d B relocs=%d diff=%d' % (
            result['module'], '0x%08x' % result['address'],
            'EXACT' if exact else 'differ', result['length'], result['bytes'],
            result['relocations'], len(result['diff'])))
        for offset in result['diff'][:8]:
            begin = offset & ~3
            got = int.from_bytes(result['patched'][begin:begin + 4], 'little')
            exp = int.from_bytes(result['want'][begin:begin + 4], 'little')
            print('   +0x%04x image %08x object %08x' % (begin, exp, got))
    return exact


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--module', default=None)
    parser.add_argument('--address', default=None)
    parser.add_argument('--bytes', type=int, default=None)
    parser.add_argument('--source', type=Path, default=None)
    parser.add_argument('--batch', type=Path, default=None)
    parser.add_argument('--flags', default=None, help='override the flag profile id list')
    parser.add_argument('--quiet', action='store_true')
    args = parser.parse_args(argv)
    config = source_units.load_config(ROOT)
    extra = None
    if args.flags:
        profile = config['profiles'][args.flags]
        extra = [flag for flag in profile if flag not in ('-thumb', '-c')]
    if args.batch:
        found = sorted(args.batch.glob('probe_*.c'))
        exact = 0
        for path in found:
            match = re.match(r'probe_([a-z0-9]+)_([0-9a-f]{8})(?:_([0-9]+))?\.c$', path.name)
            if not match:
                continue
            module, address = match.group(1), int(match.group(2), 16)
            result = probe(config, module, address, path, extra)
            exact += bool(report(result, not args.quiet))
        print('\n%d/%d exact' % (exact, len(found)))
        return 0 if exact == len(found) else 1
    if not (args.module and args.address and args.source):
        parser.error('--module, --address and --source are required without --batch')
    result = probe(config, args.module, int(args.address, 0), args.source, extra)
    return 0 if report(result) else 1


if __name__ == '__main__':
    sys.exit(main())
