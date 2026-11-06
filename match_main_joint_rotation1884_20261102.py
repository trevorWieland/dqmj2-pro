import gzip
import json
from pathlib import Path
from project import ROOT,configuration,write_json,sha256
from link_runtime_unit import measured_module
from save_link_snapshots import freeze_link
import match_main_oam_reference296_closed_20261101 as builder
import main_joint_rotation1884_fixture_20261102 as fixture
from match_main_joint_helpers644_20261102 import SOURCES as HELPERS

WORK=ROOT/'work/main-joint-rotation1884-qualified-20261102'
REPORT=ROOT/'evidence/matches/main-joint-rotation1884-20261102.json'
SOURCES=[ROOT/'src/runtime/20261102_joint_animation4588_ranked/native_main_02033068.c',
 ROOT/'src/runtime/20261102_joint_animation4588/native_main_02033480.c']


def main():
    config=configuration();assert sha256(config['rom'])==config['romSha256']
    metadata,image,_=measured_module('main');assert metadata['sha256']=='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'
    builder.WORK=WORK;bodies={};rows=[];sources={};helpers=[]
    for path in[*SOURCES,*HELPERS]:
        row,proof,body=builder.build(path,path.stem,True);address=int(row['address'],0);assert len(body)==fixture.SPANS[address]
        row.update(exactBytes=len(body),sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceLanguage='C',genuineLinkComparison=freeze_link(proof))
        (rows if path in SOURCES else helpers).append(row);bodies[address]=body;sources[address]=path
    cases=[];excluded=[];observed=set();pools=set();hardware=helper_returns=0
    for index in range(2048):
        try:fixture.inputs(index)
        except fixture.DegenerateRotation as error:excluded.append(dict(index=index,reason=str(error)));continue
        original=fixture.execute(image,{},index);candidate=fixture.execute(image,bodies,index)
        assert original==candidate and original['modelPassed'],(index,original['context'])
        cases.append(original);observed.update(original['ownObserved']);hardware+=len(original['hardwareOperations'])*2;helper_returns+=len(original['actualHelperReturns'])*2
        for address,size,value in original['reads']:
            if any(base<=address and address+size<=base+length for base,length in fixture.OWN.items()):pools.update(range(address,address+size))
    controls=[]
    for address in fixture.OWN:
        path=sources[address];text=path.read_text(encoding='utf-8');old='a->y * b->z - a->z * b->y';new='a->y * b->z + a->z * b->y'
        changed=text.replace(old,new);assert changed!=text
        label=f'cross-{address:08x}';wrong=ROOT/f'nonmatching/integration/20261102-joint-rotation1884/{label}/source.c';wrong.parent.mkdir(parents=True,exist_ok=True)
        if wrong.exists():assert wrong.read_text(encoding='utf-8')==changed
        else:wrong.write_text(changed,encoding='utf-8')
        row,proof,body=builder.build(wrong,label,False);assert len(body)<=fixture.OWN[address]
        bad={**bodies,address:body};indices=[c['index']for c in cases if c['entry']==address]
        results=[fixture.execute(image,bad,i)for i in indices];rejected=sum(not row['modelPassed']for row in results);assert rejected
        controls.append(dict(label=label,source=wrong.relative_to(ROOT).as_posix(),sourceSha256=sha256(wrong),
         actualWrongReturns=len(results),rejected=rejected,positiveControls=len(results)-rejected))
    try:fixture.execute(image,bodies,0,bound=1)
    except AssertionError:pass
    else:raise AssertionError('Prefix counted as return')
    own={a for a in observed if any(base<=a<base+n for base,n in fixture.OWN.items())}
    missing={hex(base):[hex(a)for a in range(base,base+n,4)if a not in own and a not in{p&~3 for p in pools}]for base,n in fixture.OWN.items()}
    trace=ROOT/'evidence/traces/main-joint-rotation1884-20261102.json.gz'
    trace.write_bytes(gzip.compress(json.dumps(dict(cases=cases),sort_keys=True,separators=(',',':')).encode(),mtime=0))
    write_json(REPORT,dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),romSha256=config['romSha256'],
     processor='arm9',program='',module='main',moduleSha256=metadata['sha256'],matches=rows,matchedFunctions=2,matchedBytes=1884,
     actualCompiledHelperDependencies=helpers,helperSourceCreditInThisReport=0,
     oracle=dict(pairs=len(cases),actualTopReturns=2*len(cases),actualNativeHelperReturns=helper_returns,functionProviders=0,cpu='ARM946',
      ownInstructionBytesObserved=len(own)*4,generatedPoolBytes=len(pools),unobservedCodeAddresses=missing,
      actualModeledHardwareOperations=hardware,completeRegistersFlagsMainInputStackOrderedReadsWritesCompared=True,
      independentCompressedMatrixWeightedInterpolationNormalizationAndCrossModels=True,excludedZeroAxisInputs=excluded),
     negativeControls=controls,replayDependencies=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p))for p in[Path(fixture.__file__),trace]],
     reproductionCommand='python match_main_joint_rotation1884_20261102.py',limitations=[
      'Synthetic32-element encoded rotation dictionaries and128 index entries; bounded frames0..32 and four fractional edges',
      'Degenerate zero interpolated axes are listed and excluded before execution; no zero-vector/division-by-zero result claim',
      'Compiled decoder and normalizer execute; math hardware completes immediately with no timing/interrupt/error-path claim',
      'Per-unit integer ranks and32-bit header layouts measured; no unified portable LP64 header or Android device proof',
      'No data/helper extra source credit, complete asset validation/animation scene, source-only ROM or full native game']))
    print(dict(functions=2,bytes=1884,pairs=len(cases),actualReturns=2*len(cases),nativeHelpers=helper_returns,
     hardwareOperations=hardware,observedBytes=len(own)*4,poolBytes=len(pools),wrongReturns=sum(c['actualWrongReturns']for c in controls),
     wrongRejected=sum(c['rejected']for c in controls),excluded=len(excluded),missing=missing))


if __name__=='__main__':
    main()
