import gzip
import hashlib
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import match_runtime as compiler
from main_fifo_send136_fixture_20261101 import execute, IRQ
from main_fifo_requests_fixture_20261101 import ENTRIES as CALLERS, execute as execute_caller
from project import ROOT, configuration, write_json, read_json, sha256
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link

WORK = ROOT / 'work/fifo-send136-20261101'


def build(source, label, exact):
    compiler.WORK = WORK / label / 'compile'
    rows, unused = compiler.compare(source, 'main', 2, 'off', True)
    assert len(rows) == 1 and not rows[0].get('compileFailed')
    row = rows[0]
    try:
        proof = validate(row, qualified_bindings(row), WORK / label / 'link')
    except ValueError as error:
        if exact:
            raise
        assert not exact and isinstance(error.args[0], dict)
        proof = error.args[0]
    return row, proof, (WORK / label / 'link/caller.bin').read_bytes()




def main():
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    metadata,image,unused = measured_module('main')
    source = ROOT/'src/runtime/20261101_fifo_send136/native_main_0200a440.c'
    entry,size = 0x0200A440,136
    row,proof,compiled = build(source,'positive',True)
    native = image[entry-0x02000000:entry-0x02000000+size]
    assert compiled == native
    cases,observed,helpers,controls = [],set(),set(),[]
    for index in range(768):
        first,second = execute(image,entry,native,index),execute(image,entry,compiled,index)
        assert first == second
        observed.update(first['observed']);helpers.update(first['helperObserved'])
        cases.append(dict(index=index,original=first,candidate=second))
    assert len(observed) == 132 and len(helpers) == 44
    for number,(before,after) in enumerate([('word.flag = flag;','word.flag = flag ^ 1U;'),('return -1;','return -3;'),('return -2;','return -4;')]):
        text = source.read_text();assert text.count(before) == 1
        path = ROOT/f'nonmatching/integration/20261101-fifo-send-controls/{number}/source.c'
        path.parent.mkdir(parents=True,exist_ok=True)
        changed = text.replace(before,after)
        if path.exists():assert path.read_text() == changed
        path.write_text(changed,encoding='utf-8')
        bad,badproof,badbody = build(path,f'negative-{number}',False)
        results = [execute(image,entry,badbody,index,require_model=False)for index in range(96)]
        rejects = sum(not value['modelPassed']for value in results);assert rejects > 0
        controls.append(dict(compilation=bad,genuineLinkComparison=badproof,actualReturns=len(results),
            independentRejections=rejects,unchangedPositiveCases=len(results)-rejects,cases=results))
    trace_report = read_json(ROOT/'evidence/matches/main-fifo-requests352-v2-20261101.json')
    trace = trace_report['oracle']['traceArchive'];assert sha256(ROOT/trace['path']) == trace['sha256']
    prior = json.loads(gzip.decompress((ROOT/trace['path']).read_bytes()))
    originals = {(int(x['entry'],0),x['original']['index']):x['original']for x in prior}
    image_with_source = bytearray(image)
    image_with_source[entry-0x02000000:entry-0x02000000+size] = compiled
    composed,caller_proofs = [],[]
    for caller,length in CALLERS.items():
        path = ROOT/f'src/runtime/20261101_fifo_requests352/native_main_{caller:08x}.c'
        compiler.WORK = WORK/f'caller-{caller:08x}'/'compile'
        rows,unused = compiler.compare(path,'main',2,'off')
        assert len(rows) == 1
        linked = validate(rows[0],qualified_bindings(rows[0]),WORK/f'caller-{caller:08x}'/'link')
        body = (WORK/f'caller-{caller:08x}'/'link/caller.bin').read_bytes()
        assert body == image[caller-0x02000000:caller-0x02000000+length]
        caller_proofs.append(dict(compilation=rows[0],genuineLinkComparison=freeze_link(linked)))
        for index in range(128):
            result = execute_caller(bytes(image_with_source),caller,body,index)
            assert result == originals[caller,index]
            composed.append(dict(entry=hex(caller),index=index,result=result))
    try:execute(image,entry,native,0,bound=1)
    except AssertionError:pass
    else:raise AssertionError('Exhausted prefix is not a return')
    raw = json.dumps(dict(direct=cases,composed=composed),sort_keys=True,separators=(',',':')).encode()
    archive = ROOT/'evidence/traces/main-fifo-send136-20261101.json.gz';archive.parent.mkdir(parents=True,exist_ok=True);archive.write_bytes(gzip.compress(raw,mtime=0))
    row.update(genuineLinkComparison=freeze_link(proof),exactBytes=136,sourceOnlyCompilerInput=True,originalObjectScaffolding=False)
    returns = sum(x[side]['actualNativeDependencyReturns']for x in cases for side in ['original','candidate'])
    source_returns = sum(x['result']['actualNativeDependencyReturns']for x in composed)
    references = ['deps/reference/nitro-10e447b8/src/pxi/pxi.c','deps/reference/nitro-10e447b8/include/nitro/pxi.h']
    report = dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),
        fixture='main_fifo_send136_fixture_20261101.py',fixtureSha256=sha256(ROOT/'main_fifo_send136_fixture_20261101.py'),
        romSha256=config['romSha256'],processor='arm9',program='',module='main',moduleSha256=metadata['sha256'],
        matches=[row],matchedFunctions=1,matchedBytes=136,compiledCallerCompositions=caller_proofs,
        oracle=dict(pairs=768,actualDirectTopReturns=1536,actualSourceComposedParentReturns=len(composed),
            actualDirectNativeDependencyReturns=returns,actualComposedLowerReturns=source_returns,
            suppliedCalls=0,ownCodeBytesObserved=132,generatedLiteralBytes=4,
            independentPackingModel='channel low5 | flag low1 atbit5 | payload low26 atbit6',
            actualReturnAndFullCpuPageStackOrderedEffectComparison=True,
            traceArchive=dict(path=archive.relative_to(ROOT).as_posix(),sha256=sha256(archive),decodedSha256=hashlib.sha256(raw).hexdigest())),
        negativeEvidence=dict(compiledReturningControls=controls,exhaustedPrefixReturnCredit=0),
        replayDependencies=[dict(path=archive.relative_to(ROOT).as_posix(),sha256=sha256(archive))],
        comparisonReferences=[dict(path=path,sha256=sha256(ROOT/path),compilerInput=False,unmodified=True)for path in references],
        reproductionCommand='python match_main_fifo_send136_20261101.py',
        limitations=['Private FIFO register byte snapshots, not physical hardware W1C or ARM7 message processing',
            'Native IRQ helpers execute directly; three caller bodies and FIFO sender compile freshly for composition',
            'Reference SDK revision identity, concurrency, game-scene availability and source-only ROM remain unproved'])
    write_json(ROOT/'evidence/matches/main-fifo-send136-20261101.json',report)
    print(dict(newFunctions=1,newBytes=136,directReturns=1536,composedParentReturns=len(composed),nativeLowerReturns=returns,
        composedLowerReturns=source_returns,wrongReturns=sum(x['actualReturns']for x in controls),independentRejections=sum(x['independentRejections']for x in controls),suppliedCalls=0))


if __name__ == '__main__':main()
