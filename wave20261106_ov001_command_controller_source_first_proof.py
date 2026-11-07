import argparse
import gzip
import json
from pathlib import Path
import match_runtime as C
import unicorn
from project import ROOT,read_json,write_json,sha256,configuration
from wave20261106_ov001_command_controller_source_first_paths import SOURCE,EVIDENCE,WORK,assert_owned
from wave20261106_ov001_command_controller_source_first_build import build
from wave20261106_ov001_command_controller_source_first_models import fixtures
from wave20261106_ov001_command_controller_source_first_execution import run
from wave20261106_ov001_command_controller_source_first_controls import execute as controls


def source_policy(row):
    import re
    paths=[ROOT/row['source'],*[ROOT/p['path']for p in row['sourceDependencies']]];pins={row['source']:row['sourceSha256'],**{p['path']:p['sha256']for p in row['sourceDependencies']}};includes=set()
    for path in paths:
        text=path.read_text()
        if not path.resolve().is_relative_to(SOURCE.resolve())or sha256(path)!=pins[path.relative_to(ROOT).as_posix()]or len(text.splitlines())>500 or re.search(r'/\*|//|\b(?:asm|__asm|__asm__|INCBIN)\b',text)or re.search(r'^\s*#\s*include\s*<',text,re.M):raise ValueError('Complete closed ordinary owned C source policy differs')
        includes.update((path.parent/name).resolve()for name in re.findall(r'^\s*#\s*include\s*"([^"<>]+)"',text,re.M))
    if includes!={p.resolve()for p in paths[1:]}:raise ValueError('Actual quoted include closure differs')
    return dict(ordinaryC=True,actualIncludesPinned=True,maximumFileLines=max(len(p.read_text().splitlines())for p in paths))


def negative_cases():
    all_fixtures=fixtures()
    def choose(entry,**fields):return[f for f in all_fixtures if f['entry']==entry and all(f.get(k)==v for k,v in fields.items())][:1]
    return[
      (0x021fe4ac,'field58>>5','field58>>4',choose(0x021fe4ac,counter=31)),
      (0x021fe4ac,'(e*f)<<5','(e*f)<<4',choose(0x021fe4ac,counter=31)),
      (0x021fe4ac,'if(h)','if(!h)',choose(0x021fe4ac,counter=31)),
      (0x021fe618,'native_data_02239c64[group]','native_data_02239c64[0]',choose(0x021fe618,group=1),2),
      (0x021fe618,'index,a,8,b','index,a,9,b',choose(0x021fe618,group=0)),
      (0x021fe618,'added<<5','added<<4',choose(0x021fe618,added=1)),
      (0x0220aba0,'field18|=2','field18|=4',choose(0x0220aba0,index=0)),
      (0x0220aba0,'field0++','field0+=2',choose(0x0220aba0,index=0)),
      (0x0220aba0,'=(s8)index;','=(s8)(index+1);',choose(0x0220aba0,index=0)),
      (0x0220ac9c,'0x3000','0x3001',choose(0x0220ac9c,code=0)),
      (0x0220ac9c,'0x17b','0x17a',choose(0x0220ac9c,code=1)),
      (0x0220ac9c,'position+8','position+7',choose(0x0220ac9c,position=32767)),
      (0x0220ac9c,'arg4,arg5,data','arg4,0,data',choose(0x0220ac9c,flag=-128)),
      (0x0220afe4,'2,1,3,16','2,1,4,16',choose(0x0220afe4,owner=-128)),
      (0x0220afe4,'flags->field4high','flags->field4low',choose(0x0220afe4,bits=0xabcd)),
      (0x0220afe4,'record->field10','(u8)record->field10',choose(0x0220afe4,owner=-128),2),
      (0x0220b3e4,'field0|=1','field0|=4',choose(0x0220b3e4,mode=0,flags=0),2),
      (0x0220b3e4,'field10=a','field10=b',choose(0x0220b3e4,mode=2,flags=0))]


def wrong_c(case,ordinal,images):
    entry,old,new,selected,*count=case;count=count[0]if count else 1;tag=format(entry,'08x');directory=WORK/'n'/str(ordinal)/tag
    if not selected:raise ValueError(('Meaningful wrong-C fixture absent',tag,old))
    directory.mkdir(parents=True,exist_ok=True)
    for path in(SOURCE/tag).iterdir():
        if path.is_file():(directory/path.name).write_bytes(path.read_bytes())
    source=directory/'main.c';text=source.read_text()
    if text.count(old)!=count:raise ValueError(('Exact wrong-C source mutation ambiguous',tag,old,text.count(old),count))
    source.write_text(text.replace(old,new));row,body=build(source,directory/'build',True);rejections=[]
    for n,f in enumerate(selected):
        try:
            result=run(row,body,f,images,n)
            if not result['modelFailures']:raise ValueError(('Genuine wrong C retained all independent modeled behavior',tag,old))
            rejections.append(dict(actualTopReturn=result['actualTopReturn'],modelFailures=result['modelFailures']))
        except unicorn.UcError as error:rejections.append(dict(actualTopReturn=False,rejectedAtMemoryBoundary=True,error=str(error)))
    return dict(ordinal=ordinal,caller=hex(entry),old=old,new=new,sourceOccurrences=count,fixtures=selected,genuineWrongC=row,rejected=rejections,sourceCredit=0,abortedRunsAreNotCallerReturns=True)


def execute(expected):
    assert_owned(EVIDENCE);path=EVIDENCE/'inputs.json'
    if sha256(path)!=expected:raise ValueError('Explicit immutable input manifest changed')
    inputs=read_json(path)
    for pin in inputs['files']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Immutable packet input changed: '+pin['path'])
    if unicorn.__version__!='2.1.4':raise ValueError('Qualified bounded native fixture runtime differs')
    reference=read_json(EVIDENCE/'native-inputs.json');images=[(0x02000000,(ROOT/reference['mainImage']['path']).read_bytes()),(int(reference['base'],0),(ROOT/reference['image']['path']).read_bytes())];rows=[];outputs={}
    for pin in inputs['entries']:
        row,body=build(ROOT/pin['source'],WORK/'positive'/format(int(pin['address'],0),'08x'));source_policy(row)
        if any(row.get(k)!=pin.get(k)for k in['program','processor','module','mode','address','bytes','source','sourceSha256','sourceDependencies','targetSha256','compilerSha256','compilerFlags']):raise ValueError('Fresh full source/native/compiler contract differs')
        row.update(sourceLanguage='C',ordinaryCOnly=True,ordinaryCBytes=row['bytes'],justifiedAssemblyBytes=0,originalObjectScaffolding=False,wholeModuleLinked=False,originalDataSourceCredit=0,sourcePolicy=source_policy(row));rows.append(row);outputs[row['name']]=body
    by={int(r['address'],0):r for r in rows};traces=[];coverage={r['address']:set()for r in rows}
    for n,f in enumerate(fixtures()):
        row=by[f['entry']];at=f['entry']-images[1][0];native=images[1][1][at:at+row['bytes']];original=run(row,native,f,images,n);rebuilt=run(row,outputs[row['name']],f,images,n)
        if original!=rebuilt or original['modelFailures']or not original['actualTopReturn']:write_json(WORK/'fixture-failure.json',dict(ordinal=n,fixture=f,original=original,rebuilt=rebuilt));raise ValueError('Independent complete caller/model mismatch')
        coverage[row['address']].update(pc for pc in original['pcs']if f['entry']<=pc<f['entry']+row['bytes']);traces.append(dict(ordinal=n,fixture=f,result=original))
    print(dict(positiveNativeSourcePairs=len(traces),functions=len(rows),bytes=sum(r['bytes']for r in rows)),flush=True);negative=[wrong_c(case,n,images)for n,case in enumerate(negative_cases())];qualified=controls(rows);write_json(EVIDENCE/'controls.json',qualified);raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode();artifact=EVIDENCE/'traces.json.gz';artifact.write_bytes(gzip.compress(raw,mtime=0));symbols={}
    for row in rows:
        for name,binding in row['nativeSymbolEntries'].items():
            if name in symbols and symbols[name]!=binding:raise ValueError('Conflicting complete module-qualified report symbols')
            symbols[name]=binding
    covered=[dict(address=a,executedOriginalInstructionBytes=4*len(pcs),completeNativeSpanBytes=by[int(a,0)]['bytes'])for a,pcs in coverage.items()]
    for row in rows:row['oracle']=dict(supported=True,supportedReturningVectors=sum(f['entry']==int(row['address'],0)for f in fixtures()),actualNativeCalleeBodiesExecuted=0,calleeOrStorageCredit=0)
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],program='',processor='arm9',module='ov001',mode='arm',allPassed=True,matches=rows,canonicalMatchedFunctions=len(rows),canonicalMatchedBytes=sum(r['bytes']for r in rows),acceptedSourceCredit=0,wholeModuleLinked=False,sourceReconstructionComplete=False,cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),actualNativeAndSourcePartialStops=0,nativeCalleeBodiesExecutedInCallerFixtures=0,nativeCalleeBodiesExecuted=0,nativeCalleeBodyExecutionCountScope='caller-fixtures-only',actualStandaloneOriginalEntryExecutions=6,separateActualNativeHelperReturnCredit=0,nativeSymbols={n:b['address']for n,b in symbols.items()},nativeSymbolModules={n:b['module']for n,b in symbols.items()},nativeSymbolEntries=symbols,nativeSymbolBindings=symbols,fixtureInstructionCoverage=covered,fixtureCoveredOriginalInstructionBytes=sum(r['executedOriginalInstructionBytes']for r in covered),negativeEvidence=negative,wholeCNegativeControlsRejected=len(negative),controls=dict(path=(EVIDENCE/'controls.json').relative_to(ROOT).as_posix(),sha256=sha256(EVIDENCE/'controls.json')),inputs=dict(path=path.relative_to(ROOT).as_posix(),sha256=sha256(path)),inputManifest=path.relative_to(ROOT).as_posix(),inputManifestSha256=sha256(path),generatorSources=inputs['generatorSources'],generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=C.sha(raw)),callerFixtureTraceSha256=C.sha(raw),producer=Path(__file__).name,producerSha256=sha256(__file__),sourceContractsUnchanged=True,limits=[
      'Six independently admitted complete OV001 ARMv5TE game/controller functions1136B,27original relocations,actual base2.0 O2/inline-off/speed/C99/noIPA. Only closed readable C/headers are implementation inputs; no original object,ASM,instruction/object/symbol/relocation patch,profile/allocation grid or hidden SDK context.',
      '82 independent native/source pairs check actual fixed02102a18+12*index record addressing with a consumed8-byte EntryView prefix,11/12-word boundaries including signed bytes,overlapping ov001 BSS views,post-call counter/link/resource reloads,wrapped arithmetic,complete borrowed bytes,reserved high bits,field18 bit preservation,exact halfword-container nibble extraction,signed16 draw-coordinate wrap and exact ROM-table read indices/widths.',
      'The4-case controller uses the admitted CMP/ADDLS/BX-LR-default/four-AL-B-case structure and preserves all other52-byte state words. Original malformed table,full namespace/binding,required prototypes,actual primitive/bitfield ABI,field geometry,ordinary-C frontend and genuine wrong-C controls remain mandatory.',
      'Imported providers are bounded modeled call/borrow contracts; no provider/rendering/device/game scene body executes in caller fixtures,and no imported helper/storage credit is taken. Separate accepted20-byte getter ABI execution credits0 additional bytes. Field views are measured prefixes rather than complete unknown object/storage declarations. No unsupported semantic game names are inferred.',
      'All three residuals772B remain reserved and uncredited; shared coordinator acceptance alone grants source credit. Fresh source-only/copied-root canonical replay is required; all prior Ready/source/helper inputs remain unchanged.' ])
    write_json(EVIDENCE/'match.json',report);print(dict(functions=len(rows),bytes=report['canonicalMatchedBytes'],pairs=len(traces),genuineWrongC=len(negative),coveredInstructionBytes=report['fixtureCoveredOriginalInstructionBytes']),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--inputs-sha256',required=True);execute(parser.parse_args().inputs_sha256)
