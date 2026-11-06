import gzip
import json
from pathlib import Path
from project import ROOT,configuration,write_json,sha256
from link_runtime_unit import measured_module
from save_link_snapshots import freeze_link
import match_main_oam_reference296_closed_20261101 as builder
import main_joint_scalar752_fixture_20261102 as fixture

WORK=ROOT/'work/main-joint-scalar752-qualified-20261102'
REPORT=ROOT/'evidence/matches/main-joint-scalar752-20261102.json'
SOURCES=[ROOT/'src/runtime/20261102_joint_animation4588/native_main_02032b90.c',
 ROOT/'src/runtime/20261102_joint_animation4588_ranked/native_main_02032ed4.c']


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
        assert original==candidate and original['modelPassed'],(index,original['context'])
        cases.append(original);observed.update(original['ownObserved'])
        for address,size,value in original['reads']:
            if any(base<=address and address+size<=base+length for base,length in fixture.SPANS.items()):pools.update(range(address,address+size))
    controls=[]
    for label,address,old,new in[
     ('translation-wrap',0x02032B90,'if (pJntAnm->flag & NNS_G3D_JNTANM_OPTION_END_TO_START_INTERPOLATION)',
      'if (!(pJntAnm->flag & NNS_G3D_JNTANM_OPTION_END_TO_START_INTERPOLATION))'),
     ('scale-wrap',0x02032ED4,'if (pJntAnm->flag & NNS_G3D_JNTANM_OPTION_END_TO_START_INTERPOLATION)',
      'if (!(pJntAnm->flag & NNS_G3D_JNTANM_OPTION_END_TO_START_INTERPOLATION))'),
     ('translation-width',0x02032B90,'const fx16 * p_fx16','const u16 * p_fx16'),
     ('scale-width',0x02032ED4,'const fx16 * p_fx16','const u16 * p_fx16')]:
        text=sources[address].read_text(encoding='utf-8');changed=text.replace(old,new);assert changed!=text
        path=ROOT/f'nonmatching/integration/20261102-joint-scalar752/{label}/source.c';path.parent.mkdir(parents=True,exist_ok=True)
        if path.exists():assert path.read_text(encoding='utf-8')==changed
        else:path.write_text(changed,encoding='utf-8')
        row,proof,body=builder.build(path,label,False);assert len(body)<=fixture.SPANS[address]
        bad={**bodies,address:body};indices=[i for i in range(4096)if bool(i%2)==(address==0x02032ED4)]
        results=[fixture.execute(image,bad,i)for i in indices];rejected=sum(not row['modelPassed']for row in results);assert rejected
        controls.append(dict(label=label,source=path.relative_to(ROOT).as_posix(),sourceSha256=sha256(path),actualWrongReturns=len(results),rejected=rejected,positiveControls=len(results)-rejected))
    try:fixture.execute(image,bodies,0,bound=1)
    except AssertionError:pass
    else:raise AssertionError('Prefix counted as return')
    missing={hex(base):[hex(a)for a in range(base,base+n,4)if a not in observed and a not in{p&~3 for p in pools}]for base,n in fixture.SPANS.items()}
    trace=ROOT/'evidence/traces/main-joint-scalar752-20261102.json.gz'
    trace.write_bytes(gzip.compress(json.dumps(dict(cases=cases),sort_keys=True,separators=(',',':')).encode(),mtime=0))
    write_json(REPORT,dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),romSha256=config['romSha256'],
     processor='arm9',program='',module='main',moduleSha256=metadata['sha256'],matches=rows,matchedFunctions=2,matchedBytes=752,
     oracle=dict(pairs=4096,actualTopReturns=8192,functionProviders=0,cpu='ARM946',ownInstructionBytesObserved=len(observed)*4,
      generatedPoolBytes=len(pools),unobservedCodeAddresses=missing,independentSingleFloorInterpolationModel=True,
      completeRegistersFlagsMainInputStackOrderedReadsWritesCompared=True,signedArithmeticOverflowExcluded=True),
     negativeControls=controls,replayDependencies=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p))for p in[Path(fixture.__file__),trace]],
     reproductionCommand='python match_main_joint_scalar752_20261102.py',limitations=[
      'Bounded initialized128-sample arrays, frame0..32, four fraction edges, both16/32-bit scalar storage and step/end-wrap settings',
      'Synthetic metadata may not describe valid game assets; no complete encoded-track validation or scene animation claim',
      'Unsigned long rank is required for the404-byte unit on pinned32-bit compiler; compile-time width assertion does not establish Android LP64 portability',
      'No callee/data source credit, source-only ROM, Windows execution of this group, full native game or Android device proof']))
    print(dict(functions=2,bytes=752,actualReturns=8192,observedBytes=len(observed)*4,poolBytes=len(pools),
     wrongReturns=sum(c['actualWrongReturns']for c in controls),wrongRejected=sum(c['rejected']for c in controls),missing=missing))


if __name__=='__main__':
    main()
