import hashlib
import re
from slice_reference_sdk_entities_v3_20261102 import functions, declaration_name, NONCODE


def externalize(text):
    records = functions(text)
    spans = {r['start']: r for r in records}
    function_names = {r['name'] for r in records}
    mask = NONCODE.sub(lambda match: ' ' * len(match.group()), text)
    edits, evidence = [], []
    start = at = depth = 0
    while at < len(text):
        if at in spans:
            at = start = spans[at]['end']
            continue
        char = mask[at]
        if char == '{': depth += 1
        elif char == '}': depth -= 1
        elif char == ';' and depth == 0:
            declaration = text[start:at + 1]
            name = declaration_name(declaration)
            if declaration.lstrip().startswith('static ') and name not in function_names:
                replacement = re.sub(r'\bstatic\b', 'extern', declaration, count=1)
                brace = paren = bracket = 0
                initializer = None
                for i, value in enumerate(replacement):
                    if value == '{': brace += 1
                    elif value == '}': brace -= 1
                    elif value == '(': paren += 1
                    elif value == ')': paren -= 1
                    elif value == '[': bracket += 1
                    elif value == ']': bracket -= 1
                    elif value == '=' and not (brace or paren or bracket):
                        initializer = i
                        break
                if initializer is not None: replacement = replacement[:initializer].rstrip() + ';'
                edits.append((start, at + 1, replacement))
                evidence.append(dict(name=name, originalDeclarationSha256=hashlib.sha256(declaration.encode()).hexdigest(),
                    originalInitializerRemoved=initializer is not None, sourceDataCredit=0))
            start = at + 1
        at += 1
    assert depth == 0
    for start, end, replacement in reversed(edits): text = text[:start] + replacement + text[end:]
    return text, evidence
