import re


def recover_global_records(source):
    pattern = re.compile(r"M2C_FIELD\((native_\w+), (u8|s8|u16|s16|u32|s32) \*, (0x[0-9A-Fa-f]+|\d+)\)")
    groups = {}
    for match in pattern.finditer(source):
        groups.setdefault(match[1], []).append(match)
    changes = []
    for name, matches in groups.items():
        declaration = "extern u8 " + name + "[];"
        if declaration not in source or len(re.findall(r"\b" + re.escape(name) + r"\b", source)) != len(matches) + 1:
            continue
        fields = {}
        for match in matches:
            offset, scalar = int(match[3], 0), match[2]
            fields.setdefault(offset, set()).add(scalar)
        if len(fields) > 64 or any(len(types) != 1 for types in fields.values()):
            continue
        cursor, lines, accepted = 0, [], True
        record = "Record_" + name
        for offset, types in sorted(fields.items()):
            scalar = next(iter(types))
            size = int(scalar[1:]) // 8
            if offset < cursor or offset % size or offset > 0x100000:
                accepted = False
                break
            if offset > cursor:
                lines.append(f"    u8 unknown_{cursor:x}[{offset - cursor:#x}];")
            lines.append(f"    {scalar} field_{offset:x};")
            cursor = offset + size
        if not accepted:
            continue
        replacement = "typedef struct {\n" + "\n".join(lines) + "\n} " + record + ";\nextern " + record + " " + name + ";"
        source = source.replace(declaration, replacement)
        for match in matches:
            source = source.replace(match[0], name + f".field_{int(match[3], 0):x}")
        changes.append({"global": name, "fields": [{"offset": offset, "type": next(iter(types))} for offset, types in sorted(fields.items())],
                        "scope": "Only named byte-array globals used exclusively by these nonoverlapping aligned scalar field accesses"})
    return source, changes
