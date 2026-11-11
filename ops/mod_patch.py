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
file; the input image is never modified in place.

Header checksum
---------------
The DS header carries a 16-bit checksum at ROM offset 0x15E, computed over bytes
0x000..0x15D as `(0x10000 - ((sum + 0x55) & 0xFFFF)) & 0xFFFF` and stored
little-endian. `--check` reports the stored value, the recomputed value and
whether they agree; `fixHeaderChecksum` writes the recomputed value after the
patches are applied.

Usage
-----
    python tools/mod_patch.py --spec docs/modding/example-title.json --check
    python tools/mod_patch.py --spec docs/modding/example-title.json
    python tools/mod_patch.py --spec <spec> --dry-run

Exit codes: 0 success, 1 bad spec or before-byte mismatch, 2 I/O problem.
"""
import argparse
import json
import struct
import sys
from pathlib import Path

HEADER_SIZE = 0x200
CHECKSUM_OFFSET = 0x15E
CHECKSUM_RANGE = 0x15E


def parse_int(value):
    if isinstance(value, int):
        return value
    return int(str(value), 0)


def header_checksum(image):
    """Standard DS header checksum over bytes 0x000..0x15D."""
    total = sum(image[:CHECKSUM_RANGE]) & 0xFFFF
    return (0x10000 - ((total + 0x55) & 0xFFFF)) & 0xFFFF


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
    parser.add_argument('--spec', required=True, help='patch spec JSON')
    parser.add_argument('--root', default='.', help='directory the spec paths are relative to')
    parser.add_argument('--check', action='store_true', help='verify only, write nothing')
    parser.add_argument('--dry-run', action='store_true', help='verify and report, write nothing')
    args = parser.parse_args(argv)

    root = Path(args.root)
    try:
        spec = load_spec(args.spec)
    except (OSError, ValueError) as error:
        print(f'error: {error}', file=sys.stderr)
        return 1

    source = root / spec['input']
    if not source.is_file():
        print(f'error: input image not found: {source}', file=sys.stderr)
        return 2
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

    if args.check:
        print('\n--check: verification passed, nothing written')
        return 0
    if args.dry_run:
        print('\n--dry-run: patches verified, nothing written')
        return 0

    output = root / spec.get('output', str(source.with_suffix('.mod.nds')))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(image)
    print(f'\nwrote {output} ({len(image)} bytes)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
