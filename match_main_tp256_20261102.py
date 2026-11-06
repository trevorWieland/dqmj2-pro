import gzip
import json
from pathlib import Path
import main_tp256_fixture_20261102 as fixture
import match_main_oam_reference296_closed_20261101 as builder
from project import ROOT, configuration, write_json, sha256
from link_runtime_unit import measured_module
from save_link_snapshots import freeze_link


SOURCE = ROOT / 'src/runtime/20261102_tp256/native_main_0200ded8.c'


def main():
    builder.WORK = ROOT / 'work/main-tp256-native-proof-20261102'
    row, proof, body = builder.build(SOURCE, 'positive', True)
    metadata, image, _ = measured_module('main')
    native = image[0xDED8:0xDFD8]
    assert len(body) == 256 and body == native
    cases, observed = [], set()
    for index in range(3360):
        original = fixture.execute(image, native, index)
        candidate = fixture.execute(image, body, index)
        assert original == candidate and original['modelPassed'], index
        observed.update(original['observedInstructionAddresses'])
        cases.append(dict(index=index, original=original, candidate=candidate))
    assert observed == set(range(fixture.ENTRY, fixture.ENTRY + 252, 4))
    text = SOURCE.read_text(encoding='utf-8')
    mutations = [('touch-clear', '.samplingBufs[i].touch = 0 ;', '.samplingBufs[i].touch = 1 ;'),
        ('forwarded-frequency', 'TPi_AutoSamplingOn(vcount, (u8)frequence)', 'TPi_AutoSamplingOn(vcount, (u8)(frequence + 1))'),
        ('command-flag', 'command_flg |= TP_REQUEST_COMMAND_FLAG_AUTO_ON;', 'command_flg |= TP_REQUEST_COMMAND_FLAG_AUTO_OFF;')]
    controls = []
    for label, before, after in mutations:
        assert text.count(before) == 1
        wrong = ROOT / f'nonmatching/integration/20261102-tp256/{label}/source.c'
        wrong.parent.mkdir(parents=True, exist_ok=True)
        changed = text.replace(before, after)
        if wrong.exists(): assert wrong.read_text(encoding='utf-8') == changed
        else: wrong.write_text(changed, encoding='utf-8')
        badrow, badproof, badbody = builder.build(wrong, 'wrong-' + label, False)
        results = [fixture.execute(image, badbody, i * 17 % 3360) for i in range(240)]
        rejected = sum(not r['modelPassed'] for r in results)
        assert rejected and all(r['actualReturn'] for r in results)
        controls.append(dict(label=label, source=wrong.relative_to(ROOT).as_posix(), sourceSha256=sha256(wrong),
            compilation=badrow, genuineLinkComparison=badproof, actualWrongReturns=240,
            modelRejections=rejected, cases=results))
    try: fixture.execute(image, body, 0, bound=1)
    except AssertionError: pass
    else: raise AssertionError('Prefix counted as return')
    trace = ROOT / 'evidence/traces/main-tp256-20261102.json.gz'
    trace.parent.mkdir(parents=True, exist_ok=True)
    trace.write_bytes(gzip.compress(json.dumps(dict(cases=cases, controls=controls), sort_keys=True,
        separators=(',', ':')).encode(), mtime=0))
    row.update(genuineLinkComparison=freeze_link(proof), exactBytes=256, sourceOnlyCompilerInput=True,
        originalObjectScaffolding=False, sourceLanguage='C')
    report = dict(schemaVersion=1, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        romSha256=configuration()['romSha256'], processor='arm9', program='', module='main', moduleSha256=metadata['sha256'],
        matches=[row], matchedFunctions=1, matchedBytes=256,
        oracle=dict(pairs=3360, actualTopReturns=6720, instructionBytesObserved=252, generatedPoolBytes=4,
            actualNativeLowerReturns=0, suppliedBoundaryCalls=sum(r['original']['suppliedBoundaryCalls'] * 2 for r in cases),
            actualReturnRequired=True, independentMemoryAndOrderedCallModel=True,
            fullRegistersFlagsDataStackAndOrderedWritesCompared=True),
        negativeEvidence=dict(actualWrongReturns=720, independentModelRejections=sum(r['modelRejections'] for r in controls),
            controls=[{k: v for k, v in r.items() if k != 'cases'} for r in controls]),
        replayDependencies=[dict(path=p.relative_to(ROOT).as_posix(), sha256=sha256(p)) for p in [Path(fixture.__file__), trace]],
        referenceRevision='ccbbcc8b6db4c4dbba3d503d2026978d78977840', measuredStructurePrefixBytes=4,
        reproductionCommand='python match_main_tp256_20261102.py',
        limitations=['Interrupt, PXI and callback calls are explicit supplied ABI boundaries; no hardware/native lower return credit',
            'Bounded buffers0/1/2/7 and valid disjoint pointers; unsupported oversized or malformed pointer contexts remain unproved',
            'Source data structure includes measured four-byte unknown prefix; prefix meaning and original data source unproved',
            'No physical touch panel, concurrency, scene, audio, Android or full native game proof',
            'Caller interface review and shared module/ROM regression acceptance pending'])
    write_json(ROOT / 'evidence/matches/main-tp256-20261102.json', report)
    print(dict(functions=1, bytes=256, actualTopReturns=6720, wrongReturns=720,
        wrongRejections=report['negativeEvidence']['independentModelRejections'], sourceAcceptancePending=True))


if __name__ == '__main__':
    main()
