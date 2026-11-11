"""Apply a byte patch spec to a Nintendo DS ROM image, refusing unsafe edits.

A patch spec is a small JSON document:

    {
      "input": "inputs/game.nds",
      "output": "build/mods/title/game-mod.nds",
      "fixHeaderChecksum": true,
      "patches": [
        {"offset": "0x00B", "before": "50", "after": "4D",
         "note": "title last character P -> M"}
      ]
    }

Every patch must carry the bytes expected at that offset. If they do not match,
the tool changes nothing and exits non-zero: a patch written for one ROM revision
can therefore never silently corrupt a different one. The output is always a new
file; the input image is never modified, and an output path that resolves to the
input is refused.

Header checksum
---------------
The DS header carries a **CRC-16** at ROM offset 0x15E (poly 0xA001, init 0xFFFF)
over bytes 0x000..0x15D, and a second CRC-16 at 0x15C over the logo, bytes
0xC0..0x15B. This mirrors `audit_regions.py` (`nds_header`) and
`utility_runtime.py:180`, which use `ndspy._common.crc16` for both. It is *not* a
byte sum: the provided image stores 0x82CD and the CRC-16 reproduces it exactly.

`--verify-header` mirrors the repository validator: logo CRC, header CRC and the
eight header fields (`8I` at 0x20) are checked, and the command fails if the image
would not pass it.

Usage
-----
    python ops/mod_patch.py --spec docs/modding/example-title.json --check
    python ops/mod_patch.py --spec docs/modding/example-title.json
    python ops/mod_patch.py --spec <spec> --dry-run
    python ops/mod_patch.py --spec <spec> --verify-header build/mods/title/game-title.nds

Exit codes: 0 success, 1 bad spec / before-byte mismatch / header invalid,
2 I/O problem.
"""
import argparse
import json
import struct
import sys
from pathlib import Path

CHECKSUM_OFFSET = 0x15E
CHECKSUM_RANGE = 0x15E
LOGO_OFFSET = 0x15C
LOGO_RANGE = slice(0xC0, 0x15C)
HEADER_FIELDS = 0x20


def parse_int(value):
    if isinstance(value, int):
        return value
    return int(str(value), 0)


def crc16(data):
    """CRC-16/ARC: polynomial 0xA001 reflected, initial value 0xFFFF."""
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            crc = (crc >> 1) ^ 0xA001 if crc & 1 else crc >> 1
    return crc & 0xFFFF


def header_checksum(image):
    """CRC-16 over the header bytes 0x000..0x15D, as the DS validator expects."""
    return crc16(image[:CHECKSUM_RANGE])


def verify_header(image):
    """Mirror of audit_regions.nds_header: logo CRC, header CRC and field bounds."""
    problems = []
    if len(image) < 0x160:
        return ['image shorter than the header']
    stored_logo = struct.unpack_from('<H', image, LOGO_OFFSET)[0]
    if crc16(image[LOGO_RANGE]) != stored_logo:
        problems.append(f'logo CRC mismatch: stored {stored_logo:#06x}, '
                        f'computed {crc16(image[LOGO_RANGE]):#06x}')
    stored = struct.unpack_from('<H', image, CHECKSUM_OFFSET)[0]
    computed = header_checksum(image)
    if stored != computed:
        problems.append(f'header CRC mismatch: stored {stored:#06x}, computed {computed:#06x}')
    fields = struct.unpack_from('<8I', image, HEADER_FIELDS)
    for index in (0, 4):
        if fields[index] < 0x200:
            problems.append(f'header field {index} offset {fields[index]:#x} < 0x200')
        if fields[index + 3] == 0:
            problems.append(f'header field {index + 3} size is zero')
        if fields[index] + fields[index + 3] > len(image):
            problems.append(f'header field {index} range exceeds the image')
    return problems


def load_spec(path):
    spec = json.loads(Path(path).read_text())
    for field in ('input', 'patches'):
        if field not in spec:
            raise ValueError(f'spec is missing "{field}"')
    if not spec['patches']:
        raise ValueError('spec has no patches')
    return spec


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--spec', help='patch spec JSON (required unless --verify-header)')
    parser.add_argument('--root', default='.', help='directory the spec paths are relative to')
    parser.add_argument('--check', action='store_true', help='verify only, write nothing')
    parser.add_argument('--dry-run', action='store_true', help='verify and report, write nothing')
    parser.add_argument('--verify-header', metavar='IMAGE',
                        help='validate an image header and exit')
    args = parser.parse_args(argv)

    root = Path(args.root)

    if args.verify_header:
        image = Path(args.verify_header).read_bytes()
        problems = verify_header(image)
        if problems:
            print('header INVALID:')
            for problem in problems:
                print(f'  {problem}')
            return 1
        stored = struct.unpack_from('<H', image, CHECKSUM_OFFSET)[0]
        print(f'header valid: logo CRC ok, header CRC {stored:#06x}, fields in range')
        return 0

    if not args.spec:
        parser.error('--spec is required unless --verify-header is given')

    try:
        spec = load_spec(args.spec)
    except (OSError, ValueError) as error:
        print(f'error: {error}', file=sys.stderr)
        return 1

    source = (root / spec['input']).resolve()
    if not source.is_file():
        print(f'error: input image not found: {source}', file=sys.stderr)
        return 2
    output = (root / spec.get('output', str(source.with_suffix('.mod.nds')))).resolve()
    if output == source:
        print('error: output resolves to the input image; refusing to overwrite it in place',
              file=sys.stderr)
        return 1

    image = bytearray(source.read_bytes())
    stored = struct.unpack_from('<H', image, CHECKSUM_OFFSET)[0]
    computed = header_checksum(image)
    print(f'input      {source} ({len(image)} bytes)')
    print(f'checksum   stored {stored:#06x}  computed {computed:#06x}  '
          f'{"match" if stored == computed else "MISMATCH"}')

    failures = 0
    for index, patch in enumerate(spec['patches']):
        offset = parse_int(patch['offset'])
        before = bytes.fromhex(patch['before'])
        after = bytes.fromhex(patch['after'])
        if len(before) != len(after):
            print(f'patch {index}: before/after length differ', file=sys.stderr)
            failures += 1
            continue
        window = bytes(image[offset:offset + len(before)])
        status = 'ok' if window == before else 'MISMATCH'
        print(f'patch {index}  {offset:#08x}  {len(before)} B  {status}'
              + (f'  ({patch["note"]})' if patch.get('note') else ''))
        if window != before:
            print(f'  expected {before.hex()}  found {window.hex()}', file=sys.stderr)
            failures += 1
            continue
        image[offset:offset + len(after)] = after

    if failures:
        print(f'\nrefusing to write: {failures} problem(s); image unchanged', file=sys.stderr)
        return 1

    new_checksum = header_checksum(image)
    if spec.get('fixHeaderChecksum', True):
        struct.pack_into('<H', image, CHECKSUM_OFFSET, new_checksum)
        print(f'checksum   written {new_checksum:#06x}')
    else:
        print(f'checksum   left as stored (recomputed would be {new_checksum:#06x})')

    problems = verify_header(image)
    if problems:
        print('refusing to write: the patched header would not validate:', file=sys.stderr)
        for problem in problems:
            print(f'  {problem}', file=sys.stderr)
        return 1
    print('header     valid after patch (logo CRC, header CRC, field bounds)')

    if args.check:
        print('\n--check: verification passed, nothing written')
        return 0
    if args.dry_run:
        print('\n--dry-run: patches verified, nothing written')
        return 0

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(image)
    print(f'\nwrote {output} ({len(image)} bytes)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
