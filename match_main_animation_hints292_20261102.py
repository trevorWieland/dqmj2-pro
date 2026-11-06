import gzip
import json
from pathlib import Path
from project import ROOT, configuration, write_json, sha256
from link_runtime_unit import measured_module
from save_link_snapshots import freeze_link
import match_main_oam_reference296_closed_20261101 as builder
import main_animation_hints292_fixture_v2_20261102 as fixture

WORK = ROOT / 'work/main-animation-hints292-qualified-20261102'
REPORT = ROOT / 'evidence/matches/main-animation-hints292-20261102.json'


def main():
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    metadata, image, _ = measured_module('main')
    assert metadata['sha256'] == 'ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'
    builder.WORK = WORK
    bodies, sources, rows = {}, {}, []
    for address, length in fixture.OWN.items():
        source = ROOT / f'src/runtime/20261102_animation_hints292/native_main_{address:08x}.c'
        text = source.read_text(encoding='utf-8')
        assert len(text.splitlines()) <= 500 and not any(t in text for t in ['/*', '//', 'asm ', '__asm'])
        row, proof, body = builder.build(source, source.stem, True)
        assert len(body) == length
        row.update(sourceLanguage='C', exactBytes=length, sourceOnlyCompilerInput=True,
            originalObjectScaffolding=False, genuineLinkComparison=freeze_link(proof))
        bodies[address], sources[address] = body, source
        rows.append(row)
    cases, observed = [], set()
    for index in range(3072):
        original, candidate = fixture.execute(image, {}, index), fixture.execute(image, bodies, index)
        assert original == candidate and original['modelPassed'], index
        cases.append(original)
        observed.update(original['ownObserved'])
    mutations = [
        (0x0202EA64, 'wrong-present-bit', '0x0100', '0x0200'),
        (0x0202FA04, 'wrong-word-bit', 'i & 31', 'i & 15'),
        (0x0202EBC0, 'wrong-obsolete-bit', '0x00000010', '0x00000020'),
    ]
    controls = []
    for address, label, old, new in mutations:
        text = sources[address].read_text(encoding='utf-8')
        assert text.count(old) == 1
        changed = text.replace(old, new)
        path = ROOT / f'nonmatching/integration/20261102-animation-hints292/{label}/source.c'
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists(): assert path.read_text(encoding='utf-8') == changed
        else: path.write_text(changed, encoding='utf-8')
        row, proof, body = builder.build(path, label, False)
        assert len(body) <= fixture.OWN[address]
        bad = {**bodies, address: body}
        indices = [i for i in range(3072) if fixture.inputs(i)[2] == address]
        results = [fixture.execute(image, bad, index) for index in indices]
        rejected = sum(not result['modelPassed'] for result in results)
        assert rejected
        controls.append(dict(label=label, source=path.relative_to(ROOT).as_posix(), sourceSha256=sha256(path),
            actualWrongReturns=len(results), modelRejections=rejected, positiveControls=len(results) - rejected,
            compiledEntry=row, genuineNonmatchingLinkProof=proof))
    try: fixture.execute(image, bodies, 0, bound=1)
    except AssertionError: pass
    else: raise AssertionError('Bounded prefix counted as return')
    trace = ROOT / 'evidence/traces/main-animation-hints292-20261102.json.gz'
    trace.write_bytes(gzip.compress(json.dumps(dict(cases=cases), sort_keys=True, separators=(',', ':')).encode(), mtime=0))
    missing = {hex(a): [hex(pc) for pc in range(a, a + n, 4) if pc not in observed] for a, n in fixture.OWN.items()}
    write_json(REPORT, dict(schemaVersion=1, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        romSha256=config['romSha256'], processor='arm9', program='', module='main', moduleSha256=metadata['sha256'],
        matches=rows, matchedFunctions=3, matchedBytes=292,
        oracle=dict(pairs=3072, actualTopReturns=6144,
            actualNativeHelperReturns=sum(c['actualNativeHelperReturns'] for c in cases) * 2,
            functionProviders=0, ownInstructionBytesObserved=len(observed) * 4, unobservedOriginalAddresses=missing,
            independentBitsetUnionAndListRemovalModel=True,
            fullRegistersFlagsMainDataStackOrderedAccessesAndRawCallsCompared=True),
        negativeControls=controls, reproductionCommand='python match_main_animation_hints292_20261102.py',
        replayDependencies=[dict(path=p.relative_to(ROOT).as_posix(), sha256=sha256(p)) for p in [Path(fixture.__file__), trace]],
        limitations=[
            'Acyclic distinct lists of0/1/2/4/7 nodes and mapping counts through255; incoming vector words include0,all1 and random values',
            'Unsigned1U removes the original signed1<<31 undefined-shift domain without changing any matching bytes',
            'Removal models three disjoint categories, head/interior/tail/absent/null and opaque unmatched needle words; cyclic or aliased category lists unsupported',
            'Previously accepted116-byte original removal helper executes without additional source credit',
            'No renderer, real asset/scene reachability, source-only ROM or complete native game claim']))
    print(dict(functions=3, bytes=292, actualReturns=6144,
        actualNativeHelperReturns=sum(c['actualNativeHelperReturns'] for c in cases) * 2,
        wrongReturns=sum(c['actualWrongReturns'] for c in controls),
        wrongRejected=sum(c['modelRejections'] for c in controls), missing=missing))


if __name__ == '__main__':
    main()
