import gzip
import json
from pathlib import Path
from project import ROOT,configuration,write_json,sha256
from link_runtime_unit import measured_module
from save_link_snapshots import freeze_link
import match_main_oam_reference296_closed_20261101 as builder
import main_material_track1120_fixture_20261102 as fixture

WORK=ROOT/'work/main-material-track1120-qualified-20261102'
REPORT=ROOT/'evidence/matches/main-material-track1120-20261102.json'
SOURCES=[ROOT/f'src/runtime/20261102_material_track1120/native_main_{a:08x}.c'for a in list(fixture.SPANS)[:3]]
SOURCES.append(ROOT/'src/runtime/20261102_material_track1120_v2/native_main_02033e48.c')


def main():
    config=configuration();assert sha256(config['rom'])==config['romSha256']
    metadata,image,_=measured_module('main');assert metadata['sha256']=='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'
    builder.WORK=WORK;bodies={};rows=[];sources={}
    for path in SOURCES:
        row,proof,body=builder.build(path,path.stem,True);address=int(row['address'],0);assert len(body)==fixture.SPANS[address]
        row.update(exactBytes=len(body),sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceLanguage='C',genuineLinkComparison=freeze_link(proof))
        rows.append(row);bodies[address]=body;sources[address]=path
    cases=[];observed=set();pools=set()
    for index in range(4096):
        original=fixture.execute(image,{},index);candidate=fixture.execute(image,bodies,index)
        assert original==candidate and original['modelPassed'],(index,original['context'],original['registers'][0])
        cases.append(original);observed.update(original['ownObserved'])
        for address,size,value in original['reads']:
            if any(base<=address and address+size<=base+length for base,length in fixture.SPANS.items()):pools.update(range(address,address+size))
    controls=[]
    for kind,address in enumerate(fixture.SPANS):
        path=sources[address];text=path.read_text(encoding='utf-8');old='STEP_2                = 0x40000000'if kind<2 else'STEP_2            = 0x40000000'
        if old not in text:
            import re
            match=re.search(r'STEP_2\s+= 0x40000000',text);assert match;old=match.group()
        changed=text.replace(old,old.replace('0x40000000','0x80000000'));assert changed!=text
        wrong=ROOT/f'nonmatching/integration/20261102-material-track1120/step-{kind}/source.c';wrong.parent.mkdir(parents=True,exist_ok=True)
        if wrong.exists():assert wrong.read_text(encoding='utf-8')==changed
        else:wrong.write_text(changed,encoding='utf-8')
        row,proof,body=builder.build(wrong,f'step-{kind}',False);assert len(body)<=fixture.SPANS[address]
        bad={**bodies,address:body};results=[fixture.execute(image,bad,i)for i in range(kind,4096,4)]
        rejected=sum(not row['modelPassed']for row in results);assert rejected
        controls.append(dict(label=f'step-{kind}',source=wrong.relative_to(ROOT).as_posix(),sourceSha256=sha256(wrong),
         actualWrongReturns=len(results),rejected=rejected,positiveControls=len(results)-rejected))
    try:fixture.execute(image,bodies,0,bound=1)
    except AssertionError:pass
    else:raise AssertionError('Prefix counted as return')
    missing={hex(base):[hex(a)for a in range(base,base+n,4)if a not in observed and a not in{p&~3 for p in pools}]for base,n in fixture.SPANS.items()}
    trace=ROOT/'evidence/traces/main-material-track1120-20261102.json.gz'
    trace.write_bytes(gzip.compress(json.dumps(dict(cases=cases),sort_keys=True,separators=(',',':')).encode(),mtime=0))
    write_json(REPORT,dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),romSha256=config['romSha256'],
     processor='arm9',program='',module='main',moduleSha256=metadata['sha256'],matches=rows,matchedFunctions=4,matchedBytes=1120,
     oracle=dict(pairs=4096,actualTopReturns=8192,functionProviders=0,cpu='ARM946',ownInstructionBytesObserved=len(observed)*4,
      generatedPoolBytes=len(pools),unobservedCodeAddresses=missing,independentPerChannelWeightedInterpolation=True,
      completeRegistersFlagsMainInputStackOrderedReadsWritesCompared=True,signedArithmeticOverflowExcluded=True),
     negativeControls=controls,replayDependencies=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p))for p in[Path(fixture.__file__),trace]],
     reproductionCommand='python match_main_material_track1120_20261102.py',limitations=[
      'Synthetic initialized256-sample tracks, frame0..31, last interpolation0/frame, both16/32-bit vector storage and constant/step flags',
      'Synthetic metadata does not establish valid encoded assets, complete renderer or scene reachability',
      'Unsigned long is target32-bit and compile-time asserted; Android LP64 source portability remains unproved',
      'No data or callee credit, source-only ROM, full native game or Android device proof']))
    print(dict(functions=4,bytes=1120,actualReturns=8192,observedBytes=len(observed)*4,poolBytes=len(pools),
     wrongReturns=sum(c['actualWrongReturns']for c in controls),wrongRejected=sum(c['rejected']for c in controls),missing=missing))


if __name__=='__main__':
    main()
