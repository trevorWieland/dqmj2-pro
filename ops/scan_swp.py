"""Scan the extracted images for ARM/Thumb SWP/SWPB instructions.

`-avoid_byte strb` makes mwcc materialise a member read-modify-write through a scratch
register, and on ARM that path uses `swp`/`swpb`. Two zero-swp results are therefore
evidence the flag route does not apply; a hit would rule it IN.

ARM encoding (unambiguous 32-bit word match):
    cond 00010 B 00 Rn Rd 0000 1001 Rm
    mask 0x0FB00FF0, value 0x01000090 (SWP) or 0x01400090 (SWPB, bit 22)

Thumb-1 encoding collides with PUSH (0xB4xx), so the Thumb pass reports candidates and
marks them inconclusive rather than counting them as hits.
"""
import argparse
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def scan_arm(data):
    hits = []
    for offset in range(0, len(data) - 3, 4):
        word = struct.unpack_from('<I', data, offset)[0]
        if (word & 0x0FB00FF0) == 0x01000090:
            hits.append((offset, 'swp', word))
        elif (word & 0x0FB00FF0) == 0x01400090:
            hits.append((offset, 'swpb', word))
    return hits


def scan_thumb(data):
    candidates = 0
    for offset in range(0, len(data) - 1, 2):
        half = struct.unpack_from('<H', data, offset)[0]
        if (half & 0xFF00) == 0xB400:
            candidates += 1
    return candidates


def images(root):
    for path in sorted((root / 'extract').rglob('*.bin')):
        yield path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--root', default=str(ROOT))
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()

    total_swp = 0
    total_thumb = 0
    scanned = 0
    for path in images(root):
        data = path.read_bytes()
        scanned += 1
        hits = scan_arm(data)
        candidates = scan_thumb(data)
        total_swp += len(hits)
        total_thumb += candidates
        if hits:
            relative = path.relative_to(root).as_posix()
            for offset, kind, word in hits[:6]:
                print(f'  ARM HIT {relative}+{offset:#x} {kind} word={word:#010x}')
    print(f'images scanned: {scanned}')
    print(f'ARM swp/swpb hits: {total_swp}')
    print(f'Thumb 0xB4xx halfwords (SWP or PUSH, inconclusive): {total_thumb}')
    return 0 if total_swp == 0 else 1


if __name__ == '__main__':
    raise SystemExit(main())
