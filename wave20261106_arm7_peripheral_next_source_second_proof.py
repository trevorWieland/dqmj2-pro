import gzip
import json
from pathlib import Path
import match_runtime as C
import unicorn
from project import ROOT,read_json,write_json,sha256,configuration
from wave20261106_arm7_peripheral_next_source_second_build import SOURCE,LANE,WORK,build_all
from wave20261106_arm7_peripheral_next_source_second_models import fixtures
from wave20261106_arm7_peripheral_next_source_second_execution import run
from wave20261106_arm7_peripheral_next_source_second_controls import execute as controls


def negative_cases():
    all_fixtures=fixtures()
    def choose(entry,**fields):return [f for f in all_fixtures if f['entry']==entry and all(f.get(key)==value for key,value in fields.items())][:1]
    return [
      (0x038043a4,'SPI_SendWait(0x84','SPI_SendWait(0x85',choose(0x038043a4,history=0,key1=0xa5bf,busy=0),2),
      (0x038043a4,'if (!native_host_arm7_data_03809ea8)','if (native_host_arm7_data_03809ea8)',choose(0x038043a4,history=0,key1=0xa5ff,busy=0)),
      (0x038043a4,'return TOUCH_MAY_OFFNOISE','return TOUCH_ON',choose(0x038043a4,history=1,key1=0xa5ff,key2=0xa5bf,busy=0)),
      (0x038043a4,'0x0040','0x0080',choose(0x038043a4,history=0,key1=0xa5bf,busy=0),3),
      (0x038046ac,'range = -range','range = range',choose(0x038046ac,first=1,second=1,range=-7,x=0x1234)),
      (0x038046ac,'*density = 0','*density = 1',choose(0x038046ac,first=0)),
      (0x038046ac,'data->e.x = temp_pos','data->e.y = temp_pos',choose(0x038046ac,first=1,second=1,range=0,x=0x1234)),
      (0x038046ac,'== SPI_TP_VALIDITY_INVALID_Y','!= SPI_TP_VALIDITY_INVALID_Y',choose(0x038046ac,first=1,second=1,range=0,x=0x1234)),
      (0x038046ac,'i < 12','i < 11',choose(0x038046ac,first=1,second=1,range=0,x=0x1234)),
      (0x038046ac,'if (temp_touch == TOUCH_MAY_OFFNOISE)','if (temp_touch == TOUCH_ON)',choose(0x038046ac,first=1,second=1,range=0,x=0x1234)),
      (0x038046ac,'native_host_arm7_data_03809ea8 = 1','native_host_arm7_data_03809ea8 = 2',choose(0x038046ac,first=1,second=1,range=0,x=0x1234)),
      (0x038046ac,'density_x >= density_y','density_x <= density_y',choose(0x038046ac,first=1,second=1,range=0,x=0x1234)),
      (0x038046ac,'data->e.touch = SPI_TP_TOUCH_ON','data->e.touch = SPI_TP_TOUCH_OFF',choose(0x038046ac,first=1,second=1,range=0,x=0x1234),2),
      (0x038046ac,'data->e.y = temp_pos','data->e.y = (temp_pos >> 1)',choose(0x038046ac,first=1,second=1,range=0,x=0x1234))]







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
    if SOURCE!=ROOT/'src/arm7/parallel_wave20261106/peripheral-next/second' or LANE!=ROOT/'evidence/lanes/parallel-wave20261106/arm7-peripheral-next/second' or WORK!=ROOT/'work/w6per/second':raise ValueError('Exact newly owned peripheral source/evidence/work scope differs')
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
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],program='',processor='arm7',module='arm7-wram',allPassed=True,matches=rows,canonicalMatchedFunctions=len(rows),canonicalMatchedBytes=sum(r['bytes']for r in rows),cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecutedInCallerFixtures=0,nativeSymbols={n:b['address']for n,b in symbols.items()},nativeSymbolModules={n:b['module']for n,b in symbols.items()},nativeSymbolEntries=symbols,nativeSymbolBindings=symbols,calleeSourceCredit=0,externalStorageCredit=0,fixtureInstructionCoverage=covered,fixtureCoveredOriginalInstructionBytes=sum(r['originalInstructionBytes']for r in covered),negativeEvidence=negative,controls=dict(path=(LANE/'controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'controls.json')),inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=C.sha(raw)),producer=Path(__file__).name,producerSha256=sha256(__file__),limits=[
      'Two complete independently admitted host ARM7-wram ARMv4T touch callers748B; all14 original relocations/addends genuinely link under actual base2.0 C99/O4/inline-on/file-IPA using closed ordinary readable C/headers. Shared last_touch_flg is a typed imported BSS halfword at03809ea8 with exact original ABS32 origins and zero storage/provider credit.',
      '83 original/source caller pairs check initial/reloaded touch history, first/second key-bit reads and repeated sampling/noise detection, signed range magnitude, packed12-bit coordinates and validity/touch fields preserving high reserved bits, all normal state transitions,13 ordered dummy calls and both SPI modes, local16-bit output reuse and density maximum/ties.',
      'Mapped SPI/key read-width/order/value and bounded busy-poll scripts are explicit device model inputs, not physical touch/SPI/IRQ/timing claims. DetectPos/DetectTouch/DummyWait/EXI/termination provider bodies execute0; caller fixtures cover only normal0/1/2 touch-return contracts and do not claim the terminal invalid-state provider body. Fresh C99,required prototypes,geometry/actual bitfield ABI,typed BSS/per-origin scope negatives,genuine wrong-C and source-only canonical copied-root are required; shared acceptance alone grants source credit.'  ])
    write_json(LANE/'match.json',report);print(dict(functions=len(rows),bytes=report['canonicalMatchedBytes'],pairedCases=len(traces),genuineWrongC=len(negative),boundedInstructionBytes=report['fixtureCoveredOriginalInstructionBytes']),flush=True)


if __name__=='__main__':execute()
