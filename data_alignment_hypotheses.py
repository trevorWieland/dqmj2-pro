import re


def variants(source):
    declarations = []
    pattern = re.compile(r'^(extern\s+[^;\n{}()]+?\b((?:native_data_|data_)\w*?([0-9a-f]{8}))(?:\s*\[[^;\n]*\])?\s*);', re.M)
    for match in pattern.finditer(source):
        if ',' in match[1]:
            continue
        address = int(match[3], 16)
        if not address:
            continue
        alignment = min(32, address & -address)
        if alignment < 2:
            continue
        declarations.append((match.start(), match.end(), match[1], match[2], address, alignment))
    for start, end, declaration, name, address, maximum in declarations:
        alignment = 2
        while alignment <= maximum:
            replacement = declaration.rstrip() + f' __attribute__((aligned({alignment})));'
            yield f'fixed-address-alignment-{name}-{alignment}', source[:start] + replacement + source[end:]
            alignment *= 2
    if len(declarations) > 1:
        changed = source
        for start, end, declaration, name, address, alignment in reversed(declarations):
            replacement = declaration.rstrip() + f' __attribute__((aligned({alignment})));'
            changed = changed[:start] + replacement + changed[end:]
        yield 'fixed-address-object-alignments', changed
