import gzip
import json
from pathlib import Path
import match_runtime as C
import unicorn
from project import ROOT,read_json,write_json,sha256,configuration
from wave20261106_arm7_wl_source_requests_build import SOURCE,LANE,WORK,build_all
from wave20261106_arm7_wl_source_requests_models import fixtures
from wave20261106_arm7_wl_source_requests_execution import run
from wave20261106_arm7_wl_source_requests_controls import execute as controls


def negative_cases():
    all_fixtures=fixtures()
    def choose(entry,**fields):return [f for f in all_fixtures if f['entry']==entry and all(f.get(key)==value for key,value in fields.items())][:1]
    return [
      (0x027ec938,'pConfig->Mode != 2','pConfig->Mode != 1',choose(0x027ec938,mode=2)),
      (0x027ec938,'pWork->STA < 0x20','pWork->STA <= 0x20',choose(0x027ec938,sta=32)),
      (0x027ec938,'ssidLength > 32','ssidLength >= 32',choose(0x027ec938,ssid=32)),
      (0x027ec938,'beaconPeriod < 10','beaconPeriod <= 10',choose(0x027ec938,beacon=10,mode=2,sta=0x40)),
      (0x027ec938,'beaconPeriod > 1000','beaconPeriod >= 1000',choose(0x027ec938,beacon=1000)),
      (0x027ec938,'dtimPeriod > 255','dtimPeriod >= 255',choose(0x027ec938,dtim=255)),
      (0x027ec938,'channel & 0xFFF0','channel & 0xFFE0',choose(0x027ec938,channel=16)),
      (0x027ec938,'timeOut > 2000','timeOut >= 2000',choose(0x027ec938,timeout=2000)),
      (0x027ec938,'native_host_arm7_arm_037f9238(0x20','native_host_arm7_arm_037f9238(0x10',choose(0x027ec938,ssid=0)),
      (0x027ec938,'pMLME->State = (0x00 | 0x20)','pMLME->State = (0x01 | 0x20)',choose(0x027ec938,mode=3)),
      (0x027ec938,'return 0x80','return 0x81',choose(0x027ec938,mode=3)),
      (0x027ef5f8,'length > 1508','length > 1507',choose(0x027ef5f8,mode=2,length=1508)),
      (0x027ef5f8,'!= 0x40','!= 0x30',choose(0x027ef5f8,mode=1,length=1508,cam=3,sta=0x40)),
      (0x027ef5f8,'LoadLow(&pFrm->MacHeader.Tx.rsv_AppRate)','pFrm->MacHeader.Tx.rsv_AppRate',choose(0x027ef5f8,mode=2,length=1508,appRate=0xab00)),
      (0x027ef5f8,'pFrm->MacHeader.Tx.rsv_AppRate = 0','pFrm->MacHeader.Tx.rsv_AppRate = 1',choose(0x027ef5f8,mode=2,length=1508,appRate=0xab05)),
      (0x027ef5f8,'+ 4 + 4 + 4','+ 4 + 4 + 3',choose(0x027ef5f8,mode=2,length=1508)),
      (0x027ef5f8,'pWork->FrameCtrl | 0x0040','pWork->FrameCtrl | 0x0080',choose(0x027ef5f8,mode=2,length=0)),
      (0x027ef5f8,'->CamMan.PowerMgtMode & ~','->CamMan.PowerMgtMode & ',choose(0x027ef5f8,mode=1,cam=0,power=3,notClass3=3)),
      (0x027ef5f8,'return 0x81','return 0x80',choose(0x027ef5f8,mode=2,length=1508))]



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
    if SOURCE!=ROOT/'src/arm7/parallel_wave20261106/wl-next/requests' or LANE!=ROOT/'evidence/lanes/parallel-wave20261106/arm7-wl-next/requests' or WORK!=ROOT/'work/w6wlc/requests':raise ValueError('Exact newly owned PM source/evidence/work scope differs')
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
      'Two complete admitted host ARM7-main ARMv4T WL request callers900B: MLME_JoinReqCmd440 and MA_DataReqCmd460. All26 original relocations/addends genuinely link under explicit C99/sp1p5/O4/inline-on/file-IPA; complete readable owned C/headers are the only implementation compiler inputs, with no algorithm ASM or binary/object/relocation/name patches.',
      '78 independent original/source caller pairs check complete1684-byte WL state,256-byte request and64-byte confirmation regions. Join cases cover confirmation length before early returns, mode/state/order, deliberate state change before invalid request returns, SSID/beacon/DTIM/channel/basic/support rate/timeout limits, channel/flash failures, preamble choices, provider arguments and MLME pointers/state before task posting.',
      'Data-request cases cover1508/1509 length boundary, parent search/class rejection, child/hotspot/other modes, low-byte application-rate test but full16-bit explicit rate copy,32-to16-bit interval truncation, null/WEP/plain MPDU calculations, all address-copy orders, broadcast power-mask queue gating and directed enqueue/provider arguments. Synthetic providers execute0 bodies and receive0 additional source/storage credit; queue/physical-radio/IRQ execution and asynchronous task completion are not claimed.',
      'Fresh actual compiler field layout, positive and20 missing-prototype controls, promoted-byte/16/32-bit ABI probes, per-origin original boundary/binding negatives, genuinely-linked wrong-C variants, actual explicit C99/C++ frontend proof and source-only plus canonical copied-root replay are mandatory. Historical admission/research/source materials are diagnostic0credit rather than runtime inputs. All four previously frozen WL2468B files and all older packets remain unchanged. Accepted source credit awaits shared coordinator gates.' ])
    write_json(LANE/'match.json',report);print(dict(functions=len(rows),bytes=report['canonicalMatchedBytes'],pairedCases=len(traces),genuineWrongC=len(negative),boundedInstructionBytes=report['fixtureCoveredOriginalInstructionBytes']),flush=True)


if __name__=='__main__':execute()
