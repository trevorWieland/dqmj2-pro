import gzip
import json
from pathlib import Path
import match_runtime as C
import unicorn
from project import ROOT,read_json,write_json,sha256,configuration
from wave20261106_arm7_rtc_loop_source_first_build import SOURCE,LANE,WORK,build_all
from wave20261106_arm7_rtc_loop_source_first_models import fixtures
from wave20261106_arm7_rtc_loop_source_first_execution import run
from wave20261106_arm7_rtc_loop_source_first_controls import execute as controls


def negative_cases():
    values=fixtures()
    def choose(**fields):return[f for f in values if all(f.get(k)==v for k,v in fields.items())][:1]
    return[
      (0x27f60b4,'native_host_arm7_arm_027f6638();\n            (native_host_arm7_data_027f8e34.work).busy = 0 ;','native_host_arm7_arm_027f6638();\n            (native_host_arm7_data_027f8e34.work).busy = 1 ;',choose(command=0)),
      (0x27f60b4,'prd->a.status1.format','prd->a.status1.reset',choose(command=1,format=1)),
      (0x27f60b4,'native_host_arm7_arm_027f6074(0x13 , RTC_PXI_RESULT_ILLEGAL_STATUS);','native_host_arm7_arm_027f6074(0x13 , RTC_PXI_RESULT_SUCCESS);',choose(command=0x13,result=0)),
      (0x27f60b4,'case 0x21 :\n            native_host_arm7_arm_027f6830(&prd->t.time);','case 0x21 :\n            native_host_arm7_arm_027f6830((RTCRawTime *)&prd->t.date);',choose(command=0x21)),
      (0x27f60b4,'native_host_arm7_arm_027f6074(comm, RTC_PXI_RESULT_INVALID_COMMAND);','native_host_arm7_arm_027f6074(comm, RTC_PXI_RESULT_SUCCESS);',choose(command=65535)),
      (0x27f60b4,'while (1 ) {','while (0 ) {',choose(command=0))]


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
    if SOURCE!=ROOT/'src/arm7/parallel_wave20261106/rtc-loop-next/first' or LANE!=ROOT/'evidence/lanes/parallel-wave20261106/arm7-rtc-loop-next/first' or WORK!=ROOT/'work/w6rtcl/first':raise ValueError('Exact newly owned PM source/evidence/work scope differs')
    if unicorn.__version__!='2.1.4':raise ValueError('Actual native ARMv4T fixture runtime differs')
    inputs=read_json(LANE/'inputs.json')
    for pin in inputs['files']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Frozen actual PM compiler/source/native/runtime input changed: '+pin['path'])
    rows,outputs=build_all(WORK/'proof-positive')
    from closed_c_compiler_inputs_20261105 import compiler_inputs
    for row in rows:compiler_inputs(row)
    by={int(r['address'],0):r for r in rows};images=[(int(m['base'],0),(ROOT/m['binary']).read_bytes())for m in read_json(ROOT/'evidence/arm7/runtime-layout.json')['modules']];traces=[];coverage={r['address']:set()for r in rows}
    for number,f in enumerate(fixtures()):
        row=rows[0];image=(ROOT/row['binary']).read_bytes();native=image[int(row['address'],0)-row['base']:int(row['address'],0)-row['base']+row['bytes']];original=run(row,native,f,images,number);rebuilt=run(row,outputs[row['name']],f,images,number)
        if original!=rebuilt or original['modelFailures']or original['actualTopReturn'] or not original['boundedIterationComplete']:
            write_json(WORK/'fixture-failure.json',dict(ordinal=number,fixture=f,original=original,rebuilt=rebuilt));raise ValueError('Independent complete PM caller/model mismatch')
        coverage[row['address']].update(pc for pc in original['pcs']if int(row['address'],0)<=pc<int(row['address'],0)+row['bytes']);traces.append(dict(ordinal=number,fixture=f,result=original))
    print(dict(positiveNativeSourcePairs=len(traces),functions=len(rows),bytes=sum(r['bytes']for r in rows)),flush=True)
    negative=[wrong_c(case,number,images)for number,case in enumerate(negative_cases())];controlled=controls(rows);write_json(LANE/'controls.json',controlled);raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode();artifact=LANE/'traces.json.gz';artifact.write_bytes(gzip.compress(raw,mtime=0));symbols={}
    for row in rows:
        for name,binding in row['nativeSymbolEntries'].items():
            if name in symbols and symbols[name]!=binding:raise ValueError('Conflicting complete report-level ARM7 PM symbols')
            symbols[name]=binding
    covered=[dict(address=address,originalInstructionBytes=4*len(pcs),completeNativeSpanBytes=by[int(address,0)]['bytes'])for address,pcs in coverage.items()]
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],program='',processor='arm7',module='arm7-main',allPassed=True,matches=rows,canonicalMatchedFunctions=len(rows),canonicalMatchedBytes=sum(r['bytes']for r in rows),cases=len(traces),actualNativeAndSourceCallerReturns=0,actualNativeAndSourceBoundedLoopIterations=2*len(traces),intentionalNonreturn=True,nativeCalleeBodiesExecutedInCallerFixtures=0,nativeSymbols={n:b['address']for n,b in symbols.items()},nativeSymbolModules={n:b['module']for n,b in symbols.items()},nativeSymbolEntries=symbols,nativeSymbolBindings=symbols,calleeSourceCredit=0,externalStorageCredit=0,fixtureInstructionCoverage=covered,fixtureCoveredOriginalInstructionBytes=sum(r['originalInstructionBytes']for r in covered),negativeEvidence=negative,controls=dict(path=(LANE/'controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'controls.json')),inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=C.sha(raw)),producer=Path(__file__).name,producerSha256=sha256(__file__),limits=[
      'One complete HOST ARM7-main ARMv4T published RtcThread1156-byte caller,1140instruction plus16literal bytes,all56actual PC24/ABS32 relocations and genuine original namespace/modes preserved by real source/split/MWlink.',
      '58 independent original/source pairs each complete exactly one bounded message iteration and stop at the next original OS_ReceiveMessage entry before provider execution. Actual top-level returns are0,intentionally. This does not turn the infinite thread into a returning function or prove scheduler/hardware behavior.',
      'Fixtures cover every actual42-slot guarded dispatch index,42/65535 default commands,all six boolean-helper success/failure branches,negative nonzero BOOL returns,the status-format bit,and command replacement by a supplied queue provider before the native read. Read-time then write-datetime checks shared-byte propagation.',
      'All GPRs/CPSR,persistent40-byte thread stack,ordered writes/imports and every byte of a synthetic478-byte consumed global prefix and8-byte shared raw clock view are compared. Providers execute0bodyinstructions;no provider,calendar,time,clock-device,IRQ,PXI,concurrency or full-game behavior credit.',
      'Before compilation the source genuinely declares one external typed group with4opaque prefixbytes and published RTCWork. Its data addends0/4/256 naturally preserve native027f8e34/027f8e38/027f8f34 references. No compiled local symbol/relocation rebinding,object/instruction patch or BSS allocation.',
      'The952-byte source view type and published948-byte RTCWork size are consumed compiler types,not proof of whole native allocation. Actual source object defines no allocated noncode storage;native BSS,shared systemwork,borrowed message/clock buffers and all supporting entries receive0extra initialized-storage/source credit.'

 ])
    write_json(LANE/'match.json',report);print(dict(functions=len(rows),bytes=report['canonicalMatchedBytes'],pairedCases=len(traces),genuineWrongC=len(negative),boundedInstructionBytes=report['fixtureCoveredOriginalInstructionBytes']),flush=True)


if __name__=='__main__':execute()
