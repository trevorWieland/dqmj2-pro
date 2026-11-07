import argparse
import hashlib
import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256,now
from wave20261106_ov006_resource_slot_source_second_paths import SOURCE,EVIDENCE,WORK,assert_owned
from wave20261106_ov006_resource_slot_source_second_build import build
from wave20261106_ov006_resource_slot_source_second_boundary import check as check_boundary
from wave20261106_ov006_resource_slot_source_second_models import check as check_models
from wave20261106_ov006_resource_slot_source_second_controls import execute as check_controls

CONTRACT=['name','program','processor','module','mode','address','bytes','source','sourceSha256','sourceDependencies','targetSha256','compiler','compilerSha256','compilerFlags','nativeSymbolEntries']


def source_policy(entry):
    paths=[ROOT/entry['source'],*[ROOT/p['path']for p in entry['sourceDependencies']]];pins={entry['source']:entry['sourceSha256'],**{p['path']:p['sha256']for p in entry['sourceDependencies']}};includes=set()
    for path in paths:
        text=path.read_text()
        if not path.resolve().is_relative_to(SOURCE.resolve())or sha256(path)!=pins[path.relative_to(ROOT).as_posix()]:raise ValueError('Frozen ordinary C/include differs')
        if len(text.splitlines())>500 or'/*'in text or'//'in text or re.search(r'\b(?:asm|__asm|__asm__|INCBIN)\b',text):raise ValueError('Ordinary C source policy failed')
        if re.search(r'^\s*#\s*include\s*<',text,re.M):raise ValueError('Implicit system include forbidden')
        includes.update((path.parent/name).resolve()for name in re.findall(r'^\s*#\s*include\s*"([^"<>]+)"',text,re.M))
    if includes!={p.resolve()for p in paths[1:]}:raise ValueError('Actual full include closure differs')
    return dict(ordinaryC=True,commentFree=True,maximumFileLines=max(len(p.read_text().splitlines())for p in paths),actualIncludesPinned=True)


def main():
    assert_owned();parser=argparse.ArgumentParser();parser.add_argument('--inputs-sha256',required=True);args=parser.parse_args();path=EVIDENCE/'inputs.json'
    if sha256(path)!=args.inputs_sha256:raise ValueError('Explicit immutable packet manifest changed')
    inputs=read_json(path)
    for pin in inputs['files']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Immutable packet input changed: '+pin['path'])
    boundary=check_boundary();matches=[];flats=[]
    for entry in inputs['entries']:
        source_policy(entry);row,body=build(ROOT/entry['source'],WORK/'proof'/entry['module']/format(int(entry['address'],0),'08x'))
        if any(row.get(k)!=entry.get(k)for k in CONTRACT):raise ValueError('Fresh whole source/compiler/native/import contract differs')
        row.update(sourceLanguage='C',ordinaryCOnly=True,ordinaryCBytes=row['bytes'],justifiedAssemblyBytes=0,originalObjectScaffolding=False,originalDataSourceCredit=0,wholeModuleLinked=False,sourcePolicy=source_policy(entry));matches.append(row);flats.append(body)
    models=check_models(matches,flats);controls=check_controls(matches)
    trace=hashlib.sha256(__import__('json').dumps(models['records'],sort_keys=True).encode()).hexdigest()
    for row in matches:row['oracle']=dict(supported=True,supportedReturningVectors=sum(r['address']==row['address']for r in models['records']),nativeAndCompiledReturningCalls=2*sum(r['address']==row['address']for r in models['records']),actualNativeCalleeBodiesExecuted=0,helperCodeAndExtentCredit=0,originalDataStorageExtentAuthorshipCredit=0,limitations=models['limits'],suppliedServiceBodyInstructionsExecuted=0)
    for name,value in[('boundary-proof.json',boundary),('caller-fixtures.json',models),('binding-layout-controls.json',controls)]:write_json(EVIDENCE/name,value)
    report=dict(importedPhysicalStateViews=models['physicalAliasExplicit'],schemaVersion=1,createdUtc=now(),romSha256=configuration()['romSha256'],program=matches[0]['program'],processor='arm9',modules=sorted({r['module']for r in matches}),mode='arm',matches=matches,exactFunctions=len(matches),exactInitializedBytes=sum(r['bytes']for r in matches),allPassed=True,acceptedSourceCredit=0,wholeModuleLinked=False,sourceReconstructionComplete=False,inputManifest=path.relative_to(ROOT).as_posix(),inputManifestSha256=sha256(path),generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=inputs['generatorSources'],actualNativeAndSourceCallerReturns=models['nativeAndCompiledReturningCalls'],actualNativeAndSourcePartialStops=0,nativeCalleeBodiesExecuted=0,callerFixtureTraceSha256=trace,replayCanonicalReportRefreshed=True,replayRoot=str(ROOT),sourceContractsUnchanged=True,wholeCNegativeControlsRejected=controls['wholeCNegativeControlsRejected'],suppliedServiceCalls=models['suppliedServiceCalls'],suppliedServiceBodyInstructionsExecuted=0,actualStandaloneOriginalEntryExecutions=0,limits=models['limits'])
    write_json(EVIDENCE/'match.json',report);print(dict(functions=len(matches),bytes=report['exactInitializedBytes'],returns=models['nativeAndCompiledReturningCalls'],wrongC=controls['wholeCNegativeControlsRejected']),flush=True)


if __name__=='__main__':main()
