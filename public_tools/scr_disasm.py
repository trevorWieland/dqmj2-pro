"""Decode a script/command byte stream with the opcode table proven from native code.

The table is not a guess: it is read out of a matched function.  `native_main_02047428`
(`src/runtime/parallel_wave20261104/main-command-middle/first/02047428.c`) reads
`opcode = *input`, advances its consumed-byte counter by two, and dispatches over 47
opcodes to three handler families.  This tool parses those `case` arms at run time, so the
listing cannot drift from the source that proves it.

    python public_tools/scr_disasm.py --root <private-checkout> --image extract/files/ActTbl.bin \
        --offset 0 --length 256
    python public_tools/scr_disasm.py --root <private-checkout> --image <file> --streams --limit 20
    python public_tools/scr_disasm.py --opcodes

Streams are decoded as: one opcode byte per command (the base two-byte consumption is
proven, but which byte is the second half is **not**, so only the opcode byte is consumed),
`0x00` terminates the stream, and the `0xe3` escape family is emitted with its sub-opcode
when it is one of the two proven forms (`0xe3 0x1b` block end, `0xe3 0x1c <byte>`).

Anything else is emitted as `.byte` and counted as undecoded.  Coverage is reported so a
low number is visible instead of hidden: the runtime text block these commands build is
assembled in RAM (`native_data_020fb264`), so a ROM file only ever contains fragments.
"""

import argparse
import re
import sys
from pathlib import Path

DECODER_SOURCE = ('src/runtime/parallel_wave20261104/main-command-middle/first/02047428.c')
HANDLERS = {'native_fn_02047b90': 'text', 'native_fn_02047bfc': 'alt', 'native_fn_02047ac0': 'walk'}
ESCAPE = 0xE3
BLOCK_END = 0x1B
ESCAPE_SKIP = 0x1C
ESCAPE_15 = 0x15
SCR_CODE_OFFSET = 4100
FPK_MAGIC = b'FPK\x00'
TERMINATOR = 0x00


def parse_table(path):
    """Return {opcode: (mnemonic, handler, arguments)} from the matched decoder."""
    text = path.read_text(encoding='utf-8-sig', errors='replace')
    start = text.find('switch (opcode)')
    if start < 0:
        return None
    body = text[start:]
    table = {}
    for match in re.finditer(r'case (0x[0-9a-fA-F]+):\s*\n?\s*(.*?)\n?\s*break;', body, re.S):
        opcode = int(match.group(1), 16)
        statement = ' '.join(match.group(2).split())
        call = re.search(r'(native_fn_02047(?:b90|bfc|ac0))\(([^)]*)\)', statement)
        if call is None:
            table[opcode] = ('cmd_%02x' % opcode, 'nop', '')
            continue
        handler = HANDLERS.get(call.group(1), 'other')
        arguments = ', '.join(part.strip() for part in call.group(2).split(','))
        table[opcode] = ('text_%s' % arguments.replace(', ', '_') if handler == 'text'
                         else 'alt_%s' % arguments.replace(', ', '_') if handler == 'alt'
                         else 'walk_%s' % arguments, handler, arguments)
    return table or None


def opcodes_report(table):
    lines = ['opcode  mnemonic        handler  arguments']
    for opcode in sorted(table):
        mnemonic, handler, arguments = table[opcode]
        lines.append('0x%02x    %-15s %-8s %s' % (opcode, mnemonic, handler, arguments))
    return '\n'.join(lines)


def decode_stream(data, start, table, address_base=0):
    """Decode one command stream from `start`; return (lines, consumed, decoded, unknown)."""
    lines, index, decoded, unknown = [], start, 0, 0
    while index < len(data):
        byte = data[index]
        address = '0x%08x' % (address_base + index)
        if byte == TERMINATOR:
            lines.append('%s  00           .end' % address)
            index += 1
            decoded += 1
            break
        if byte == ESCAPE and index + 1 < len(data):
            sub = data[index + 1]
            if sub == BLOCK_END:
                lines.append('%s  e3 1b        .block_end' % address)
                index += 2
                decoded += 2
                break
            if sub == ESCAPE_SKIP and index + 2 < len(data):
                lines.append('%s  e3 1c %02x     .escape_skip 0x%02x' % (address, data[index + 2], data[index + 2]))
                index += 3
                decoded += 3
                continue
            if sub == ESCAPE_15:
                lines.append('%s  e3 15        .escape_15    ; proven escape, length from native_fn_02046fc8 (unrecovered)' % address)
                index += 2
                unknown += 2
                continue
            lines.append('%s  e3 %02x        .escape 0x%02x   ; unknown escape sub-opcode' % (address, sub, sub))
            index += 2
            unknown += 2
            continue
        if byte in table:
            mnemonic, handler, arguments = table[byte]
            lines.append('%s  %02x           %s%s' % (address, byte, mnemonic,
                                                      ('  ; ' + arguments) if arguments else ''))
            index += 1
            decoded += 1
            continue
        lines.append('%s  %02x           .byte 0x%02x   ; unknown opcode' % (address, byte, byte))
        index += 1
        unknown += 1
    return lines, index - start, decoded, unknown


def find_streams(data, table, minimum=4, limit=20, require_terminator=True):
    """Find runs of known opcodes (optionally 0x00-terminated), longest first."""
    runs, index = [], 0
    while index < len(data):
        if data[index] in table or data[index] == TERMINATOR:
            start = index
            count = 0
            while index < len(data) and data[index] in table:
                count += 1
                index += 1
            ended = index < len(data) and (data[index] == TERMINATOR or
                                           (data[index] == ESCAPE and index + 1 < len(data)
                                            and data[index + 1] == BLOCK_END))
            if count >= minimum and (ended or not require_terminator):
                runs.append((count, start))
            else:
                index = start + 1
        else:
            index += 1
    runs.sort(reverse=True)
    return runs[:limit]


def main():
    parser = argparse.ArgumentParser(description='Decode a command stream with the proven opcode table.')
    parser.add_argument('--root', type=Path, default=Path('.'),
                        help='checkout containing the matched decoder source and the image')
    parser.add_argument('--image', help='image path relative to --root')
    parser.add_argument('--offset', type=lambda text: int(text, 0), default=0)
    parser.add_argument('--length', type=lambda text: int(text, 0), default=256)
    parser.add_argument('--streams', action='store_true', help='list the longest terminator-ended known-opcode runs')
    parser.add_argument('--scan', action='store_true', help='list the longest known-opcode runs (terminator not required)')
    parser.add_argument('--limit', type=int, default=8, help='streams to list in --streams/--scan mode')
    parser.add_argument('--min', type=int, default=4, help='minimum run length (default 4)')
    parser.add_argument('--opcodes', action='store_true', help='print the proven opcode table')
    parser.add_argument('--scr', action='store_true',
                        help='image is a decoded SCR image: start at the documented code offset %d '
                             '(after the 4096-byte entry table)' % 4100)
    args = parser.parse_args()
    root = args.root.resolve()
    table = parse_table(root / DECODER_SOURCE)
    if table is None:
        print('opcode table unavailable: the matched decoder source is missing', file=sys.stderr)
        return 2
    if args.opcodes:
        print(opcodes_report(table))
        return 0
    if not args.image:
        print('--image is required unless --opcodes is used', file=sys.stderr)
        return 2
    image = root / args.image
    if not image.is_file():
        print('image not found: ' + str(image), file=sys.stderr)
        return 2
    data = image.read_bytes()
    if data[:4] == FPK_MAGIC:
        print('%s is an FPK archive, not an SCR script image. Decode its member with the pinned '
              'FPK/ASH reader described in docs/2026-10-29-interpreted-script-inventory.md, then '
              'point --image (or --scr) at the decoded SCR image.' % args.image, file=sys.stderr)
        return 1
    if args.scr:
        args.offset = SCR_CODE_OFFSET
    if args.streams or args.scan:
        runs = find_streams(data, table, minimum=args.min, limit=args.limit, require_terminator=args.streams)
        if not runs:
            print('no run of at least 4 known opcodes followed by a terminator', file=sys.stderr)
            return 1
        print('# %s: %d stream(s), longest %d byte(s)' % (args.image, len(runs), runs[0][0]))
        for count, start in runs:
            print('# stream at 0x%08x, %d command byte(s)' % (start, count))
            lines, consumed, decoded, unknown = decode_stream(data, start, table)
            print('\n'.join(lines))
        return 0
    window = data[args.offset:args.offset + args.length]
    lines, consumed, decoded, unknown = decode_stream(window, 0, table, args.offset)
    print('\n'.join(lines))
    total = consumed or 1
    print('# coverage: %d byte(s) %s, decoded %d (%.1f%%), undecoded %d' %
          (consumed, 'read', decoded, 100.0 * decoded / total, unknown), file=sys.stderr)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
