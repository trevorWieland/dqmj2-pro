import re
from project import ROOT, configuration, sha256, write_json


def masked(text):
    return re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', lambda match: ' ' * len(match[0]), text)


def closing(text, start, left, right):
    depth = 0
    for index in range(start, len(text)):
        if text[index] == left:
            depth += 1
        elif text[index] == right:
            depth -= 1
            if not depth:
                return index
    raise ValueError('Unbalanced source syntax')


def arguments(text):
    if not text.strip() or text.strip() == 'void':
        return []
    result, start, depth = [], 0, 0
    for index, char in enumerate(text):
        if char in '([{':
            depth += 1
        elif char in ')]}':
            depth -= 1
        elif char == ',' and not depth:
            result.append(text[start:index].strip())
            start = index + 1
    result.append(text[start:].strip())
    return result


def definition(text, name):
    for match in re.finditer(r'\b' + re.escape(name) + r'\s*\(', text):
        first = text.index('(', match.start())
        last = closing(text, first, '(', ')')
        tail = re.match(r'\s*\{', text[last + 1:])
        if tail:
            begin = last + 1 + tail.end() - 1
            end = closing(text, begin, '{', '}')
            return arguments(text[first + 1:last]), begin, end
    return None


def main():
    from ledger_state import collect_matches
    selected, rejected = collect_matches(configuration()['romSha256'])
    assert not rejected
    host = {key: row for key, row in selected.items()
            if key[0] == 'main' or re.fullmatch(r'ov\d{3}', key[0])}
    sources, definitions = {}, {}
    for key, row in host.items():
        path = ROOT / row['source']
        if path.suffix != '.c':
            continue
        if row['source'] not in sources:
            sources[row['source']] = masked(path.read_text(encoding='utf-8-sig'))
        found = definition(sources[row['source']], row['name'])
        if found:
            definitions[key] = found
    leads, checked, unknown = [], 0, 0
    for key, found in definitions.items():
        row = host[key]
        text = sources[row['source']]
        begin, end = found[1:]
        for match in re.finditer(r'\bnative_fn_([A-Za-z_0-9]+)\s*\(', text[begin:end]):
            suffix = match[1]
            address_match = re.search(r'([0-9a-fA-F]{8})$', suffix)
            if not address_match:
                unknown += 1
                continue
            address = int(address_match[1], 16) & ~1
            module_match = re.match(r'(ov\d{3})_', suffix)
            module = module_match[1] if module_match else 'main' if 0x02000000 <= address < 0x021D7240 else key[0]
            choices = [target for target in definitions if target[0] == module and target[2] == address]
            if len(choices) != 1:
                unknown += 1
                continue
            target = choices[0]
            first = begin + match.end() - 1
            last = closing(text, first, '(', ')')
            supplied = arguments(text[first + 1:last])
            expected = definitions[target][0]
            variadic = bool(expected and expected[-1] == '...')
            required = len(expected) - int(variadic)
            checked += 1
            if len(supplied) != required and not (variadic and len(supplied) >= required):
                leads.append({'callerModule': key[0], 'callerAddress': hex(key[2]), 'callerSource': row['source'],
                              'callerSourceSha256': row['sourceSha256'], 'callerMode': key[1], 'processor': 'arm9',
                              'line': text.count('\n', 0, first) + 1, 'calleeModule': target[0],
                              'calleeAddress': hex(address), 'calleeMode': target[1], 'calleeSource': host[target]['source'],
                              'calleeSourceSha256': host[target]['sourceSha256'],
                              'suppliedArguments': len(supplied), 'selectedDefinitionArguments': required,
                              'sourceCredit': 0, 'status': 'manual native ABI review required'})
    report = {'romSha256': configuration()['romSha256'], 'sourceRegistrySha256': sha256(ROOT / 'recovery.json'),
              'evidenceClass': 'static-call-arity-review', 'reproductionCommand': 'python audit_selected_call_arity_20261030.py',
              'sourceCredit': 0, 'acceptedSourcesChanged': False, 'definitionsParsed': len(definitions),
              'knownDirectCallsChecked': checked, 'unresolvedTargets': unknown, 'arityReviewLeads': len(leads),
              'leads': leads, 'generatorSha256': sha256(ROOT / 'audit_selected_call_arity_20261030.py'),
              'limitations': ['Static review leads only; selected definitions may also need native ABI qualification',
                              'Indirect calls, compiler helpers, macros and non-C definitions are outside this pass',
                              'Main and same-module overlay resolution is conservative; no raw address selects another overlapping overlay',
                              'No accepted source, match credit or source-selection policy is changed']}
    write_json(ROOT / 'evidence/verification/selected-call-arity-review-20261030.json', report)
    print({key: report[key] for key in ['definitionsParsed', 'knownDirectCallsChecked', 'arityReviewLeads', 'sourceCredit']})


if __name__ == '__main__':
    main()
