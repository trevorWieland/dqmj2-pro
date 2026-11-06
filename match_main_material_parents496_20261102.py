import gzip
import json
from pathlib import Path
from project import ROOT,configuration,write_json,sha256
from link_runtime_unit import measured_module
from save_link_snapshots import freeze_link
import match_main_oam_reference296_closed_20261101 as builder
import main_material_parents496_fixture_20261102 as fixture
from match_main_material_track1120_20261102 import SOURCES as LEAVES

WORK=ROOT/'work/main-material-parents496-qualified-20261102'
REPORT=ROOT/'evidence/matches/main-material-parents496-20261102.json'
SOURCES=[ROOT/f'src/runtime/20261102_material_parents496/native_main_{a:08x}.c'for a in fixture.PARENTS]


def main():
    config=configuration();assert sha256(config['rom'])==config['romSha256']
    metadata,image,_=measured_module('main');assert metadata['sha256']=='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'
    builder.WORK=WORK;bodies={};rows=[];sources={};helpers=[]
    for path in[*SOURCES,*LEAVES]:
        row,proof,body=builder.build(path,path.stem,True);address=int(row['address'],0);assert len(body)==fixture.SPANS[address]
        row.update(exactBytes=len(body),sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceLanguage='C',genuineLinkComparison=freeze_link(proof))
        (rows if path in SOURCES else helpers).append(row);bodies[address]=body;sources[address]=path
    cases=[];observed=set();pools=set()
    for index in range(1024):
        original=fixture.execute(image,{},index);candidate=fixture.execute(image,bodies,index)
        assert original==candidate and original['modelPassed'],(index,original['context'])
        cases.append(original);observed.update(original['ownObserved'])
        for address,size,value in original['reads']:
            if any(base<=address and address+size<=base+length for base,length in fixture.PARENTS.items()):pools.update(range(address,address+size))
    controls=[]
    for address,old,new in[(0x02033C58,'0x00008000','0x00004000'),
     (0x02033F54,'NNS_G3D_MATANM_RESULTFLAG_TEXMTX_TRANSZERO = 0x00000004','NNS_G3D_MATANM_RESULTFLAG_TEXMTX_TRANSZERO = 0x00000020')]:
        path=sources[address];text=path.read_text(encoding='utf-8');changed=text.replace(old,new);assert changed!=text
        label=f'parent-{address:08x}';wrong=ROOT/f'nonmatching/integration/20261102-material-parents496/{label}/source.c';wrong.parent.mkdir(parents=True,exist_ok=True)
        if wrong.exists():assert wrong.read_text(encoding='utf-8')==changed
        else:wrong.write_text(changed,encoding='utf-8')
        row,proof,body=builder.build(wrong,label,False);assert len(body)<=fixture.PARENTS[address]
        bad={**bodies,address:body};kind=0 if address==0x02033C58 else 1
        results=[fixture.execute(image,bad,i)for i in range(kind,1024,2)];rejected=sum(not row['modelPassed']for row in results);assert rejected
        controls.append(dict(label=label,source=wrong.relative_to(ROOT).as_posix(),sourceSha256=sha256(wrong),
         actualWrongReturns=len(results),rejected=rejected,positiveControls=len(results)-rejected))
    try:fixture.execute(image,bodies,0,bound=1)
    except AssertionError:pass
    else:raise AssertionError('Prefix counted as return')
    own={a for a in observed if any(base<=a<base+n for base,n in fixture.PARENTS.items())}
    missing={hex(base):[hex(a)for a in range(base,base+n,4)if a not in own and a not in{p&~3 for p in pools}]for base,n in fixture.PARENTS.items()}
    trace=ROOT/'evidence/traces/main-material-parents496-20261102.json.gz'
    trace.write_bytes(gzip.compress(json.dumps(dict(cases=cases),sort_keys=True,separators=(',',':')).encode(),mtime=0))
    write_json(REPORT,dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),romSha256=config['romSha256'],
     processor='arm9',program='',module='main',moduleSha256=metadata['sha256'],matches=rows,matchedFunctions=2,matchedBytes=496,
     actualCompiledLeafDependencies=helpers,leafSourceCreditInThisReport=0,
     oracle=dict(pairs=1024,actualTopReturns=2048,actualNativeHelperReturns=10240,functionProviders=0,cpu='ARM946',
      ownInstructionBytesObserved=len(own)*4,generatedPoolBytes=len(pools),unobservedCodeAddresses=missing,
      completeRegistersFlagsMainInputStackOrderedReadsWritesCompared=True,independentResultFlagsAndPackedChannels=True),
     negativeControls=controls,replayDependencies=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p))for p in[Path(fixture.__file__),trace]],
     reproductionCommand='python match_main_material_parents496_20261102.py',limitations=[
      'Four-entry initialized dictionaries and frame0..31 with bounded synthetic tracks; no malformed asset/null/index recovery claim',
      'Original parent and four independently qualified compiled leaves execute together; no renderer or ordinary scene proof',
      'Unsigned long and pointers target32-bit; no Android LP64 portability or device execution',
      'No data/helper additional source credit, source-only ROM or full native Windows game']))
    print(dict(functions=2,bytes=496,actualReturns=2048,nativeHelperReturns=10240,observedBytes=len(own)*4,poolBytes=len(pools),
     wrongReturns=1024,wrongRejected=sum(c['rejected']for c in controls),missing=missing))


if __name__=='__main__':
    main()
