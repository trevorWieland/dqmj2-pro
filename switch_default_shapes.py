import re


TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|/\*[\s\S]*?\*/|//[^\n]*|[A-Za-z_]\w*|[^\s]')


def closing(tokens, start, opening, ending):
    depth = 0
    for index in range(start, len(tokens)):
        value = tokens[index][0]
        depth += value == opening
        depth -= value == ending
        if depth == 0:
            return index
    return None


def terminates(tokens):
    values = [token[0] for token in tokens]
    while values and values[0] == '{' and closing(tokens, 0, '{', '}') == len(tokens) - 1:
        tokens = tokens[1:-1]
        values = values[1:-1]
    if not values or values[-1] != ';':
        return False
    braces, parentheses, start = 0, 0, 0
    for index, value in enumerate(values[:-1]):
        braces += value == '{'
        braces -= value == '}'
        parentheses += value == '('
        parentheses -= value == ')'
        if not braces and not parentheses and value in (';', '}'):
            start = index + 1
    return values[start] in ('break', 'return', 'goto')


def variants(source):
    if re.search(r'^\s*#\s*(?:if|elif|else|endif)\b', source, re.M):
        return
    tokens = [(match[0], match.start(), match.end()) for match in TOKEN.finditer(source)
              if not match[0].startswith(('/*', '//'))]
    for index, token in enumerate(tokens):
        if token[0] != 'switch' or index + 1 >= len(tokens) or tokens[index + 1][0] != '(':
            continue
        condition_end = closing(tokens, index + 1, '(', ')')
        if condition_end is None or condition_end + 1 >= len(tokens) or tokens[condition_end + 1][0] != '{':
            continue
        opening = condition_end + 1
        end = closing(tokens, opening, '{', '}')
        if end is None or opening + 3 >= end or [row[0] for row in tokens[opening + 1:opening + 3]] != ['default', ':']:
            continue
        depth, next_case = 1, None
        for cursor in range(opening + 3, end):
            value = tokens[cursor][0]
            if depth == 1 and value == 'case':
                next_case = cursor
                break
            depth += value == '{'
            depth -= value == '}'
        if next_case is None or not terminates(tokens[opening + 3:next_case]):
            continue
        start, boundary, finish = tokens[opening + 1][1], tokens[next_case][1], tokens[end][1]
        moved = source[start:boundary]
        changed = source[:start] + source[boundary:finish] + '\n' + moved + source[finish:]
        yield f'switch-default-last-{token[1]}', changed
