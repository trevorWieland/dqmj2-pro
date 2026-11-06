import re
from call_prototypes import masked


def convert(source, match):
    clean = masked(source)
    start = match.end()
    depth, end = 1, start
    while end < len(clean) and depth:
        depth += (clean[end] == '{') - (clean[end] == '}')
        end += 1
    if depth:
        return None
    body = source[start:end - 1]
    clean_body = clean[start:end - 1]
    indent = match[1]
    labels = []
    depth, previous = 0, 0
    pattern = re.compile(r'^' + re.escape(indent) + r'(?:case\s+(-?(?:0[xX][0-9a-fA-F]+|[0-9]+))[uUlL]*|default):[ \t]*\n', re.M)
    for label in pattern.finditer(clean_body):
        for char in clean_body[previous:label.start()]:
            depth += (char == '{') - (char == '}')
        previous = label.start()
        if depth == 0:
            labels.append(label)
    if not labels or any(label[1] is None for label in labels[:-1]):
        return None
    pieces = []
    for index, label in enumerate(labels):
        content = body[label.end():labels[index + 1].start() if index + 1 < len(labels) else len(body)]
        terminal = re.search(r'\bbreak\s*;\s*$', masked(content))
        if terminal is not None:
            content = content[:terminal.start()].rstrip()
        elif not re.search(r'\b(?:return|goto)\b[^;]*;\s*$', masked(content)):
            return None
        if not content.strip():
            return None
        condition = ('if' if index == 0 else 'else if') + f' ({match[2]} == {label[1]})' if label[1] else 'else'
        pieces.append(indent + condition + ' {\n' + content.rstrip() + '\n' + indent + '}\n')
    return source[:match.start()] + ''.join(pieces) + source[end:]


def variants(source):
    if re.search(r'\bvolatile\b', masked(source)):
        return
    pattern = re.compile(r'(?m)^([ \t]*)switch\s*\(([A-Za-z_]\w*(?:(?:\.|->)[A-Za-z_]\w*)*)\)\s*\{\n')
    current = source
    seen = {source}
    for index in range(8):
        candidates = list(pattern.finditer(masked(current)))
        changed = None
        for match in reversed(candidates):
            changed = convert(current, match)
            if changed is not None and changed not in seen:
                break
        if changed is None or changed in seen:
            return
        seen.add(changed)
        yield f'sequential-state-chain-{index + 1}', changed
        current = changed
