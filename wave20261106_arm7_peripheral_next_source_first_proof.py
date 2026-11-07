import gzip
import json
from pathlib import Path
import match_runtime as C
import unicorn
from project import ROOT,read_json,write_json,sha256,configuration
from wave20261106_arm7_peripheral_next_source_first_build import SOURCE,LANE,WORK,build_all
from wave20261106_arm7_peripheral_next_source_first_models import fixtures
from wave20261106_arm7_peripheral_next_source_first_execution import run
from wave20261106_arm7_peripheral_next_source_first_controls import execute as controls


def negative_cases():
    all_fixtures=fixtures()
    def choose(entry,**fields):return [f for f in all_fixtures if f['entry']==entry and all(f.get(key)==value for key,value in fields.items())][:1]
    return [
      (0x027f5188,'if (!native_host_arm7_arm_03803b0c','if (native_host_arm7_arm_03803b0c',choose(0x027f5188,process=32,available=1)),
      (0x027f5188,'case 0x0020','case 0x0030',choose(0x027f5188,process=32,available=1)),
      (0x027f5188,'native_host_arm7_arm_027f580c(entry->arg[0], entry->arg[1]','native_host_arm7_arm_027f580c(entry->arg[0], entry->arg[0]',choose(0x027f5188,process=37,valid=1)),
      (0x027f6538,'intr_num |= 1','intr_num |= 2',choose(0x027f6538,status1=16,status2=85)),
      (0x027f6538,'stat2.intr_mode = 0x0','stat2.intr_mode = 0x1',choose(0x027f6538,status1=16,status2=85)),
      (0x027f65c8,'>= 0xA','> 0xA',choose(0x027f65c8,bcd=0x1111111a)),
      (0x027f65c8,'w *= 10','w *= 8',choose(0x027f65c8,bcd=0x12345678)),
      (0x027f667c,'format %= 2','format %= 4',choose(0x027f667c,format=3,status=0)),
      (0x027f667c,'0x50','0x40',choose(0x027f667c,format=1,status=0),2),
      (0x0380433c,'SPI_TP_VALIDITY_INVALID_XY','SPI_TP_VALIDITY_INVALID_X',choose(0x0380433c,argument=0,queued=0)),
      (0x0380433c,'& 0xFF','& 0x7F',choose(0x0380433c,argument=0xffffffff,queued=0)),
      (0x038044bc,'*density = maxRange','*density = 0',choose(0x038044bc,samples=[0,4095,2048,1024,3072],range=7,axis=0,busy=0)),
      (0x038044bc,'<= range','< range',choose(0x038044bc,samples=[1000]*5,range=0,axis=0,busy=0)),
      (0x038044bc,'(temp[i] << 1)','temp[i]',choose(0x038044bc,samples=[100,101,102,4000,4095],range=2,axis=0,busy=0)),
      (0x038044bc,'~0x7','~0x3',choose(0x038044bc,samples=[100,101,102,4000,4095],range=2,axis=0,busy=0),2),
      (0x038044bc,'0xD1','0x91',choose(0x038044bc,samples=[1000]*5,range=0,axis=0,busy=0)),
      (0x038044bc,'0x7FF8','0xFFF8',choose(0x038044bc,samples=[1000]*5,range=0,axis=0,busy=1))]




def wrong_c(case,ordinal,images):
    entry,old,new,selected,*occurrence=case;expectedOccurrences=occurrence[0]if occurrence else 1;tag=format(entry,'08x');name='native_host_arm7_'+('wram_'if entry>=0x037f8000 else'main_')+tag;directory=WORK/'wrong-c'/str(ordinal)/tag
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
    if SOURCE!=ROOT/'src/arm7/parallel_wave20261106/peripheral-next/first' or LANE!=ROOT/'evidence/lanes/parallel-wave20261106/arm7-peripheral-next/first' or WORK!=ROOT/'work/w6per/first':raise ValueError('Exact newly owned peripheral source/evidence/work scope differs')
    if unicorn.__version__!='2.1.4':raise ValueError('Actual native ARMv4T fixture runtime differs')
    inputs=read_json(LANE/'inputs.json')
    for pin in inputs['files']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Frozen actual peripheral compiler/source/native/runtime input changed: '+pin['path'])
    rows,outputs=build_all(WORK/'proof-positive');by={int(r['address'],0):r for r in rows};images=[(int(m['base'],0),(ROOT/m['binary']).read_bytes())for m in read_json(ROOT/'evidence/arm7/runtime-layout.json')['modules']];traces=[];coverage={r['address']:set()for r in rows}
    for number,f in enumerate(fixtures()):
        row=by[f['entry']];image=(ROOT/row['binary']).read_bytes();native=image[f['entry']-row['base']:f['entry']-row['base']+row['bytes']];original=run(row,native,f,images,number);rebuilt=run(row,outputs[row['name']],f,images,number)
        if original!=rebuilt or original['modelFailures']or not original['actualTopReturn']:
            write_json(WORK/'fixture-failure.json',dict(ordinal=number,fixture=f,original=original,rebuilt=rebuilt));raise ValueError('Independent complete peripheral caller/model mismatch')
        coverage[row['address']].update(pc for pc in original['pcs']if f['entry']<=pc<f['entry']+row['bytes']);traces.append(dict(ordinal=number,fixture=f,result=original))
    print(dict(positiveNativeSourcePairs=len(traces),functions=len(rows),bytes=sum(r['bytes']for r in rows)),flush=True)
    negative=[wrong_c(case,number,images)for number,case in enumerate(negative_cases())];controlled=controls(rows);write_json(LANE/'controls.json',controlled);raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode();artifact=LANE/'traces.json.gz';artifact.write_bytes(gzip.compress(raw,mtime=0));symbols={}
    for row in rows:
        for name,binding in row['nativeSymbolEntries'].items():
            if name in symbols and symbols[name]!=binding:raise ValueError('Conflicting complete report-level ARM7 peripheral symbols')
            symbols[name]=binding
    covered=[dict(address=address,originalInstructionBytes=4*len(pcs),completeNativeSpanBytes=by[int(address,0)]['bytes'])for address,pcs in coverage.items()]
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],program='',processor='arm7',module='mixed',allPassed=True,matches=rows,canonicalMatchedFunctions=len(rows),canonicalMatchedBytes=sum(r['bytes']for r in rows),cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecutedInCallerFixtures=0,nativeSymbols={n:b['address']for n,b in symbols.items()},nativeSymbolModules={n:b['module']for n,b in symbols.items()},nativeSymbolEntries=symbols,nativeSymbolBindings=symbols,calleeSourceCredit=0,externalStorageCredit=0,fixtureInstructionCoverage=covered,fixtureCoveredOriginalInstructionBytes=sum(r['originalInstructionBytes']for r in covered),negativeEvidence=negative,controls=dict(path=(LANE/'controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'controls.json')),inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=C.sha(raw)),producer=Path(__file__).name,producerSha256=sha256(__file__),limits=[
      'Six complete independently admitted host ARM7 ARMv4T peripheral callers1872B in arm7-main and arm7-wram; all73 original relocations/addends genuinely link with actual base2.0 C99/O4/inline-on/file-IPA closed ordinary readable C/headers. RTC hour-format caller retains original ordinary-C GpioTransfer TU context for partial inlining; selected split discards its executable helper body and credits only292 caller bytes.',
      '151 original/source pairs cover all14 NVRAM commands and invalid/exclusive/permission paths, raw32-bit arguments and narrowed16-bit write lengths/results, RTC alarm bitfields and byte reads preserving unwritten high bytes, BCD valid/invalid nibbles, odd-only hour-format guard and alarm-buffer dataflow, touch queue failures preserving indeterminate stack bits, and five-sample filtering/density/weighted first-triple/fallback behavior.',
      'Touch filtering executes exact ordered halfword SPI register writes and scripted bounded read-width/order/value contracts, including busy polling and ADC noise masking. These deterministic mapped-device responses are model inputs rather than physical SPI/touch/timing claims. Alarm conversion is an explicit modeled provider buffer mutation; provider bodies execute0 and no calendar/helper/storage credit is taken.',
      'Caller stack/register/borrowed-RAM and initialized native images remain checked; fresh C99/strict prototypes/actual field/bit geometry/primitive ABI/qualified full namespace bindings/genuine wrong-C and fresh source-only canonical copied-root are required. Shared acceptance alone grants source credit; every earlier source/Ready remains immutable.'  ])
    write_json(LANE/'match.json',report);print(dict(functions=len(rows),bytes=report['canonicalMatchedBytes'],pairedCases=len(traces),genuineWrongC=len(negative),boundedInstructionBytes=report['fixtureCoveredOriginalInstructionBytes']),flush=True)


if __name__=='__main__':execute()
