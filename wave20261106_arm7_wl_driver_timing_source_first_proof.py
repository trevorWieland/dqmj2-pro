import gzip
import json
from pathlib import Path
import match_runtime as C
import unicorn
from project import ROOT,read_json,write_json,sha256,configuration
from wave20261106_arm7_wl_driver_timing_source_first_build import SOURCE,LANE,WORK,build_all
from wave20261106_arm7_wl_driver_timing_source_first_models import fixtures
from wave20261106_arm7_wl_driver_timing_source_first_execution import run
from wave20261106_arm7_wl_driver_timing_source_first_controls import execute as controls


def negative_cases():
    all_fixtures=fixtures()
    def choose(entry,**fields):return [f for f in all_fixtures if f['entry']==entry and all(f.get(key)==value for key,value in fields.items())][:1]
    return [
      (0x027e97bc,'ench & 0x7FFE','ench & 0x7FFF',choose(0x027e97bc,channel=65535)),
      (0x027e97bc,'RxDtims = 1','RxDtims = 2',choose(0x027e97bc,channel=0)),
      (0x027e9d88,'case 2 :','case 1 :',choose(0x027e9d88,rf=2,bbp=0)),
      (0x027e9d88,'bp & 0x7F','bp & 0x3F',choose(0x027e9d88,rf=2,bbp=0x12ff)),
      (0x027eab68,'/ 64 / 1000','/ 64 / 1001',choose(0x027eab68,time=0xffffffff)),
      (0x027eaaf8,'33514000 / 1000','33513000 / 1000',choose(0x027eaaf8,time=1000)),
      (0x027eaaf8,'pFunc, 0','pFunc, (void*)1',choose(0x027eaaf8,time=1)),
      (0x027e9e3c,'lifeTime > 0x00010000','lifeTime >= 0x00010000',choose(0x027e9e3c,life=6553600,beacon=1)),
      (0x027e9e3c,'FrameLifeTimePerBeacon = lifeTimePerBeacon','FrameLifeTimePerBeacon = lifeTimePerBeacon+1',choose(0x027e9e3c,life=5,beacon=100)),
      (0x027e89ec,'DmaMaxCount = 0xFFFFFFFF','DmaMaxCount = 0',choose(0x027e89ec,dma=0)),
      (0x027e89ec,'&pInit->heapType','&pInit->dmaMaxSize',choose(0x027e89ec,crc=0,dma=0)),
      (0x027e89ec,'DiagResult |= 0x0080','DiagResult |= 0x0040',choose(0x027e89ec,crc=1)),
      (0x027e89ec,'pRecvMsgQueue = pInit->sendMsgQueuep','pRecvMsgQueue = pInit->recvMsgQueuep',choose(0x027e89ec,crc=0,dma=0)),
      (0x027e89ec,'pInit->priority','pInit->dmaChannel',choose(0x027e89ec,crc=0,dma=0))]




def wrong_c(case,ordinal,images):
    entry,old,new,selected,*occurrence=case;expectedOccurrences=occurrence[0]if occurrence else 1;tag=format(entry,'08x');name='native_host_arm7_main_'+tag;directory=WORK/'wrong-c'/str(ordinal)/tag
    if not selected:raise ValueError(('Meaningful wrong-C selection empty',name,old))
    directory.mkdir(parents=True,exist_ok=True)
    for path in (SOURCE/tag).iterdir():
        if path.is_file():(directory/path.name).write_bytes(path.read_bytes())
    path=directory/'main.c';text=path.read_text()
    if text.count(old)!=expectedOccurrences:raise ValueError(('Meaningful ordinary C mutation not unique',name,old,text.count(old)))
    path.write_text(text.replace(old,new));rows,outputs=build_all(directory/'build',{name:path},{name},{name});row=rows[0];rejected=[]
    for number,f in enumerate(selected):
        try:
            result=run(row,outputs[name],f,images,number)
            if not result['modelFailures']:raise ValueError(('Wrong C did not alter modeled behavior',name,old))
            rejected.append(dict(actualTopReturn=result['actualTopReturn'],modelFailures=result['modelFailures']))
        except unicorn.UcError as error:rejected.append(dict(actualTopReturn=False,rejectedAtMemoryBoundary=True,error=str(error)))
    return dict(case=ordinal,function=name,old=old,new=new,mutatedOccurrences=expectedOccurrences,genuinelyLinkedWrongC=rows,fixtures=selected,rejected=rejected,abortedRunsAreNotCallerReturns=True)


def execute():
    if SOURCE!=ROOT/'src/arm7/parallel_wave20261106/wl-driver-timing-next/first' or LANE!=ROOT/'evidence/lanes/parallel-wave20261106/arm7-wl-driver-timing-next/first' or WORK!=ROOT/'work/w6wdt/first':raise ValueError('Exact newly owned PM source/evidence/work scope differs')
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
      'Six independently admitted hostARM7-main ARMv4T driver/timing callers1324B:DefaultParameters336,WakeUp180,UsTimeOut132,TimeOut112,FrameLifeTime100,InitDriver464. All71 original relocation origins/types/addends genuinely link under actual C99/sp1p5/O4/inline-on/file-IPA, closed readable C/headers, unchanged canonical namespace/core derivation/per-function split, no algorithm assembler/object edit/opaque implementation input/profile sweep.',
      'Three complete imported primary constant objects116B have exact original ABS32 words/addends, raw-module hashes, source types/counts/extents and fresh compiler geometry;0storage/helper credit. Default-parameter fixtures check every ordered provider argument,6-byte MAC and2-byte channel reads, full constant-interface bytes,masking,default values,three volatile seed reads and preserved surrounding state.',
      'Wakeup fixtures cover RF IDs0,1,2,3,5,65535,exact MMIO reads/writes,BBP masking/full argument words and measured delays. Sole packet-local callback027ea9a8 is independently admitted: original absolute pointer027e9e24,three reachable ARM words,owned void(void*) C declaration,full caller/module hashes and17 substitutions. Only a copied functions map receives that exact qualifier result before unchanged original derivation; no canonical inventory/shared guard change or generic fallback. Its separate diagnostic C/native leaf and genuine typed-pointer ABI prove12-byte zero-word store with0body/source/storage credit; production callers execute0 callback/provider bodies.',
      'Timer fixtures distinguish unsigned32/64 multiplication,shift/division andR0/R1 quotient words,callback/null opaque argument words and exact stack ABI. Three original BL sites bind unchanged compiler intrinsic names_ll_udiv and_u32_div_f to actual ARM7-wram entries03806bf0/03806e44 under exact profiles;33 negatives plus14 fresh typed-C/genuine-link/original-native quotient returns qualify ABI without ARM9 aliases or helper credit. Frame-life fixtures cover specialFFFF,exact65536,greater bound,low16 stores and32-bit multiplication wrap.',
      'Driver fixtures check52-byte WlInit,1684-byte exact clear,global pointer publication,full signed-lockID/dma words,zero/max DMA count,28-byte CAM division,queue direction,FLASH reads,checksum failure/success,original initialization order,typed original ARM7 thread callback and six-word thread-creation register/stack ABI,final diagnostic re-read and all borrowed bytes. External providers are controlled models, not reconstructed/executed bodies; physical hardware,SDK initialization correctness,timing and game claims remain unproven.',
      'Every prior WM/PM/WL/configuration/FLASH/table Ready stays immutable; optional652-byte channel setter remains unclaimed and unqualified. Fresh C99/prototype/field-layout/typed-table/binding/boundary/wrong-C/native/source-only canonical copied-root proofs are required. Historical claim/admission/research TU epochs remain diagnostic; only actual consumed static certificates,owned C/headers,qualified callbacks/helper code and tool/runtime inputs are production dependencies. Shared acceptance alone grants source credit.'
 ])
    write_json(LANE/'match.json',report);print(dict(functions=len(rows),bytes=report['canonicalMatchedBytes'],pairedCases=len(traces),genuineWrongC=len(negative),boundedInstructionBytes=report['fixtureCoveredOriginalInstructionBytes']),flush=True)


if __name__=='__main__':execute()
