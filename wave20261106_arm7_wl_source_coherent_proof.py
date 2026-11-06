import gzip
import json
from pathlib import Path
import match_runtime as C
import unicorn
from project import ROOT,read_json,write_json,sha256,configuration
from wave20261106_arm7_wl_source_coherent_build import SOURCE,LANE,WORK,build_all
from wave20261106_arm7_wl_source_coherent_models import fixtures
from wave20261106_arm7_wl_source_coherent_execution import run
from wave20261106_arm7_wl_source_coherent_controls import execute as controls


def negative_cases():
    all_fixtures=fixtures()
    def choose(entry,**fields):return [f for f in all_fixtures if f['entry']==entry and all(f.get(key)==value for key,value in fields.items())][:2]
    return [
      (0x027f4b88,'> 32','>= 32',choose(0x027f4b88,length=32)),
      (0x027f4b88,'pApList->lifeTime < life1','pApList->lifeTime > life1',choose(0x027f4b88,pattern='oldest',length=3)),
      (0x027f4b88,'pApList->lifeTime = 1024','pApList->lifeTime = 1023',choose(0x027f4b88,pattern='empty',length=3)),
      (0x027f4b88,'LoadLow(&pFrm->MacHeader.Rx.rsv_RSSI)','pFrm->MacHeader.Rx.rsv_RSSI',choose(0x027f4b88,pattern='empty',length=3)),
      (0x027f1888,'statusCode = 19','statusCode = 18',choose(0x027f1888,status=0,aid=0,allocated=True)),
      (0x027f1888,'|= 0xC000','|= 0x8000',choose(0x027f1888,status=0,aid=1,allocated=True)),
      (0x027f1888,'ofst + 2 + 2 + 2','ofst + 2 + 2 + 1',choose(0x027f1888,status=0,aid=1,allocated=True)),
      (0x027f1888,'pReq->header.code = 0xFFFF','pReq->header.code = 0xFFFE',choose(0x027f1888,status=0,aid=1,allocated=True)),
      (0x027f1be8,'ofst + 8 + 2 + 2','ofst + 8 + 2 + 1',choose(0x027f1be8,gameLength=8,align=1,allocated=True)),
      (0x027f1be8,'(0x05 * 0x0010)','(0x04 * 0x0010)',choose(0x027f1be8,gameLength=8,align=1,allocated=True)),
      (0x027f1be8,'pReq->header.code = 0xFFFF','pReq->header.code = 0xFFFE',choose(0x027f1be8,gameLength=8,align=1,allocated=True)),
      (0x027f0484,'pCounter->tx.success++;','pCounter->tx.success += 2;',choose(0x027f0484,frameType=0,failed=False)),
      (0x027f0484,'pCounter->tx.failed++;','pCounter->tx.failed += 2;',choose(0x027f0484,frameType=0,failed=True)),
      (0x027f0484,'pCounter->tx.wep++;','pCounter->tx.wep += 2;',choose(0x027f0484,frameType=0,failed=False)),
      (0x027f0484,'0x2000','0x1000',choose(0x027f0484,frameType=0,failed=False,flag=2,ps=True)),
      (0x027f0484,'.Busy = 0','.Busy = 1',choose(0x027f0484,frameType=0))]



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
    if SOURCE!=ROOT/'src/arm7/parallel_wave20261106/wl-next/coherent' or LANE!=ROOT/'evidence/lanes/parallel-wave20261106/arm7-wl-next/coherent' or WORK!=ROOT/'work/w6wlc/coherent':raise ValueError('Exact newly owned PM source/evidence/work scope differs')
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
      'Four complete host ARM7-main ARMv4T callers/2468 initialized bytes: UpdateApList324, TxqEndManCtrl1228, MakeAssResFrame372 and MakeProbeResFrame544. All77 original relocations/addends retain original symbols and genuinely link. Explicit C99/sp1p5/O4/inline-on/file-IPA reproduces complete native spans; no executable/prebuilt object is an implementation input or patched.',
      'Pinned complete wl_arm7 ApList.c/TxCtrl.c contexts were lexically closed to readable owned C/headers; original out-of-packet helper bodies become external declarations. Two imported static declaration qualifiers were corrected to extern before freezing after strict prototype controls exposed the mismatch; exact body/relocations and fresh genuine links remain unchanged. Retained SetDSParamSet/SetGameInfoElement/TxManCtrlFrame helpers supply only code genuinely inlined into these four functions, with no separate helper credit.',
      '100 independent original/source caller pairs check complete1684-byte WL state,200-byte AP cache and poisoned constructor buffers. Cases cover SSID32/rejection33, last-free/matching/strict-oldest choices, RSSI low-byte extraction, status/AID/error16-bit fields and lengths, optional SSID append, game-info alignment/zero length and an explicit synthetic volatile-timestamp mutation between provider calls. Native byte reads/copies/allocators/builders/state notifications are controlled provider contracts; their bodies execute0 and receive0 credit.',
      'Transmit-completion fixtures cover32-bit counter wrap, retry low byte, unicast/multicast/WEP, power-save/MoreData, auth and assoc/reassoc success, failed-association null deauth allocation, basic disassoc/deauth station transitions, release/free/busy clearing and post-free queue kick. They exclude the nonnull deauth enqueue/inlined transmit path, broadcast disconnect loops, station-mode reset, MLME confirmations and special deauth FrameId paths. Full genuine1228-byte equality proves the complete caller; bounded fixtures do not claim execution of untested paths, physical radio/IRQ/timing or a whole game.',
      'Actual compiler geometry/primitive ABI, positive and35 missing-prototype controls, per-origin boundary and namespace/mode/binding controls, meaningful genuinely-linked wrong-C variants, actual explicit C99/C++ frontend discrimination and source-only canonical copied-root replay are mandatory. All native provider/storage/MMIO boundaries have0 additional source/data credit. The other two admitted WL bodies/900B remain reserved and uncredited; accepted credit awaits shared coordinator gates.'])
    write_json(LANE/'match.json',report);print(dict(functions=len(rows),bytes=report['canonicalMatchedBytes'],pairedCases=len(traces),genuineWrongC=len(negative),boundedInstructionBytes=report['fixtureCoveredOriginalInstructionBytes']),flush=True)


if __name__=='__main__':execute()
