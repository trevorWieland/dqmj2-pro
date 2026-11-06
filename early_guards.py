import re


def masked(text):
    pattern = r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/'
    return re.sub(pattern, lambda match: ''.join('\n' if char == '\n' else ' ' for char in match[0]), text)


def closing(text, start, first, last):
    if start >= len(text) or text[start] != first:
        return None
    depth = 1
    for index in range(start + 1, len(text)):
        if text[index] == first:
            depth += 1
        elif text[index] == last:
            depth -= 1
            if depth == 0:
                return index
    return None


def next_token(text, start):
    while start < len(text) and text[start].isspace():
        start += 1
    return start


def variant(source, name):
    code = masked(source)
    function = None
    for match in re.finditer(r'\b' + re.escape(name) + r'\s*\(', code):
        opening = code.index('(', match.start())
        ending = closing(code, opening, '(', ')')
        if ending is None:
            continue
        body = next_token(code, ending + 1)
        if body < len(code) and code[body] == '{':
            end = closing(code, body, '{', '}')
            if end is not None:
                function = body, end
                break
    if function is None:
        return None
    body, end = function
    for match in re.finditer(r'\bif\s*\(', code[body + 1:end]):
        start = body + 1 + match.start()
        prefix = code[body + 1:start]
        if prefix.count('{') != prefix.count('}'):
            continue
        opening = code.index('(', start)
        condition_end = closing(code, opening, '(', ')')
        if condition_end is None:
            continue
        block = next_token(code, condition_end + 1)
        if block >= end or code[block] != '{':
            continue
        block_end = closing(code, block, '{', '}')
        if block_end is None:
            continue
        tail = code[block_end + 1:end]
        if not re.fullmatch(r'\s*return\b[^;]*;\s*', tail):
            continue
        contents = code[block + 1:block_end]
        if not re.search(r'\breturn\b[^;]*;\s*$', contents):
            continue
        condition = source[opening + 1:condition_end]
        statement = source[block_end + 1:end].strip()
        rewritten = source[:start] + 'if (!(' + condition + ')) { ' + statement + ' }\n    ' + source[block:block_end + 1] + '\n' + source[end:]
        if len(rewritten.splitlines()) > 500:
            return None
        return rewritten
    return None
