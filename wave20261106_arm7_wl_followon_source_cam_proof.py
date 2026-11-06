import gzip
import json
from pathlib import Path
import match_runtime as C
import unicorn
from project import ROOT,read_json,write_json,sha256,configuration
from wave20261106_arm7_wl_followon_source_cam_build import SOURCE,LANE,WORK,build_all
from wave20261106_arm7_wl_followon_source_cam_models import fixtures
from wave20261106_arm7_wl_followon_source_cam_execution import run
from wave20261106_arm7_wl_followon_source_cam_controls import execute as controls


def negative_cases():
    all_fixtures=fixtures()
    def choose(entry,**fields):return [f for f in all_fixtures if f['entry']==entry and all(f.get(key)==value for key,value in fields.items())][:1]
    return [
      (0x027ec280,'pos < pWlMan->Config.MaxStaNum','pos <= pWlMan->Config.MaxStaNum',choose(0x027ec280,label='no-entries')),
      (0x027ec280,'pCAM->lifeTime != 0xFFFF','pCAM->lifeTime != 0xFFFE',choose(0x027ec280,label='infinite-lifetime')),
      (0x027ec280,'--pCAM->lifeTime','pCAM->lifeTime--',choose(0x027ec280,label='unassociated-expire')),
      (0x027ec280,'pCAM->state >= 0x20','pCAM->state > 0x20',choose(0x027ec280,label='class1-expire')),
      (0x027ec280,'pWlMan->CamMan.Count--;','pWlMan->CamMan.Count++;',choose(0x027ec280,label='unassociated-expire')),
      (0x027ec280,'state > 0x20','state >= 0x20',choose(0x027ec280,label='class1-expire')),
      (0x027ebc50,'state < 0x40','state <= 0x40',choose(0x027ebc50,state=64)),
      (0x027ebc50,'->CamMan.NotClass3 |=','->CamMan.NotClass3 ^=',choose(0x027ebc50,state=32,cam=1)),
      (0x027ebc50,'->CamMan.NotClass3 &= ~(1 << camAdrs)','->CamMan.NotClass3 |= (1 << camAdrs)',choose(0x027ebc50,state=64,cam=1)),
      (0x027ebebc,'i = 1, map = 2','i = 0, map = 1',choose(0x027ebebc,bitmap=0)),
      (0x027ebebc,'i < 16','i < 15',choose(0x027ebebc,bitmap=0x7fff)),
      (0x027ebebc,'pCamMan->ConnectSta++;','pCamMan->ConnectSta += 2;',choose(0x027ebebc,bitmap=0,connected=0)),
      (0x027ebb50,'pCAM->frameCount++;','pCAM->frameCount += 2;',choose(0x027ebb50,count=65535)),
      (0x027ebb50,'CamMan.NotSetTIM & (1 << cam_adrs)) == 0','CamMan.NotSetTIM & (1 << cam_adrs)) != 0',choose(0x027ebb50,mode=2,count=1,skip=False)),
      (0x027ebd58,'(pmtMode << camAdrs)','((pmtMode & 1) << camAdrs)',choose(0x027ebd58,cam=0,value=3,mask=0)),
      (0x027ebd58,'& ~pCamMan->NotClass3','& pCamMan->NotClass3',choose(0x027ebd58,cam=0,value=1,mask=65535)),
      (0x027ebd58,'0x0AC) = (0x0001 << 3)','0x0AC) = (0x0001 << 2)',choose(0x027ebd58,cam=0,value=1,mask=0)),
      (0x027ebd58,'0x0AE) = (0x0001 << 3)','0x0AE) = (0x0001 << 2)',choose(0x027ebd58,cam=0,value=1,mask=65535)),
      (0x027ebdb4,'== 0x40','!= 0x40',choose(0x027ebdb4,state=64)),
      (0x027ec438,'->CamMan.Count--;','->CamMan.Count++;',choose(0x027ec438,count=0)),
      (0x027ec438,'].state = 0x00','].state = 0x01',choose(0x027ec438,count=1))]



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
    if SOURCE!=ROOT/'src/arm7/parallel_wave20261106/wl-followon-next/cam' or LANE!=ROOT/'evidence/lanes/parallel-wave20261106/arm7-wl-followon-next/cam' or WORK!=ROOT/'work/w6wlf/cam':raise ValueError('Exact newly owned PM source/evidence/work scope differs')
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
      'Seven complete independently admitted host ARM7-main ARMv4T CAM callers1220B, all26 original relocations/addends genuinely linked. Pinned complete CAM.c source is closed to ordinary readable owned C/headers under actual C99/sp1p5/O4/inline-on/file-IPA. No algorithm ASM, executable/prebuilt implementation inputs, object/relocation/symbol/instruction patches or profile/allocation sweep is used.',
      '125 independent original/source pairs check every byte of1684-byte WL state,16x28-byte station table,64-byte input/output frames and both TX queue halfword words. Cases cover class thresholds/mode/AID/power bits, IRQ-mask word preservation, frame count and connection-count16-bit wrap, first/free/last/no AID choice, post-restore timer-reset masking, sleep-state updates and count underflow.',
      'Timer fixtures cover zero/infinite/decrement/expiry lifetimes, class1/lower classes, parent and child/AP-peer paths, null and nonnull deauth construction, pending-frame retention versus immediate slot release, holes and initial active-count loop bounds. Synthetic provider contracts mutate only declared table/state fields, proving caller order and effects; provider and IRQ/scheduler/radio bodies execute0 and receive0 additional source/storage credit.',
      'The power-mode caller executes its exact native halfword stores to048080ac/048080ae in mapped VM fixture memory, with both selected register/value and unchanged peer word checked. This is instruction-level caller behavior, not physical MMIO/radio/IRQ or game execution. The restored-mask mutation fixture is an explicit provider contract, not a hardware concurrency claim.',
      'Fresh C99/strict required-prototype full body+relocation proofs, compiler-derived complete typed field geometry, actual primitive ABI, boundary/mode/namespace/binding and genuinely-linked wrong-C controls, source-only and canonical copied-root replay are mandatory. Retained helpers only supply measured inlined selected code with0 independent helper credit. Remaining nine admitted follow-on callers3648B stay reserved/uncredited, every prior WL/WM/PM/SOCL pin stays immutable, and accepted source credit awaits shared coordinator gates.' ])
    write_json(LANE/'match.json',report);print(dict(functions=len(rows),bytes=report['canonicalMatchedBytes'],pairedCases=len(traces),genuineWrongC=len(negative),boundedInstructionBytes=report['fixtureCoveredOriginalInstructionBytes']),flush=True)


if __name__=='__main__':execute()
