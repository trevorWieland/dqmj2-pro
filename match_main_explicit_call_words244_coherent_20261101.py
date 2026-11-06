import gzip
import json
from pathlib import Path
from project import ROOT, configuration, read_json, write_json, sha256
import match_main_indexed_word32_20261101 as builder
import main_explicit_call_words244_fixture_20261101 as fixture
from link_runtime_unit import measured_module
from save_link_snapshots import freeze_link

WORK = ROOT / 'work/main-explicit-call-words244-coherent-20261101'
CHANGES = {0x02039F2C: ('var_r6, var_r5, arg3, arg4', '(u8) var_r6, (u8) var_r5, arg3, arg4'),
    0x020193F8: ('        native_fn_02006018(arg0);', '        native_fn_02006018(0U);'),
    0x0203A4FC: ('return native_fn_0203a554(arg0);', 'return native_fn_0203a554(0U);')}


def main():
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    input_path = ROOT / 'evidence/attempts/explicit-call-words-coherent-20261101.json'
    hypotheses = [row for row in read_json(input_path)['results'] if row['label'] != 'typed-pointer-casts']
    assert len(hypotheses) == 3 and all(row['exact'] for row in hypotheses)
    metadata, image, unused = measured_module('main')
    builder.WORK = WORK
    matches, traces, controls = [], [], []
    native_returns = provided = 0
    for hypothesis in hypotheses:
        entry = int(hypothesis['address'], 0)
        source_input = ROOT / hypothesis['source']
        assert sha256(source_input) == hypothesis['sourceSha256']
        source = ROOT / f'src/runtime/20261101_explicit_call_words244_coherent/native_main_{entry:08x}.c'
        source.parent.mkdir(parents=True, exist_ok=True)
        text = source_input.read_text()
        if source.exists():
            assert source.read_text() == text
        else:
            source.write_text(text, encoding='utf-8')
        row, proof, body = builder.build(source, hypothesis['compilation'], f'correct-{entry:08x}', True)
        size = fixture.ENTRIES[entry]
        native = image[entry - 0x02000000:entry - 0x02000000 + size]
        assert body == native and len(body) == size
        cases, own, helpers = [], set(), set()
        for index in range(192):
            original = fixture.execute(image, entry, native, index)
            candidate = fixture.execute(image, entry, body, index)
            assert original == candidate and original['modelPassed'], (hex(entry), index)
            own.update(original['ownedObserved'])
            helpers.update(original['helperObserved'])
            native_returns += original['actualNativeReturns'] * 2
            provided += original['providedCalls'] * 2
            cases.append(dict(index=index, original=original, candidate=candidate))
        assert own == set(range(entry, entry + size, 4))
        before, after = CHANGES[entry]
        assert text.count(before) == (2 if entry == 0x0203A4FC else 1)
        wrong = ROOT / f'nonmatching/integration/20261101-explicit-call-words244-coherent/{entry:08x}/source.c'
        wrong.parent.mkdir(parents=True, exist_ok=True)
        changed = text.replace(before, after)
        if wrong.exists():
            assert wrong.read_text() == changed
        else:
            wrong.write_text(changed, encoding='utf-8')
        bad_row, bad_proof, bad_body = builder.build(wrong, hypothesis['compilation'], f'wrong-{entry:08x}', False)
        wrong_cases = [fixture.execute(image, entry, bad_body, index) for index in range(128)]
        rejected = sum(not case['modelPassed'] for case in wrong_cases)
        assert rejected > 0 and all(case['actualReturn'] for case in wrong_cases)
        controls.append(dict(entry=hex(entry), compilation=bad_row, genuineLinkComparison=bad_proof,
            actualWrongReturns=128, independentRejections=rejected, unchangedPositives=128 - rejected, cases=wrong_cases))
        row.update(genuineLinkComparison=freeze_link(proof), exactBytes=size,
            sourceOnlyCompilerInput=True, originalObjectScaffolding=False)
        matches.append(row)
        traces.append(dict(entry=hex(entry), cases=cases, ownObserved=sorted(own), helperObserved=sorted(helpers)))
    try:
        fixture.execute(image, 0x020193F8, image[0x193F8:0x1941C], 0, bound=1)
    except AssertionError:
        pass
    else:
        raise AssertionError('Prefix admitted as return')
    trace = ROOT / 'evidence/traces/main-explicit-call-words244-coherent-20261101.json.gz'
    trace.parent.mkdir(parents=True, exist_ok=True)
    trace.write_bytes(gzip.compress(json.dumps(traces, sort_keys=True, separators=(',', ':')).encode(), mtime=0))
    report = dict(schemaVersion=1, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        romSha256=config['romSha256'], processor='arm9', program='', module='main', moduleSha256=metadata['sha256'],
        matches=matches, matchedFunctions=3, matchedBytes=244,
        oracle=dict(pairs=576, actualTopReturns=1152, actualNativeHelperReturnsSeparate=native_returns,
            suppliedCallsSeparate=provided, actualReturnRequired=True, instructionBytesObserved=244, generatedPoolBytes=0,
            originalIrqAndConsumerEarlyReturnCodeRetained=True,
            fullCoreFlagsStackGuardDataOsPageAndOrderedCallWordsCompared=True),
        negativeEvidence=dict(controls=controls, actualWrongReturns=384,
            independentRejections=sum(row['independentRejections'] for row in controls),
            unchangedPositives=sum(row['unchangedPositives'] for row in controls), boundedPrefixCredit=0),
        replayDependencies=[dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)) for path in
            [input_path, trace, Path(fixture.__file__), Path(builder.__file__)]],
        reproductionCommand='python match_main_explicit_call_words244_coherent_20261101.py',
        limitations=['Main193F8 uses system mode, synthetic027FFFEC halfword1, first argument unequal1, and IRQ restore flags0/0x80 only',
            'Its original06018/05FF8 wrappers tail into original05F08 mismatch-return code; wrapper observations do not add distinct helper returns',
            'The deeper consumer/IPC path and malformed IRQ control words remain unsupported',
            'The resource getter and two object service calls are explicit supplied boundaries with synthetic effects, not original scene semantics',
            'Selected379C4/3A554 pointer signatures are preserved; unreconstructed38F18/3A28C retain explicit compatible word views with historical formals still unproved',
            'No helper, literal/data, whole module, source-only ROM or full native game credit'])
    write_json(ROOT / 'evidence/matches/main-explicit-call-words244-coherent-20261101.json', report)
    print(dict(newFunctions=3, initializedBytes=244, topReturns=1152, actualNativeHelperReturns=native_returns,
        suppliedCalls=provided, wrongReturns=384, wrongRejections=report['negativeEvidence']['independentRejections'], sourceAcceptancePending=True))


if __name__ == '__main__':
    main()
