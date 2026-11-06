import gzip
import json
from pathlib import Path
from project import ROOT,configuration,write_json,sha256
from link_runtime_unit import measured_module
from save_link_snapshots import freeze_link
import match_main_oam_reference296_closed_20261101 as builder
import main_base_joint296_fixture_20261102 as fixture

WORK=ROOT/'work/main-base_joint296-qualified-20261102'
REPORT=ROOT/'evidence/matches/main-base_joint296-20261102.json'
SOURCES=[ROOT/f'src/runtime/20261102_base_joint296/native_main_{a:08x}.c'for a in fixture.SPANS]


def main():
    config=configuration();assert sha256(config['rom'])==config['romSha256']
    metadata,image,_=measured_module('main');assert metadata['sha256']=='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'
    builder.WORK=WORK;bodies={};rows=[];sources={}
    for path in SOURCES:
        row,proof,body=builder.build(path,path.stem,True);address=int(row['address'],0);assert len(body)==fixture.SPANS[address]
        row.update(exactBytes=len(body),sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceLanguage='C',genuineLinkComparison=freeze_link(proof))
        rows.append(row);bodies[address]=body;sources[address]=path
    cases=[];observed=set();pools=set()
    for index in range(2048):
        original=fixture.execute(image,{},index);candidate=fixture.execute(image,bodies,index)
        assert original==candidate and original['modelPassed'],(index,original['context'],original['registers'][0])
        cases.append(original);observed.update(original['ownObserved'])
        for address,size,value in original['reads']:
            if any(base<=address and address+size<=base+length for base,length in fixture.SPANS.items()):pools.update(range(address,address+size))
    controls=[]
    for kind,address in enumerate(fixture.SPANS):
        path=sources[address];text=path.read_text(encoding='utf-8');old,new=('pResult->flag |= NNS_G3D_JNTANM_RESULTFLAG_TRANS_ZERO','pResult->flag |= NNS_G3D_JNTANM_RESULTFLAG_ROT_ZERO')if address==0x020323DC else('p += 2 * sizeof(fx16);','p += 4 * sizeof(fx16);');changed=text.replace(old,new);assert changed!=text
        wrong=ROOT/f'nonmatching/integration/20261102-base_joint296/palette-{kind}/source.c';wrong.parent.mkdir(parents=True,exist_ok=True)
        if wrong.exists():assert wrong.read_text(encoding='utf-8')==changed
        else:wrong.write_text(changed,encoding='utf-8')
        row,proof,body=builder.build(wrong,f'palette-{kind}',False);assert len(body)<=fixture.SPANS[address]
        bad={**bodies,address:body};indices=[i for i in range(2048)if fixture.inputs(i)[2]==address]
        results=[fixture.execute(image,bad,i)for i in indices]
        rejected=sum(not row['modelPassed']for row in results);assert rejected
        controls.append(dict(label=f'palette-{kind}',source=wrong.relative_to(ROOT).as_posix(),sourceSha256=sha256(wrong),
         actualWrongReturns=len(results),rejected=rejected,positiveControls=len(results)-rejected))
    try:fixture.execute(image,bodies,0,bound=1)
    except AssertionError:pass
    else:raise AssertionError('Prefix counted as return')
    missing={hex(base):[hex(a)for a in range(base,base+n,4)if a not in observed and a not in{p&~3 for p in pools}]for base,n in fixture.SPANS.items()}
    trace=ROOT/'evidence/traces/main-base_joint296-20261102.json.gz'
    trace.write_bytes(gzip.compress(json.dumps(dict(cases=cases),sort_keys=True,separators=(',',':')).encode(),mtime=0))
    write_json(REPORT,dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),romSha256=config['romSha256'],
     processor='arm9',program='',module='main',moduleSha256=metadata['sha256'],matches=rows,matchedFunctions=2,matchedBytes=296,
     oracle=dict(pairs=2048,actualTopReturns=4096,suppliedCallbackCalls=sum(c['functionProviders']for c in cases)*2,cpu='ARM946',ownInstructionBytesObserved=len(observed)*4,
      generatedPoolBytes=len(pools),unobservedCodeAddresses=missing,independentNodeDictionaryAndCallbackOffsetModel=True,
      completeRegistersFlagsMainInputStackOrderedReadsWritesCompared=True,signedArithmeticOverflowExcluded=True),
     negativeControls=controls,replayDependencies=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p))for p in[Path(fixture.__file__),trace]],
     reproductionCommand='python match_main_base_joint296_20261102.py',limitations=[
      'Valid8-entry dictionary, aligned128-byte nodes and bounded command node indices0..7; invalid dictionary indices/null pointers are unsupported C paths',
      'All16 low-nibble node flag combinations and upper matrix-stack fields are synthetic; no model/animation asset or scene reachability claim',
      'Scale callback is explicitly supplied with six initialized payload words and no memory effects; callback semantics/source and graphics hardware are not recovered here',
      'No data/renderer/Windows/Android/full-game/source-only ROM credit']))
    print(dict(functions=2,bytes=296,actualReturns=4096,observedBytes=len(observed)*4,poolBytes=len(pools),
     wrongReturns=sum(c['actualWrongReturns']for c in controls),wrongRejected=sum(c['rejected']for c in controls),missing=missing))


if __name__=='__main__':
    main()
