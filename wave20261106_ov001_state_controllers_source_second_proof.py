import argparse
import gzip
import json
from pathlib import Path
import match_runtime as C
import unicorn
from project import ROOT,read_json,write_json,sha256,configuration
from wave20261106_ov001_state_controllers_source_second_paths import SOURCE,EVIDENCE,WORK,assert_owned
from wave20261106_ov001_state_controllers_source_second_build import build
from wave20261106_ov001_state_controllers_source_second_models import fixtures
from wave20261106_ov001_state_controllers_source_second_execution import run
from wave20261106_ov001_state_controllers_source_second_controls import execute as controls
WORK=WORK/'proof1'


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
 selected={entry:[f for f in fixtures()if f['entry']==entry]for entry in [0x02213da8,0x02213ee0]}
 changes=[
 (0x02213da8,'return 0;','return 1;',1,'main.c'),
 (0x02213ee0,'return 0;','return 1;',1,'main.c'),
 (0x02213da8,'if (native_fn_ov001_021db8d0','if (!native_fn_ov001_021db8d0',1,'main.c'),
 (0x02213da8,'== 0x31','== 0x30',1,'main.c'),
 (0x02213da8,'= native_fn_ov001_021e9610(0);','= native_fn_ov001_021e9610(1);',1,'main.c'),
 (0x02213da8,'native_fn_ov001_021e9610(native_data_ov001_0222f1c8);','native_fn_ov001_021e9610((s8)native_data_ov001_0222f1c8);',1,'main.c'),
 (0x02213da8,'[native_data_ov001_02242aac.selector0]','[0]',2,'main.c'),
 (0x02213da8,'extern u8 native_data_ov001_0222f1c8;','extern u32 native_data_ov001_0222f1c8;',1,'context.h'),
 (0x02213ee0,'SignedEntryView12 { s8 value0;','SignedEntryView12 { u8 value0;',1,'context.h'),
 (0x02213ee0,'counter3 > 30','counter3 >= 30',1,'main.c'),
 (0x02213ee0,'counter3 > 15','counter3 >= 15',1,'main.c'),
 (0x02213ee0,'field1e4 == 0','field1e4 != 0',1,'main.c'),
 (0x02213ee0,'.value0,1,0,1)','.value0,1,0,0)',1,'main.c'),
 (0x02213ee0,'actor4,4,1)','actor4,4,2)',1,'main.c'),
 ]
 return [(entry,old,new,selected[entry],count,filename)for entry,old,new,count,filename in changes]


def wrong_c(case,ordinal,images):
    entry,old,new,selected,count,filename=case;tag=format(entry,'08x');directory=WORK/'n'/str(ordinal)/tag
    if not selected:raise ValueError(('Meaningful wrong-C fixture absent',tag,old))
    directory.mkdir(parents=True,exist_ok=True)
    for path in(SOURCE/tag).iterdir():
        if path.is_file():(directory/path.name).write_bytes(path.read_bytes())
    source=directory/filename;text=source.read_text()
    if text.count(old)!=count:raise ValueError(('Exact wrong-C source mutation ambiguous',tag,old,text.count(old),count))
    source.write_text(text.replace(old,new));row,body=build(directory/'main.c',directory/'build',True);rejections=[]
    for n,f in enumerate(selected):
        try:
            result=run(row,body,f,images,n)
            if not result['modelFailures']:continue
            rejections.append(dict(actualTopReturn=result['actualTopReturn'],modelFailures=result['modelFailures']))
        except unicorn.UcError as error:rejections.append(dict(actualTopReturn=False,rejectedAtMemoryBoundary=True,error=str(error)))
    if not rejections:raise ValueError(('Genuine wrong C retained every independent bounded fixture',tag,old))
    return dict(ordinal=ordinal,caller=hex(entry),old=old,new=new,sourceOccurrences=count,mutatedFile=filename,fixtures=selected,genuineWrongC=row,rejected=rejections,sourceCredit=0,abortedRunsAreNotCallerReturns=True)


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
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],program='',processor='arm9',module='ov001',mode='arm',allPassed=True,matches=rows,canonicalMatchedFunctions=len(rows),canonicalMatchedBytes=sum(r['bytes']for r in rows),acceptedSourceCredit=0,wholeModuleLinked=False,sourceReconstructionComplete=False,cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),actualNativeAndSourcePartialStops=0,nativeCalleeBodiesExecutedInCallerFixtures=0,nativeCalleeBodiesExecuted=0,nativeCalleeBodyExecutionCountScope='caller-fixtures-only',actualStandaloneOriginalEntryExecutions=30,separateActualNativeHelperReturnCredit=0,nativeSymbols={n:b['address']for n,b in symbols.items()},nativeSymbolModules={n:b['module']for n,b in symbols.items()},nativeSymbolEntries=symbols,nativeSymbolBindings=symbols,fixtureInstructionCoverage=covered,fixtureCoveredOriginalInstructionBytes=sum(r['executedOriginalInstructionBytes']for r in covered),negativeEvidence=negative,wholeCNegativeControlsRejected=len(negative),controls=dict(path=(EVIDENCE/'controls.json').relative_to(ROOT).as_posix(),sha256=sha256(EVIDENCE/'controls.json')),inputs=dict(path=path.relative_to(ROOT).as_posix(),sha256=sha256(path)),inputManifest=path.relative_to(ROOT).as_posix(),inputManifestSha256=sha256(path),generatorSources=inputs['generatorSources'],generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=C.sha(raw)),callerFixtureTraceSha256=C.sha(raw),producer=Path(__file__).name,producerSha256=sha256(__file__),sourceContractsUnchanged=True,limits=[
      'Two complete admitted OV001 ARMv5TE functions712B=688instruction+24literal bytes;28 original relocations;actual pinned MW2.0/base O2/off/speed/C99/noIPA. No attributes/register/volatile/flag/object/relocation/normalizer edits or allocation search.',
      'Independent complete returning fixtures cover all entry-reachable instructions,signed counters/record words,12-byte stride selectors,nullable status,positive/negative branches,five-word callback ABI and original return values. Bounded provider mutations qualify pointer/table/cache reloads rather than physical provider behavior.',
      'One initialized borrowed scalar byte0222f1c8 is independently qualified at exact original ABS32/LDR/STRB/LDRB origins with16 binding/type/actual-word controls and compiler declaration negatives. Adjacent bytes are preserved; cache/BSS/record storage receives0credit.',
      'Existing24-byte swap-byte helper executes thirty independent original input/old-byte cases with0additional credit; all provider bodies are modeled in caller fixtures. Fullgenuine links,strictC99/type/prototype/boundary/negative/source-only copied-root checks remain mandatory. First8/2132 and all older source/Ready inputs remain immutable.' ])
    write_json(EVIDENCE/'match.json',report);print(dict(functions=len(rows),bytes=report['canonicalMatchedBytes'],pairs=len(traces),genuineWrongC=len(negative),coveredInstructionBytes=report['fixtureCoveredOriginalInstructionBytes']),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--inputs-sha256',required=True);execute(parser.parse_args().inputs_sha256)
