import re


def order_register_locals(source, name):
    signature = re.search(r"\b" + re.escape(name) + r"\([^\n]*\)\s*\{\n", source)
    if not signature:
        return source
    start = signature.end()
    end = source.find("\n\n", start)
    if end == -1:
        return source
    declarations = source[start:end].splitlines()
    if not declarations or any(not re.fullmatch(r"    [\w\s*]+\b\w+;", line) for line in declarations):
        return source
    def register_number(line):
        match = re.search(r"\b(?:var|temp)_r(\d+)(?:_\d+)?;", line)
        return int(match.group(1)) if match else 99
    ordered = sorted(declarations, key=register_number)
    return source[:start] + "\n".join(ordered) + source[end:]
