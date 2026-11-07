import argparse
import gzip
import json
from pathlib import Path
import match_runtime as C
import unicorn
from project import ROOT,read_json,write_json,sha256,configuration
from wave20261106_ov001_large_controller_source_abi_clean_paths import SOURCE,EVIDENCE,WORK,assert_owned
from wave20261106_ov001_large_controller_source_abi_clean_build import build
from wave20261106_ov001_large_controller_source_abi_clean_models import fixtures
from wave20261106_ov001_large_controller_source_abi_clean_execution import run
from wave20261106_ov001_large_controller_source_abi_clean_controls_v2 import execute as controls
WORK=WORK/'v4'


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
    selected=fixtures();entry=0x0222c338
    return[(entry,old,new,selected,count)for old,new,count in[
      ('0xd7','0xd6',1),('counter7 > 30','counter7 >= 30',2),('counter7 > 45','counter7 >= 45',1),('counter7++;','counter7 += 2;',3),('selector0, i','selector0, 0',2),('object, 8, 1, -1, 0','object, 9, 1, -1, 0',1),('object->field234','(u8)object->field234',1),('field1 = 7','field1 = 6',1),('state8 = 20','state8 = 21',1),('state8 = 40','state8 = 41',1),('native_fn_ov001_021f1414(native_data_022497e8.selector0))','native_fn_ov001_021f1414(native_data_022497e8.selector0) ^ 1)',1),('return 0;','return 1;',1),('i < 3','i < 2',2)]]


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
            if not result['modelFailures']:continue
            rejections.append(dict(actualTopReturn=result['actualTopReturn'],modelFailures=result['modelFailures']))
        except unicorn.UcError as error:rejections.append(dict(actualTopReturn=False,rejectedAtMemoryBoundary=True,error=str(error)))
    if not rejections:raise ValueError(('Genuine wrong C retained every independent bounded fixture',tag,old))
    return dict(ordinal=ordinal,caller=hex(entry),old=old,new=new,sourceOccurrences=count,fixtures=selected,genuineWrongC=row,rejected=rejections,sourceCredit=0,abortedRunsAreNotCallerReturns=True)


def execute(expected):
    assert_owned(EVIDENCE);path=EVIDENCE/'inputs-v2.json'
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
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],program='',processor='arm9',module='ov001',mode='arm',allPassed=True,matches=rows,canonicalMatchedFunctions=len(rows),canonicalMatchedBytes=sum(r['bytes']for r in rows),acceptedSourceCredit=0,wholeModuleLinked=False,sourceReconstructionComplete=False,cases=len(traces),actualNativeAndSourceCallerReturns=2*len(traces),actualNativeAndSourcePartialStops=0,nativeCalleeBodiesExecutedInCallerFixtures=0,nativeCalleeBodiesExecuted=0,nativeCalleeBodyExecutionCountScope='caller-fixtures-only',actualStandaloneOriginalEntryExecutions=39,separateActualNativeHelperReturnCredit=0,nativeSymbols={n:b['address']for n,b in symbols.items()},nativeSymbolModules={n:b['module']for n,b in symbols.items()},nativeSymbolEntries=symbols,nativeSymbolBindings=symbols,fixtureInstructionCoverage=covered,fixtureCoveredOriginalInstructionBytes=sum(r['executedOriginalInstructionBytes']for r in covered),negativeEvidence=negative,wholeCNegativeControlsRejected=len(negative),controls=dict(path=(EVIDENCE/'controls.json').relative_to(ROOT).as_posix(),sha256=sha256(EVIDENCE/'controls.json')),inputs=dict(path=path.relative_to(ROOT).as_posix(),sha256=sha256(path)),inputManifest=path.relative_to(ROOT).as_posix(),inputManifestSha256=sha256(path),generatorSources=inputs['generatorSources'],generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=C.sha(raw)),callerFixtureTraceSha256=C.sha(raw),producer=Path(__file__).name,producerSha256=sha256(__file__),sourceContractsUnchanged=True,limits=[
      'One complete admitted OV001 ARMv5TE function484B=480instruction+4literal bytes;13 original relocations;actual pinned MW2.0/base O2/off/speed/C99/noIPA. The two independently measured stage loops use separate lexical object/index lifetimes; no registers/volatile/flags/objects/relocations/normalizers patched and no allocation grid.',
      'Corrected1414return-to1438argument dataflow is explicit and independently checked.81 independent original/fresh caller pairs cover initial/unknown/terminal states,all30/45 counter boundaries,unsigned-byte wrap,three actual bank slots,invalid selectors/null records,signed-byte+0x234,5-word notification ABI and complete shared BSS/borrowed bytes. Provider mutations are modeled reload/borrow witnesses,not claims about physical game/provider behavior.',
      'The exact four-bank/three-slot getter,status fields and40-byte getter are separately executed with0callee/storage credit. In caller fixtures imported bodies remain modeled boundaries; only this484-byte caller gains pending source credit after shared acceptance.',
      'Closed ordinary C99/header/source/type/prototype/binding/boundary/genuine wrong-C and fresh copied-root proofs are mandatory. First2/520 and all earlier Ready/source/helper/input pins remain immutable. Further11/3452 admitted bytes remain uncredited.' ])
    write_json(EVIDENCE/'match.json',report);print(dict(functions=len(rows),bytes=report['canonicalMatchedBytes'],pairs=len(traces),genuineWrongC=len(negative),coveredInstructionBytes=report['fixtureCoveredOriginalInstructionBytes']),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--inputs-sha256',required=True);execute(parser.parse_args().inputs_sha256)
