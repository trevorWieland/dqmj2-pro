import re


def indexed_uses(source, name):
    result = []
    for match in re.finditer(r'\b' + re.escape(name) + r'\s*\[', source):
        opening = source.index('[', match.start())
        depth, cursor = 1, opening + 1
        while cursor < len(source) and depth:
            depth += (source[cursor] == '[') - (source[cursor] == ']')
            cursor += 1
        expression = source[opening + 1:cursor - 1].strip()
        if depth == 0 and expression:
            result.append((match.start(), cursor, expression))
    return result


def variants(source):
    declarations = list(re.finditer(r'extern\s+(?:u8|s8)\s+(native_data_\w+)\s*\[\s*\]\s*;', source))
    pointers = list(re.finditer(r'\b(?:u8|s8)\s*\*\s*(\w+)\b', source))
    names = sorted({match[1] for match in declarations + pointers})
    seen = {source}
    for name in names:
        uses = indexed_uses(source, name)
        if not uses:
            continue
        for scalar in ('u16', 'u32', 's16', 's32'):
            changed = source
            for start, end, expression in reversed(uses):
                replacement = f'M2C_FIELD({name}, {scalar} *, ({expression}))'
                changed = changed[:start] + replacement + changed[end:]
            if changed not in seen:
                seen.add(changed)
                yield f'array-byte-offset-width-{name}-{scalar}', changed
            changed = re.sub(r'\b(u8|s8)(\s*\*\s*' + re.escape(name) + r'\b)', scalar + r'\2', source)
            changed = re.sub(r'(extern\s+)(?:u8|s8)(\s+' + re.escape(name) + r'\s*\[\s*\])', r'\1' + scalar + r'\2', changed)
            if changed not in seen:
                seen.add(changed)
                yield f'array-element-width-{name}-{scalar}', changed
