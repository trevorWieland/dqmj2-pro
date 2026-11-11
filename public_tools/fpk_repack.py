"""Inspect and repack an FPK archive without the pinned reader.

FPK layout, measured from the extract's archives (``extract/files/*.e`` script archives and
``extract/files/*.m`` model packs):

    header          4 B magic ``FPK\\0``
                    4 B member count (little endian)
    member table    count × 0x28 B:
                      0x00..0x1F  raw name field, NUL padded, preserved verbatim
                      0x20..0x23  member offset, absolute from archive start (u32 LE)
                      0x24..0x27  stored length in bytes (u32 LE)
    data            member bytes, in table order and contiguous in every archive inspected
                    (first offset == 8 + count * 0x28)

A member's stored bytes may themselves be an ``ASH\\0`` container (the script archives are), so
this tool edits **stored** bytes: it does not decompress or recompress. That is deliberate — a
recompressor is not part of the reconstruction, and pretending otherwise would corrupt archives.

Usage:

    python public_tools/fpk_repack.py --list <archive>
    python public_tools/fpk_repack.py --verify <archive>          # round-trip must be identical
    python public_tools/fpk_repack.py --replace <archive> --member 0 --bytes <file> --out <new>
"""

import argparse
import hashlib
import struct
import sys
from pathlib import Path

MAGIC = b'FPK\x00'
ENTRY = 0x28
NAME = 0x20


def parse(data):
    if len(data) < 8 or data[:4] != MAGIC:
        raise ValueError('not an FPK archive (magic is ' + repr(data[:4]) + ')')
    count = struct.unpack_from('<I', data, 4)[0]
    table_end = 8 + count * ENTRY
    if table_end > len(data):
        raise ValueError('member table runs past the end of the archive')
    members = []
    for index in range(count):
        base = 8 + index * ENTRY
        raw = data[base:base + NAME]
        name = raw.split(b'\x00', 1)[0].decode('ascii', 'replace')
        offset, size = struct.unpack_from('<II', data, base + NAME)
        if offset + size > len(data):
            raise ValueError('member %d runs past the end of the archive' % index)
        members.append(dict(index=index, name=name, raw=raw, offset=offset, size=size))
    return count, table_end, members


def rebuild(header, members, payload):
    """Rebuild the archive from preserved name fields, offsets/sizes and member payloads."""
    body = bytearray(header)
    for member in members:
        body += member['raw']
        body += struct.pack('<II', member['offset'], member['size'])
    return bytes(body) + payload


def roundtrip(data):
    """Return the archive rebuilt without changes."""
    count, table_end, members = parse(data)
    payload = data[members[0]['offset']:] if members else data[table_end:]
    return rebuild(data[:8], members, payload)


def contiguity(data, members, table_end):
    """Report whether member payloads tile the data region with no gaps or overlaps."""
    cursor = members[0]['offset'] if members else table_end
    problems = []
    if members and members[0]['offset'] != table_end:
        problems.append('first member starts at 0x%x, table ends at 0x%x'
                        % (members[0]['offset'], table_end))
    for member in members:
        if member['offset'] != cursor:
            problems.append('member %d starts at 0x%x, expected 0x%x'
                            % (member['index'], member['offset'], cursor))
        cursor = member['offset'] + member['size']
    return problems


def digest(data):
    return hashlib.sha256(data).hexdigest()


def describe(members, data):
    lines = []
    for member in members:
        payload = data[member['offset']:member['offset'] + member['size']]
        kind = 'ASH' if payload[:4] == b'ASH\x00' else 'raw'
        lines.append('  %2d  %-24s offset=0x%06x size=%-7d %s'
                     % (member['index'], member['name'], member['offset'], member['size'], kind))
    return '\n'.join(lines)


def replace(archive, data, index, new_bytes):
    """Return a new archive with member `index` replaced by `new_bytes`."""
    count, table_end, members = parse(data)
    if not 0 <= index < count:
        raise SystemExit('member index out of range: %d (archive has %d members)' % (index, count))
    target = members[index]
    old = data[target['offset']:target['offset'] + target['size']]
    if len(new_bytes) == target['size']:
        # Same size: patch in place, keep the table and every other byte untouched.
        patched = data[:target['offset']] + new_bytes + data[target['offset'] + target['size']:]
        return patched, 'in-place'
    # Different size: re-emit the payloads in table order and recompute every offset.
    offsets = []
    payload = bytearray()
    cursor = table_end
    for member in members:
        if member['index'] == index:
            chunk = new_bytes
        else:
            chunk = data[member['offset']:member['offset'] + member['size']]
        offsets.append((cursor, len(chunk)))
        payload += chunk
        cursor += len(chunk)
    rebuilt = []
    for member, (offset, size) in zip(members, offsets):
        copy = dict(member)
        copy['offset'] = offset
        copy['size'] = size
        rebuilt.append(copy)
    return rebuild(data[:8], rebuilt, bytes(payload)), 'rebuilt'


def main():
    parser = argparse.ArgumentParser(description='List, verify or repack an FPK archive.')
    parser.add_argument('--archive', '--list', dest='archive', help='archive to inspect')
    parser.add_argument('--verify', action='store_true', help='rebuild unchanged and compare hashes')
    parser.add_argument('--replace', action='store_true', help='replace one member')
    parser.add_argument('--member', type=int, help='member index for --replace')
    parser.add_argument('--bytes', type=Path, help='file holding the new stored bytes')
    parser.add_argument('--out', type=Path, help='output archive for --replace')
    args = parser.parse_args()
    if not args.archive:
        print('--archive is required', file=sys.stderr)
        return 2
    path = Path(args.archive)
    data = path.read_bytes()
    try:
        count, table_end, members = parse(data)
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 1

    print('%s: %d member(s), %d bytes, sha256 %s' % (path.name, count, len(data), digest(data)))
    print(describe(members, data))
    problems = contiguity(data, members, table_end)
    print('layout: ' + ('contiguous' if not problems else '; '.join(problems)))

    if args.verify:
        rebuilt = roundtrip(data)
        ok = rebuilt == data
        print('round-trip: %s (%d -> %d bytes, sha256 %s)'
              % ('identical' if ok else 'DIFFERENT', len(data), len(rebuilt), digest(rebuilt)))
        return 0 if ok else 1

    if args.replace:
        if args.member is None or args.bytes is None or args.out is None:
            print('--replace needs --member, --bytes and --out', file=sys.stderr)
            return 2
        new_bytes = Path(args.bytes).read_bytes()
        new_archive, mode = replace(path, data, args.member, new_bytes)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_bytes(new_archive)
        print('replace member %d: %s (%d -> %d stored bytes), wrote %s'
              % (args.member, mode, members[args.member]['size'], len(new_bytes), args.out))
        print('  before sha256 %s' % digest(data))
        print('  after  sha256 %s' % digest(new_archive))
        return 0
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
