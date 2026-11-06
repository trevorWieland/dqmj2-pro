import re


def recover_single_stack_buffer(source, assembly):
    unknown = re.findall(r"\bM2C_UNK(?:8|16|32|64)?\s+(sp[0-9A-Fa-f]+)\s*;", source)
    if unknown != ["sp0"]:
        return source, []
    frames = re.findall(r"^\s*sub\s+sp,\s*sp,\s*#(0x[0-9a-f]+|[0-9]+)\s*$", assembly, re.M)
    if len(frames) != 1:
        return source, []
    size = int(frames[0], 0)
    if not 4 <= size <= 4096 or size % 4:
        return source, []
    declaration = re.search(r"\bM2C_UNK(?:8|16|32|64)?\s+sp0\s*;", source)
    remainder = source[:declaration.start()] + source[declaration.end():]
    if re.search(r"\bsp[0-9A-Fa-f]+\b", remainder.replace("&sp0", "")) or "&sp0" not in remainder:
        return source, []
    changed = source[:declaration.start()] + f"u8 sp0[{size}];" + source[declaration.end():]
    return changed, [{"local": "sp0", "bytes": size, "evidence": "single static native frame and address-only unknown local", "status": "unverified source type hypothesis until complete compiler/relocation comparison"}]
