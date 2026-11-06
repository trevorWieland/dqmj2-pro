import gzip
import json
from pathlib import Path
from project import ROOT,configuration,write_json,sha256
from link_runtime_unit import measured_module
from save_link_snapshots import freeze_link
import match_main_oam_reference296_closed_20261101 as builder
import main_canvas_areas1224_fixture_20261102 as fixture

WORK=ROOT/'work/main-canvas_areas1224-qualified-20261102'
REPORT=ROOT/'evidence/matches/main-canvas_areas1224-20261102.json'
SOURCES=[ROOT/f'src/runtime/20261102_canvas_areas1224/native_main_{a:08x}.c'for a in fixture.OWN]


def main():
    config=configuration();assert sha256(config['rom'])==config['romSha256']
    metadata,image,_=measured_module('main');assert metadata['sha256']=='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'
    builder.WORK=WORK;bodies={};rows=[];sources={}
    for path in SOURCES:
        row,proof,body=builder.build(path,path.stem,True);address=int(row['address'],0);assert len(body)==fixture.SPANS[address]
        row.update(exactBytes=len(body),sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceLanguage='C',genuineLinkComparison=freeze_link(proof))
        rows.append(row);bodies[address]=body;sources[address]=path
    cases=[];observed=set();pools=set()
    for index in range(3072):
        original=fixture.execute(image,{},index);candidate=fixture.execute(image,bodies,index)
        assert original==candidate and original['modelPassed'],(index,original['context'],original['registers'][0])
        cases.append(original);observed.update(original['ownObserved'])
        for address,size,value in original['reads']:
            if any(base<=address and address+size<=base+length for base,length in fixture.OWN.items()):pools.update(range(address,address+size))
    controls=[]
    for kind,address in enumerate(bodies):
        path=sources[address];text=path.read_text(encoding='utf-8');old,new=('u32 x4 = (unsigned int)x * 4;','u32 x4 = (unsigned int)x * 2;')if address==0x02035650 else('val << 4','val << 3');changed=text.replace(old,new);assert changed!=text
        wrong=ROOT/f'nonmatching/integration/20261102-canvas_areas1224/palette-{kind}/source.c';wrong.parent.mkdir(parents=True,exist_ok=True)
        if wrong.exists():assert wrong.read_text(encoding='utf-8')==changed
        else:wrong.write_text(changed,encoding='utf-8')
        row,proof,body=builder.build(wrong,f'palette-{kind}',False);assert len(body)<=fixture.SPANS[address]
        bad={**bodies,address:body};indices=[i for i in range(3072)if fixture.inputs(i)[2]==address]
        results=[fixture.execute(image,bad,i)for i in indices]
        rejected=sum(not row['modelPassed']for row in results);assert rejected
        controls.append(dict(label=f'palette-{kind}',source=wrong.relative_to(ROOT).as_posix(),sourceSha256=sha256(wrong),
         actualWrongReturns=len(results),rejected=rejected,positiveControls=len(results)-rejected))
    try:fixture.execute(image,bodies,0,bound=1)
    except AssertionError:pass
    else:raise AssertionError('Prefix counted as return')
    missing={hex(base):[hex(a)for a in range(base,base+n,4)if a not in observed and a not in{p&~3 for p in pools}]for base,n in fixture.OWN.items()}
    trace=ROOT/'evidence/traces/main-canvas_areas1224-20261102.json.gz'
    trace.write_bytes(gzip.compress(json.dumps(dict(cases=cases),sort_keys=True,separators=(',',':')).encode(),mtime=0))
    write_json(REPORT,dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),romSha256=config['romSha256'],
     processor='arm9',program='',module='main',moduleSha256=metadata['sha256'],matches=rows,matchedFunctions=3,matchedBytes=1224,
     oracle=dict(pairs=3072,actualTopReturns=6144,actualSelectedNestedReturns=sum(c['actualSelectedNestedReturns']for c in cases)*2,actualNativeHelperReturns=sum(c['actualNativeHelperReturns']for c in cases)*2,functionProviders=0,cpu='ARM946',ownInstructionBytesObserved=len(observed)*4,
      generatedPoolBytes=len(pools),unobservedCodeAddresses=missing,independentPackedPixelAndObjectBlockAddressModel=True,
      completeRegistersFlagsMainInputStackOrderedReadsWritesCompared=True,signedArithmeticOverflowExcluded=True),
     negativeControls=controls,replayDependencies=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p))for p in[Path(fixture.__file__),trace]],
     reproductionCommand='python match_main_canvas_areas1224_20261102.py',limitations=[
      'Parents use bounded4bpp1/2/4/8-tile canvases; original276-byte six-word index helper and accepted76-byte original-assembly fill helper execute without additional source credit',
      'Direct clear supports4bpp nonempty widths and8bpp full-tile or cross-word rectangles; undefined original32bit shift domains for left/right-only8bpp rectangles and zero-width direct calls are explicitly excluded',
      'All selected C units run together; source/input/stack/registers/flags/ordered accesses are compared with no providers or hardware',
      'No asset/VRAM/rendered scene, Windows/Android or source-only ROM/full-game claim']))
    print(dict(functions=3,bytes=1224,actualReturns=6144,observedBytes=len(observed)*4,poolBytes=len(pools),
     wrongReturns=sum(c['actualWrongReturns']for c in controls),wrongRejected=sum(c['rejected']for c in controls),missing=missing))


if __name__=='__main__':
    main()
