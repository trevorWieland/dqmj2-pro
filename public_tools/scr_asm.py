"""Assemble script/command listings produced by public_tools/scr_disasm.py.

The opcode table is parsed at run time from the matched dispatcher
(`src/runtime/parallel_wave20261104/main-command-middle/first/02047428.c`) with
`scr_disasm.parse_table`, so the assembler cannot drift from the source that
proves it.

Listing syntax (exactly what `scr_disasm.py` emits):

    0x00000000  21           walk_0
    0x00000001  e3 1b        .block_end
    0x00000003  e3 1c 05     .escape_skip 0x05
    0x00000006  00           .end
    0x00000007  ff           .byte 0xff   ; unknown opcode

Columns are: address, hex bytes, statement, optional `; comment`.  Statements:

    .end                     0x00
    .block_end               0xe3 0x1b
    .escape_skip <byte>      0xe3 0x1c <byte>
    .escape <byte>           0xe3 <byte>
    .escape_15               0xe3 0x15
    .byte <byte>             <byte>            (undecoded)
    <mnemonic>               the opcode byte that mnemonic maps to

Refusal rule: a listing that contains anything `scr_disasm.py` could not decode
(`.byte`, `.escape`, `.escape_15`) is refused, because emitting those bytes would
invent a semantic the recovered model does not have.  `--allow-undecoded` exists
only to inspect the partial stream; it returns failure as well.

Modes:

    python public_tools/scr_asm.py --root . --opcodes
    python public_tools/scr_asm.py --root . --input listing.txt --output out.bin
    python public_tools/scr_asm.py --root . --roundtrip --input listing.txt \
        --image extract/files/<image> --offset <n> [--scr]

`--roundtrip` assembles the listing and compares the result with the original
image window, printing matched/mismatched byte counts and the first disagreement.
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import scr_disasm

LINE_RE = re.compile(r'^\s*(0x[0-9a-fA-F]+)\s+((?:[0-9a-fA-F]{2}\s+)+)(\S.*)?$')
UNDECODED_COMMENT = 'unknown'
UNDECODED_DIRECTIVES = ('.byte', '.escape', '.escape_15')


def build_mnemonics(table):
    """Return {mnemonic: opcode}; fails loudly if two opcodes share a mnemonic."""
    reverse = {}
    for opcode, (mnemonic, _handler, _arguments) in table.items():
        if mnemonic in reverse:
            raise ValueError('duplicate mnemonic %r for opcodes 0x%02x and 0x%02x'
                             % (mnemonic, reverse[mnemonic], opcode))
        reverse[mnemonic] = opcode
    return reverse


def parse_listing(text):
    """Parse listing lines into dicts: address, bytes, statement, argument, comment."""
    entries = []
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        match = LINE_RE.match(line)
        if match is None:
            entries.append(dict(line=number, error='unparsed line: ' + line))
            continue
        address = int(match.group(1), 16)
        listed = bytes(int(token, 16) for token in match.group(2).split())
        rest = (match.group(3) or '').strip()
        comment = ''
        if ';' in rest:
            rest, comment = rest.split(';', 1)
            rest, comment = rest.strip(), comment.strip()
        parts = rest.split(None, 1)
        statement = parts[0] if parts else ''
        argument = parts[1].strip() if len(parts) > 1 else ''
        entries.append(dict(line=number, address=address, bytes=listed,
                            statement=statement, argument=argument, comment=comment))
    return entries


def encode_entry(entry, mnemonics):
    """Return (encoded bytes, undecoded flag) or raise ValueError."""
    statement = entry['statement']
    argument = entry['argument']
    if statement == '.end':
        return b'\x00', False
    if statement == '.block_end':
        return b'\xe3\x1b', False
    if statement == '.escape_skip':
        return b'\xe3\x1c' + bytes([int(argument, 0) & 0xff]), False
    if statement == '.escape_15':
        return b'\xe3\x15', True
    if statement == '.escape':
        return b'\xe3' + bytes([int(argument, 0) & 0xff]), True
    if statement == '.byte':
        return bytes([int(argument, 0) & 0xff]), True
    if statement in mnemonics:
        return bytes([mnemonics[statement]]), False
    raise ValueError('unknown statement %r' % statement)


def assemble(entries, mnemonics):
    """Assemble entries; return (data, undecoded addresses, errors)."""
    data = bytearray()
    undecoded = []
    errors = []
    expected_address = None
    for entry in entries:
        if 'error' in entry:
            errors.append('line %d: %s' % (entry['line'], entry['error']))
            continue
        if expected_address is not None and entry['address'] != expected_address:
            errors.append('line %d: address 0x%08x is not contiguous (expected 0x%08x)'
                          % (entry['line'], entry['address'], expected_address))
        try:
            encoded, unknown = encode_entry(entry, mnemonics)
        except (ValueError, TypeError) as error:
            errors.append('line %d: %s' % (entry['line'], error))
            continue
        if encoded != entry['bytes']:
            errors.append('line %d: listed bytes %s do not match %s for %r'
                          % (entry['line'], entry['bytes'].hex(), encoded.hex(), entry['statement']))
        if unknown:
            undecoded.append(entry['address'])
        data.extend(encoded)
        expected_address = entry['address'] + len(encoded)
    return bytes(data), undecoded, errors


def opcodes_report(table):
    return scr_disasm.opcodes_report(table)


def load_table(root):
    table = scr_disasm.parse_table(root / scr_disasm.DECODER_SOURCE)
    if table is None:
        raise SystemExit('opcode table unavailable: matched decoder source is missing')
    return table


def main():
    parser = argparse.ArgumentParser(description='Assemble scr_disasm.py listings.')
    parser.add_argument('--root', type=Path, default=Path('.'))
    parser.add_argument('--input', type=Path, help='listing file')
    parser.add_argument('--output', type=Path, help='output byte stream')
    parser.add_argument('--roundtrip', action='store_true',
                        help='assemble --input and compare with --image at --offset')
    parser.add_argument('--image', help='original image for --roundtrip')
    parser.add_argument('--offset', type=lambda text: int(text, 0), default=None)
    parser.add_argument('--length', type=lambda text: int(text, 0), default=None)
    parser.add_argument('--scr', action='store_true',
                        help='use the documented SCR code offset %d' % scr_disasm.SCR_CODE_OFFSET)
    parser.add_argument('--allow-undecoded', action='store_true',
                        help='assemble undecoded statements anyway and fail afterwards')
    parser.add_argument('--opcodes', action='store_true')
    args = parser.parse_args()
    root = args.root.resolve()

    table = load_table(root)
    mnemonics = build_mnemonics(table)
    if args.opcodes:
        print(opcodes_report(table))
        return 0
    if not args.input:
        parser.error('--input is required (or use --opcodes)')
    listing = args.input.read_text(encoding='utf-8')
    entries = parse_listing(listing)
    data, undecoded, errors = assemble(entries, mnemonics)

    if args.output and not errors and (not undecoded or args.allow_undecoded):
        args.output.write_bytes(data)

    if args.roundtrip:
        if not args.image:
            parser.error('--roundtrip requires --image')
        offset = scr_disasm.SCR_CODE_OFFSET if args.scr else (args.offset or 0)
        image_path = root / args.image
        if not image_path.is_file():
            parser.error('image not found: %s' % image_path)
        original = image_path.read_bytes()
        window = original[offset:offset + len(data)]
        matched = sum(1 for left, right in zip(data, window) if left == right)
        mismatched = len(data) - matched
        print('listing: %d statements, %d bytes assembled' % (len(entries), len(data)))
        print('image: %s offset 0x%x, window %d bytes' % (args.image, offset, len(window)))
        print('bytes matched: %d, mismatched: %d' % (matched, mismatched))
        if undecoded:
            print('REFUSED: %d undecoded statement(s); first at 0x%08x'
                  % (len(undecoded), undecoded[0]))
            for address in undecoded[:5]:
                print('  undecoded at 0x%08x' % address)
            return 1
        if errors:
            for error in errors[:10]:
                print('error: ' + error)
            return 1
        if mismatched or len(window) != len(data):
            print('mismatch: assembled %d bytes, window %d bytes' % (len(data), len(window)))
            for index in range(min(len(data), len(window))):
                if data[index] != window[index]:
                    print('first mismatch at 0x%08x: %02x != %02x'
                          % (offset + index, data[index], window[index]))
                    break
            return 1
        print('round-trip exact')
        return 0

    if undecoded and not args.allow_undecoded:
        print('REFUSED: %d undecoded statement(s); first at 0x%08x'
              % (len(undecoded), undecoded[0]))
        print('the listing contains bytes scr_disasm.py could not decode; '
              'the assembler will not invent their meaning')
        return 1
    for error in errors:
        print('error: ' + error)
    if errors:
        return 1
    if args.output:
        print('wrote %d bytes to %s' % (len(data), args.output))
    else:
        print('%d bytes assembled (use --output to write)' % len(data))
    return 0


if __name__ == '__main__':
    sys.exit(main())
