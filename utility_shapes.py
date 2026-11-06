import re
from decompiler_shapes import order_register_locals


def reverse_register_locals(source, name):
    ordered = order_register_locals(source, name)
    signature = re.search(r"\b" + re.escape(name) + r"\([^\n]*\)\s*\{\n", ordered)
    if not signature:
        return source
    start = signature.end()
    end = ordered.find("\n\n", start)
    if end == -1:
        return source
    declarations = ordered[start:end].splitlines()
    if not declarations or any(not re.fullmatch(r"    [\w\s*]+\b\w+;", line) for line in declarations):
        return source
    def number(line):
        match = re.search(r"\b(?:var|temp)_r(\d+)(?:_\d+)?;", line)
        return int(match.group(1)) if match else -1
    declarations.sort(key=number, reverse=True)
    return ordered[:start] + "\n".join(declarations) + ordered[end:]
