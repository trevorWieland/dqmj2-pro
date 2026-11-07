import gzip
import json
from pathlib import Path
import match_runtime as C
import unicorn
from project import ROOT,read_json,write_json,sha256,configuration
from wave20261106_arm7_wl_configuration_source_maintenance_build import SOURCE,LANE,WORK,build_all
from wave20261106_arm7_wl_configuration_source_maintenance_models import fixtures
from wave20261106_arm7_wl_configuration_source_maintenance_execution import run
from wave20261106_arm7_wl_configuration_source_maintenance_controls import execute as controls


def negative_cases():
    all_fixtures=fixtures()
    def choose(entry,**fields):return [f for f in all_fixtures if f['entry']==entry and all(f.get(key)==value for key,value in fields.items())][:1]
    return [
      (0x027e93ac,'mainAntenna > 1','mainAntenna >= 1',choose(0x027e93ac,main=1)),
      (0x027e93ac,'Config.UseAntenna ^','Config.UseAntenna |',choose(0x027e93ac,main=1,use=1)),
      (0x027e9414,'useAntenna > 1','useAntenna >= 1',choose(0x027e9414,diversity=0,use=1,mode=1)),
      (0x027e9414,'->Config.Mode != 1','->Config.Mode == 1',choose(0x027e9414,diversity=1,use=0,mode=1)),
      (0x027e9414,'->Config.UseAntenna = 0','->Config.UseAntenna = 1',choose(0x027e9414,diversity=1,use=0,mode=1)),
      (0x027eaf7c,'pWork->TxBufResCount++;','pWork->TxBufResCount += 2;',choose(0x027eaf7c,mode=2,mask=31,busy=0)),
      (0x027eaf7c,'if (pTxCtrl->Txq[2].Busy)','if (!pTxCtrl->Txq[2].Busy)',choose(0x027eaf7c,mode=2,mask=31,busy=0)),
      (0x027eaf7c,'native_host_arm7_arm_027eaf30(&pTxCtrl->Txq[1]);','native_host_arm7_arm_027eaf30(&pTxCtrl->Txq[0]);',choose(0x027eaf7c,mode=1,mask=8)),
      (0x027eaf7c,'0x004) = 1','0x004) = 2',choose(0x027eaf7c,mode=3,command=0)),
      (0x027eb13c,'DiagResult |= 0x8000','DiagResult |= 0x4000',choose(0x027eb13c,state=0)),
      (0x027eb13c,'->Work.STA != 0x00','->Work.STA == 0x00',choose(0x027eb13c,state=0,mlme=0)),
      (0x027eb13c,'->MLME.State = 0x00','->MLME.State = 0x01',choose(0x027eb13c,state=64,mlme=0x35,race=False)),
      (0x027eb13c,'resultCode = 0x06','resultCode = 0x05',choose(0x027eb13c,state=64,mlme=0x35,race=False)),
      (0x027eb13c,'native_host_arm7_arm_037f8650(3 )','native_host_arm7_arm_037f8650(2 )',choose(0x027eb13c,state=0,mlme=0)),
      (0x027eb13c,'native_host_arm7_arm_037f8598(3 , 23 )','native_host_arm7_arm_037f8598(3 , 22 )',choose(0x027eb13c,state=0,mlme=0)),
      (0x027eb13c,'!= 0xFFFF','== 0xFFFF',choose(0x027eb13c,state=0,mlme=0))]



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
    if SOURCE!=ROOT/'src/arm7/parallel_wave20261106/wl-configuration-next/maintenance' or LANE!=ROOT/'evidence/lanes/parallel-wave20261106/arm7-wl-configuration-next/maintenance' or WORK!=ROOT/'work/w6wlg/maintenance':raise ValueError('Exact newly owned PM source/evidence/work scope differs')
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
      'Four complete independently admitted host ARM7-main ARMv4T maintenance callers728B: WSetMainAntenna104,WSetDiversity212,WCheckTxBuf252,TerminateWlTask160. All18 original relocations/addends genuinely link under actual C99/sp1p5/O4/inline-on/file-IPA using closed ordinary readable C/headers, no ASM/executable/prebuilt implementation inputs/patch/allocation sweep.',
      '52 independent original/source pairs check every byte of1684-byte WL state and complete request/confirmation/frame buffers plus exact ordered MMIO sequences. Antenna cases cover valid0/1 versus invalid2/0xffff0001 full32-bit boundaries, mode refusal, both selectors, XOR output and preservation of adjacent packed bits. Three actual C99 set/get leaf probes in both source contexts contribute90 real ABI returns with16-bit store-width/one-bit/full-neighbor preservation.',
      'Queue recovery covers parent/child/hotspot/unknown modes, every queue check/restore boundary, busy-dependent stop, AID argument,16-bit recovery counter wrap and idle command register write. Shutdown covers already-stopped/active state, partial confirmation before shutdown, post-stop MLME reload, complete bounded delete-task sequences and final release-task identity.',
      'Provider,wait/IRQ/task/radio/previous frame-builder bodies execute0 and receive0 extra source/storage credit. Native halfword MMIO executes only against mapped fixture memory; provider state changes are explicit synthetic caller contracts and no physical radio/scheduler/IRQ/concurrency/game execution is claimed.',
      'Fresh actual C99/strict prototypes/primitive ABI/per-source bitfield geometry/per-origin boundaries/bindings/genuinely-linked wrong-C and source-only canonical copied-root replay are mandatory. Every previous frozen source/helper/input remains unchanged. All13 admitted configuration callers2032B have closed source candidates, but source credit requires ordinary shared acceptance.' ])
    write_json(LANE/'match.json',report);print(dict(functions=len(rows),bytes=report['canonicalMatchedBytes'],pairedCases=len(traces),genuineWrongC=len(negative),boundedInstructionBytes=report['fixtureCoveredOriginalInstructionBytes']),flush=True)


if __name__=='__main__':execute()
