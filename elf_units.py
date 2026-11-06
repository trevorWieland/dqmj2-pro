import re
import struct
import hashlib


def thumb_alignment(path, item):
    address = int(item.get("address", item.get("start", "0")), 0)
    if (item.get("mode") or "").lower() != "thumb" or address % 4 != 2:
        return None
    data = bytearray(path.read_bytes())
    table = struct.unpack_from("<I", data, 32)[0]
    previous = struct.unpack_from("<I", data, table + 40 + 32)[0]
    if previous <= 2:
        return None
    if previous != 4:
        raise ValueError("Unexpected Thumb source section alignment")
    struct.pack_into("<I", data, table + 40 + 32, 2)
    path.write_bytes(data)
    return {"originalAlignment": previous, "linkAlignment": 2, "reason": "Source symbol split at measured native halfword entry; instruction/data bytes and relocations unchanged", "stagedObjectSha256": hashlib.sha256(data).hexdigest()}


def split_symbol(elf, name, output, interior=None, relocation_aliases=None, section_padding=0, function_aliases=None, target_section=None):
    symbol_table = elf.get_section_by_name(".symtab")
    symbols = list(symbol_table.iter_symbols())
    raw_symbols = symbol_table.data()
    function_aliases = set(function_aliases or [])
    chosen = next(symbol for symbol in symbols if symbol.name == name)
    section_index = chosen["st_shndx"]
    section = elf.get_section(section_index)
    placed_data = target_section is not None and target_section != section.name
    if placed_data and (not re.fullmatch(r"\.\w+", target_section) or chosen["st_info"]["type"] != "STT_OBJECT" or section["sh_flags"] & 4):
        raise ValueError("Only typed non-executable data can receive a different placement section")
    extent = chosen["st_size"]
    padding = section["sh_size"] - extent
    if chosen["st_value"] & ~1 or padding != section_padding:
        raise ValueError("Source symbol must occupy its complete section")
    if padding and (not 0 < padding < section["sh_addralign"] or section["sh_type"] != "SHT_PROGBITS" or any(section.data()[extent:])):
        raise ValueError("Declared assembler section padding is not alignment-only zero fill")
    relocations = []
    relocation_kind = None
    for item in elf.iter_sections():
        if item["sh_type"] in ("SHT_REL", "SHT_RELA") and item["sh_info"] == section_index:
            if relocation_kind and relocation_kind != item["sh_type"]:
                raise ValueError("Mixed implicit/explicit-addend relocation sections")
            relocation_kind = item["sh_type"]
            relocations.extend(item.iter_relocations())
    if any(item["r_offset"] + 4 > extent for item in relocations):
        raise ValueError("Relocation reaches outside the source symbol")
    used = {item["r_info_sym"] for item in relocations}
    used.update(i for i, symbol in enumerate(symbols) if symbol["st_shndx"] == section_index)
    used.discard(0)
    ordered = sorted(used, key=lambda i: symbols[i]["st_info"]["bind"] != "STB_LOCAL")
    indices, symbol_bytes, strings = {0: 0}, bytearray(16), bytearray(b"\0")
    bind = {"STB_LOCAL": 0, "STB_GLOBAL": 1, "STB_WEAK": 2}
    types = {"STT_NOTYPE": 0, "STT_OBJECT": 1, "STT_FUNC": 2, "STT_SECTION": 3, "STT_FILE": 4}
    first_global = 1 + int(placed_data) + sum(symbols[i]["st_info"]["bind"] == "STB_LOCAL" for i in ordered)
    existing = set()
    if placed_data:
        strings.extend(b"$d\0")
        symbol_bytes.extend(struct.pack("<IIIBBH", 1, 0, 0, 0, 0, 1))
        existing.add("$d")
    aliases = {alias: int(offset, 0) if isinstance(offset, str) else offset for alias, offset in (interior or {}).items()}
    for alias, offset in aliases.items():
        if not re.fullmatch(r"[A-Za-z_]\w*", alias) or not 0 <= offset < extent:
            raise ValueError("Invalid interior source symbol")
    for index in ordered:
        symbol = symbols[index]
        defined = symbol["st_shndx"] == section_index
        injected = symbol.name in aliases and not defined
        if not defined and symbol["st_info"]["bind"] == "STB_LOCAL":
            raise ValueError("Source depends on a local symbol outside its section")
        indices[index] = len(symbol_bytes) // 16
        name_offset = len(strings)
        strings.extend(symbol.name.encode() + b"\0")
        existing.add(symbol.name)
        symbol_bytes.extend(struct.pack("<IIIBBH", name_offset, aliases[symbol.name] if injected else symbol["st_value"] if defined else 0,
            symbol["st_size"] if defined else 0,
            (0x12 if symbol.name in function_aliases else 0x11) if injected else raw_symbols[index * 16 + 12],
            raw_symbols[index * 16 + 13], 1 if defined or injected else 0))
    for alias, offset in aliases.items():
        if alias in existing:
            continue
        at = len(strings)
        strings.extend(alias.encode() + b"\0")
        symbol_bytes.extend(struct.pack("<IIIBBH", at, offset, 0, 0x12 if alias in function_aliases else 0x11, 0, 1))
    relocation_symbols = {}
    for offset, alias in (relocation_aliases or {}).items():
        offset = int(offset)
        if not re.fullmatch(r"[A-Za-z_]\w*", alias) or not 0 <= offset < len(section.data()):
            raise ValueError("Invalid external relocation alias")
        if not any(item["r_offset"] == offset and item["r_info_type"] in (1, 2, 10, 15, 28, 29) for item in relocations):
            raise ValueError("Native alias must select a supported address/branch relocation")
        at = len(strings)
        strings.extend(alias.encode() + b"\0")
        relocation_symbols[offset] = len(symbol_bytes) // 16
        symbol_bytes.extend(struct.pack("<IIIBBH", at, 0, 0, 0x10, 0, 0))
    explicit = relocation_kind != "SHT_REL"
    relocation_bytes = bytearray()
    for item in relocations:
        target_index = relocation_symbols.get(item["r_offset"], indices[item["r_info_sym"]])
        relocation_bytes.extend(struct.pack("<II", item["r_offset"], target_index << 8 | item["r_info_type"]))
        if explicit:
            relocation_bytes.extend(struct.pack("<i", item["r_addend"]))
    placed_section = target_section or section.name
    section_names = [placed_section, (".rela" if explicit else ".rel") + placed_section, ".symtab", ".strtab", ".shstrtab"]
    names, offsets = bytearray(b"\0"), []
    for section_name in section_names:
        offsets.append(len(names))
        names.extend(section_name.encode() + b"\0")
    nobits = section["sh_type"] == "SHT_NOBITS"
    data = bytes(extent) if nobits else section.data()[:extent]
    items = [(offsets[0], 8 if nobits else 1, section["sh_flags"], b"" if nobits else data, extent, 0, 0, section["sh_addralign"], section["sh_entsize"]),
             (offsets[1], 4 if explicit else 9, 0, relocation_bytes, len(relocation_bytes), 3, 1, 4, 12 if explicit else 8),
             (offsets[2], 2, 0, symbol_bytes, len(symbol_bytes), 4, first_global, 4, 16),
             (offsets[3], 3, 0, strings, len(strings), 0, 0, 1, 0),
             (offsets[4], 3, 0, names, len(names), 0, 0, 1, 0)]
    result, headers = bytearray(52), [bytes(40)]
    for at, kind, flags, payload, size, link, info, alignment, entry_size in items:
        alignment = max(alignment, 1)
        result.extend(bytes((-len(result)) % alignment))
        offset = len(result)
        result.extend(payload)
        headers.append(struct.pack("<IIIIIIIIII", at, kind, flags, 0, offset, size, link, info, alignment, entry_size))
    result.extend(bytes((-len(result)) % 4))
    section_offset = len(result)
    result.extend(b"".join(headers))
    result[:52] = struct.pack("<16sHHIIIIIHHHHHH", b"\x7fELF\x01\x01\x01" + bytes(9),
                              1, 40, 1, 0, 0, section_offset, elf["e_flags"], 52, 0, 0, 40, 6, 5)
    output.write_bytes(result)
    return data, [item["r_offset"] for item in relocations]
