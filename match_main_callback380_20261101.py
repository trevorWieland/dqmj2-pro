import gzip
import json
from pathlib import Path
from project import ROOT, configuration, read_json, write_json, sha256
import match_main_indexed_word32_20261101 as builder
import main_callback380_fixture_20261101 as fixture
from link_runtime_unit import measured_module
from save_link_snapshots import freeze_link

WORK = ROOT / 'work/main-callback380-proof-20261101'


def main():
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    input_path = ROOT / 'evidence/attempts/main-callback380-20261101.json'
    hypothesis = next(row for row in read_json(input_path)['results'] if row['label'] == 'read-predicate-first' and not row['speed'])
    assert hypothesis['exact']
    source_input = ROOT / hypothesis['source']
    assert sha256(source_input) == hypothesis['sourceSha256']
    source = ROOT / 'src/runtime/20261101_callback380/native_main_0202fb98.c'
    source.parent.mkdir(parents=True, exist_ok=True)
    text = source_input.read_text(encoding='utf-8')
    if source.exists():
        assert source.read_text(encoding='utf-8') == text
    else:
        source.write_text(text, encoding='utf-8')
    builder.WORK = WORK
    row, proof, body = builder.build(source, hypothesis['compilation'], 'correct', True)
    metadata, image, unused = measured_module('main')
    native = image[0x2FB98:0x2FB98 + 380]
    assert body == native
    cases, own, supplied = [], set(), 0
    for index in range(512):
        original = fixture.execute(image, native, index)
        candidate = fixture.execute(image, body, index)
        assert original == candidate and original['modelPassed'], index
        own.update(original['ownedObserved'])
        supplied += len(original['calls']) * 2
        cases.append(dict(index=index, original=original, candidate=candidate))
    assert own == set(range(fixture.ENTRY, fixture.ENTRY + 380, 4))
    changes = [('advance', 'M2C_FIELD(arg0, void **, 0) + 3;', 'M2C_FIELD(arg0, void **, 0) + 4;'),
        ('skip-mask', 's32 *, 8) & 0x200', 's32 *, 8) & 0x100'),
        ('initial-flag', 's32 *, 8) | 4)', 's32 *, 8) | 8)')]
    controls = []
    for label, before, after in changes:
        assert text.count(before) == 1
        changed = text.replace(before, after)
        wrong = ROOT / f'nonmatching/integration/20261101-callback380/{label}/source.c'
        wrong.parent.mkdir(parents=True, exist_ok=True)
        if wrong.exists():
            assert wrong.read_text(encoding='utf-8') == changed
        else:
            wrong.write_text(changed, encoding='utf-8')
        bad_row, bad_proof, bad_body = builder.build(wrong, hypothesis['compilation'], 'wrong-' + label, False)
        wrong_cases = [fixture.execute(image, bad_body, index) for index in range(128)]
        rejected = sum(not item['modelPassed'] for item in wrong_cases)
        assert rejected > 0 and all(item['actualReturn'] for item in wrong_cases)
        controls.append(dict(label=label, source=wrong.relative_to(ROOT).as_posix(), sourceSha256=sha256(wrong),
            compilation=bad_row, genuineLinkComparison=bad_proof, actualWrongReturns=128,
            independentModelRejections=rejected, unchangedPositives=128 - rejected, cases=wrong_cases))
    try:
        fixture.execute(image, native, 0, bound=1)
    except AssertionError:
        pass
    else:
        raise AssertionError('Instruction-bound prefix admitted as return')
    trace = ROOT / 'evidence/traces/main-callback380-20261101.json.gz'
    trace.parent.mkdir(parents=True, exist_ok=True)
    trace.write_bytes(gzip.compress(json.dumps(dict(cases=cases, controls=controls), sort_keys=True,
        separators=(',', ':')).encode(), mtime=0))
    row.update(genuineLinkComparison=freeze_link(proof), exactBytes=380,
        sourceOnlyCompilerInput=True, originalObjectScaffolding=False)
    report = dict(schemaVersion=1, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        romSha256=config['romSha256'], processor='arm9', program='', module='main', moduleSha256=metadata['sha256'],
        matches=[row], matchedFunctions=1, matchedBytes=380,
        oracle=dict(pairs=512, actualTopReturns=1024, actualReturnRequired=True,
            actualNativeHelperReturnsSeparate=0, suppliedCallsSeparate=supplied,
            instructionBytesObserved=380, generatedPoolBytes=0,
            fullRegistersFlagsDataStackAndOrderedWritesCompared=True),
        negativeEvidence=dict(actualWrongReturns=384, independentModelRejections=sum(item['independentModelRejections'] for item in controls),
            unchangedPositives=sum(item['unchangedPositives'] for item in controls),
            controls=[{key:value for key,value in item.items() if key != 'cases'} for item in controls],
            instructionBoundPrefixCredit=0),
        replayDependencies=[dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)) for path in
            [input_path, trace, Path(fixture.__file__), Path(builder.__file__)]],
        reproductionCommand='python match_main_callback380_20261101.py',
        limitations=['Both indirect callbacks are explicitly supplied synthetic boundaries, with recorded argument words and effects',
            'Synthetic records and callback phase/flag changes do not establish the original scene or callback meanings',
            'Full machine-state equivalence is bounded to the documented contexts; malformed pointers and concurrent mutation are unsupported',
            'No original callee code, historical callback C formals, source-only ROM or full-game execution credit'])
    write_json(ROOT / 'evidence/matches/main-callback380-20261101.json', report)
    print(dict(functions=1, bytes=380, actualTopReturns=1024, suppliedCalls=supplied,
        wrongReturns=384, wrongRejections=report['negativeEvidence']['independentModelRejections'], acceptancePending=True))


if __name__ == '__main__':
    main()
