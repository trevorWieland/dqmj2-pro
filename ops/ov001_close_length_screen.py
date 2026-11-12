"""Compile every lane file and report object-vs-image length (fast first screen)."""
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'ops'))
sys.path.insert(0, str(ROOT / 'public_tools'))

import form_search  # noqa: E402
import source_units  # noqa: E402
import verify_asm_chunk_scan as verify  # noqa: E402


def cached_ledger():
    rows = {}
    for line in (ROOT / 'ledger/functions.jsonl').open(encoding='utf-8'):
        if not line.strip():
            continue
        row = json.loads(line)
        rows[(row['module'], int(row['address'], 16))] = row
    return rows


def main():
    lane = sys.argv[1] if len(sys.argv) > 1 else 'src/ov001/p12_ov001_close/arm'
    ledger = cached_ledger()
    verify.ledger_row = lambda module, address: ledger.get((module, address))
    config = source_units.load_config(ROOT)
    work = Path(tempfile.mkdtemp(prefix='length-screen-'))
    image = (ROOT / 'extract/arm9_overlays/ov001.bin').read_bytes()
    bad = []
    for path in sorted((ROOT / lane / 'ov001').glob('native_ov001_*.c')):
        address = int(path.stem.split('_')[-1], 16)
        row = ledger[('ov001', address)]
        want = image[int(row['binaryOffset']):int(row['binaryOffset']) + int(row['bytes'])]
        rule = source_units.resolve(config, path.relative_to(ROOT).as_posix())
        try:
            text, defined, relocations = verify.compile_unit(config, rule, path,
                                                             work / ('%08x.o' % address))
        except SystemExit as error:
            bad.append((address, int(row['bytes']), 'compile', str(error).splitlines()[-1]))
            print('%-12s COMPILE FAIL %s' % ('0x%08x' % address, str(error).splitlines()[-1]))
            continue
        pinned = verify.pin_relocations(relocations, defined, want, address, 'arm')
        patched = form_search.relocate(text, address, pinned, defined,
                                       modes=form_search.TargetModes(ROOT, 'ov001'))
        if len(patched) != len(want):
            bad.append((address, int(row['bytes']), len(patched), 'length'))
            print('0x%08x image %4d B object %4d B  %+d' % (
                address, len(want), len(patched), len(patched) - len(want)))
            continue
        diff = [i for i in range(len(want)) if patched[i] != want[i]]
        if diff:
            bad.append((address, int(row['bytes']), len(patched), diff[:8]))
            print('0x%08x image %4d B same length, diff at %s' % (
                address, len(want), diff[:8]))
    print('\n%d rows screened, %d bad' % (len(list((ROOT / lane / 'ov001').glob('*.c'))),
                                          len(bad)))
    (ROOT / 'work/ov001-close/length-screen.json').write_text(
        json.dumps([{'address': '0x%08x' % b[0], 'imageBytes': b[1], 'detail': b[2:]}
                    for b in bad], indent=1) + '\n')
    return 0 if not bad else 1


if __name__ == '__main__':
    sys.exit(main())
