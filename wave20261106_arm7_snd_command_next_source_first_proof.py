import gzip
import json
from pathlib import Path
import match_runtime as C
import unicorn
from project import ROOT,read_json,write_json,sha256,configuration
from wave20261106_arm7_snd_command_next_source_first_build import SOURCE,LANE,WORK,build_all
from wave20261106_arm7_snd_command_next_source_first_models import fixtures
from wave20261106_arm7_snd_command_next_source_first_execution import run
from wave20261106_arm7_snd_command_next_source_first_controls import execute as controls


def negative_cases():
    all_fixtures=fixtures()
    def choose(entry,**fields):return [f for f in all_fixtures if f['entry']==entry and all(f.get(key)==value for key,value in fields.items())][:1]
    return [
      (0x03801f1c,'command_p = command.next','command_p = 0',choose(0x03801f1c,mutate=True)),
      (0x03801f1c,'finishCommandTag++','finishCommandTag+=2',choose(0x03801f1c)),
      (0x03801f1c,'(s16)command.arg[2]','(s8)command.arg[2]',[all_fixtures[21]]),
      (0x03801f1c,'(s16)command.arg[1]','(s8)command.arg[1]',[all_fixtures[23]]),
      (0x03801f1c,'( 24)) - 1','( 16)) - 1',[all_fixtures[15]]),
      (0x03801f1c,'(OSTick)command.arg[1]','(OSTick)(s32)command.arg[1]',[all_fixtures[37]]),
      (0x03801f1c,'(OSTick)command.arg[2]','(OSTick)(s32)command.arg[2]',[all_fixtures[37]]),
      (0x03801f1c,'(SNDSharedWork *)command.arg[0]','(SNDSharedWork *)command.arg[1]',[all_fixtures[59]]),
      (0x03801f1c,'(const void *)command.arg[1]','(const void *)command.arg[2]',[all_fixtures[1]],5),
      (0x03801f1c,'( 27)) - 1','( 26)) - 1',[all_fixtures[28]]),
      (0x03801f1c,'( 22)) - 1','( 21)) - 1',[all_fixtures[29]]),
      (0x03801f1c,'( 24)) & ((1 << ( 7))','( 23)) & ((1 << ( 7))',[all_fixtures[29]]),
      (0x03801f1c,'for (ch = 0; ch < 16 && chBitMask','for (ch = 0; ch < 15 && chBitMask',[all_fixtures[85]],3),
      (0x03801f1c,'0x0080 | 0x8000','0x0080 | 0x4000',[all_fixtures[71]]),
      (0x03801f1c,'native_host_arm7_arm_037fea20(i, (s32)flags)','native_host_arm7_arm_037fea20(i, 0)',[all_fixtures[27]]),
      (0x03801f1c,'sizeof(native_host_arm7_data_03807ee0)','sizeof(native_host_arm7_data_03807ee0)-4',[all_fixtures[67]]),
      (0x03801f1c,'info->workAddress = &native_host_arm7_data_03807ee0','info->workAddress = (SNDWork*)((u8*)&native_host_arm7_data_03807ee0+4)',[all_fixtures[67]]),
      (0x03801f1c,'ch < 16 ;','ch < 15 ;',[all_fixtures[67]])]




def wrong_c(case,ordinal,images):
    entry,old,new,selected,*occurrence=case;expectedOccurrences=occurrence[0]if occurrence else 1;tag=format(entry,'08x');name='native_host_arm7_wram_'+tag;directory=WORK/'wrong-c'/str(ordinal)/tag
    if not selected:raise ValueError(('Meaningful wrong-C selection empty',name,old))
    directory.mkdir(parents=True,exist_ok=True)
    for path in (SOURCE/tag).iterdir():
        if path.is_file():(directory/path.name).write_bytes(path.read_bytes())
    count=0
    for path in directory.glob('*'):
        if path.suffix not in ['.c','.h']:continue
        text=path.read_text();count+=text.count(old)
        if old in text:path.write_text(text.replace(old,new))
    if count!=expectedOccurrences:raise ValueError(('Meaningful ordinary C mutation not unique',name,old,count))
    path=directory/'main.c' ;rows,outputs=build_all(directory/'build',{name:path},{name},{name});row=rows[0];rejected=[]
    for number,f in enumerate(selected):
        try:
            result=run(row,outputs[name],f,images,number)
            if not result['modelFailures']:raise ValueError(('Wrong C did not alter modeled behavior',name,old))
            rejected.append(dict(actualTopReturn=result['actualTopReturn'],modelFailures=result['modelFailures']))
        except unicorn.UcError as error:rejected.append(dict(actualTopReturn=False,rejectedAtMemoryBoundary=True,error=str(error)))
    return dict(case=ordinal,function=name,old=old,new=new,mutatedOccurrences=expectedOccurrences,genuinelyLinkedWrongC=rows,fixtures=selected,rejected=rejected,abortedRunsAreNotCallerReturns=True)


def execute():
    if SOURCE!=ROOT/'src/arm7/parallel_wave20261106/snd-command-next/first' or LANE!=ROOT/'evidence/lanes/parallel-wave20261106/arm7-snd-command-next/first' or WORK!=ROOT/'work/w6sndc/first':raise ValueError('Exact newly owned PM source/evidence/work scope differs')
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
      'One whole independently admitted host ARM7-wram ARMv4T SND_CommandProc1712B:1692 original instruction bytes and20 literal bytes. First evidence-led C99/base/O4/inline-on/file-IPA primary-TU profile naturally matches every nonrelocated byte,then closed readable ordinary C/three headers genuinely links all46 original relocation words/addends using unchanged namespace/derivation/splitter. No compiler grid,original binary implementation,object edit,algorithm assembler or extra callable entry.',
      'Independent queue/list/provider models exercise every34 command IDs,unknown IDs,empty/null/multiple messages,copied24-byte command snapshot under provider mutation,per-list finish-tag wrap and replacement shared-work pointers. Numeric arguments preserve signed16 extension,32-bit words,64-bit zero-extension,packed PCM/PSG/noise/capture fields and exact register/stack ordering for up to10-word calls.',
      'Timer masks cover channels0..15,alarms0..7,ignored high mask bits,zero/full masks,all capture combinations,8-bit/16-bit mapped MMIO read/write widths,enable-bit preservation and disable stores,interrupt-mode boundary words and exact provider ordering. These are synthetic device/provider contracts; no physical sound/audio,timer,interrupt or engine-provider body claim.',
      'Driver-info fixtures preserve4480 borrowed SNDWork bytes,copy destination and work-address identity,all16 returned channel controls,locked-mask word and24 deliberately unwritten trailing bytes of4576-byte SNDDriverInfo. The640-byte shared work and32-byte external queue are complete typed bounded objects; three imported original BSS references carry0storage/source credit and emit no implementation storage.',
      'Fresh actual C99/strict prototypes/primitive ABI/struct-field geometry/per-origin boundary/typed BSS/switch mutation/binding/genuine wrong-C and source-only canonical copied-root proofs are mandatory. Source matches explain this dispatcher correspondence only; imported provider/callee bodies remain unexecuted in production fixtures with0source/storage credit. Every prior Ready and shared registry/config/index/dispatch/Git state stays unchanged; only coordinator acceptance grants credit.'
 ])
    write_json(LANE/'match.json',report);print(dict(functions=len(rows),bytes=report['canonicalMatchedBytes'],pairedCases=len(traces),genuineWrongC=len(negative),boundedInstructionBytes=report['fixtureCoveredOriginalInstructionBytes']),flush=True)


if __name__=='__main__':execute()
