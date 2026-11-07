import gzip
import json
from pathlib import Path
import match_runtime as C
import unicorn
from project import ROOT,read_json,write_json,sha256,configuration
from wave20261106_arm7_wl_channel_source_first_build import SOURCE,LANE,WORK,build_all
from wave20261106_arm7_wl_channel_source_first_models import fixtures
from wave20261106_arm7_wl_channel_source_first_execution import run
from wave20261106_arm7_wl_channel_source_first_controls import execute as controls


def negative_cases():
    values=fixtures()
    def choose(**fields):return[f for f in values if all(f.get(k)==v for k,v in fields.items())][:1]
    return[
      (0x27e990c,'if (bDirect) {','if (!bDirect) {',choose(enabled=True,direct=0,rf=2,bk=0)),
      (0x27e990c,'return 0x05 ;','return 0x04 ;',choose(enabled=False)),
      (0x27e990c,'ch_Reg[channel - 1][0]','ch_Reg[channel - 1][1]',choose(enabled=True,rf=2,bk=0)),
      (0x27e990c,'= bkpwr;','= bkpwr ^ 1;',choose(enabled=True,rf=2,bk=0)),
      (0x27e990c,'+ 0x048) = 3;','+ 0x048) = 2;',choose(enabled=True,rf=2,bk=0)),
      (0x27e990c,'reg |= (5 << 16);','reg |= (4 << 16);',choose(enabled=True,rf=3,chan=1))]


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
    if SOURCE!=ROOT/'src/arm7/parallel_wave20261106/wl-channel-next/first' or LANE!=ROOT/'evidence/lanes/parallel-wave20261106/arm7-wl-channel-next/first' or WORK!=ROOT/'work/w6wch/first':raise ValueError('Exact newly owned PM source/evidence/work scope differs')
    if unicorn.__version__!='2.1.4':raise ValueError('Actual native ARMv4T fixture runtime differs')
    inputs=read_json(LANE/'inputs-v2.json')
    for pin in inputs['files']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Frozen actual PM compiler/source/native/runtime input changed: '+pin['path'])
    rows,outputs=build_all(WORK/'proof-positive')
    from closed_c_compiler_inputs_20261105 import compiler_inputs
    for row in rows:compiler_inputs(row)
    by={int(r['address'],0):r for r in rows};images=[(int(m['base'],0),(ROOT/m['binary']).read_bytes())for m in read_json(ROOT/'evidence/arm7/runtime-layout.json')['modules']];traces=[];coverage={r['address']:set()for r in rows}
    for number,f in enumerate(fixtures()):
        row=rows[0];image=(ROOT/row['binary']).read_bytes();native=image[int(row['address'],0)-row['base']:int(row['address'],0)-row['base']+row['bytes']];original=run(row,native,f,images,number);rebuilt=run(row,outputs[row['name']],f,images,number)
        if original!=rebuilt or original['modelFailures']or not original['actualTopReturn']:
            write_json(WORK/'fixture-failure.json',dict(ordinal=number,fixture=f,original=original,rebuilt=rebuilt));raise ValueError('Independent complete PM caller/model mismatch')
        coverage[row['address']].update(pc for pc in original['pcs']if int(row['address'],0)<=pc<int(row['address'],0)+row['bytes']);traces.append(dict(ordinal=number,fixture=f,result=original))
    print(dict(positiveNativeSourcePairs=len(traces),functions=len(rows),bytes=sum(r['bytes']for r in rows)),flush=True)
    negative=[wrong_c(case,number,images)for number,case in enumerate(negative_cases())];controlled=controls(rows);write_json(LANE/'controls.json',controlled);raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode();artifact=LANE/'traces.json.gz';artifact.write_bytes(gzip.compress(raw,mtime=0));symbols={}
    for row in rows:
        for name,binding in row['nativeSymbolEntries'].items():
            if name in symbols and symbols[name]!=binding:raise ValueError('Conflicting complete report-level ARM7 PM symbols')
            symbols[name]=binding
    covered=[dict(address=address,originalInstructionBytes=4*len(pcs),completeNativeSpanBytes=by[int(address,0)]['bytes'])for address,pcs in coverage.items()]
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],program='',processor='arm7',module='arm7-main',allPassed=True,matches=rows,canonicalMatchedFunctions=len(rows),canonicalMatchedBytes=sum(r['bytes']for r in rows),cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),nativeCalleeBodiesExecutedInCallerFixtures=0,nativeSymbols={n:b['address']for n,b in symbols.items()},nativeSymbolModules={n:b['module']for n,b in symbols.items()},nativeSymbolEntries=symbols,nativeSymbolBindings=symbols,calleeSourceCredit=0,externalStorageCredit=0,fixtureInstructionCoverage=covered,fixtureCoveredOriginalInstructionBytes=sum(r['originalInstructionBytes']for r in covered),negativeEvidence=negative,controls=dict(path=(LANE/'controls.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'controls.json')),inputs=dict(path=(LANE/'inputs-v2.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'inputs-v2.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=C.sha(raw)),producer=Path(__file__).name,producerSha256=sha256(__file__),limits=[
      'One complete HOST ARM7-main ARMv4T published WSetChannel652-byte caller,636instruction plus16literal bytes,all8actual PC24/ABS32 relocations and original typed ARM callback identities preserved by genuine compiler/split/MWlink.',
      '43 independent original/source pairs cover enabled/disabled channel masks,valid1..14 channels,both boolean/direct callback alternatives,RF IDs2/5/3 and unknown IDs,all backup-register flag branches,zero/nonzero bounded RF/BBP loops,partial1/3byte scratch writes,and synthetic status transitions ending in state0/9.',
      'Whole synthetic1684-byte consumed WL view,ordered writes/imports,all GPRs/CPSR/SP/callee-saved state and exact MMIO width/order/value are compared. One provider changes the backup-register word to check actual post-call rereads;all imported providers execute0bodyinstructions and receive0credit.',
      'Flash callback first argument is a scalar flash offset,not a RAM alias. Callback pointer selectorR9 and its8native indirect sites are separately scoped to exactly2real HOST ARM7 ARM entries;no global validator/return guard changes.',
      'Source-visible WL/flash sizes are compiler consumed views,not proof of full native allocation. Fixed wlMan pointer,synthetic state,flash bytes,hardware addresses and imported helpers receive0storage/bodycredit. No physical radio/flash/time/concurrency/device/game or complete portableABI claim.',
      'No larger-channel undefined C shifts or RF table outside-range dereferences are claimed. Bounded hardware-register status fixtures model caller contracts only. Complete source-byte equality and dynamic instruction coverage are separate metrics.'

 ])
    write_json(LANE/'match.json',report);print(dict(functions=len(rows),bytes=report['canonicalMatchedBytes'],pairedCases=len(traces),genuineWrongC=len(negative),boundedInstructionBytes=report['fixtureCoveredOriginalInstructionBytes']),flush=True)


if __name__=='__main__':execute()
