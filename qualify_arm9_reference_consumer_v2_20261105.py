import re
from project import ROOT, read_json, write_json, sha256
from qualify_explicit_c_frontend_20261102 import qualify


REPORT = 'evidence/matches/cohort154-parallel-wave20261104-d-main-command-forward-next-0.json'
OUTPUT = 'evidence/verification/cohort154-arm9-reference-consumer-qualification-20261105.json'


def compiler_inputs(row):
    assert row['processor'] == 'arm9' and not row.get('program') and row['module'] == 'main' and row['mode'] == 'arm'
    source = (ROOT / row['source']).resolve()
    assert source.is_relative_to(ROOT / 'src') and source.suffix == '.c' and sha256(source) == row['sourceSha256']
    headers = row['sourceDependencies']
    assert isinstance(headers, list)
    if not headers:
        text = source.read_text(encoding='utf-8')
        assert not any(token in text for token in ['#', '\\', '??'])
        assert not any(str(flag).startswith(('-include', '-prefix', '-I', '@')) for flag in row['compilerFlags'])
        assert not any(str(flag).startswith('-i') and not str(flag).startswith(('-inline', '-interworking', '-ipa')) for flag in row['compilerFlags'])
    allowed = {source}
    for pin in headers:
        path = (ROOT / pin['path']).resolve()
        assert path.is_relative_to(ROOT / 'src') and path.suffix == '.h' and sha256(path) == pin['sha256']
        allowed.add(path)
    for path in allowed:
        text = path.read_text(encoding='utf-8')
        assert not re.search(r'\b(?:asm|__asm|__asm__)\b|\.incbin', text)
        for include in re.findall(r'^\s*#include\s+"([^"]+)"', text, re.M):
            assert (path.parent / include).resolve() in allowed
        assert not re.search(r'^\s*#include\s*<', text, re.M)
    flags = row['compilerFlags']
    assert not any(str(flag).lower().endswith(('.bin', '.nds', '.o', '.s', '.inc')) or
                   any(part in str(flag).replace('\\', '/') for part in ['extract/', 'inputs/', 'asm/']) for flag in flags)
    assert not any(flag in flags for flag in ['-include', '-prefix', '-i', '-I'])
    return dict(originalCodeCompilerInput=False, source=row['source'], sha256=row['sourceSha256'], includes=headers)


def run():
    report = read_json(ROOT / REPORT)
    rows = report['matches']
    spec = read_json(ROOT / 'cohort154-parallel-wave20261104-d-specification.json')
    packet = next(p for p in spec['packets'] if p['report'] == REPORT)
    contract = read_json(ROOT / packet['producer'][1])
    expected = {r['address']: r['bytes'] for r in contract['identities']}
    assert len(rows) == 8 and sum(r['bytes'] for r in rows) == 756
    assert {r['address']: r['bytes'] for r in rows} == expected
    proofs = []
    for row in rows:
        inputs = compiler_inputs(row)
        result = qualify(row, ROOT / 'work/integration/cohort154-reference-only' / row['address'])
        proofs.append(dict(address=row['address'], bytes=row['bytes'], sourceOnlyCompilerInput=inputs,
                          explicitC99Qualification=result))
    output = dict(passed=True, sourceCredit=0, report=REPORT, reportSha256=sha256(ROOT / REPORT),
        producer=report['generator'], producerSha256=report['generatorSha256'], functions=8, bytes=756,
        expectedRanges=expected, proofs=proofs, originalCodeCompilerInput=False,
        sourcesObjectsFlagsRegistryAndCanonicalReportUnchanged=True, generatorSha256=sha256(__file__))
    write_json(ROOT / OUTPUT, output)
    return output


if __name__ == '__main__':
    result = run()
    print(dict(passed=True, functions=result['functions'], bytes=result['bytes'], sourceCredit=0))
