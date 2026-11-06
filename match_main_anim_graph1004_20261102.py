import gzip
import hashlib
import json
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
import match_main_oam_reference296_closed_20261101 as builder
import match_main_release704_20261101 as layouts
from main_anim_init160_fixture_20261102 import execute,ENTRY,CALLBACKS
from link_runtime_unit import measured_module
from save_link_snapshots import freeze_link

WORK=ROOT/'work/main-anim-graph1004-20261102'
REPORT=ROOT/'evidence/matches/main-anim-graph1004-20261102.json'
SPECS={ENTRY:(160,148),0x02033B84:(212,208),0x0203416C:(220,216),0x02034054:(212,208),0x020343FC:(76,72),0x02032324:(124,120)}


def source_path(entry):
    group='20261101_anim_init160'if entry==ENTRY else'20261102_anim_callbacks'
    return ROOT/f'src/runtime/{group}/native_main_{entry:08x}.c'


def main():
    builder.WORK=WORK;layouts.WORK=WORK;WORK.mkdir(parents=True,exist_ok=True)
    config=configuration();assert sha256(config['rom'])==config['romSha256']
    metadata,image,unused=measured_module('main');assert metadata['sha256']=='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'
    matches=[];bodies={};witnesses=[]
    for entry,(size,code_size)in SPECS.items():
        source=source_path(entry);row,proof,body=builder.build(source,f'correct-{entry:08x}',True);assert row['bytes']==size
        row.update(exactBytes=size,sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceLanguage='C',genuineLinkComparison=freeze_link(proof))
        matches.append(row);bodies[entry]=body
        if entry==ENTRY:
            expressions=['sizeof(u32)','sizeof(s32)','sizeof(NNSG3dAnmObj)','sizeof(NNSG3dAnmObjInitFunc)',
             '(u32)&((NNSG3dAnmObj*)0)->priority','(u32)&((NNSG3dAnmObj*)0)->numMapData',
             '(u32)&((NNSG3dAnmObj*)0)->mapData','(u32)&((NNSG3dAnmObjInitFunc*)0)->func',
             '(u32)&((NNSG3dResMdl*)0)->info.numNode','(u32)&((NNSG3dResMdl*)0)->info.numMat']
            witnesses.append(layouts.witness(source,row,expressions,[4,4,28,8,24,25,26,4,23,24],'animation-object-and-table'))
    original=image[ENTRY-0x02000000:ENTRY-0x02000000+160];cases=[];observed=set();body_observed=set();helpers=0
    callback_bodies={a:bodies[a]for a in CALLBACKS}
    for index in range(640):
        native=execute(image,original,index);candidate=execute(image,bodies[ENTRY],index,callback_bodies=callback_bodies)
        assert native==candidate and native['modelPassed'],(index,native['context'])
        observed.update(native['ownedObserved']);body_observed.update(native['bodyObserved']);helpers+=native['actualNativeHelperReturns']*2;cases.append(native)
    own_expected=set(range(ENTRY,ENTRY+148,4));assert observed==own_expected
    trace=ROOT/'evidence/traces/main-anim-graph1004-20261102.json.gz';trace.parent.mkdir(parents=True,exist_ok=True)
    trace.write_bytes(gzip.compress(json.dumps(dict(cases=cases,actualTopReturns=1280),sort_keys=True,separators=(',',':')).encode(),mtime=0))
    controls=[]
    for entry in SPECS:
        text=source_path(entry).read_text(encoding='utf-8')
        old,new=('priority = 127','priority = 126')if entry==ENTRY else('>> 24','>> 23')if entry==0x02032324 else('0x100','0x200')
        wrong=text.replace(old,new);assert wrong!=text
        path=WORK/f'wrong-{entry:08x}.c';path.write_text(wrong,encoding='utf-8')
        row,proof,body=builder.build(path,f'wrong-{entry:08x}',False)
        callbacks=dict(callback_bodies);top=bodies[ENTRY]
        if entry==ENTRY:top=body
        else:callbacks[entry]=body
        results=[execute(image,top,i,callback_bodies=callbacks)for i in range(640)]
        rejected=sum(not r['modelPassed']for r in results);assert rejected>0,hex(entry)
        controls.append(dict(address=hex(entry),actualWrongTopReturns=640,rejected=rejected,positiveControls=640-rejected,
         sourceSha256=sha256(path),objectSha256=row['objectSha256'],resultsSha256=hashlib.sha256(json.dumps(results,sort_keys=True,separators=(',',':')).encode()).hexdigest()))
    try:execute(image,original,0,bound=1)
    except AssertionError:pass
    else:raise AssertionError('Instruction prefix accepted as return')
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),romSha256=config['romSha256'],
     processor='arm9',program='',module='main',moduleSha256=metadata['sha256'],matches=matches,matchedFunctions=6,matchedBytes=1004,
     layoutWitnesses=witnesses,oracle=dict(pairs=640,actualTopReturns=1280,actualNativeHelperReturnsSeparate=helpers,
      providedCalls=0,reconstructedBodiesInstalledTogether=6,initializerInstructionBytesObserved=148,
      independentFirstMatchInitializationAndMapModels=True,fullRegistersFlagsInputMainStackReadsWritesAndCallsCompared=True),
     bodyCoverage=[dict(address=hex(a),sourceCodeBytes=c,observedCodeBytes=sum(a<=pc<a+c for pc in body_observed)*4,
      missing=[hex(pc)for pc in range(a,a+c,4)if pc not in body_observed])for a,(s,c)in SPECS.items()],
     negativeControls=controls,sourceInterface=dict(rawInitializerViewMatchesThreeSelectedCallers=True,
      callbacksUseTypedSharedObjectAndModelLayout=True,dictionaryViewMatchesSelectedRawWordInterface=True),
     replayDependencies=[dict(path=trace.relative_to(ROOT).as_posix(),sha256=sha256(trace))],
     reproductionCommand='python match_main_anim_graph1004_20261102.py',
     limitations=['Original format/function-pointer data receive no source credit; count0/10/null/duplicate entries are explicit synthetic counterfactuals',
      'Bounded dictionaries and maps up to255 slots; unsupported malformed pointers, aliases, concurrent mutation and ordinary game lifecycle',
      'CPU fill and selected dictionary helper execute original code and receive no additional source credit',
      'Full callback instruction coverage and Windows graph execution are separate evidence; no full game or source-only ROM claim'])
    write_json(REPORT,report);print(dict(functions=6,bytes=1004,actualTopReturns=1280,helperReturns=helpers,providedCalls=0,
     wrongActualTopReturns=3840,wrongRejected=sum(r['rejected']for r in controls)))


if __name__=='__main__':
    main()
