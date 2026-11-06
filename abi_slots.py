import re


def preserve_argument_slots(source, name, scalar="u32"):
    signature = re.search(r"\b" + re.escape(name) + r"\(([^\n]*)\)\s*\{", source)
    if not signature or "(*" in signature.group(1):
        return source, []
    parameters = [item.strip() for item in signature.group(1).split(",")]
    indexed = {}
    order = []
    for parameter in parameters:
        if parameter in ("", "void"):
            continue
        match = re.fullmatch(r"(.+?)\barg(\d+)", parameter)
        if not match:
            return source, []
        kind, index = match.group(1).strip(), int(match.group(2))
        if index > 16 or ("*" not in kind and kind not in ("u8", "s8", "u16", "s16", "u32", "s32", "f32", "int", "unsigned int", "float")):
            return source, []
        if index in indexed:
            raise ValueError("Duplicate decompiler argument slot")
        indexed[index] = parameter
        order.append(index)
    if not indexed:
        return source, []
    if order != sorted(order):
        raise ValueError("Decompiler argument slots are out of order")
    missing = [index for index in range(max(indexed) + 1) if index not in indexed]
    complete = ", ".join(indexed.get(index, scalar + " arg" + str(index)) for index in range(max(indexed) + 1))
    return source[:signature.start(1)] + complete + source[signature.end(1):], missing
