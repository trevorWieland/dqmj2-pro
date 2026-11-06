import re
from call_prototypes import masked


def closing(text, start, left, right):
    depth = 0
    for index in range(start, len(text)):
        depth += (text[index] == left) - (text[index] == right)
        if depth == 0:
            return index
    return None


def inverted(condition):
    return '!(' + condition + ')'


def variants(source):
    clean = masked(source)
    candidates = []
    for match in re.finditer(r'\bif\s*\(', clean):
        opening = clean.index('(', match.start())
        end_condition = closing(clean, opening, '(', ')')
        if end_condition is None:
            continue
        then = re.match(r'\s*\{', clean[end_condition + 1:])
        if then is None:
            continue
        first = end_condition + 1 + then.end() - 1
        end_first = closing(clean, first, '{', '}')
        if end_first is None:
            continue
        otherwise = re.match(r'\s*else\s*\{', clean[end_first + 1:])
        if otherwise is None:
            continue
        second = end_first + 1 + otherwise.end() - 1
        end_second = closing(clean, second, '{', '}')
        if end_second is None:
            continue
        changed = source[match.start():opening + 1] + inverted(source[opening + 1:end_condition]) + source[end_condition:first + 1]
        changed += source[second + 1:end_second] + source[end_first:second + 1] + source[first + 1:end_first] + '}'
        candidates.append((match.start(), end_second + 1, changed))
    for start, end, changed in candidates:
        yield 'invert-if-else-' + str(start), source[:start] + changed + source[end:]
    selected = []
    for candidate in candidates:
        if not selected or selected[-1][1] <= candidate[0]:
            selected.append(candidate)
    if len(selected) > 1:
        changed = source
        for start, end, replacement in reversed(selected):
            changed = changed[:start] + replacement + changed[end:]
        yield 'invert-independent-if-else-arms', changed
