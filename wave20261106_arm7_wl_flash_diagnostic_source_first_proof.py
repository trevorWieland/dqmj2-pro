import gzip
import json
from pathlib import Path
import match_runtime as C
import unicorn
from project import ROOT,read_json,write_json,sha256,configuration
from wave20261106_arm7_wl_flash_diagnostic_source_first_build import SOURCE,LANE,WORK,build_all
from wave20261106_arm7_wl_flash_diagnostic_source_first_models import fixtures
from wave20261106_arm7_wl_flash_diagnostic_source_first_execution import run
from wave20261106_arm7_wl_flash_diagnostic_source_first_controls import execute as controls


def negative_cases():
    all_fixtures=fixtures()
    def choose(entry,**fields):return [f for f in all_fixtures if f['entry']==entry and all(f.get(key)==value for key,value in fields.items())][:1]
    return [
      (0x027ef4cc,'MacHeader.Tx.Status = 0','MacHeader.Tx.Status = 1',choose(0x027ef4cc,signal=1)),
      (0x027ef4cc,'(0x0001 << 15)','(0x0001 << 14)',choose(0x027ef4cc,signal=1)),
      (0x027ef4cc,'(0x0001 << 0)','(0x0001 << 1)',choose(0x027ef4cc,signal=0)),
      (0x027eb3d0,'*p16++ = w16--;','*p16++ = w16++;',choose(0x027eb3d0,fault='none')),
      (0x027eb3d0,'err++ > 32','err++ >= 32',choose(0x027eb3d0,fault='all'),3),
      (0x027eb3d0,'DiagResult |= 0x0002','DiagResult |= 0x0004',choose(0x027eb3d0,fault='first')),
      (0x027f4ecc,'length > (0x200 - 0x002a)','length >= (0x200 - 0x002a)',choose(0x027f4ecc,length=470,allocated=True)),
      (0x027f4ecc,'length < (sizeof(FLASH_TABLE)','length <= (sizeof(FLASH_TABLE)',choose(0x027f4ecc,length=164,allocated=True)),
      (0x027f4ecc,'length += 2','length += 1',choose(0x027f4ecc,length=164,allocated=True)),
      (0x027f4ecc,'+ (12/2) * 2','+ (12/2) * 1',choose(0x027f4ecc,length=164,allocated=True)),
      (0x027f4d38,'(crc << 16)','(crc << 8)',choose(0x027f4d38,length=164,good=True,output=True)),
      (0x027f4d38,'crc != rcrc','crc == rcrc',choose(0x027f4d38,length=164,good=True)),
      (0x027f4e1c,'adrs - 0x002a','adrs - 0x0028',choose(0x027f4e1c,address=42,size=1,null=False)),
      (0x027f4ddc,'statusReg & 0x20','statusReg & 0x10',choose(0x027f4ddc,statuses=[32,0])),
      (0x027f4ddc,'statusReg & 0x01','statusReg & 0x02',choose(0x027f4ddc,statuses=[1,0]))]



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
    if SOURCE!=ROOT/'src/arm7/parallel_wave20261106/wl-flash-diagnostic-next/first' or LANE!=ROOT/'evidence/lanes/parallel-wave20261106/arm7-wl-flash-diagnostic-next/first' or WORK!=ROOT/'work/w6wfd/first':raise ValueError('Exact newly owned PM source/evidence/work scope differs')
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
      'Six complete independently admitted host ARM7-main ARMv4T FLASH/diagnostic callers1080B: MakeImage236,VerifyCheckSum164,Read96,Wait64,DiagMacMemory396,IntrCarrierSuppresionSignal124. All15 original relocations/addends genuinely link under actual C99/sp1p5/O4/inline-on/file-IPA using closed ordinary readable C/headers only, no ASM/executable/prebuilt implementation input/patch/profile sweep.',
      '45 independent original/source caller pairs check complete1684-byte WL state,12-byte allocator-header offset,FLASH/CRC/input/output and exact stack-local32-bit fields, plus all8192 mapped MAC-memory bytes. FLASH cases cover164/470 minimum/maximum and rejected bounds, successful/failed allocation partial state, SPI32-bit lock IDs,2-byte table-length read after local zero, checksum match/mismatch/packing/null output, byte offsets/empty reads, status error-reset precedence and busy polling.',
      'The independent CRC provider contract uses ordinary bitwise reflected0xA001 steps matching the pinned primary nibble-table recurrence; no CRC/SPI/NVRAM/allocator/reset provider body executes and no imported callee/storage credit is taken. Native caller words and every controlled provider argument/data boundary are checked.',
      'The memory diagnostic executes the complete bounded three-pattern8192-byte test in mapped VM memory. Independent expected read/write addresses,widths,values and final bytes are checked under ideal memory, first-word stuck-low-bit and every-word stuck-low-bit contracts; error threshold34 and diagnostic-bit preservation are explicit. New private executor only adds the exact mapped hardware bank, deterministic post-store fault contracts and a bounded500000-instruction diagnostic budget; every old/frozen executor/verifier remains unchanged.',
      'Carrier fixtures check both exact frame halfword updates and all ordered register writes/preserved enable bits. These are synthetic mapped-memory/provider contracts, not physical RAM/SPI/radio/IRQ/timing/device or game claims. Fresh actual C99/strict prototypes/primitive ABI/field geometry/per-origin boundary/binding/genuine wrong-C and source-only canonical copied-root replay are mandatory. Optional652-byte channel setter remains unclaimed/unqualified; all earlier inputs immutable and ordinary shared acceptance alone grants source credit.' ])
    write_json(LANE/'match.json',report);print(dict(functions=len(rows),bytes=report['canonicalMatchedBytes'],pairedCases=len(traces),genuineWrongC=len(negative),boundedInstructionBytes=report['fixtureCoveredOriginalInstructionBytes']),flush=True)


if __name__=='__main__':execute()
