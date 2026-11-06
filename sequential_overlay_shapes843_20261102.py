import re
from call_prototypes import masked


def closing(text, start, opening, ending):
    level = 1
    for index in range(start + 1, len(text)):
        level += (text[index] == opening) - (text[index] == ending)
        if level == 0:
            return index
    raise ValueError('Unbalanced source delimiters')


def arm(content):
    clean = masked(content)
    terminal = re.search(r'\bbreak\s*;\s*$', clean)
    breaks = list(re.finditer(r'\bbreak\b', clean))
    if breaks and (len(breaks) != 1 or terminal is None or breaks[0].start() != terminal.start()):
        raise ValueError('Internal break requires an independent control-flow proof')
    if terminal:
        return content[:terminal.start()].rstrip(), True
    terminal = re.search(r'\b(?:return\b[^;]*|goto\s+[A-Za-z_]\w*)\s*;\s*$', clean)
    return content.rstrip(), terminal is not None


def convert_one(source, match):
    clean = masked(source)
    open_parenthesis = clean.index('(', match.start())
    close_parenthesis = closing(clean, open_parenthesis, '(', ')')
    expression = source[open_parenthesis + 1:close_parenthesis].strip()
    if re.search(r'\+\+|--|(?<![=!<>])=(?!=)|\bvolatile\b', expression):
        raise ValueError('Side-effectful switch selector is unsupported')
    start = close_parenthesis + 1
    while clean[start].isspace():
        start += 1
    if clean[start] != '{':
        raise ValueError('Unbraced switch is unsupported')
    end = closing(clean, start, '{', '}')
    body = source[start + 1:end]
    clean_body = clean[start + 1:end]
    pattern = re.compile(r'(?m)^[ \t]*(?:case\s+(-?(?:0[xX][0-9a-fA-F]+|[0-9]+))[uUlL]*|default)\s*:[ \t]*(?:\n|$)')
    labels = []
    level = previous = 0
    for label in pattern.finditer(clean_body):
        for character in clean_body[previous:label.start()]:
            level += (character == '{') - (character == '}')
        previous = label.start()
        if level == 0:
            labels.append(label)
    if not labels or clean_body[:labels[0].start()].strip():
        raise ValueError('Switch declarations or unknown labels precede the first case')
    defaults = [index for index, label in enumerate(labels) if label[1] is None]
    if len(defaults) > 1:
        raise ValueError('Duplicate default label')
    arms = []
    for index, label in enumerate(labels):
        content = body[label.end():labels[index + 1].start() if index + 1 < len(labels) else len(body)]
        arms.append(arm(content))
    paths = []
    for index in range(len(labels)):
        pieces = []
        for content, terminal in arms[index:]:
            pieces.append(content)
            if terminal:
                break
        paths.append('\n'.join(pieces).rstrip())
    line_start = source.rfind('\n', 0, match.start()) + 1
    indentation = source[line_start:match.start()]
    if indentation.strip():
        raise ValueError('Switch must start on its own source line')
    conditions = [(label[1], paths[index]) for index, label in enumerate(labels) if label[1] is not None]
    result = []
    for index, (value, content) in enumerate(conditions):
        keyword = 'if' if index == 0 else 'else if'
        result.append(indentation + keyword + ' (' + expression + ' == ' + value + ') {\n' + content + '\n' + indentation + '}')
    if defaults:
        result.append(indentation + 'else {\n' + paths[defaults[0]] + '\n' + indentation + '}')
    replacement = '\n'.join(result)
    return source[:line_start] + replacement + source[end + 1:], dict(selector=expression, cases=[label[1] for label in labels], explicitFallthroughExpansion=True)


def convert(source):
    records = []
    while True:
        matches = list(re.finditer(r'\bswitch\s*\(', masked(source)))
        if not matches:
            return source, records
        source, record = convert_one(source, matches[-1])
        records.append(record)
        if len(records) > 12:
            raise ValueError('Bounded switch-count limit exceeded')
