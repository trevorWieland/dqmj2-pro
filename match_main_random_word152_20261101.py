import gzip
import json
from pathlib import Path
from project import ROOT, configuration, read_json, write_json, sha256
import match_main_indexed_word32_20261101 as builder
import main_random_word152_fixture_20261101 as fixture
from link_runtime_unit import measured_module
from save_link_snapshots import freeze_link

WORK = ROOT / 'work/main-random-word152-20261101'


def main():
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    input_path = ROOT / 'evidence/attempts/main-random-word152-trials-20261101.json'
    trial = next(row for row in read_json(input_path)['results'] if row['label'] == 'u16-temp_r0-0')
    assert trial['exact']
    original_source = ROOT / trial['source']
    assert sha256(original_source) == trial['sourceSha256']
    source = ROOT / 'src/runtime/20261101_random_word152/native_main_0203d158.c'
    source.parent.mkdir(parents=True, exist_ok=True)
    text = original_source.read_text()
    if source.exists():
        assert source.read_text() == text
    else:
        source.write_text(text, encoding='utf-8')
    builder.WORK = WORK
    row, proof, body = builder.build(source, trial['compilation'], 'correct', True)
    metadata, image, unused = measured_module('main')
    native = image[fixture.ENTRY - 0x02000000:fixture.ENTRY - 0x02000000 + 152]
    assert body == native and len(body) == 152
    cases, own, helpers = [], set(), set()
    helper_returns = 0
    vectors = fixture.cases()
    for index, case in enumerate(vectors):
        original = fixture.execute(image, native, case, index)
        candidate = fixture.execute(image, body, case, index)
        assert original == candidate and original['modelPassed'], (index, case)
        own.update(original['ownObserved'])
        helpers.update(original['helperObserved'])
        helper_returns += original['actualNativeHelperReturns'] * 2
        cases.append(dict(original=original, candidate=candidate))
    assert own == set(range(fixture.ENTRY, fixture.ENTRY + 144, 4))
    assert sum(case['original']['iterations'] > 1 for case in cases) >= 8
    wrong = ROOT / 'nonmatching/integration/20261101-random-word152/wrong-encoding/source.c'
    wrong.parent.mkdir(parents=True, exist_ok=True)
    assert text.count('0x7B') == 1
    changed = text.replace('0x7B', '0x7C')
    if wrong.exists():
        assert wrong.read_text() == changed
    else:
        wrong.write_text(changed, encoding='utf-8')
    bad_row, bad_proof, bad_body = builder.build(wrong, trial['compilation'], 'wrong-encoding', False)
    wrong_cases = [fixture.execute(image, bad_body, case, index) for index, case in enumerate(vectors[:128])]
    rejected = sum(not case['modelPassed'] for case in wrong_cases)
    assert rejected > 0 and rejected < 128 and all(case['actualReturn'] for case in wrong_cases)
    try:
        fixture.execute(image, native, vectors[0], 0, bound=1)
    except AssertionError:
        pass
    else:
        raise AssertionError('Incomplete prefix accepted as return')
    trace = ROOT / 'evidence/traces/main-random-word152-20261101.json.gz'
    trace.parent.mkdir(parents=True, exist_ok=True)
    trace.write_bytes(gzip.compress(json.dumps(cases, sort_keys=True, separators=(',', ':')).encode(), mtime=0))
    row.update(genuineLinkComparison=freeze_link(proof), exactBytes=152, sourceOnlyCompilerInput=True, originalObjectScaffolding=False)
    report = dict(schemaVersion=1, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        romSha256=config['romSha256'], processor='arm9', program='', module='main', moduleSha256=metadata['sha256'],
        matches=[row], matchedFunctions=1, matchedBytes=152,
        oracle=dict(pairs=512, actualTopReturns=1024, actualNativeHelperReturnsSeparate=helper_returns,
            providers=0, instructionBytesObserved=144, generatedPoolBytes=8, actualReturnRequired=True,
            ownObserved=sorted(own), helperObserved=sorted(helpers), repeatedLoopCases=sum(case['original']['iterations'] > 1 for case in cases),
            independentModel='LCG state/draws, encoded word predicate, finite retry iterations and full ordered nonstack memory effects'),
        negativeEvidence=dict(compilation=bad_row, genuineLinkComparison=bad_proof, actualWrongReturns=128,
            independentRejections=rejected, unchangedPositives=128 - rejected, cases=wrong_cases, boundedPrefixCredit=0),
        replayDependencies=[dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)) for path in
            [input_path, original_source, trace, Path(fixture.__file__), Path(builder.__file__)]],
        reproductionCommand='python match_main_random_word152_20261101.py',
        limitations=['Synthetic seeded state and bounded finite retries; no observation of future in-game RNG state or player control',
            'Only the measured encoded-word structure is named; its scene, persistence and gameplay meaning remain unproved',
            'Original RNG, predicate and division execute; their existing or unreconstructed source bytes add no new coverage here',
            'No malformed state, concurrent RNG mutation, arbitrary nontermination, complete scene or full native game claim'])
    write_json(ROOT / 'evidence/matches/main-random-word152-20261101.json', report)
    print(dict(newFunctions=1, initializedBytes=152, topReturns=1024, nativeHelperReturns=helper_returns,
        providers=0, repeatedLoopCases=report['oracle']['repeatedLoopCases'], wrongRejections=rejected, sourceAcceptancePending=True))


if __name__ == '__main__':
    main()
