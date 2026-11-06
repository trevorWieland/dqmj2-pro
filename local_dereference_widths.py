import re


def variants(source):
    declarations = list(re.finditer(r'\b(?:u8|s8)\s*\*\s*(\w+)\b', source))
    names = sorted({match[1] for match in declarations})
    protected = {match.start(): match.end() for match in declarations}
    seen = {source}
    for name in names:
        pattern = re.compile(r'(?<![\w*])\*(?=\s*(?:\(\s*)?' + re.escape(name) + r'\b)')
        for scalar in ('u32', 'u16', 's32', 's16'):
            def replacement(match):
                if any(start <= match.start() < end for start, end in protected.items()):
                    return match[0]
                return '*(' + scalar + ' *)'
            changed = pattern.sub(replacement, source)
            if changed not in seen:
                seen.add(changed)
                yield 'local-dereference-width-' + name + '-' + scalar, changed
