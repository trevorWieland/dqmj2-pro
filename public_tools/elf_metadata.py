import hashlib
import re
import struct
from pathlib import Path


def inspect(path):
    raw = Path(path).read_bytes()
    if len(raw) < 52 or raw[:7] != b"\x7fELF\x01\x01\x01":
        raise ValueError("Compiler output is not little-endian ELF32")
    header = struct.unpack_from("<16sHHIIIIIHHHHHH", raw)
    unused, kind, machine, version, unused_entry, unused_ph, table, flags, hsize, unused_psize, unused_pcount, ssize, count, names_index = header
    if kind != 1 or machine != 40 or version != 1 or hsize != 52 or ssize != 40 or not 0 < count <= 65535 or names_index >= count:
        raise ValueError("Expected a standard relocatable ARM ELF32 object")
    def chunk(offset, size):
        if offset < 0 or size < 0 or offset + size > len(raw):
            raise ValueError("ELF payload leaves the object")
        return raw[offset:offset + size]
    def string(table_bytes, offset):
        if not 0 <= offset < len(table_bytes):
            raise ValueError("ELF string index leaves its table")
        end = table_bytes.find(b"\0", offset)
        if end < 0:
            raise ValueError("Unterminated ELF string")
        return table_bytes[offset:end].decode("utf-8", errors="replace")
    chunk(table, count * ssize)
    sections = [struct.unpack_from("<IIIIIIIIII", raw, table + index * ssize) for index in range(count)]
    names = sections[names_index]
    if names[1] != 3:
        raise ValueError("ELF section-name table is not a string table")
    section_names = chunk(names[4], names[5])
    allocated = [dict(name=string(section_names, s[0]), type=s[1], flags=s[2], bytes=s[5]) for s in sections if s[2] & 2]
    symbols = []
    for section in sections:
        if section[1] != 2:
            continue
        if section[9] != 16 or section[5] % 16 or section[6] >= count:
            raise ValueError("Unsupported ELF32 symbol-table layout")
        strings = sections[section[6]]
        if strings[1] != 3:
            raise ValueError("Symbol names are not in a string table")
        table_bytes = chunk(strings[4], strings[5])
        body = chunk(section[4], section[5])
        for offset in range(0, len(body), 16):
            name, value, size, info, other, index = struct.unpack_from("<IIIBBH", body, offset)
            symbols.append(dict(name=string(table_bytes, name), value=value, bytes=size, type=info & 15, binding=info >> 4, visibility=other & 3, section=index))
    if not symbols:
        raise ValueError("Compiler object has no symbol table")
    functions = []
    for symbol in symbols:
        index = symbol["section"]
        if symbol["type"] != 2 or not 0 < index < count:
            continue
        section = sections[index]
        start, size = symbol["value"] & ~1, symbol["bytes"]
        if section[1] != 1 or not section[2] & 4 or start + size > section[5]:
            raise ValueError("Function leaves its executable source section")
        mappings = [(s["value"] & ~1, re.fullmatch(r"\$([atd])(?:\..*)?", s["name"])[1]) for s in symbols
                    if s["section"] == index and re.fullmatch(r"\$([atd])(?:\..*)?", s["name"]) and (s["value"] & ~1) <= start]
        mode = {"a": "arm", "t": "thumb", "d": "data"}.get(max(mappings)[1]) if mappings else "unknown"
        code = chunk(section[4] + start, size)
        functions.append(dict(name=symbol["name"], bytes=size, sectionIndex=index, sectionOffset=start, mode=mode,
                              binding=symbol["binding"], visibility=symbol["visibility"], sourceFunctionSha256=hashlib.sha256(code).hexdigest()))
    return dict(format="ELF32-little-ARM-relocatable", flags=flags, functions=functions, allocatedSections=allocated,
                nativeMatchingVerified=False, originalInputsRead=False)
