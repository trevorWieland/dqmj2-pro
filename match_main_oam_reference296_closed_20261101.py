import gzip
import json
from pathlib import Path
import match_runtime as compiler
import main_reference_oam296_fixture_v2_20261101 as fixture
from project import ROOT, configuration, read_json, write_json, sha256
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link

WORK = ROOT / 'work/main-oam-reference296-closed-20261101'
SOURCE = ROOT / 'src/runtime/20261101_reference_oam296/native_main_0203716c.c'


def build(source, label, exact):
    before = compiler.FLAGS
    try:
        compiler.FLAGS = [*before, '-lang', 'c99', '-ipa', 'file']
        compiler.WORK = WORK / label / 'compile'
        rows, unused = compiler.compare(source, 'main', '4,p', 'on,noauto',
            compiler=ROOT / 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe')
    finally:
        compiler.FLAGS = before
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
    text = SOURCE.read_text(encoding='utf-8')
    assert len(text.splitlines()) <= 500 and '#include' not in text and '/*' not in text and '//' not in text
    assert all(word not in text for word in ['va_list','J2pUnknown','size_t','asm '])
    caller = ROOT / 'src/runtime/runtime05/native_main_020489c4.c'
    caller_text = caller.read_text(encoding='utf-8')
    assert 's32 temp_r4;' in caller_text and 'return native_fn_0203716c(temp_r4 + 0x520);' in caller_text
    row, proof, body = build(SOURCE, 'correct', True)
    metadata, image, unused = measured_module('main')
    native = image[0x3716C:0x3716C + 296]
    assert body == native
    cases, own, helpers = [], set(), set()
    for index in range(600):
        original = fixture.execute(image, native, index)
        candidate = fixture.execute(image, body, index)
        assert original == candidate and original['modelPassed'], index
        own.update(original['ownedObserved']); helpers.update(original['helperObserved'])
        cases.append(dict(index=index, original=original, candidate=candidate))
    assert own == set(range(fixture.ENTRY, fixture.ENTRY+288, 4))
    assert helpers == {address for base,length in fixture.NATIVE.items() for address in range(base,base+length,4)}
    mutations = [('fill', '192', '193'),
        ('assigned-return', 'return pMan->managedAffineArea.currentIdx = pMan->managedAffineArea.fromIdx;',
         'return pMan->managedAffineArea.currentIdx = pMan->managedAffineArea.fromIdx + 1;')]
    controls = []
    for label,before,after in mutations:
        assert text.count(before) == (2 if label == 'fill' else 1)
        wrong = ROOT / f'nonmatching/integration/20261101-oam296-closed/{label}/source.c'
        wrong.parent.mkdir(parents=True,exist_ok=True)
        changed=text.replace(before,after)
        if wrong.exists(): assert wrong.read_text(encoding='utf-8') == changed
        else: wrong.write_text(changed,encoding='utf-8')
        bad_row,bad_proof,bad_body=build(wrong,'wrong-'+label,False)
        bad_cases=[fixture.execute(image,bad_body,index)for index in range(240)]
        rejected=sum(not item['modelPassed']for item in bad_cases)
        assert rejected and all(item['actualReturn']for item in bad_cases)
        controls.append(dict(label=label,source=wrong.relative_to(ROOT).as_posix(),sourceSha256=sha256(wrong),
            compilation=bad_row,genuineLinkComparison=bad_proof,actualWrongReturns=240,
            independentModelRejections=rejected,unchangedPositives=240-rejected,cases=bad_cases))
    try: fixture.execute(image,native,0,bound=1)
    except AssertionError: pass
    else: raise AssertionError('Prefix admitted as return')
    trace=ROOT/'evidence/traces/main-oam-reference296-closed-20261101.json.gz'
    trace.parent.mkdir(parents=True,exist_ok=True)
    trace.write_bytes(gzip.compress(json.dumps(dict(cases=cases,controls=controls),sort_keys=True,separators=(',',':')).encode(),mtime=0))
    row.update(genuineLinkComparison=freeze_link(proof),exactBytes=296,
        sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceLanguage='C')
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),
        romSha256=config['romSha256'],processor='arm9',program='',module='main',moduleSha256=metadata['sha256'],
        matches=[row],matchedFunctions=1,matchedBytes=296,
        oracle=dict(pairs=600,actualTopReturns=1200,actualReturnRequired=True,instructionBytesObserved=288,
            generatedPoolBytes=8,actualNativeHelperReturnsSeparate=sum(item['original']['actualNativeReturns']*2 for item in cases),
            suppliedDmaCallsSeparate=sum(item['original']['providedCalls']*2 for item in cases),
            fullRegistersFlagsDataStackAndOrderedWritesCompared=True,fastFlagWords=[0,1,2,0x80000000,0xFFFFFFFF]),
        negativeEvidence=dict(actualWrongReturns=480,independentModelRejections=sum(item['independentModelRejections']for item in controls),
            unchangedPositives=sum(item['unchangedPositives']for item in controls),
            controls=[{key:value for key,value in item.items()if key!='cases'}for item in controls],boundedPrefixCredit=0),
        replayDependencies=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p))for p in [Path(fixture.__file__),trace,caller]],
        sourceOrigin=dict(publicReferenceRevision='d636fb5d2b212e8736f09859fff447be2bd0ac85',
            declaredSdkVersionForGame=False,standaloneTypedC=True,headerOrLibcPlaceholderInputs=False,
            historicalSdkVoidApiDistinctFromMeasuredRawWordReturn=True),
        reproductionCommand='python match_main_oam_reference296_closed_20261101.py',
        limitations=['Cache arrays and DMA word remain explicitly bound original data with zero source-data credit',
            'Banks0..2 and from/to0..127 with bounded valid/invalid-window states; malformed/aliased objects unsupported',
            'Original cache and CPU-fill instructions return; no actual cache/device coherence or concurrency claim',
            'DMA remains an explicitly supplied word-fill boundary; no rendering or scene claim',
            'The raw signed-word argument and unsigned assignment return match the selected game caller; no status meaning',
            'Whole-module and full-regression acceptance remains pending; no source-only ROM or complete native game proof'])
    write_json(ROOT/'evidence/matches/main-oam-reference296-closed-20261101.json',report)
    print(dict(functions=1,bytes=296,actualTopReturns=1200,nativeHelperReturns=report['oracle']['actualNativeHelperReturnsSeparate'],
        suppliedDmaCalls=report['oracle']['suppliedDmaCallsSeparate'],wrongReturns=480,
        wrongRejections=report['negativeEvidence']['independentModelRejections'],acceptancePending=True))


if __name__=='__main__':
    main()
