import gzip
import json
from pathlib import Path
from project import ROOT,configuration,write_json,sha256
from link_runtime_unit import measured_module
from save_link_snapshots import freeze_link
import match_main_oam_reference296_closed_20261101 as builder
from main_sound_fader92_fixture_20261102 import execute,SET,GET

WORK=ROOT/'work/main-sound-fader92-qualified-20261102'
FOLDER=ROOT/'src/runtime/20261102_sound_fader92'
REPORT=ROOT/'evidence/matches/main-sound-fader92-20261102.json'


def main():
    config=configuration();assert sha256(config['rom'])==config['romSha256']
    meta,image,_=measured_module('main');assert meta['sha256']=='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'
    builder.WORK=WORK;rows=[];bodies={}
    for path in sorted(FOLDER.glob('*.c')):
        row,proof,body=builder.build(path,path.stem,True)
        address=int(row['address'],0);assert len(body)=={SET:40,GET:52}[address]
        row.update(exactBytes=len(body),sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceLanguage='C',genuineLinkComparison=freeze_link(proof))
        rows.append(row);bodies[address]=body
    assert set(bodies)=={SET,GET}
    cases=[];observed=set();divisions=transitions=0
    for index in range(2048):
        native=execute(image,{},index);candidate=execute(image,bodies,index)
        assert native==candidate and native['modelPassed'],index
        observed.update(native['ownedObserved']);divisions+=native['divisionCallContinuations']*2;transitions+=native['getterCallContinuations']*2
        cases.append(native)
    assert observed==set(range(SET,GET+52,4))
    controls=[];source=FOLDER/'native_main_020379ec.c';text=source.read_text(encoding='utf-8')
    for label,old,new in [('clamp','return fader->target;','return fader->origin;'),('slope','fader->target - fader->origin','fader->target + fader->origin')]:
        changed=text.replace(old,new);assert changed!=text
        path=ROOT/f'nonmatching/integration/20261102-sound-fader92/{label}/source.c';path.parent.mkdir(parents=True,exist_ok=True)
        if path.exists():assert path.read_text(encoding='utf-8')==changed
        else:path.write_text(changed,encoding='utf-8')
        row,proof,body=builder.build(path,label,False);assert len(body)==52
        wrong={**bodies,GET:body};rejected=sum(not execute(image,wrong,index)['modelPassed']for index in range(2048));assert rejected
        controls.append(dict(label=label,source=path.relative_to(ROOT).as_posix(),sourceSha256=sha256(path),actualWrongReturns=2048,rejected=rejected,positiveControls=2048-rejected))
    try:execute(image,bodies,0,bound=1)
    except AssertionError:pass
    else:raise AssertionError('Prefix counted as return')
    trace=ROOT/'evidence/traces/main-sound-fader92-20261102.json.gz'
    trace.write_bytes(gzip.compress(json.dumps(dict(cases=cases),sort_keys=True,separators=(',',':')).encode(),mtime=0))
    write_json(REPORT,dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),romSha256=config['romSha256'],
     processor='arm9',program='',module='main',moduleSha256=meta['sha256'],matches=rows,matchedFunctions=2,matchedBytes=92,
     admission=dict(newFunctions=1,newBytes=52,existingSetterMigrationBytes=40,sourceCreditPendingWholeModuleAcceptance=True),
     oracle=dict(pairs=2048,actualTopReturns=4096,functionProviders=0,cpu='ARM946',ownInstructionBytesObserved=92,
      actualOriginalDivisionCallContinuationsSeparate=divisions,actualGetterCallContinuationsSeparate=transitions,
      allRegistersFlagsMainInputStackOrderedReadsWritesCompared=True,independentSignedTruncationAndSetterModel=True),
     negativeControls=controls,replayDependencies=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p))for p in[trace,ROOT/'main_sound_fader92_fixture_20261102.py']],
     reproductionCommand='python match_main_sound_fader92_20261102.py',limitations=[
      'Reference identifies origin/target/counter/frame sound interpolation; no hardware timestamp or persistent-save meaning',
      'Target-origin and product remain representable signed32; no overflow or divide-by-zero language semantics claim',
      'Negative counters only with positive frame; zero/negative frame tested only on completed/clamped branch',
      'Original signed divide executes; no helper source credit, physical timing, full game or Android claim']))
    print(dict(newBytes=52,migratedBytes=40,pairs=2048,actualReturns=4096,divisionContinuations=divisions,getterContinuations=transitions,wrongReturns=4096,wrongRejected=sum(r['rejected']for r in controls)))


if __name__=='__main__':
    main()
