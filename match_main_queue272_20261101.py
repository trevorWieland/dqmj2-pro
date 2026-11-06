import gzip
import json
from pathlib import Path
from project import ROOT, configuration, read_json, write_json, sha256
import match_main_indexed_word32_20261101 as builder
import main_queue272_fixture_20261101 as fixture
from link_runtime_unit import measured_module
from save_link_snapshots import freeze_link

WORK = ROOT / 'work/main-queue272-proof-20261101'


def main():
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    input_path = ROOT / 'evidence/attempts/main-queue272-qualified-20261101.json'
    hypothesis = read_json(input_path)
    assert hypothesis['exact']
    source_input = ROOT / hypothesis['source']
    assert sha256(source_input) == hypothesis['sourceSha256']
    source = ROOT / 'src/runtime/20261101_queue272/native_main_020095e8.c'
    source.parent.mkdir(parents=True, exist_ok=True)
    text = source_input.read_text(encoding='utf-8')
    if source.exists():
        assert source.read_text(encoding='utf-8') == text
    else:
        source.write_text(text, encoding='utf-8')
    builder.WORK = WORK
    row, proof, body = builder.build(source, hypothesis['compilation'], 'correct', True)
    metadata, image, unused = measured_module('main')
    native = image[0x95E8:0x95E8 + 272]
    assert body == native
    cases, own, helpers, helper_returns, supplied = [], set(), set(), 0, 0
    for index in range(288):
        original = fixture.execute(image, native, index)
        candidate = fixture.execute(image, body, index)
        assert original == candidate and original['modelPassed'], index
        own.update(original['ownedObserved'])
        helpers.update(original['helperObserved'])
        helper_returns += original['actualNativeReturns'] * 2
        supplied += len(original['calls']) * 2
        cases.append(dict(index=index, original=original, candidate=candidate))
    assert own == set(range(fixture.ENTRY, fixture.ENTRY + 264, 4))
    assert helpers == {address for base,length in fixture.HELPERS.items() for address in range(base,base+length,4)}
    controls = []
    for label, before, after in [('wrap', 'if (temp_r1 > 8)', 'if (temp_r1 > 7)'),
        ('count', 's32 *, 0x1C) - 1)', 's32 *, 0x1C) - 2)')]:
        assert text.count(before) == 1
        changed = text.replace(before, after)
        wrong = ROOT / f'nonmatching/integration/20261101-queue272/{label}/source.c'
        wrong.parent.mkdir(parents=True, exist_ok=True)
        if wrong.exists():
            assert wrong.read_text(encoding='utf-8') == changed
        else:
            wrong.write_text(changed, encoding='utf-8')
        bad_row, bad_proof, bad_body = builder.build(wrong, hypothesis['compilation'], 'wrong-' + label, False)
        wrong_cases = [fixture.execute(image, bad_body, index) for index in range(144)]
        rejected = sum(not item['modelPassed'] for item in wrong_cases)
        assert rejected > 0 and all(item['actualReturn'] for item in wrong_cases)
        controls.append(dict(label=label, source=wrong.relative_to(ROOT).as_posix(), sourceSha256=sha256(wrong),
            compilation=bad_row, genuineLinkComparison=bad_proof, actualWrongReturns=144,
            independentModelRejections=rejected, unchangedPositives=144 - rejected, cases=wrong_cases))
    try:
        fixture.execute(image, native, 0, bound=1)
    except AssertionError:
        pass
    else:
        raise AssertionError('Instruction-bound prefix admitted as return')
    trace = ROOT / 'evidence/traces/main-queue272-20261101.json.gz'
    trace.parent.mkdir(parents=True, exist_ok=True)
    trace.write_bytes(gzip.compress(json.dumps(dict(cases=cases, controls=controls), sort_keys=True,
        separators=(',', ':')).encode(), mtime=0))
    row.update(genuineLinkComparison=freeze_link(proof), exactBytes=272,
        sourceOnlyCompilerInput=True, originalObjectScaffolding=False)
    report = dict(schemaVersion=1, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        romSha256=config['romSha256'], processor='arm9', program='', module='main', moduleSha256=metadata['sha256'],
        matches=[row], matchedFunctions=1, matchedBytes=272,
        oracle=dict(pairs=288, actualTopReturns=576, actualReturnRequired=True,
            actualNativeHelperReturnsSeparate=helper_returns, suppliedCallsSeparate=supplied,
            instructionBytesObserved=264, generatedPoolBytes=8, originalIrqAndBusyWaitHelpersRetained=True,
            fullRegistersFlagsDataStackAndOrderedWritesCompared=True),
        negativeEvidence=dict(actualWrongReturns=288, independentModelRejections=sum(item['independentModelRejections'] for item in controls),
            unchangedPositives=sum(item['unchangedPositives'] for item in controls),
            controls=[{key:value for key,value in item.items() if key != 'cases'} for item in controls],
            instructionBoundPrefixCredit=0),
        replayDependencies=[dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)) for path in
            [input_path, trace, Path(fixture.__file__), Path(builder.__file__)]],
        reproductionCommand='python match_main_queue272_20261101.py',
        limitations=['The9DBC service return is an explicitly supplied opaque word with a deterministic sequence',
            'The blocking path uses one to three synthetic same-word polls before release; no scheduler or concurrency claim',
            'Slots0..8 and bounded0..3-link acyclic synthetic lists are supported; malformed pointers, cycles and invalid counters are unsupported',
            'Original IRQ disable/restore and100-cycle busy-wait routines actually execute and return; they add no source credit',
            'No literal-only or helper source credit, whole module, source-only ROM or full-game execution proof'])
    write_json(ROOT / 'evidence/matches/main-queue272-20261101.json', report)
    print(dict(functions=1, bytes=272, actualTopReturns=576, actualNativeHelperReturns=helper_returns,
        suppliedCalls=supplied, wrongReturns=288,
        wrongRejections=report['negativeEvidence']['independentModelRejections'], acceptancePending=True))


if __name__ == '__main__':
    main()
