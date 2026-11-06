import gzip
import json
from pathlib import Path
import match_runtime as C
import unicorn
from project import ROOT,read_json,write_json,sha256,configuration
from wave20261106_arm7_pm_mic_next_second_build import SOURCE,LANE,WORK,build_all
from wave20261106_arm7_pm_mic_next_second_models import fixtures
from wave20261106_arm7_pm_mic_next_second_execution import run
from wave20261106_arm7_pm_mic_next_second_controls import execute as controls


def negative_cases():
    all_fixtures=fixtures()
    def choose(entry,**fields):return [f for f in all_fixtures if f['entry']==entry and all(f.get(key)==value for key,value in fields.items())][:2]
    return [
      (0x03804d40,'native_host_arm7_arm_0380528c(1)','native_host_arm7_arm_0380528c(2)',choose(0x03804d40,operation=1)),
      (0x03804d40,'native_host_arm7_arm_03804cf0(12)','native_host_arm7_arm_03804cf0(4)',choose(0x03804d40,operation=8)),
      (0x03804d40,'native_host_arm7_arm_037fe708();','',choose(0x03804d40,operation=14)),
      (0x03804d40,'native_host_arm7_arm_03804c7c(1)&1','native_host_arm7_arm_03804c7c(1)&2',choose(0x03804d40,operation=15,value=0,register=0xa5)),
      (0x03804d40,'native_host_arm7_arm_03804c7c(0)&12','native_host_arm7_arm_03804c7c(0)&4',choose(0x03804d40,operation=15,value=1,register=255)),
      (0x03804d40,'return(u16)native_host_arm7_arm_038052a8()','return(u8)native_host_arm7_arm_038052a8()',choose(0x03804d40,operation=15,value=6,pattern=0xffffffff)),
      (0x03804d40,'default:return 2','default:return 3',choose(0x03804d40,operation=15,value=65535)),
      (0x03804d40,'(2,value&1)','(2,value&3)',choose(0x03804d40,operation=16,value=3)),
      (0x03804d40,'(3,value&3)','(3,value&1)',choose(0x03804d40,operation=17,value=3)),
      (0x03804d40,'value>>8','value>>7',choose(0x03804d40,operation=20,value=0x12ab)),
      (0x03804d40,'value&255','value&127',choose(0x03804d40,operation=20,value=0x12ab)),
      (0x03804d40,'case 3:return 0','case 3:return 1',choose(0x03804d40,operation=15,value=3)),
      (0x03804d40,'\n return 0;\n}','\n return 1;\n}',choose(0x03804d40,operation=0))]



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
    if SOURCE!=ROOT/'src/arm7/parallel_wave20261106/pm-mic-next/second' or LANE!=ROOT/'evidence/lanes/parallel-wave20261106/arm7-pm-mic-next/second' or WORK!=ROOT/'work/w6px/second':raise ValueError('Exact newly owned PM source/evidence/work scope differs')
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
      'One complete admitted532-byte ARM7-wram ARMv4T body,29 actual unchanged original relocations/addends, actual explicit C99/base/O4,s/file-IPA/on,noauto production and independent genuine links. No object/code/symbol/relocation patches, algorithm ASM or profile/allocation sweep.',
      'Pinned primary PM utility C grounds the LED/control family; native query/write extensions15..20,16-bit data promotion, masks and return values are independently measured. Native names/revision are qualified. No whole original/prebuilt executable object is an implementation input.',
      '140 independent original/source caller pairs cover all21 dispatch entries, unknown/full32-bit operation values, all7 query selections/defaults, low/high-byte register writes,8-bit provider values and16-bit query truncation. All imported bodies and hardware/sound/IRQ/platform effects execute0; modeled imports are explicit word-level contracts. No callee/data/storage credit.',
      'Actual compiler/CPU probes prove promoted16-bit upper-byte extraction,16-bit query truncation and full32-bit return ABI. Required prototypes, original per-origin boundaries/bindings, meaningful genuine wrong-C and source-only/canonical copied-root replay are mandatory. Earlier packets remain immutable; accepted credit awaits coordinator gates.'])
    write_json(LANE/'match.json',report);print(dict(functions=len(rows),bytes=report['canonicalMatchedBytes'],pairedCases=len(traces),genuineWrongC=len(negative),boundedInstructionBytes=report['fixtureCoveredOriginalInstructionBytes']),flush=True)


if __name__=='__main__':execute()
