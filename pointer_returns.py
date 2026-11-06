import re


def memory_result_hints(assembly):
    aliases, hints = {}, set()
    register = r'r(?:1[0-2]|[0-9])'
    for line in assembly.splitlines():
        text = line.strip()
        call = re.fullmatch(r'bl(?:x)?(?:eq|ne|lt|le|gt|ge|hi|ls|hs|lo)?\s+(func_\w+)', text)
        if call:
            aliases = {name: owner for name, owner in aliases.items() if name not in ('r0', 'r1', 'r2', 'r3', 'r12')}
            aliases['r0'] = call[1]
            continue
        if re.match(r'(?:b|bx)\s+', text):
            aliases.clear()
            continue
        base = re.search(r'\[(' + register + r')(?:\s*,\s*#[-\w]+)?\s*\]', text)
        multiple = re.match(r'(?:ldm|stm)\w*\s+(' + register + r')[!,]', text)
        address = base[1] if base else multiple[1] if multiple else None
        if address in aliases:
            hints.add(aliases[address])
        move = re.fullmatch(r'mov\w*\s+(' + register + r'),\s*(' + register + r')', text)
        offset = re.fullmatch(r'(?:add|sub)\w*\s+(' + register + r'),\s*(' + register + r'),\s*#[-\w]+', text)
        transfer = move or offset
        if transfer:
            if transfer[2] in aliases:
                aliases[transfer[1]] = aliases[transfer[2]]
            else:
                aliases.pop(transfer[1], None)
            continue
        if re.match(r'(?:str|stm|cmp|cmn|tst|teq)\w*\s', text):
            continue
        destination = re.match(r'\w+\s+(' + register + r'),', text)
        if destination:
            aliases.pop(destination[1], None)
    return hints
