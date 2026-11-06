import gzip
import json
from pathlib import Path
from project import ROOT,configuration,write_json,sha256
from link_runtime_unit import measured_module,validate
from recover_linked_runtime import qualified_bindings
import match_runtime as compiler
from save_link_snapshots import freeze_link
import match_main_oam_reference296_closed_20261101 as builder
import main_canvas_clear284_fixture_20261102 as fixture

WORK=ROOT/'work/main-canvas_clear284-qualified-20261102'
REPORT=ROOT/'evidence/matches/main-canvas_clear284-20261102.json'
SOURCES=[ROOT/'src/verified_assembly/20261102_mi_clear76/native_main_02008c58.c',*[ROOT/f'src/runtime/20261102_canvas_clear208/native_main_{a:08x}.c'for a in list(fixture.SPANS)[1:]]]


def build(path,label,exact):
    if 'verified_assembly'not in path.as_posix()and 'wrong-fill'not in label:return builder.build(path,label,exact)
    compiler.WORK=WORK/label/'compile';rows,unused=compiler.compare(path,'main','2','off',compiler=ROOT/'tools/mwccarm/mwccarm/2.0/sp1p5/mwccarm.exe');assert len(rows)==1
    row=rows[0];directory=WORK/label/'link'
    try:proof=validate(row,qualified_bindings(row),directory);assert exact
    except ValueError as error:assert not exact and isinstance(error.args[0],dict);proof=error.args[0]
    return row,proof,(directory/'caller.bin').read_bytes()


def main():
    config=configuration();assert sha256(config['rom'])==config['romSha256']
    metadata,image,_=measured_module('main');assert metadata['sha256']=='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'
    builder.WORK=WORK;bodies={};rows=[];sources={}
    for path in SOURCES:
        row,proof,body=build(path,path.stem,True);address=int(row['address'],0);assert len(body)==fixture.SPANS[address]
        row.update(exactBytes=len(body),sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceLanguage='C',genuineLinkComparison=freeze_link(proof))
        if address==0x02008C58:
            row.update(sourceLanguage='assembly',assemblyJustification=dict(classification='verified-original-SDK-assembly',publishedSource='deps/reference/NitroSDK-ccbbcc8b6db4c4dbba3d503d2026978d78977840/libraries/mi/src/mi_memory.c',function='MIi_CpuClearFast',line=220,originalExplicitAsmDeclaration=True,sourceStatementsDerivedFromPublishedSdkNotDisassembly=True,labelsAndPublicSymbolRenamed=True,conditionalAsmBugWorkaroundInactiveForMeasuredBuild=True,historicalExactSdkRevisionProved=False,ordinaryLogicAssemblyExceptions=0))
        rows.append(row);bodies[address]=body;sources[address]=path
    cases=[];observed=set();pools=set()
    for index in range(3072):
        original=fixture.execute(image,{},index);candidate=fixture.execute(image,bodies,index)
        assert original==candidate and original['modelPassed'],(index,original['context'],original['registers'][0])
        cases.append(original);observed.update(original['ownObserved'])
        for address,size,value in original['reads']:
            if any(base<=address and address+size<=base+length for base,length in fixture.SPANS.items()):pools.update(range(address,address+size))
    controls=[]
    for kind,address in enumerate(fixture.SPANS):
        path=sources[address];text=path.read_text(encoding='utf-8');old,new=('mov r8, r2','mvn r8, r2')if address==0x02008C58 else('val << 4','val << 3');changed=text.replace(old,new);assert changed!=text
        wrong=ROOT/f'nonmatching/integration/20261102-canvas_clear284/palette-{kind}/source.c';wrong.parent.mkdir(parents=True,exist_ok=True)
        if wrong.exists():assert wrong.read_text(encoding='utf-8')==changed
        else:wrong.write_text(changed,encoding='utf-8')
        row,proof,body=build(wrong,f'wrong-fill-{kind}'if kind==0 else f'palette-{kind}',False);assert len(body)<=fixture.SPANS[address]
        bad={**bodies,address:body};indices=[i for i in range(3072)if fixture.inputs(i)[2]==address]
        results=[fixture.execute(image,bad,i)for i in indices]
        rejected=sum(not row['modelPassed']for row in results);assert rejected
        controls.append(dict(label=f'palette-{kind}',source=wrong.relative_to(ROOT).as_posix(),sourceSha256=sha256(wrong),
         actualWrongReturns=len(results),rejected=rejected,positiveControls=len(results)-rejected))
    try:fixture.execute(image,bodies,0,bound=1)
    except AssertionError:pass
    else:raise AssertionError('Prefix counted as return')
    missing={hex(base):[hex(a)for a in range(base,base+n,4)if a not in observed and a not in{p&~3 for p in pools}]for base,n in fixture.SPANS.items()}
    trace=ROOT/'evidence/traces/main-canvas_clear284-20261102.json.gz'
    trace.write_bytes(gzip.compress(json.dumps(dict(cases=cases),sort_keys=True,separators=(',',':')).encode(),mtime=0))
    write_json(REPORT,dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),romSha256=config['romSha256'],
     processor='arm9',program='',module='main',moduleSha256=metadata['sha256'],matches=rows,matchedFunctions=3,matchedBytes=284,ordinaryCFunctions=2,ordinaryCBytes=208,verifiedOriginalAssemblyFunctions=1,verifiedOriginalAssemblyBytes=76,
     oracle=dict(pairs=3072,actualTopReturns=6144,functionProviders=0,cpu='ARM946',ownInstructionBytesObserved=len(observed)*4,
      generatedPoolBytes=len(pools),unobservedCodeAddresses=missing,independentWordFillAndCanvasRowsModel=True,
      completeRegistersFlagsMainInputStackOrderedReadsWritesCompared=True,signedArithmeticOverflowExcluded=True),
     negativeControls=controls,replayDependencies=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p))for p in[Path(fixture.__file__),trace]],
     reproductionCommand='python match_main_canvas_clear284_20261102.py',limitations=[
      'Bounded aligned RAM: fast-fill sizes0..1024 multiples4; canvas widths0..16 heights0..8, bpp4/8, valid palettes and bounded row strides',
      'Fast-fill is recovered from an explicit published asm definition, independently compiled with pinnedSP1p5 and genuinely mwld-linked, with no generated disassembly or binary edits',
      'Historical exact SDK revision is not proved; the original source explicitly implements this identical routine in assembly',
      'Both ordinary C callers and the verified original-assembly callee run together without providers; no MMIO/cache/DMA/concurrency/VRAM claim',
      'No device/dual-screen scene, source-only ROM or complete native game']))
    print(dict(functions=3,bytes=284,actualReturns=6144,observedBytes=len(observed)*4,poolBytes=len(pools),
     wrongReturns=sum(c['actualWrongReturns']for c in controls),wrongRejected=sum(c['rejected']for c in controls),missing=missing))


if __name__=='__main__':
    main()
