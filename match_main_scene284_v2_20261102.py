import gzip
import json
from pathlib import Path
import main_scene284_fixture_v2_20261102 as fixture
import match_main_oam_reference296_closed_20261101 as builder
from project import ROOT, configuration, read_json, write_json, sha256
from link_runtime_unit import measured_module
from save_link_snapshots import freeze_link


SOURCE = ROOT / 'src/runtime/20261102_scene284/native_main_0203db28.c'
WORK = ROOT / 'work/main-scene284-qualification-20261102'


def main():
    builder.WORK = WORK
    row, proof, body = builder.build(SOURCE, 'positive', True)
    metadata, image, _ = measured_module('main')
    native = image[0x3DB28:0x3DC44]
    assert body == native and len(body) == 284
    cases, observed = [], set()
    for index in range(400):
        original = fixture.execute(image, native, index)
        candidate = fixture.execute(image, body, index)
        assert original == candidate and original['modelPassed'], index
        observed.update(original['observedInstructionAddresses'])
        cases.append(dict(index=index, original=original, candidate=candidate))
    assert observed == set(range(fixture.ENTRY, fixture.ENTRY + 276, 4))
    text = SOURCE.read_text(encoding='utf-8')
    mutations = [('final-byte', 'field_a = 0x31;', 'field_a = 0x30;'),
        ('threshold', 'var_r0 = 2;', 'var_r0 = 3;'),
        ('forwarded-byte', 'native_fn_ov000_021df200(native_data_020f6054.field_c);',
            'native_fn_ov000_021df200(native_data_020f6054.field_c + 1);')]
    controls = []
    for label, before, after in mutations:
        assert text.count(before) == 1
        wrong = ROOT / f'nonmatching/integration/20261102-scene284/{label}/source.c'
        wrong.parent.mkdir(parents=True, exist_ok=True)
        changed = text.replace(before, after)
        if wrong.exists(): assert wrong.read_text(encoding='utf-8') == changed
        else: wrong.write_text(changed, encoding='utf-8')
        badrow, badproof, badbody = builder.build(wrong, 'wrong-' + label, False)
        results = [fixture.execute(image, badbody, i) for i in range(160)]
        rejected = sum(not r['modelPassed'] for r in results)
        assert rejected and all(r['actualReturn'] for r in results)
        controls.append(dict(label=label, source=wrong.relative_to(ROOT).as_posix(), sourceSha256=sha256(wrong),
            compilation=badrow, genuineLinkComparison=badproof, actualWrongReturns=160,
            modelRejections=rejected, cases=results))
    try: fixture.execute(image, body, 0, bound=1)
    except AssertionError: pass
    else: raise AssertionError('Prefix counted as return')
    trace = ROOT / 'evidence/traces/main-scene284-20261102.json.gz'
    trace.parent.mkdir(parents=True, exist_ok=True)
    trace.write_bytes(gzip.compress(json.dumps(dict(cases=cases, controls=controls), sort_keys=True,
        separators=(',', ':')).encode(), mtime=0))
    row.update(genuineLinkComparison=freeze_link(proof), exactBytes=284, sourceOnlyCompilerInput=True,
        originalObjectScaffolding=False, sourceLanguage='C')
    report = dict(schemaVersion=1, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        romSha256=configuration()['romSha256'], processor='arm9', program='', module='main',
        moduleSha256=metadata['sha256'], matches=[row], matchedFunctions=1, matchedBytes=284,
        oracle=dict(pairs=400, actualTopReturns=800, instructionBytesObserved=276, generatedPoolBytes=8,
            actualNativeHelperReturns=0, suppliedBoundaryCalls=sum(r['original']['suppliedBoundaryCalls'] * 2 for r in cases),
            actualReturnRequired=True, independentOrderedCallArgumentsAndDataModel=True,
            fullRegistersFlagsDataStackAndOrderedWritesCompared=True),
        negativeEvidence=dict(actualWrongReturns=480, independentModelRejections=sum(r['modelRejections'] for r in controls),
            controls=[{k: v for k, v in r.items() if k != 'cases'} for r in controls]),
        replayDependencies=[dict(path=p.relative_to(ROOT).as_posix(), sha256=sha256(p)) for p in [Path(fixture.__file__), trace]],
        selectedF200RawWordMigrationPending=True,
        reproductionCommand='python match_main_scene284_v2_20261102.py',
        limitations=['All lower function calls are explicitly supplied ABI boundaries; no lower native returns or ordinary scene proof',
            'No save, encounter, progression, UI, battle or Android meaning inferred from this call sequence',
            'Selected ov000021DF200 raw-word migration must qualify before shared source acceptance',
            'Original data remains zero-credit scaffolding; shared module/ROM regression acceptance pending'])
    write_json(ROOT / 'evidence/matches/main-scene284-20261102.json', report)
    print(dict(functions=1, bytes=284, actualTopReturns=800, wrongReturns=480,
        wrongRejections=report['negativeEvidence']['independentModelRejections'], abiMigrationPending=True))


if __name__ == '__main__':
    main()
