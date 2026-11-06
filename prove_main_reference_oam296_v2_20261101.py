import gzip
import json
from pathlib import Path
import match_runtime as compiler
import main_reference_oam296_fixture_20261101 as fixture
from project import ROOT, read_json, write_json, sha256, configuration
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings

WORK = ROOT / 'work/main-reference-oam296-proof-20261101'


def build(source, label, exact):
    profile = read_json(ROOT / 'evidence/attempts/main-full-reference-oam-parse-only-probe-20261101.json')
    flags = list(profile['extraFlags'])
    for index, value in enumerate(flags):
        if index and flags[index-1] == '-i':
            parts = value.replace(chr(92), '/').split('/dqmj2pro-decomp/', 1)
            assert len(parts) == 2
            flags[index] = parts[1]
    original_flags = compiler.FLAGS
    try:
        compiler.FLAGS = [*original_flags, *flags]
        compiler.WORK = WORK / label / 'compile'
        rows, unused = compiler.compare(source, 'main', '4,p', 'on,noauto', compiler=ROOT / 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe')
    finally:
        compiler.FLAGS = original_flags
    assert len(rows) == 1 and not rows[0].get('compileFailed')
    row = rows[0]
    directory = WORK / label / 'link'
    try:
        proof = validate(row, qualified_bindings(row), directory)
        assert exact
    except ValueError as error:
        assert not exact and isinstance(error.args[0], dict)
        proof = error.args[0]
    return row, proof, (directory / 'caller.bin').read_bytes()


def main():
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    acquisition = ROOT / 'evidence/tools/public-sdk-reference-acquisition-20261101.json'
    dependencies = []
    for reference in read_json(acquisition)['references']:
        for record in reference['unmodifiedFiles']:
            assert sha256(ROOT / record['path']) == record['sha256']
            dependencies.append(record)
    source = ROOT / 'generated/recovery/20261101-full-reference-oam-signed-word/native_main_0203716c.c'
    body_source = source.with_name('g2d_OAM.reference.c')
    row, proof, body = build(source, 'correct', True)
    metadata, image, unused = measured_module('main')
    native = image[0x3716C:0x3716C + 296]
    assert native == body
    cases, own, helpers = [], set(), set()
    for index in range(240):
        original = fixture.execute(image, native, index)
        candidate = fixture.execute(image, body, index)
        assert original == candidate and original['modelPassed'], index
        own.update(original['ownedObserved'])
        helpers.update(original['helperObserved'])
        cases.append(dict(index=index, original=original, candidate=candidate))
    assert own == set(range(fixture.ENTRY, fixture.ENTRY + 288, 4))
    assert helpers == {address for base,length in fixture.NATIVE.items() for address in range(base,base+length,4)}
    bad_folder = ROOT / 'generated/recovery/20261101-reference-oam296-negative'
    bad_folder.mkdir(parents=True, exist_ok=True)
    before = '#define OAM_SETTING_INVISIBLE   192'
    text = body_source.read_text(encoding='utf-8')
    assert text.count(before) == 1
    wrong_body = bad_folder / body_source.name
    wrong_body.write_text(text.replace(before, '#define OAM_SETTING_INVISIBLE   193'), encoding='utf-8')
    wrong = bad_folder / source.name
    wrong.write_text(source.read_text(encoding='utf-8'), encoding='utf-8')
    bad_row, bad_proof, bad = build(wrong, 'wrong-fill', False)
    controls = [fixture.execute(image, bad, index) for index in range(120)]
    rejected = sum(not item['modelPassed'] for item in controls)
    assert rejected and all(item['actualReturn'] for item in controls)
    try:
        fixture.execute(image, native, 0, bound=1)
    except AssertionError:
        pass
    else:
        raise AssertionError('Prefix admitted as return')
    trace = ROOT / 'evidence/traces/main-reference-oam296-functional-v2-20261101.json.gz'
    trace.parent.mkdir(parents=True, exist_ok=True)
    trace.write_bytes(gzip.compress(json.dumps(dict(cases=cases, controls=controls), sort_keys=True, separators=(',', ':')).encode(), mtime=0))
    report = dict(sourceCredit=0, exactInitializedHypothesisBytes=296, instructionBytesObserved=288,
        generatedPoolBytes=8, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        romSha256=config['romSha256'], moduleSha256=metadata['sha256'], compilation=row, genuineLinkComparison=proof,
        actualOwnReturns=480, actualNativeHelperReturns=sum(item['original']['actualNativeReturns']*2 for item in cases),
        explicitlySuppliedDmaCalls=sum(item['original']['providedCalls']*2 for item in cases),
        actualWrongReturns=120, independentModelRejections=rejected, unchangedPositiveControls=120-rejected,
        wrongCompilation=bad_row, wrongGenuineLinkComparison=bad_proof,
        trace=trace.relative_to(ROOT).as_posix(), traceSha256=sha256(trace),
        referenceFilesVerified=len(dependencies), sourceFiles=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p))
            for p in [source, body_source, wrong, wrong_body, Path(fixture.__file__), acquisition]],
        limitations=['Isolated exact source/native hypothesis, not accepted source or whole module credit',
            'The full source/type closure still uses explicit parse-only non-varargs declaration headers and needs admission review',
            'Banks0..2/from-to0..127/bounded range states only; malformed or aliased objects unsupported',
            'Original cache-invalidation instructions and CPU-fill execute; no actual cache/device coherence or concurrency proof',
            'DMA is an explicit supplied memory-effect boundary; no rendering/OAM-device/scene claim',
            'Raw signed-word argument and assignment-value unsigned return preserve the existing caller view; historical SDK API is void'])
    write_json(ROOT / 'evidence/attempts/main-reference-oam296-functional-v2-20261101.json', report)
    print({key:report[key]for key in ['sourceCredit','exactInitializedHypothesisBytes','actualOwnReturns','actualNativeHelperReturns','explicitlySuppliedDmaCalls','actualWrongReturns','independentModelRejections']})


if __name__ == '__main__':
    main()
