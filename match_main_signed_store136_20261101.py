import gzip
import json
from pathlib import Path
from project import ROOT, configuration, read_json, write_json, sha256
import match_main_indexed_word32_20261101 as builder
import main_signed_store136_fixture_20261101 as fixture
from link_runtime_unit import measured_module
from save_link_snapshots import freeze_link

WORK = ROOT / 'work/main-signed-store136-20261101'


def main():
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    input_path = ROOT / 'evidence/attempts/main-signed-store136-exploratory-20261101.json'
    hypothesis = read_json(input_path)
    original_source = ROOT / hypothesis['source']
    assert sha256(original_source) == hypothesis['sourceSha256']
    source = ROOT / 'src/runtime/20261101_signed_store136/native_main_02037dc8.c'
    source.parent.mkdir(parents=True, exist_ok=True)
    text = original_source.read_text()
    if source.exists():
        assert source.read_text() == text
    else:
        source.write_text(text, encoding='utf-8')
    builder.WORK = WORK
    row, proof, body = builder.build(source, hypothesis['compilation'], 'correct', True)
    metadata, image, unused = measured_module('main')
    native = image[fixture.ENTRY - 0x02000000:fixture.ENTRY - 0x02000000 + 136]
    assert body == native and len(body) == 136
    cases, observed, helper_observed = [], set(), set()
    helper_returns = provided = 0
    for index in range(512):
        original = fixture.execute(image, native, index)
        candidate = fixture.execute(image, body, index)
        assert original == candidate and original['modelPassed'], index
        observed.update(original['ownedObserved'])
        helper_observed.update(original['helperObserved'])
        helper_returns += original['actualNativeHelperReturns'] * 2
        provided += len(original['calls']) * 2
        cases.append(dict(index=index, original=original, candidate=candidate))
    assert observed == set(range(fixture.ENTRY, fixture.ENTRY + 116, 4))
    controls = []
    for label, before, after in [('wrong-byte', 's8 *, 0) = -1U;', 's8 *, 0) = -2;'),
            ('wrong-state', 's32 *, 4) = 1;', 's32 *, 4) = 2;')]:
        assert text.count(before) == 1
        wrong = ROOT / f'nonmatching/integration/20261101-signed-store136/{label}/source.c'
        wrong.parent.mkdir(parents=True, exist_ok=True)
        changed = text.replace(before, after)
        if wrong.exists():
            assert wrong.read_text() == changed
        else:
            wrong.write_text(changed, encoding='utf-8')
        bad_row, bad_proof, bad_body = builder.build(wrong, hypothesis['compilation'], label, False)
        wrong_cases = [fixture.execute(image, bad_body, index) for index in range(128)]
        rejected = sum(not case['modelPassed'] for case in wrong_cases)
        assert rejected == 64 and all(case['actualReturn'] for case in wrong_cases)
        controls.append(dict(label=label, compilation=bad_row, genuineLinkComparison=bad_proof,
            actualReturns=128, independentRejections=rejected, unchangedPositives=64, cases=wrong_cases))
    try:
        fixture.execute(image, native, 0, bound=1)
    except AssertionError:
        pass
    else:
        raise AssertionError('Incomplete prefix counted as return')
    trace = ROOT / 'evidence/traces/main-signed-store136-20261101.json.gz'
    trace.parent.mkdir(parents=True, exist_ok=True)
    trace.write_bytes(gzip.compress(json.dumps(cases, sort_keys=True, separators=(',', ':')).encode(), mtime=0))
    row.update(genuineLinkComparison=freeze_link(proof), exactBytes=136, sourceOnlyCompilerInput=True, originalObjectScaffolding=False)
    report = dict(schemaVersion=1, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        romSha256=config['romSha256'], processor='arm9', program='', module='main', moduleSha256=metadata['sha256'],
        matches=[row], matchedFunctions=1, matchedBytes=136,
        oracle=dict(pairs=512, actualTopReturns=1024, actualNativeHelperReturnsSeparate=helper_returns,
            suppliedCallsSeparate=provided, instructionBytesObserved=116, generatedPoolBytes=20,
            ownObserved=sorted(observed), helperObserved=sorted(helper_observed), actualReturnRequired=True,
            fullNonstackRamRegistersFlagsStackAndOrderedEffectsCompared=True),
        negativeEvidence=dict(controls=controls, actualWrongReturns=256, independentRejections=128, unchangedPositives=128,
            boundedPrefixCompletionCredit=0),
        replayDependencies=[dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)) for path in
            [input_path, original_source, trace, Path(fixture.__file__), Path(builder.__file__)]],
        reproductionCommand='python match_main_signed_store136_20261101.py',
        limitations=['Compatible signed-byte assignment yields the native low byte; historical field signedness and aggregate type remain unproved',
            'The lower initialization flag is already nonzero; its first-time setup path is not covered',
            'Two registration wrappers and the larger initializer are explicitly supplied boundaries with no modeled external effects',
            'Callbacks are stored but never invoked; queue, thread, hardware, concurrent and complete startup behavior remain unproved',
            'No native helper bytes, whole module, source-only ROM or full native game credit'])
    write_json(ROOT / 'evidence/matches/main-signed-store136-20261101.json', report)
    print(dict(newFunctions=1, initializedBytes=136, actualTopReturns=1024, actualNativeHelperReturns=helper_returns,
        suppliedCalls=provided, wrongReturns=256, wrongRejections=128, sourceAcceptancePending=True))


if __name__ == '__main__':
    main()
