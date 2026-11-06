import gzip
import json
from pathlib import Path
import match_runtime as C
import unicorn
from project import ROOT,read_json,write_json,sha256,configuration
from wave20261106_arm7_wl_followon_source_tx_build import SOURCE,LANE,WORK,build_all
from wave20261106_arm7_wl_followon_source_tx_models import fixtures
from wave20261106_arm7_wl_followon_source_tx_execution import run
from wave20261106_arm7_wl_followon_source_tx_controls import execute as controls


def negative_cases():
    all_fixtures=fixtures()
    def choose(entry,**fields):return [f for f in all_fixtures if f['entry']==entry and all(f.get(key)==value for key,value in fields.items())][:1]
    return [
      (0x027f0e64,'i < ((LPWL_MAN)','i <= ((LPWL_MAN)',choose(0x027f0e64,multicast=True,maximum=1)),
      (0x027f0e64,'i != 255','i != 254',choose(0x027f0e64,multicast=False,index=255)),
      (0x027f0e64,'->Config.Mode == 1','->Config.Mode != 1',choose(0x027f0e64,multicast=False,mode=1,state=64)),
      (0x027f1f5c,'0xC000 | aid','0x8000 | aid',choose(0x027f1f5c,aid=1)),
      (0x027f1f5c,'28 - 6 - 2','28 - 6 - 1',choose(0x027f1f5c,aid=1)),
      (0x027f1f5c,'rsv_RetryCount = 0','rsv_RetryCount = 1',choose(0x027f1f5c,aid=1)),
      (0x027f1210,'TimeStamp[0] = 0','TimeStamp[0] = 1',choose(0x027f1210,included=True,length=0)),
      (0x027f1210,'(0x08 * 0x0010)','(0x09 * 0x0010)',choose(0x027f1210,included=True,length=0)),
      (0x027f1210,'native_host_arm7_arm_027ead30(pBuf++, 3 );','native_host_arm7_arm_027ead30(pBuf++, 2 );',choose(0x027f1210,included=True,length=0)),
      (0x027f1210,'i < pWork->SSIDLength','i <= pWork->SSIDLength',choose(0x027f1210,included=True,length=32)),
      (0x027f1210,'GameInfo & 1','GameInfo & 0',choose(0x027f1210,included=True,length=1,game=8)),
      (0x027f1210,'bUpdateGameInfo = 0','bUpdateGameInfo = 1',choose(0x027f1210,included=True,length=0)),
      (0x027f1210,'pWork->Ofst.Beacon.TIM + 2','pWork->Ofst.Beacon.TIM + 1',choose(0x027f1210,included=True,length=0)),
      (0x027f1210,'0xB6B8','0xB6B9',choose(0x027f1210,included=True,length=1,game=0,bug=True)),
      (0x027f1210,'0xFFFFFFFC','0xFFFFFFFE',choose(0x027f1210,included=True,length=1,game=0,bug=True)),
      (0x027f1210,'i++, p--','i++, p++',choose(0x027f1210,included=True,length=1,game=8)),
      (0x027f1210,'PowerMgtMode == 1','PowerMgtMode != 1',choose(0x027f1210,included=True,length=0,power=1))]



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
    if SOURCE!=ROOT/'src/arm7/parallel_wave20261106/wl-followon-next/tx' or LANE!=ROOT/'evidence/lanes/parallel-wave20261106/arm7-wl-followon-next/tx' or WORK!=ROOT/'work/w6wlf/tx':raise ValueError('Exact newly owned PM source/evidence/work scope differs')
    if unicorn.__version__!='2.1.4':raise ValueError('Actual native ARMv4T fixture runtime differs')
    inputs=read_json(LANE/'inputs.json')
    for pin in inputs['files']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Frozen actual PM compiler/source/native/runtime input changed: '+pin['path'])
    image=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes()
    if image[0x027f74b0-0x027e0000:0x027f74b6-0x027e0000]!=b'\xff'*6:raise ValueError('Original6-byte borrowed broadcast data witness changed')
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
      'Three complete independently admitted host ARM7-main ARMv4T transmit callers1148B: MakeBeaconFrame884, DeleteTxFrameByAdrs176 and MakePsPollFrame88. All42 original relocations/addends genuinely link under actual C99/sp1p5/O4/inline-on/file-IPA. Implementation compiler inputs are closed ordinary readable C/headers only; no ASM or instruction/object/relocation/symbol patches/profile sweep are used.',
      '33 independent original/source pairs check all1684 bytes of WL state,512-byte frame and64-byte game-info buffers, both the exact original borrowed6-byte broadcast boundary and selected DTIM halfword word. Beacon cases cover included/suppressed and0/1/2/32-byte SSIDs, rate/DS/TIM/vendor fields, explicit lengths/offsets, both active-zone paths, volatile timestamp capture, odd-alignment backward in-place source shift, zero length and aligned optional native marker words.',
      'PS-Poll cases preserve all unwritten header bytes, clear only measured status/retry fields, retain all16 AID bits in DurationID and verify both source MAC pointers/copy order. Delete-by-address cases cover multicast1/2/16 station bounds, a synthetic provider shortening the current loop bound, found/not-found255 station IDs and parent/other modes. The original parent not-found getter call with255 is preserved as measured behavior, not repaired or executed as a callee.',
      'Actual C99 generated leaf probes verify BeaconType as one bit in its16-bit container with15 real returns and full neighboring-field preservation; fresh field-layout negatives reject width changes. The original broadcast import is actual external constu16[3], checked through6/2-byte C type dimensions; the pinned compiler emits an undefined STT_NOTYPE as observed. Function/omitted/wrong extent/wrong element declarations reject; no original array bytes are a compiler implementation input and imported storage credit is0.',
      'All providers/radio/IRQ bodies execute0 in returning caller fixtures. Native halfword MMIO stores run only against mapped fixture memory; timestamp and configuration changes are explicit synthetic provider contracts, not physical concurrency/radio/game claims. Fresh C99/required prototypes/ABI, per-origin native boundaries/bindings, genuinely-linked wrong-C controls and source-only canonical copied-root replay are mandatory. Remaining six admitted follow-on callers2500B stay reserved/uncredited and all earlier frozen inputs remain unchanged; shared acceptance alone grants source credit.' ])
    write_json(LANE/'match.json',report);print(dict(functions=len(rows),bytes=report['canonicalMatchedBytes'],pairedCases=len(traces),genuineWrongC=len(negative),boundedInstructionBytes=report['fixtureCoveredOriginalInstructionBytes']),flush=True)


if __name__=='__main__':execute()
