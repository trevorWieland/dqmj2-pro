import argparse
import json
from pathlib import Path
import struct


def validate(data):
    if len(data) < 64 or data[:7] != b'\x7fELF\x02\x01\x01':
        raise ValueError('Expected a complete little-endian ELF64 library')
    header = struct.unpack_from('<16sHHIQQQIHHHHHH', data)
    if header[1] != 3 or header[2] != 183 or header[3] != 1:
        raise ValueError('Expected an AArch64 shared library')
    phoff, shoff, phsize, phcount = header[5], header[6], header[9], header[10]
    shsize, shcount = header[11], header[12]
    if phsize != 56 or shsize != 64 or not phcount or not shcount:
        raise ValueError('Unexpected ELF header table shape')
    if phoff + phsize * phcount > len(data) or shoff + shsize * shcount > len(data):
        raise ValueError('Truncated ELF header tables')
    loads = []
    for index in range(phcount):
        segment = struct.unpack_from('<IIQQQQQQ', data, phoff + index * phsize)
        if segment[0] == 1:
            offset, address, file_size, memory_size, alignment = segment[2], segment[3], segment[5], segment[6], segment[7]
            if alignment < 16384 or alignment & (alignment - 1) or offset % alignment != address % alignment:
                raise ValueError('LOAD segment lacks valid 16 KiB alignment')
            if file_size > memory_size or offset + file_size > len(data):
                raise ValueError('LOAD segment exceeds the library')
            loads.append(dict(offset=offset, address=address, alignment=alignment))
    sections = [struct.unpack_from('<IIQQQQIIQQ', data, shoff + index * shsize) for index in range(shcount)]
    needed = []
    for section in sections:
        if section[1] != 6:
            continue
        if section[6] >= shcount or section[9] != 16 or section[5] % 16:
            raise ValueError('Unexpected ELF dynamic table')
        strings = sections[section[6]]
        if strings[4] + strings[5] > len(data) or section[4] + section[5] > len(data):
            raise ValueError('Truncated ELF dynamic data')
        table = data[strings[4]:strings[4] + strings[5]]
        for offset in range(section[4], section[4] + section[5], 16):
            tag, value = struct.unpack_from('<qQ', data, offset)
            if tag == 1:
                end = table.find(b'\0', value)
                if value >= len(table) or end < 0:
                    raise ValueError('Invalid dynamic library name')
                needed.append(table[value:end].decode('ascii'))
    if not loads or not needed or set(needed) - {'libc.so', 'libm.so', 'libdl.so'}:
        raise ValueError('Unexpected storage-library runtime dependencies')
    return dict(architecture='aarch64', loadSegments=loads, neededLibraries=needed, alignmentPassed=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('library', type=Path)
    args = parser.parse_args()
    print(json.dumps(validate(args.library.read_bytes())))


if __name__ == '__main__':
    main()
