import re


def canonical_byte_increments(source):
    if "volatile" in source:
        return source, []
    pattern = re.compile(r"(?m)^    (?P<temporary>(?:temp|var)_r\d+(?:_\d+)?) = (?P<lvalue>[^;\n]+) \+ 1;\n"
                         r"    (?P=lvalue) = (?P=temporary);\n"
                         r"    if \((?P<cast>\(u32\) )?(?P=temporary) (?P<condition>(?:>=|<=|==|!=|>|<) (?:0x[0-9A-Fa-f]+|\d+)U?)\) \{")
    changes = []
    def replace(match):
        temporary, lvalue = match["temporary"], match["lvalue"]
        byte_field = re.fullmatch(r"M2C_FIELD\((native_\w+), u8 \*, (?:0x[0-9A-Fa-f]+|\d+)\)", lvalue)
        byte_field = byte_field and "extern u8 " + byte_field[1] + "[];" in source
        byte_global = re.fullmatch(r"\*(native_\w+)", lvalue)
        byte_global = byte_global and re.search(r"extern u8 " + re.escape(byte_global[1]) + r"\[\];", source)
        if not re.search(r"\bu8 " + re.escape(temporary) + r";", source) or len(re.findall(r"\b" + re.escape(temporary) + r"\b", source)) != 4 or not (byte_field or byte_global):
            return match[0]
        changes.append({"temporary": temporary, "lvalue": lvalue, "type": "u8", "condition": match["condition"]})
        return "    ++" + lvalue + ";\n    if (" + (match["cast"] or "") + lvalue + " " + match["condition"] + ") {"
    return pattern.sub(replace, source), changes
