import gzip
import json
from pathlib import Path
import match_runtime as C
import unicorn
from project import ROOT,read_json,write_json,sha256,configuration
from wave20261106_arm7_wl_table_diagnostic_source_first_build import SOURCE,LANE,WORK,build_all
from wave20261106_arm7_wl_table_diagnostic_source_first_models import fixtures
from wave20261106_arm7_wl_table_diagnostic_source_first_execution import run
from wave20261106_arm7_wl_table_diagnostic_source_first_controls import execute as controls


def negative_cases():
    all_fixtures=fixtures()
    def choose(entry,**fields):return [f for f in all_fixtures if f['entry']==entry and all(f.get(key)==value for key,value in fields.items())][:1]
    return [
      (0x027eb55c,'->Rf.Id == 5','->Rf.Id == 2',choose(0x027eb55c,rf=5,faultPhase=None)),
      (0x027eb55c,') == -1',') == 0x0ff',choose(0x027eb55c,rf=2,writeFailure=0)),
      (0x027eb55c,'err++ > 32','err++ >= 32',choose(0x027eb55c,rf=2,faultPhase=0),5),
      (0x027eb22c,'*pReg = 0;','*pReg = 1;',choose(0x027eb22c,registerFault='none')),
      (0x027eb22c,'DiagResult |= 0x0001','DiagResult |= 0x0002',choose(0x027eb22c,registerFault='all')),
      (0x027ea7cc,'sizeof(native_host_arm7_data_027f72ec) / 2','sizeof(native_host_arm7_data_027f72ec) / 4',choose(0x027ea7cc,rf=2,bits=24,count=0)),
      (0x027ea7cc,'(5 << 16)','(4 << 16)',choose(0x027ea7cc,rf=3,bits=8,count=1)),
      (0x027ea7cc,'~(0x1F << 10)','~(0x0F << 10)',choose(0x027ea7cc,rf=2,bits=24,count=3)),
      (0x027eadf4,'total >> 4','total >> 3',choose(0x027eadf4,data=255,total=65535),2),
      (0x027eadf4,'data & 0xf','data & 0x7',choose(0x027eadf4,data=15,total=0)),
      (0x027ea764,'i < 105','i < 104',choose(0x027ea764,seed=0)),
      (0x027ea764,'(90, 2)','(91, 2)',choose(0x027ea764,seed=1))]




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
    if SOURCE!=ROOT/'src/arm7/parallel_wave20261106/wl-table-diagnostic-next/first' or LANE!=ROOT/'evidence/lanes/parallel-wave20261106/arm7-wl-table-diagnostic-next/first' or WORK!=ROOT/'work/w6wtd/first':raise ValueError('Exact newly owned PM source/evidence/work scope differs')
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
      'Five complete independently admitted host ARM7-main ARMv4T callers1780B: DiagBaseBand736,DiagMacRegister420,InitRF392,calc_NextCRC128,InitBaseBand104. All25 original relocations/addends genuinely link with actual C99/sp1p5/O4/inline-on/file-IPA and the unchanged splitter; no assembler, object edits, binary implementation inputs or profile sweep.',
      'Six imported primary constant tables284B are bounded by original ABS32 caller origins/words/addends, exact raw-module hashes, actual closed typed extern arrays and fresh compiler sizeof/field probes; storage and provider credit remain0. Their native words remain imported reference data. Every actual modeled table read is bounded and recorded; source/native instruction, complete state and exact borrowed bytes agree.',
      'BBP diagnostics cover both measured ID-selected skip tables, ordered sentinel traversal, initial-write failure endpoints, a later ignored write-error return, every pattern phase and error34 threshold, walking bits and preserved diagnostic status. BBP provider bodies do not execute. MAC diagnostics cover every typed register/mask under ideal memory, first-register bit-inversion and all-register bit-inversion contracts, checking exact ordered MMIO writes/read addresses,widths,values and final borrowed state. No physical radio/hardware/timing claim.',
      'CRC fixtures use independent bitwise reflected0xA001 steps, every low nibble and varied high-bit/total patterns. Baseband/RF initialization covers exact EEPROM offsets,widths,partial stack/field writes,16 MAC registers,RF register bit packing,IDs2/3/5,zero/multiple init entries,MM3156 command ordinals,backup-field masking and preserved neighboring bytes. Imports are modeled boundaries with0 extra body/storage credit.',
      'InitRF requires the readable original RF_Write C body as full-TU/file-IPA context; ordinary per-function splitting discards that helper implementation and its WaitLoop dependency, retains original selected-caller relocations and supplies only genuine zero-code original ARM binding anchors. The extern-only400-byte and restored-table-value400-byte nonmatches are preserved as diagnostics; the context-qualified392-byte caller is fully genuine-linked and independently modeled.',
      'Fresh strict prototype/actualC99 frontend/primitive ABI/field geometry/typed table/boundary/binding/genuine wrong-C and source-only canonical copied-root proofs are required. Optional652-byte channel setter remains unclaimed/unqualified. All prior inputs remain immutable; only shared acceptance grants source credit.'
 ])
    write_json(LANE/'match.json',report);print(dict(functions=len(rows),bytes=report['canonicalMatchedBytes'],pairedCases=len(traces),genuineWrongC=len(negative),boundedInstructionBytes=report['fixtureCoveredOriginalInstructionBytes']),flush=True)


if __name__=='__main__':execute()
