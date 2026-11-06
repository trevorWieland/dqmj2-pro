import gzip
import json
from pathlib import Path
import match_runtime as C
import unicorn
from project import ROOT,read_json,write_json,sha256,configuration
from wave20261106_arm7_wl_followon_source_receive_build import SOURCE,LANE,WORK,build_all
from wave20261106_arm7_wl_followon_source_receive_models import fixtures
from wave20261106_arm7_wl_followon_source_receive_execution import run
from wave20261106_arm7_wl_followon_source_receive_controls import execute as controls


def negative_cases():
    all_fixtures=fixtures()
    def choose(entry,**fields):return [f for f in all_fixtures if f['entry']==entry and all(f.get(key)==value for key,value in fields.items())][:1]
    return [
      (0x027ec7f8,'header.length - 3','header.length - 2',choose(0x027ec7f8,mode=0)),
      (0x027ec7f8,'ssidLength > 32','ssidLength >= 32',choose(0x027ec7f8,length=32)),
      (0x027ec7f8,'maxChannelTime < 10','maxChannelTime <= 10',choose(0x027ec7f8,mode=2,duration=10)),
      (0x027ec7f8,'bssidMaskCount > 16','bssidMaskCount >= 16',choose(0x027ec7f8,masks=16)),
      (0x027ed634,'resultCode = 0x07','resultCode = 0x06',choose(0x027ed634,arg=0)),
      (0x027ed634,'(0x05 | 0x30)','(0x04 | 0x30)',choose(0x027ed634,arg=0)),
      (0x027edfa0,'pFrm->MacHeader.Rx.rsv_RSSI)','pFrm->MacHeader.Rx.rsv_RSSI >> 8)',choose(0x027edfa0,length=1,align=0,allocated=True)),
      (0x027edfa0,'GameInfoAlign & 1','GameInfoAlign & 0',choose(0x027edfa0,length=3,align=1,allocated=True)),
      (0x027f2778,'->Work.STA != 0x40','->Work.STA == 0x40',choose(0x027f2778,sta=64,match1=True,match2=True)),
      (0x027f2778,'- 24 - 2 - 2','- 24 - 2 - 1',choose(0x027f2778,sta=64,match1=True,match2=True)),
      (0x027f2778,'pInd->ack.txKeySts |=','pInd->ack.txKeySts =',choose(0x027f2778,sta=64,match1=True,match2=True)),
      (0x027f2778,'0x8000) >> 4','0x8000) >> 5',choose(0x027f2778,sta=64,match1=True,match2=True,high=True)),
      (0x027f3148,'if (native_host_arm7_arm_027f2000','if (!native_host_arm7_arm_027f2000',choose(0x027f3148,duplicate=True)),
      (0x027f3148,'matchFlag & 0x0001 ) == 0x0001','matchFlag & 0x0001 ) != 0x0001',choose(0x027f3148,duplicate=False,multicast=True,matched=True,allocated=True)),
      (0x027f35cc,'0x032) = 0x0000','0x032) = 0x0001',choose(0x027f35cc,hardware=True,txmap=0,rxBusy=0)),
      (0x027f35cc,'0x032) = 0x8000','0x032) = 0x4000',choose(0x027f35cc,hardware=True,txmap=0,rxBusy=0)),
      (0x027f35cc,'IcvOkCntFlag = 0','IcvOkCntFlag = 1',choose(0x027f35cc,hardware=True,txmap=0,rxBusy=0)),
      (0x027f35cc,'if (cam_adrs == 0)','if (cam_adrs != 0)',choose(0x027f35cc,cam=0)),
      (0x027f35cc,'native_host_arm7_arm_027ebfec(cam_adrs) > 0x20','native_host_arm7_arm_027ebfec(cam_adrs) >= 0x20',choose(0x027f35cc,mode=1,algo=0,oldState=32)),
      (0x027f35cc,'->Config.AuthAlgo == 1','->Config.AuthAlgo != 1',choose(0x027f35cc,mode=1,algo=0,authConfig=0)),
      (0x027f35cc,'pMLME->pReq.Auth->algorithm == 0','pMLME->pReq.Auth->algorithm == 1',choose(0x027f35cc,mode=2,algo=0,seq=2,requestAlgo=0,peer=True)),
      (0x027f35cc,'seqNum = pAuth->SeqNum + 1','seqNum = pAuth->SeqNum + 2',choose(0x027f35cc,cam=0)),
      (0x027f35cc,'CheckChallengeText(pFrm) == 0','CheckChallengeText(pFrm) != 0',choose(0x027f35cc,mode=1,algo=1,seq=3,length=5,challengeGood=True,challengeState=32,seed=0x1234)),
      (0x027f35cc,'FrameCtrl.Bit.WEP = 1','FrameCtrl.Bit.WEP = 0',choose(0x027f35cc,mode=2,algo=1,seq=2,status=0,allocated=True,requestAlgo=1,peer=True)),
      (0x027f35cc,'pMLME->State = (0x03 | 0x30)','pMLME->State = (0x02 | 0x30)',choose(0x027f35cc,mode=2,algo=1,seq=2,status=0,requestAlgo=1,peer=True))]



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
    if SOURCE!=ROOT/'src/arm7/parallel_wave20261106/wl-followon-next/receive' or LANE!=ROOT/'evidence/lanes/parallel-wave20261106/arm7-wl-followon-next/receive' or WORK!=ROOT/'work/w6wlf/receive':raise ValueError('Exact newly owned PM source/evidence/work scope differs')
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
      'Six complete independently admitted host ARM7-main ARMv4T WL receive/MLME callers2500B: scan320,beacon indication284,auth timeout64,RxAuth1440,RxMpAck212,RxProbeReq180. All64 original relocations/addends genuinely link under actual C99/sp1p5/O4/inline-on/file-IPA with closed ordinary readable C/headers only, no ASM/executable/prebuilt implementation input/patch/allocation sweep.',
      'Three selected original static functions were initially omitted as unused by the standalone compiler. Before freezing, only C-level static declaration/definition qualifiers were removed so their independently admitted original entries export; actual full body/relocation/genuine links remained exact. Historical original linkage/source discovery stays diagnostic0credit.',
      '102 independent original/source pairs check every byte of1684-byte WL state,528-byte RX wrapper/frame,request/confirmation/output/game buffers and local44-byte element checker. Scan preserves early confirmation/remaining-length side effects and covers mode/state/SSID/type/channel/timeout/mask limits; indications cover byte truncation, aligned halfword rounding versus odd-aligned byte copy, allocation failure and direct message boundaries.',
      'MP ACK fixtures preserve header overlays and existing key-status bits, verify station/MAC early exits,16-bit MPDU underflow and both hardware status-bit extractions. Probe fixtures cover duplicate/broadcast/error/BSSID-response gates, exact stack-local typed checker clear/fields/provider match and response allocation/send. Actual compiler bitfield probes verify BcSsidResponse as one bit in its16-bit container with15 real returns.',
      'Auth fixtures cover ordered optional native MMIO reset writes and every busy guard, duplicate/zero station/old-class paths, open/shared-key parent and child sequences, timeout/completion/status/error behavior, null and nonnull response constructors, child WEP/body copy,128-byte challenge generation and0/1/4/5/128-byte verification including odd tail high-byte masking and mismatch. RNG/seed/allocator/IRQ/task/radio bodies execute0; their exact arguments and explicitly declared effects are synthetic caller contracts with0 helper/storage credit.',
      'Native MMIO reads/writes execute only in mapped fixture memory, with exact ordered halfword reset writes checked. No physical radio/IRQ/timing/concurrency/game execution is claimed. Fresh C99/strict prototypes/layout/primitive ABI/per-origin boundary/binding/genuine wrong-C and source-only canonical copied-root replay are mandatory. All16 admitted follow-on bodies now have closed source candidates, but source credit waits for ordinary shared acceptance and every prior READY/input remains immutable.' ])
    write_json(LANE/'match.json',report);print(dict(functions=len(rows),bytes=report['canonicalMatchedBytes'],pairedCases=len(traces),genuineWrongC=len(negative),boundedInstructionBytes=report['fixtureCoveredOriginalInstructionBytes']),flush=True)


if __name__=='__main__':execute()
