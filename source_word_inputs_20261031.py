import re
from collections import defaultdict
from project import ROOT, read_json, write_json, sha256
from audit_zero_argument_calls_20261031 import signature

SNAPSHOT = 'evidence/verification/accepted-cohort83-identities-20261031.json'
OUTPUT = 'evidence/verification/source-word-inputs83-20261031.json'


def split_parameters(text):
    parts, start, depth = [], 0, 0
    for index, value in enumerate(text):
        if value in '([':
            depth += 1
        elif value in ')]':
            depth -= 1
        elif value == ',' and depth == 0:
            parts.append(text[start:index].strip())
            start = index + 1
    parts.append(text[start:].strip())
    return parts


def word_parameter(text):
    if not text or '...' in text or '(' in text or '[' in text:
        return False
    if '*' in text:
        return True
    text = re.sub(r'\b(?:const|volatile|register)\b', '', text).strip()
    return bool(re.fullmatch(r'(?:u8|s8|u16|s16|u32|s32|int|unsigned int|signed int|short|unsigned short|signed short|char|unsigned char|signed char)\s+[A-Za-z_]\w*', text))


def apply_context(context, catalogue, processor='arm9', program=''):
    index = defaultdict(list)
    for row in catalogue['functions']:
        if row['identity']['processor'] == processor and row['identity']['program'] == program:
            index[row['identity']['address']].append(row)
    edits = []
    pattern = r'(?m)^(\s*extern\s+[^;\n]+?\s+)((?:func|native_fn)_(?:(?:ov\d{3})_)?[0-9a-f]{8})\s*\(\s*\)(\s*;)'

    def replace(match):
        symbol = match.group(2)
        address = int(symbol[-8:], 16)
        rows = index[address]
        overlay = re.search(r'_(ov\d{3})_', symbol)
        if overlay:
            rows = [row for row in rows if row['identity']['module'] == overlay.group(1)]
        if len(rows) != 1:
            return match.group()
        row = rows[0]
        words = ', '.join('u32 arg' + str(i) for i in range(row['wordSlots']))
        edits.append(dict(symbol=symbol, identity=row['identity'], source=row['source'],
            sourceSha256=row['sourceSha256'], parameterView=row['parameterView'], opaqueWordSlots=row['wordSlots']))
        return match.group(1) + symbol + '(' + words + ')' + match.group(3)

    return re.sub(pattern, replace, context), edits


def calibrate():
    base = dict(processor='arm9', program='', module='main', mode='arm', address=0x02001000)
    row = dict(identity=base, source='synthetic.c', sourceSha256='0' * 64, parameterView='u32 input', wordSlots=1)
    catalogue = dict(functions=[row])
    text, edits = apply_context('extern u32 func_02001000();\n', catalogue)
    assert text == 'extern u32 func_02001000(u32 arg0);\n' and len(edits) == 1
    for source in ['extern u32 func_02001000(void);\n', 'extern u32 func_02001000(void *p);\n',
        'extern u32 func_02002000();\n']:
        result, edits = apply_context(source, catalogue)
        assert result == source and not edits
    assert not apply_context('extern u32 func_02001000();\n', catalogue, processor='arm7')[1]
    assert not apply_context('extern u32 func_02001000();\n', catalogue, program='utility-child')[1]
    duplicate = dict(row, identity=dict(base, module='ov000'))
    assert not apply_context('extern u32 func_02001000();\n', dict(functions=[row, duplicate]))[1]
    assert not word_parameter('u64 value') and not word_parameter('void (*callback)(int)')
    assert split_parameters('u32 value, void (*callback)(int, int)') == ['u32 value', 'void (*callback)(int, int)']
    return 10


def main():
    controls = calibrate()
    snapshot = read_json(ROOT / SNAPSHOT)
    assert snapshot['acceptedCohort'] == 83
    functions, excluded, texts = [], [], {}
    seen = set()
    for row in snapshot['functions']:
        key = row['processor'], row['program'], row['module'], row['mode'], row['address']
        assert key not in seen
        seen.add(key)
        path = row['source']
        assert sha256(ROOT / path) == row['sourceSha256']
        if path not in texts:
            texts[path] = (ROOT / path).read_text(encoding='utf-8-sig')
        parsed = signature(texts[path], row['name'])
        if parsed is None or parsed[0] in ['', 'void']:
            continue
        parts = split_parameters(parsed[0])
        if len(parts) > 8 or not all(word_parameter(part) for part in parts):
            excluded.append(dict(source=path, name=row['name'], parameters=parsed[0]))
            continue
        functions.append(dict(identity={field: row[field] for field in ['processor', 'program', 'module', 'mode', 'address']},
            buildSha256=snapshot['romSha256'], source=path, sourceSha256=row['sourceSha256'],
            parameterView=parsed[0], wordSlots=len(parts), originalPrototypeProven=False,
            nativeRegisterInputProofAdded=False, sourceCredit=0))
    report = dict(schemaVersion=1, acceptedCohort=83, romSha256=snapshot['romSha256'], snapshot=SNAPSHOT,
        snapshotSha256=sha256(ROOT / SNAPSHOT), functions=functions, excluded=excluded, calibrationControls=controls,
        generator='source_word_inputs_20261031.py', generatorSha256=sha256(__file__), sourceCredit=0,
        limitations=['Selected C parameter views are drafting hypotheses, not proof of original prototypes or all input registers',
            'Only empty generated external prototypes are changed; explicit void/typed declarations are preserved',
            'Pointers and accepted integral formal types become opaque ARM32 word inputs; no pointer layout or semantic type is inferred',
            'Float, double, 64-bit, aggregate, array, function-pointer, variadic and ambiguous address signatures are excluded',
            'Use in new unaccepted draft paths only; every candidate still needs byte/link/native validation and scoped ABI review'])
    write_json(ROOT / OUTPUT, report)
    print(dict(sourceParameterViews=len(functions), excluded=len(excluded), calibrationControls=controls, sourceCredit=0))


if __name__ == '__main__':
    main()
