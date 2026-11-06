import argparse
import re
import match_runtime
from project import ROOT, read_json, write_json, sha256


TOKENS = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[A-Za-z_]\w*|[{}();]')
SIGNATURE = re.compile(r'\b(?:unsigned\s+int|signed\s+int|struct\s+\w+|[A-Za-z_]\w*)\s*\**\s+(native_main_([0-9a-f]{8}))\s*\(')


def candidate(text):
    signatures = list(SIGNATURE.finditer(text))
    if len(signatures) != 1:
        return None
    signature = signatures[0]
    prefix = text[signature.start():signature.start(1)].strip()
    if prefix in ['void', 'return', 'extern', 'static', 'if', 'else', 'for', 'while']:
        return None
    tokens = list(TOKENS.finditer(text, signature.end()))
    opening = next((index for index, token in enumerate(tokens) if token.group() in ['{', ';']), None)
    if opening is not None and tokens[opening].group() != '{':
        return None
    if opening is None:
        return None
    depth, ending = 0, None
    for index in range(opening, len(tokens)):
        value = tokens[index].group()
        depth += (value == '{') - (value == '}')
        if depth == 0:
            ending = index
            break
    if ending is None:
        return None
    edits = [(signature.start(), signature.start(1), 'void ')]
    index = opening + 1
    while index < ending:
        token = tokens[index]
        if token.group() != 'return':
            index += 1
            continue
        finish = index + 1
        while finish < ending and tokens[finish].group() != ';':
            finish += 1
        if finish >= ending:
            return None
        expression = text[token.end():tokens[finish].start()].strip()
        if expression:
            edits.append((token.start(), tokens[finish].end(), '{ (void)(' + expression + '); return; }'))
        index = finish + 1
    if len(edits) == 1:
        return None
    for start, stop, replacement in reversed(edits):
        text = text[:start] + replacement + text[stop:]
    return int(signature.group(2), 16), text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lane', type=int, required=True)
    parser.add_argument('--lanes', type=int, default=3)
    options = parser.parse_args()
    assert 0 <= options.lane < options.lanes
    before = read_json(ROOT / 'evidence/verification/cohort95-before-adoption-20261031.json')['selected']
    accepted = {row['key'][2] for row in before if row['key'][0] == 'main'}
    for path in read_json(ROOT / 'evidence/verification/cohort-2026-10-29-95.json')['reports']:
        accepted.update(int(row['address'], 0) for row in read_json(ROOT / path).get('matches', []) if row.get('module') == 'main')
    match_runtime.WORK = ROOT / f'work/main-void-view-sweep-20261031/lane-{options.lane}'
    inputs = []
    seen = set()
    sources = [p for folder in ['src', 'nonmatching/main-runtime'] for p in (ROOT / folder).rglob('*.c')]
    for source in sorted(sources):
        original_hash = sha256(source)
        if original_hash in seen:
            continue
        seen.add(original_hash)
        text = source.read_text(encoding='utf-8-sig')
        result = candidate(text)
        if result is None or len(text.splitlines()) > 500 or '#include' in text:
            continue
        address, draft = result
        if address in accepted or not (0x02000000 <= address < 0x02040000 or 0x020D0000 <= address < 0x02400000):
            continue
        inputs.append((source, original_hash, address, draft))
    rows = []
    output = ROOT / f'evidence/attempts/main-void-view-sweep-20261031-lane-{options.lane}.json'
    for source, original_hash, address, draft in inputs[options.lane::options.lanes]:
        generated = ROOT / 'generated/main-void-views-20261031' / original_hash / source.name
        generated.parent.mkdir(parents=True, exist_ok=True)
        generated.write_text(draft, encoding='utf-8')
        trials = []
        for optimization, speed in [(2, False), (3, True)]:
            try:
                comparisons, exact = match_runtime.compare(generated, 'main', optimization, 'off', speed=speed)
                trials.append(dict(optimization=optimization, speed=speed, comparisons=comparisons, exactCount=len(exact)))
            except Exception as error:
                trials.append(dict(optimization=optimization, speed=speed, error=type(error).__name__ + ': ' + str(error)))
        assert sha256(source) == original_hash
        rows.append(dict(address=hex(address), originalSource=source.relative_to(ROOT).as_posix(), originalSha256=original_hash,
            generatedSource=generated.relative_to(ROOT).as_posix(), generatedSha256=sha256(generated), trials=trials))
        write_json(output, dict(generator=__file__, generatorSha256=sha256(__file__), lane=options.lane,
            totalEligibleInputs=len(inputs), testedSources=len(rows), generatedHypothesesOnly=True, sourceCredit=0, rows=rows,
            limitations=['Void interfaces are hypotheses; source semantics, signatures and connected execution require independent review',
                'No original source or frozen framework file changes; compilation does not accept or register a match']))
        if len(rows) % 25 == 0 or any(trial.get('exactCount') for trial in trials):
            print(dict(lane=options.lane, tested=len(rows), address=hex(address), exact=sum(trial.get('exactCount', 0) for trial in trials)), flush=True)
    print(dict(lane=options.lane, tested=len(rows), eligible=len(inputs), sourceCredit=0), flush=True)


if __name__ == '__main__':
    main()
