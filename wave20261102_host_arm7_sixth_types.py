import re
from wave20261102_host_arm7_sixth_slice import functions, NONCODE


def units(text):
    mask = NONCODE.sub(lambda m: ' ' * len(m[0]), text)
    definitions = {r['start']: r for r in functions(text)}
    rows, start, at, depth = [], 0, 0, 0
    while at < len(mask):
        if at in definitions:
            row = definitions[at]
            rows.append((row['name'], text[start:row['end']]))
            at = start = row['end']
            continue
        if mask[at] == '{':
            depth += 1
        elif mask[at] == '}':
            depth -= 1
        elif mask[at] == ';' and depth == 0:
            rows.append((None, text[start:at + 1]))
            start = at + 1
        at += 1
    if depth or text[start:].strip():
        raise ValueError('Unclosed ordinary C entity')
    return rows


def bounded(text):
    if len(text.splitlines()) <= 450:
        return text.strip() + '\n'
    result, current = [], ''
    for line in text.splitlines():
        line = line.strip()
        if len(current) + len(line) + 1 > 120:
            result.append(current)
            current = line
        else:
            current += (' ' if current else '') + line
    if current:
        result.append(current)
    if len(result) > 450:
        raise ValueError('One whole C entity exceeds450 physical lines')
    return '\n'.join(result) + '\n'


def write_closed(text, seed, destination):
    destination.parent.mkdir(parents=True, exist_ok=True)
    main, pending, headers = [], [], []
    def flush():
        if not pending:
            return
        header = destination.parent / ('context%03d.h' % len(headers))
        payload = '\n'.join(pending)
        if header.exists() and header.read_text() != payload:
            raise ValueError('Refusing closed typed header overwrite')
        header.write_text(payload)
        main.append('#include "' + header.name + '"\n')
        headers.append(header)
        pending.clear()
    for name, entity in units(text):
        entity = bounded(entity)
        if name == seed:
            flush()
            main.append(entity)
        else:
            if len('\n'.join([*pending, entity]).splitlines()) > 450:
                flush()
            pending.append(entity)
    flush()
    payload = '\n'.join(main)
    if len(payload.splitlines()) > 500:
        raise ValueError('Closed ordinary function exceeds500 physical lines')
    if destination.exists() and destination.read_text() != payload:
        raise ValueError('Refusing closed ordinary source overwrite')
    destination.write_text(payload)
    return headers
