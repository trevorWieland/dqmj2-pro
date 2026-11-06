import gzip
import json
from pathlib import Path
import match_runtime as C
import unicorn
from project import ROOT,read_json,write_json,sha256,configuration
from wave20261106_arm7_pm_mic_next_first_build import SOURCE,LANE,WORK,build_all
from wave20261106_arm7_pm_mic_next_first_models import fixtures
from wave20261106_arm7_pm_mic_next_first_execution import run
from wave20261106_arm7_pm_mic_next_first_controls import execute as controls


def negative_cases():
    all_fixtures=fixtures()
    def choose(entry,**fields):return [f for f in all_fixtures if f['entry']==entry and all(f.get(key)==value for key,value in fields.items())][:2]
    return [
      (0x038053d0,'MIC_STATUS_READY','MIC_STATUS_AUTO_START',choose(0x038053d0)),
      (0x038053d0,'i < 16','i < 15',choose(0x038053d0)),
      (0x038053d0,'~0x0080','~0x0040',choose(0x038053d0,word=0xffff)),
      (0x03805418,'0x000f0000','0x00070000',choose(0x03805418,index=15)),
      (0x03805418,'data & 0x02000000','data & 0x01000000',choose(0x03805418,command=0x41,start=False)),
      (0x03805418,'buf + wu32 >','buf + wu32 >=',choose(0x03805418,command=0x41,size=0x003f0000)),
      (0x03805418,'wu32 < 0x02000000','wu32 <= 0x02000000',choose(0x03805418,buffer=0x02000000)),
      (0x03805418,'0x0080 | 0x0040','0x0080 | 0x0000',choose(0x03805418,command=0x43,state=2,timer=True)),
      (0x03805418,'native_host_arm7_arm_037fdd14(e);','(void)e;',choose(0x03805418,command=0x43,state=2,timer=True)),
      (0x03805784,'switch (entry->process)','switch ((u16)entry->process)',choose(0x03805784,command=0xffff0040)),
      (0x03805784,'temp ^= 0x8000','temp ^= 0x0080',choose(0x03805784,command=0x40,type=3,available=True)),
      (0x03805784,'temp ^= 0x0080','temp ^= 0x8000',choose(0x03805784,command=0x40,type=2,available=True)),
      (0x03805784,'native_host_arm7_arm_038059ac','((void *)0)',choose(0x03805784,command=0x41,state=1)),
      (0x03805784,'status = MIC_STATUS_AUTO_SAMPLING','status = MIC_STATUS_AUTO_START',choose(0x03805784,command=0x41,state=1)),
      (0x03805784,'~0x0080','~0x0040',choose(0x03805784,command=0x42,state=3)),
      (0x03805784,'status = MIC_STATUS_READY','status = MIC_STATUS_AUTO_END',choose(0x03805784,command=0x42,state=3))]



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
    if SOURCE!=ROOT/'src/arm7/parallel_wave20261106/pm-mic-next/first' or LANE!=ROOT/'evidence/lanes/parallel-wave20261106/arm7-pm-mic-next/first' or WORK!=ROOT/'work/w6px/first':raise ValueError('Exact newly owned PM source/evidence/work scope differs')
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
      'Three complete host ARM7-wram ARMv4T native bodies/1336 initialized bytes:72-byte initializer,712-byte command receiver,552-byte executor. All50 actual original ELF relocations and addends genuinely link; production and independent actual C99/base/O4,s/file-IPA/on,noauto match every native byte.',
      'Pinned primary MIC C is lexically closed to owned readable C/headers. Every imported body including the ASM IRQ callback is excluded; actual original function/callback entries are declarations and zero-code anchors only. No executable/prebuilt object is an implementation input, no source/data/IRQ body credit is taken for imports, and no instruction/object/relocation/name patch or allocation/profile sweep is used.',
      '114 independent original/source caller pairs check complete borrowed60-byte MICWork/1024-byte system-work regions, message masks and signed/unsigned16/32-bit boundaries, partial state changes before error returns, buffer upper/lower/exact-end/unsigned-wrap guards, queue/timer failures, all status transitions,8/12-bit sample sign-bit conversion, null/exact original callback words and controlled timer16-bit register sequences.',
      'Provider/timer/ADC/IRQ/scheduler bodies execute0 in returning caller fixtures. Timer success writes and sample returns are explicit synthetic provider contracts that exercise caller behavior; no physical device, callback, sampling interval or full game execution is claimed. Static data/MMIO and typed external aliases allocate/credit0 storage.',
      'Actual C99 typed const callback pointer probes retain the original ARM7-wram038059ac entry and ELF function/$a identity; wrong signature/null/array/data declarations reject. Wrong-C/layout/ABI/prototype/per-origin boundary/namespace binding controls and source-only/canonical copied-root replay are mandatory. The separate532-byte PM utility routine stays unselected/uncredited; accepted credit awaits shared coordinator gates.'])
    write_json(LANE/'match.json',report);print(dict(functions=len(rows),bytes=report['canonicalMatchedBytes'],pairedCases=len(traces),genuineWrongC=len(negative),boundedInstructionBytes=report['fixtureCoveredOriginalInstructionBytes']),flush=True)


if __name__=='__main__':execute()
