"""ASH container codec - header parser today, token codec still blocked.

The script archives store their members inside an ``ASH\\0`` container. `fpk_repack.py` can rewrite
stored bytes, but putting a *decoded* edit back needs this codec, so its state matters for the
ROMHACK lens.

## What is measured (three archives, identical structure)

```
offset  bytes                          meaning
0x00    41 53 48 00                    magic "ASH\0"
0x04    e8 39 00 00                    decoded size, u32 LE (d145: 14,824; d000: 4,500; d004: 6,852)
0x08    64 00 00 00                    constant 100 in every archive inspected
0x0c    58 02 13 00                    archive-specific u32 (d145 0x00130258, d000 0x00100515,
                                       d004 0x001126d8) - varies with content, so it is a digest
                                       or size pair, not a constant
0x10    0a 53 43 52 00 ff 09 00 ...    identical in all three archives, and the literal bytes
                                       "SCR\0" appear at stored offset 0x11
```

The decoded size matches the inventory exactly: d145's code interval is 10,724 bytes starting at
member offset 4,100, i.e. a 14,824-byte decoded SCR image (`0x39E8`). The decoded layout is
documented in `docs/2026-10-29-interpreted-script-inventory.md`.

The identical 8-byte prefix across three archives with different content proves the codec is
deterministic on identical input prefixes (an LZ/RLE family, not a content-dependent tree): all
three decoded images begin the same way, so their compressed prefixes match byte for byte.

## What is blocked

The token layer. Excluded by brute force against the known 14,824-byte target and the "SCR\\0"
prefix, over stored offsets 16/17/20/21/8/12/100 and every combination of:

* flag-byte bit order (MSB-first and LSB-first) and literal/compressed polarity;
* nibble match tokens (`len<<4|disp_hi` and `disp<<4|len_hi`), byte tokens (`disp8,len8` /
  `len8,disp8`) and 16-bit tokens with a high-bit match flag (two length/displacement splits);
* literal-run control bytes (count offsets 0/1/2) with 1- and 2-byte distances, both endiannesses;
* 3-byte match tokens (length byte + u16 distance).

None produced 14,824 bytes starting with `SCR\\0`; the candidates either overshoot, undershoot or
reference before the start of the output. The remaining plausible family is a Huffman/bit-plane stage
(the constant `0x64` = 100 at offset 8 could be a tree size), which is not implementable from these
bytes alone without a reference decode to validate against.

**Missing evidence:** one known-good decoded member (or the pinned reader's source) to validate a
candidate decoder against. The private inventory's decoded hashes exist in
`evidence/encounter/scripts-inventory-20261029.json`, but the decoded bytes themselves are not in
this tree, and guessing a decoder without a validation oracle is how archives get corrupted.

## Usage

```
python public_tools/ash_codec.py --info extract/files/d145.e        # header of member 0
python public_tools/ash_codec.py --probe extract/files/d145.e       # header + first stream bytes
python public_tools/ash_codec.py --decompress extract/files/d145.e --out decoded.bin   # refuses today
```
"""

import argparse
import struct
import sys
from pathlib import Path

MAGIC = b'ASH\x00'
HEADER = 16


def read_header(member):
    """Return the measured ASH header fields, or raise ValueError."""
    if len(member) < HEADER or member[:4] != MAGIC:
        raise ValueError('not an ASH container (magic is %r)' % (member[:4],))
    decoded_size, constant, archive_word = struct.unpack_from('<III', member, 4)
    return dict(decoded_size=decoded_size, constant=constant, archive_word=archive_word,
                stream_start=HEADER, stream_head=member[HEADER:HEADER + 16].hex())


def decompress(member):
    """Decode an ASH member.

    Deliberately unimplemented: the token layer is not established (see the module docstring).
    Raising is the honest behaviour - a wrong decoder silently corrupts every archive it touches.
    """
    header = read_header(member)
    raise NotImplementedError(
        'ASH token layer not decoded (header: decoded_size=%d, constant=0x%x, word=0x%08x, '
        'stream starts at 0x%x with %s); a known-good decoded member is needed to validate a '
        'candidate decoder' % (header['decoded_size'], header['constant'], header['archive_word'],
                               header['stream_start'], header['stream_head']))


def compress(decoded):
    """Encode bytes into an ASH member. Blocked with decompress()."""
    raise NotImplementedError('ASH encoder blocked on the same unknown token layer as decompress()')


def first_member(archive_bytes):
    """Return (offset, size, bytes) of member 0 of an FPK archive."""
    if archive_bytes[:4] != b'FPK\x00':
        raise ValueError('not an FPK archive')
    offset, size = struct.unpack_from('<II', archive_bytes, 0x28)
    return offset, size, archive_bytes[offset:offset + size]


def main():
    parser = argparse.ArgumentParser(description='Inspect (and eventually decode) ASH members.')
    parser.add_argument('--archive', '--info', '--probe', '--decompress', dest='archive',
                        help='FPK archive whose member 0 is inspected')
    parser.add_argument('--member', type=int, default=0, help='member index (default 0)')
    parser.add_argument('--out', type=Path, help='decode output path')
    args = parser.parse_args()
    if not args.archive:
        print('--archive is required', file=sys.stderr)
        return 2
    data = Path(args.archive).read_bytes()
    offset, size, member = first_member(data)
    print('%s member %d: stored %d bytes at 0x%x' % (args.archive, args.member, size, offset))
    try:
        header = read_header(member)
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 1
    print('  magic "ASH\\0", decoded size %d (0x%x)' % (header['decoded_size'], header['decoded_size']))
    print('  constant 0x%x, archive word 0x%08x' % (header['constant'], header['archive_word']))
    print('  stream starts at 0x%x: %s' % (header['stream_start'], header['stream_head']))
    print('  codec: BLOCKED - token layer not decoded (see public_tools/ash_codec.py docstring)')
    if args.out:
        try:
            decoded = decompress(member)
        except NotImplementedError as error:
            print('decode refused: %s' % error, file=sys.stderr)
            return 1
        args.out.write_bytes(decoded)
        print('wrote %d bytes to %s' % (len(decoded), args.out))
        return 0
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
