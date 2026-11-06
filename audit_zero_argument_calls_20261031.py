import re
from collections import defaultdict
from project import ROOT, read_json, write_json, sha256

SNAPSHOT = 'evidence/verification/accepted-cohort83-identities-20261031.json'


def signature(text, name):
    match = re.search(r'\b' + re.escape(name) + r'\s*\((.*?)\)\s*\{', text, re.S)
    if match is None:
        return None
    tail = text[match.end():]
    depth = 1
    for token in re.finditer(r'''"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|[{}]''', tail):
        value = token.group()
        if value == '{':
            depth += 1
        elif value == '}':
            depth -= 1
            if depth == 0:
                return match.group(1).strip(), tail[:token.start()]
    return None


def main():
    sample = 'int outer(void) { const char *s = "}"; if (s) { return 0; } return 1; } int next(int x) { return missing(); }'
    parameters, body = signature(sample, 'outer')
    assert parameters == 'void' and 'missing' not in body
    assert signature('int pointer(void (*f)(int, int), int x) { return x; }', 'pointer')[0] == 'void (*f)(int, int), int x'
    assert signature('int missing(void);', 'missing') is None
    snapshot = read_json(ROOT / SNAPSHOT)
    assert snapshot['acceptedCohort'] == 83
    by_address = defaultdict(list)
    declarations, unsupported = {}, []
    texts = {}
    for row in snapshot['functions']:
        path = row['source']
        assert sha256(ROOT / path) == row['sourceSha256']
        if path not in texts:
            texts[path] = (ROOT / path).read_text(encoding='utf-8-sig')
        parsed = signature(texts[path], row['name'])
        if parsed is None:
            unsupported.append(dict(source=path, name=row['name']))
            continue
        declarations[row['source'], row['name']] = parsed
        by_address[row['processor'], row['program'], row['address']].append(row)
    candidates, ambiguous = [], []
    for caller in snapshot['functions']:
        parsed = declarations.get((caller['source'], caller['name']))
        if parsed is None:
            continue
        parameters, body = parsed
        symbols = sorted(set(re.findall(r'\b(native_fn_(?:ov\d{3}_)?[0-9a-f]{8})\s*\(\s*\)', body)))
        for symbol in symbols:
            address = int(symbol[-8:], 16)
            targets = by_address[caller['processor'], caller['program'], address]
            overlay = re.search(r'native_fn_(ov\d{3})_', symbol)
            if overlay:
                targets = [row for row in targets if row['module'] == overlay.group(1)]
            if len(targets) != 1:
                ambiguous.append(dict(caller=caller['name'], symbol=symbol, candidateCount=len(targets)))
                continue
            target = targets[0]
            declaration, callee_body = declarations[target['source'], target['name']]
            if declaration not in ['', 'void']:
                first = declaration.split(',')[0].strip()
                formal = re.search(r'\b([A-Za-z_]\w*)\s*(?:\[[^]]*\]\s*)?$', first) if '(' not in first else None
                formal = formal.group(1) if formal and len(re.findall(r'[A-Za-z_]\w*', first)) > 1 else None
                used = bool(formal and re.search(r'\b' + re.escape(formal) + r'\b', callee_body))
                candidates.append(dict(caller=caller, callerParameters=parameters, symbol=symbol,
                    selectedCallee=target, calleeParameters=declaration, classification='zero-call-arguments-to-selected-parameterized-definition',
                    firstFormalName=formal, firstFormalUsedLexically=used,
                    nativeAbiProvenByThisAudit=False, sourceChanged=False))
    report = dict(schemaVersion=1, acceptedCohort=83, snapshot=SNAPSHOT, snapshotSha256=sha256(ROOT / SNAPSHOT),
        generator='audit_zero_argument_calls_20261031.py', generatorSha256=sha256(__file__), sourceCredit=0,
        lexicalCalibrationControls=3,
        selectedFunctions=len(snapshot['functions']), parsedDeclarations=len(declarations),
        candidateCount=len(candidates), candidates=candidates, ambiguousTargets=ambiguous, unsupported=unsupported,
        limitations=['Lexical selected-source interface audit; no automatic source edits or proof of original prototypes',
            'Zero-argument call expressions are compared only with uniquely resolved selected definitions',
            'Native incoming-register use, call-site reachability and each proposed typed migration need independent qualification',
            'Lexical C declarations are hypotheses; C++ signatures, aliases and macro-generated definitions can be unsupported'])
    write_json(ROOT / 'evidence/verification/zero-argument-calls83-20261031.json', report)
    print(dict(selectedFunctions=report['selectedFunctions'], candidates=len(candidates),
        ambiguous=len(ambiguous), unsupported=len(unsupported), sourceCredit=0))


if __name__ == '__main__':
    main()
