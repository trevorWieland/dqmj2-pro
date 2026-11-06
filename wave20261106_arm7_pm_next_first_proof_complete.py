import gzip
import json
from pathlib import Path
import match_runtime as C
import unicorn
from project import ROOT,read_json,write_json,sha256,configuration
from wave20261106_arm7_pm_next_first_build import SOURCE,LANE as CERTIFICATE_LANE,WORK,build_all
LANE=CERTIFICATE_LANE.parent/'first-complete'
from wave20261106_arm7_pm_next_first_models import fixtures
from wave20261106_arm7_pm_next_first_execution import run
from wave20261106_arm7_pm_next_first_controls import execute as controls


def negative_cases():
    all_fixtures=fixtures()
    def choose(entry,**fields):return [f for f in all_fixtures if f['entry']==entry and all(f.get(key)==value for key,value in fields.items())][:2]
    return [
      (0x03804b80,'value&255','value&127',choose(0x03804b80,value=255)),
      (0x03804b80,'(8,data,error)','(8,data,0)',choose(0x03804b80,error=1)),
      (0x03804b80,'0x03000000','0x01000000',choose(0x03804b80)),
      (0x03804b80,'<0','!=0',choose(0x03804b80,results=[0xffffffff,0x80000000,3])),
      (0x03804bc4,'0x7f00','0xff00',choose(0x03804bc4,command=128)),
      (0x03804bc4,'!=0','<0',choose(0x03804bc4,command=0x63)),
      (0x038048e0,'data&0x02000000','data&0x01000000',choose(0x038048e0,start=False,end=True)),
      (0x038048e0,'data&0xf0000','data&0x70000',choose(0x038048e0,index=15,end=False)),
      (0x038048e0,'=(u16)data','=(u8)data',choose(0x038048e0,command=0x61)),
      (0x038048e0,'data&0x01000000','data&0x00800000',choose(0x038048e0,command=0x61)),
      (0x03804a20,'entry->args[0]&31','entry->args[0]&255',choose(0x03804a20,command=0x62,available=True,operation=0xffff0081)),
      (0x03804a20,'status=2','status=1',choose(0x03804a20,command=0x61,available=True)),
      (0x03804a20,'(0x61,result,0)','(0x61,(u16)result,0)',choose(0x03804a20,command=0x61,available=True)),
      (0x03804fbc,'triggers&4','triggers&8',choose(0x03804fbc,triggers=4)),
      (0x03804fbc,'if(restoreSerial)','if(0)',choose(0x03804fbc,triggers=2)),
      (0x03804fbc,'flags&0x40?6:7','flags&0x40?7:6',choose(0x03804fbc)),
      (0x03804fbc,'restore_master(previousMaster)','restore_master(1)',choose(0x03804fbc,ime=0)),
      (0x03804fbc,'(0,control)','(0,control&127)',choose(0x03804fbc,control=0xd3)),
      (0x0380516c,'counter++;','counter+=2;',choose(0x0380516c,pattern=4,counter=0)),
      (0x0380516c,'0x8000000000000000ULL','0x4000000000000000ULL',choose(0x0380516c,pattern=4,counter=0)),
      (0x0380516c,'next!=native_host_arm7_led_state_038075dc','next==native_host_arm7_led_state_038075dc',choose(0x0380516c,pattern=4)),
      (0x038052fc,'&=~2','&=~1',choose(0x038052fc,word=3))]


def wrong_c(case,ordinal,images):
    entry,old,new,selected=case;tag=format(entry,'08x');name='native_host_arm7_wram_'+tag;directory=WORK/'wrong-c'/str(ordinal)/tag
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
    if SOURCE!=ROOT/'src/arm7/parallel_wave20261106/pm-next/first' or LANE!=ROOT/'evidence/lanes/parallel-wave20261106/arm7-pm-next/first-complete' or WORK!=ROOT/'work/w6pm/first':raise ValueError('Exact newly owned PM source/evidence/work scope differs')
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
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],program='',processor='arm7',module='arm7-wram',allPassed=True,matches=rows,canonicalMatchedFunctions=len(rows),canonicalMatchedBytes=sum(r['bytes']for r in rows),cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecutedInCallerFixtures=0,nativeSymbols={n:b['address']for n,b in symbols.items()},nativeSymbolModules={n:b['module']for n,b in symbols.items()},nativeSymbolEntries=symbols,nativeSymbolBindings=symbols,calleeSourceCredit=0,externalStorageCredit=0,fixtureInstructionCoverage=covered,fixtureCoveredOriginalInstructionBytes=sum(r['originalInstructionBytes']for r in covered),negativeEvidence=negative,controls=dict(path=(LANE/'controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'controls.json')),inputs=dict(path=(LANE/'inputs.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=C.sha(raw)),producer=Path(__file__).name,producerSha256=sha256(__file__),limits=[
      'Seven whole host ARM7-wram ARMv4T functions/1556 initialized bytes, all63 unchanged original ELF relocations and actual explicit C99/base/O4,s/file-IPA/on,noauto genuine links. No object/register/instruction/symbol/relocation patches, algorithm ASM or allocation/profile sweep.',
      'Public PM source is a contextual primary reference; original native names and SDK revision correspondence remain qualified. Receiver and dispatcher command constants, raw fullword interfaces, distinct signed-negative versus nonzero FIFO retries and volatile16-bit accesses are measured from original native callers.',
      '172 independent original/source caller pairs cover command chunks, complete borrowed command/status storage, all32 trigger combinations, preserved IRQ/master/serial snapshots, all12 actual initialized blink records, defined64-bit shift/division inputs, low16/fullword ABI boundaries and controlled provider failures. Native peripheral/hardware/scheduler/SVC/provider bodies execute0 in caller fixtures; all imports are explicit controlled contracts.',
      'Separate actual compiler probes execute14 real original ARM7 unsigned quotient/remainder helper returns at03806e44, preserving implicit_u32_div_f name and exact caller/module/profile/origin certificate. No helper/source/storage extent credit.',
      'Blink fixtures require nonzero measured resolution and quotient below64, preserving the ordinary C defined shift/division domain. Serial wake writes are explicit synthetic provider mutations, not physical device execution or behavior claims.',
      'Typed external state/command/table views, zero-code anchors, MMIO and initialized blink records allocate/credit0 new storage. The separate164-byte initializer remains uncredited. Source-only and canonical copied-root replay are required before READY; accepted credit awaits shared coordinator gates.'])
    write_json(LANE/'match.json',report);print(dict(functions=len(rows),bytes=report['canonicalMatchedBytes'],pairedCases=len(traces),genuineWrongC=len(negative),boundedInstructionBytes=report['fixtureCoveredOriginalInstructionBytes']),flush=True)


if __name__=='__main__':execute()
