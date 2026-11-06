from project import ROOT, read_json, write_json, sha256
from qualify_explicit_c_frontend_20261102 import qualify
from prepare_source_cohort_v3_20261102 import classify_additions


def main():
    rows = read_json(ROOT / 'evidence/matches/ov000-20261102-helpers885.json')['matches']
    work = ROOT / 'work/explicit-c99-qualification-controls-20261102'
    positives = [qualify(row, work / str(index)) for index, row in enumerate(rows)]
    row = dict(rows[0])
    controls = []
    cases = [
        ('wrong-source-hash', dict(row, sourceSha256='0' * 64)),
        ('wrong-object-hash', dict(row, objectSha256='0' * 64)),
        ('wrong-compiler-hash', dict(row, compilerSha256='0' * 64)),
        ('explicit-cpp-override', dict(row, compilerFlags=[*row['compilerFlags'], '-lang', 'c++'])),
    ]
    for label, candidate in cases:
        try: qualify(candidate, work / label)
        except AssertionError: controls.append(dict(label=label, refused=True))
        else: raise AssertionError(label)
    cpp = work / 'cpp-only.c'
    cpp.write_text('template<class T> T cpp_only(T value) { return value; }\n', encoding='utf-8')
    candidate = dict(row, source=cpp.relative_to(ROOT).as_posix(), sourceSha256=sha256(cpp))
    try: qualify(candidate, work / 'cpp-parser')
    except AssertionError: controls.append(dict(label='cpp-only-input-rejected-by-actual-c99-parser', refused=True))
    else: raise AssertionError('C++ input admitted')
    asm = work / 'ordinary-asm.c'
    asm.write_text('void bad(void) { __asm("nop"); }\n', encoding='utf-8')
    candidate = dict(row, source=asm.relative_to(ROOT).as_posix(), sourceLanguage='C', size=row['bytes'])
    key = ('ov000', 'arm', int(row['address'], 0))
    try: classify_additions({key: candidate}, {key})
    except AssertionError: controls.append(dict(label='ordinary-logic-assembly-still-refused', refused=True))
    else: raise AssertionError('Ordinary assembly admitted')
    write_json(ROOT / 'evidence/verification/explicit-c99-language-qualification-controls-20261102.json',
        dict(passed=True, sourceCredit=0, actualExplicitC99ExactFunctionProbes=len(positives),
            completeFunctionBytesAndRelocationsEqual=True, positives=positives, controls=controls,
            productionSourcesObjectsFlagsAndRegisteredReportsChanged=False))
    print(dict(positiveExplicitC99Probes=len(positives), refusedControls=len(controls), sourceCredit=0))


if __name__ == '__main__':
    main()
