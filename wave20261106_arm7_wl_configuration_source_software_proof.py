import gzip
import json
from pathlib import Path
import match_runtime as C
import unicorn
from project import ROOT,read_json,write_json,sha256,configuration
from wave20261106_arm7_wl_configuration_source_software_build import SOURCE,LANE,WORK,build_all
from wave20261106_arm7_wl_configuration_source_software_models import fixtures
from wave20261106_arm7_wl_configuration_source_software_execution import run
from wave20261106_arm7_wl_configuration_source_software_controls import execute as controls


def negative_cases():
    all_fixtures=fixtures()
    def choose(entry,**fields):return [f for f in all_fixtures if f['entry']==entry and all(f.get(key)==value for key,value in fields.items())][:1]
    return [
      (0x027e8da8,'pHeapBufMan->Count != 0','pHeapBufMan->Count == 0',choose(0x027e8da8,count=0,nodes=2)),
      (0x027e8da8,'pNext = (u32 *)GetHeapBufNextAdrs(pBuf);','pNext = (u32 *)0xffffffff;',choose(0x027e8da8,count=3,nodes=3)),
      (0x027e8de8,'->Work.GameInfoAdrs = pGameInfo','->Work.GameInfoAdrs = (void *)0',choose(0x027e8de8,number=16)),
      (0x027e8de8,'sizeof(CONFIG_PARAM)','sizeof(CONFIG_PARAM)-2',choose(0x027e8de8,number=16)),
      (0x027e8f3c,'mode > 3','mode >= 3',choose(0x027e8f3c,mode=3)),
      (0x027e8f3c,'(0x01UL << 3)','(0x01UL << 2)',choose(0x027e8f3c,mode=1)),
      (0x027e95dc,'i < 32','i < 31',choose(0x027e95dc,length=1,state=32,mode=1)),
      (0x027e95dc,'SSIDLength != length','SSIDLength == length',choose(0x027e95dc,length=1,state=64,mode=1,previous=1)),
      (0x027e95dc,'+ 12 + 24 + 2','+ 12 + 24 + 1',choose(0x027e95dc,length=1,state=64,mode=1,previous=1,offset=12)),
      (0x027e96ec,'period < 10','period <= 10',choose(0x027e96ec,period=10)),
      (0x027e96ec,'0x08C) = period','0x08C) = period+1',choose(0x027e96ec,period=10)),
      (0x027e9f60,'length > 128','length >= 128',choose(0x027e9f60,length=128,align=0)),
      (0x027e9f60,'length > 128','(u16)length > 128',choose(0x027e9f60,length=0xffff0080,align=0)),
      (0x027e9f60,'native_host_arm7_arm_027ead30(p, 0xFF);','native_host_arm7_arm_027ead30(p, 0xFE);',choose(0x027e9f60,length=1,align=1)),
      (0x027e9f60,'GameInfoAlign & 1','GameInfoAlign & 2',choose(0x027e9f60,length=1,align=1)),
      (0x027ea048,'pWork->AID = 0','pWork->AID = 1',choose(0x027ea048,cam=1)),
      (0x027ea048,'pWork->APCamAdrs = 0','pWork->APCamAdrs = 1',choose(0x027ea048,cam=1)),
      (0x027ec690,'pMsg, 0 )','pMsg, 1 )',choose(0x027ec690,nodes=1,successes=0)),
      (0x027ec690,'(u32)pMsg != (u32)(-1)','(u32)pMsg == (u32)(-1)',choose(0x027ec690,nodes=1,successes=1)),
      (0x027ee438,'pReq->tableNumber >=','pReq->tableNumber >',choose(0x027ee438,number=16,frameLife=0)),
      (0x027ee438,'frameLifeTime > 63','frameLifeTime >= 63',choose(0x027ee438,number=1,frameLife=63)),
      (0x027ee438,'pReq->frameLifeTime != 0)','pReq->frameLifeTime == 0)',choose(0x027ee438,number=0,frameLife=0)),
      (0x027ee438,'pCAM[i].lifeTime != 0','pCAM[i].lifeTime == 0',choose(0x027ee438,number=65535,frameLife=0))]



def wrong_c(case,ordinal,images):
    entry,old,new,selected=case;tag=format(entry,'08x');name='native_host_arm7_main_'+tag;directory=WORK/'wrong-c'/str(ordinal)/tag
    if not selected:raise ValueError(('Meaningful wrong-C selection empty',name,old))
    directory.mkdir(parents=True,exist_ok=True)
    for path in (SOURCE/tag).iterdir():
        if path.is_file():(directory/path.name).write_bytes(path.read_bytes())
    path=directory/'main.c';text=path.read_text()
    if text.count(old)!=1:raise ValueError(('Meaningful ordinary C mutation not unique',name,old,text.count(old)))
    path.write_text(text.replace(old,new));rows,outputs=build_all(directory/'build',{name:path},{name},{name});row=rows[0];rejected=[]
    for number,f in enumerate(selected):
        try:
            result=run(row,outputs[name],f,images,number)
            if not result['modelFailures']:raise ValueError(('Wrong C did not alter modeled behavior',name,old))
            rejected.append(dict(actualTopReturn=result['actualTopReturn'],modelFailures=result['modelFailures']))
        except unicorn.UcError as error:rejected.append(dict(actualTopReturn=False,rejectedAtMemoryBoundary=True,error=str(error)))
    return dict(case=ordinal,function=name,old=old,new=new,genuinelyLinkedWrongC=rows,fixtures=selected,rejected=rejected,abortedRunsAreNotCallerReturns=True)


def execute():
    if SOURCE!=ROOT/'src/arm7/parallel_wave20261106/wl-configuration-next/software' or LANE!=ROOT/'evidence/lanes/parallel-wave20261106/arm7-wl-configuration-next/software' or WORK!=ROOT/'work/w6wlg/software':raise ValueError('Exact newly owned PM source/evidence/work scope differs')
    if unicorn.__version__!='2.1.4':raise ValueError('Actual native ARMv4T fixture runtime differs')
    inputs=read_json(LANE/'inputs.json')
    for pin in inputs['files']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Frozen actual PM compiler/source/native/runtime input changed: '+pin['path'])
    rows,outputs=build_all(WORK/'proof-positive');by={int(r['address'],0):r for r in rows};images=[(int(m['base'],0),(ROOT/m['binary']).read_bytes())for m in read_json(ROOT/'evidence/arm7/runtime-layout.json')['modules']];traces=[];coverage={r['address']:set()for r in rows}
    for number,f in enumerate(fixtures()):
        row=by[f['entry']];image=(ROOT/row['binary']).read_bytes();native=image[f['entry']-row['base']:f['entry']-row['base']+row['bytes']];original=run(row,native,f,images,number);rebuilt=run(row,outputs[row['name']],f,images,number)
        if original!=rebuilt or original['modelFailures']or not original['actualTopReturn']:
            write_json(WORK/'fixture-failure.json',dict(ordinal=number,fixture=f,original=original,rebuilt=rebuilt));raise ValueError('Independent complete PM caller/model mismatch')
        coverage[row['address']].update(pc for pc in original['pcs']if f['entry']<=pc<f['entry']+row['bytes']);traces.append(dict(ordinal=number,fixture=f,result=original))
    print(dict(positiveNativeSourcePairs=len(traces),functions=len(rows),bytes=sum(r['bytes']for r in rows)),flush=True)
    negative=[wrong_c(case,number,images)for number,case in enumerate(negative_cases())];controlled=controls(rows);write_json(LANE/'controls.json',controlled);raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode();artifact=LANE/'traces.json.gz';artifact.write_bytes(gzip.compress(raw,mtime=0));symbols={}
    for row in rows:
        for name,binding in row['nativeSymbolEntries'].items():
            if name in symbols and symbols[name]!=binding:raise ValueError('Conflicting complete report-level ARM7 PM symbols')
            symbols[name]=binding
    covered=[dict(address=address,originalInstructionBytes=4*len(pcs),completeNativeSpanBytes=by[int(address,0)]['bytes'])for address,pcs in coverage.items()]
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],program='',processor='arm7',module='arm7-main',allPassed=True,matches=rows,canonicalMatchedFunctions=len(rows),canonicalMatchedBytes=sum(r['bytes']for r in rows),cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecutedInCallerFixtures=0,nativeSymbols={n:b['address']for n,b in symbols.items()},nativeSymbolModules={n:b['module']for n,b in symbols.items()},nativeSymbolEntries=symbols,nativeSymbolBindings=symbols,calleeSourceCredit=0,externalStorageCredit=0,fixtureInstructionCoverage=covered,fixtureCoveredOriginalInstructionBytes=sum(r['originalInstructionBytes']for r in covered),negativeEvidence=negative,controls=dict(path=(LANE/'controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'controls.json')),inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=C.sha(raw)),producer=Path(__file__).name,producerSha256=sha256(__file__),limits=[
      'Nine complete independently admitted host ARM7-main ARMv4T configuration/heap/message callers1304B. All21 original relocations/addends genuinely link under actual C99/sp1p5/O4/inline-on/file-IPA using closed ordinary readable owned C/headers, no ASM/executable/prebuilt implementation inputs/patch/allocation sweep.',
      '100 independent original/source caller pairs check complete1684-byte WL state,16x28-byte CAM table,request/confirmation/input/game/beacon/heap-node buffers and exact scalar MMIO write sequences. Cases prove initialized configuration40/work192 clear boundaries and pre-clear game-pointer preservation,32-to16-bit station-count truncation, valid/invalid modes and preservation of unrelated flag/register bits.',
      'SSID cases cover0/1/31/32/33, parent/class3 length refusal, explicit tail clearing and bounded existing beacon patch. Game-info cases distinguish full32-bit rejected lengths,0/1/2/3/128, odd byte copies/padding from aligned halfword rounding and delayed metadata stores. Lifetime requests preserve early confirmation writes,0/broadcast/single/out-of-range station behavior, zero versus active lifetimes and optional63/65535 frame-lifetime provider calls.',
      'Heap fixtures deliberately clobber each released node next pointer through the provider after its caller-side snapshot, and message fixtures update/reload queue head after deletion, check nonblocking flags and early failed sends. A synthetic delete-provider changes AP station index to prove subsequent source reload. Providers including wait/IRQ/queue/lifetime bodies execute0 and receive0 additional source/storage credit.',
      'Exact native halfword MMIO sequences execute only against fixture memory; no physical radio/timer/IRQ/concurrency/game claim. Fresh actual C99/strict prototypes/primitive ABI/field geometry/per-origin boundaries/bindings/genuinely-linked wrong-C and source-only canonical copied-root replay are mandatory. Remaining four admitted maintenance callers728B stay reserved/uncredited, all earlier inputs immutable, and shared acceptance alone grants source credit.' ])
    write_json(LANE/'match.json',report);print(dict(functions=len(rows),bytes=report['canonicalMatchedBytes'],pairedCases=len(traces),genuineWrongC=len(negative),boundedInstructionBytes=report['fixtureCoveredOriginalInstructionBytes']),flush=True)


if __name__=='__main__':execute()
