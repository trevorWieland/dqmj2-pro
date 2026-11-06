import re
import struct


def write_unit(generated, target, name, target_name, flags, output):
    if len(generated) != 12 or struct.unpack_from("<I", generated, 8)[0] != target:
        raise ValueError("Generated linker region lacks its declared actual target pointer")
    if any(not re.fullmatch(r"[A-Za-z_]\w*", value) for value in (name, target_name)):
        raise ValueError("Linkage symbols must be qualified identifiers")
    strings = bytearray(b"\0")
    symbols = bytearray(16)
    for symbol, value, size, info, section in [("$t", 0, 0, 2, 1), ("$a", 4, 0, 2, 1), ("$d", 8, 0, 1, 1),
                                               (name, 0, 12, 0x12, 1), (target_name, 0, 0, 0x10, 0)]:
        offset = len(strings)
        strings.extend(symbol.encode() + b"\0")
        symbols.extend(struct.pack("<IIIBBH", offset, value, size, info, 0, section))
    code = generated[:8] + bytes(4)
    relocation = struct.pack("<IIi", 8, 5 << 8 | 2, 0)
    names, offsets = bytearray(b"\0"), []
    for text in [".text", ".rela.text", ".symtab", ".strtab", ".shstrtab"]:
        offsets.append(len(names))
        names.extend(text.encode() + b"\0")
    items = [(offsets[0], 1, 6, code, 0, 0, 4, 0),
             (offsets[1], 4, 0, relocation, 3, 1, 4, 12),
             (offsets[2], 2, 0, symbols, 4, 4, 4, 16),
             (offsets[3], 3, 0, strings, 0, 0, 1, 0),
             (offsets[4], 3, 0, names, 0, 0, 1, 0)]
    result, headers = bytearray(52), [bytes(40)]
    for name_offset, kind, attributes, payload, link, info, alignment, entry_size in items:
        result.extend(bytes((-len(result)) % alignment))
        offset = len(result)
        result.extend(payload)
        headers.append(struct.pack("<IIIIIIIIII", name_offset, kind, attributes, 0, offset, len(payload), link, info, alignment, entry_size))
    result.extend(bytes((-len(result)) % 4))
    section_offset = len(result)
    result.extend(b"".join(headers))
    result[:52] = struct.pack("<16sHHIIIIIHHHHHH", b"\x7fELF\x01\x01\x01" + bytes(9), 1, 40, 1, 0, 0, section_offset, flags, 52, 0, 0, 40, 6, 5)
    output.write_bytes(result)
