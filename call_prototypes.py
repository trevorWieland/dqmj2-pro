import re


def masked(source):
    result = list(source)
    pattern = r'"(?:\\.|[^"\\])*"|\x27(?:\\.|[^\x27\\])*\x27|/\*[\s\S]*?\*/|//[^\n]*'
    for match in re.finditer(pattern, source):
        for index in range(match.start(), match.end()):
            if result[index] != '\n':
                result[index] = ' '
    return ''.join(result)


def recover_call_prototypes(source):
    clean = masked(source)
    pattern = r'extern\s+(u32|s32|void)\s+(native_(?:arm7_fn|fn|utility_child_\w+)_\w+)\(([^;{}]*)\);'
    declarations = list(re.finditer(pattern, clean))
    names = {match[2] for match in declarations}
    counts = {name: set() for name in names}
    for match in re.finditer(r'\b(' + '|'.join(map(re.escape, sorted(names))) + r')\s*\(', clean) if names else []:
        if any(declaration.start() <= match.start() < declaration.end() for declaration in declarations):
            continue
        opening = clean.index('(', match.start())
        depth, braces, cursor, commas = 1, 0, opening + 1, 0
        while cursor < len(clean) and depth:
            char = clean[cursor]
            if char in '([':
                depth += 1
            elif char in ')]':
                depth -= 1
            elif char == '{':
                braces += 1
            elif char == '}':
                braces -= 1
            elif char == ',' and depth == 1 and braces == 0:
                commas += 1
            cursor += 1
        if depth == 0:
            inner = clean[opening + 1:cursor - 1].strip()
            counts[match[1]].add(commas + 1 if inner else 0)
    changes = []
    for declaration in reversed(declarations):
        scalar, name, parameters = declaration.groups()
        old = [value.strip() for value in parameters.split(',')] if parameters.strip() not in ('', 'void') else []
        if any(value not in ('u32', 's32') for value in old) or len(counts[name]) != 1:
            continue
        count = next(iter(counts[name]))
        if count > 16 or count == len(old):
            continue
        replacement = f'extern {scalar} {name}(' + (', '.join(['u32'] * count) if count else 'void') + ');'
        source = source[:declaration.start()] + replacement + source[declaration.end():]
        changes.append({'name': name, 'previousArgumentCount': len(old), 'observedSourceCallArgumentCount': count,
                        'status': 'C call-site arity hypothesis requiring complete native compiler and relocation agreement'})
    return source, list(reversed(changes))
