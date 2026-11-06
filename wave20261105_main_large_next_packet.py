import argparse
import json
import re
import shutil
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256,now
from wave20261105_main_large_next_build import build
from wave20261105_main_large_next_controls import execute as binding_controls
from wave20261105_main_large_next_fixtures import execute as data_fixtures

LANE=ROOT/'evidence/lanes/parallel-wave20261104/main-arm-large/next'
WORK=ROOT/'work/w5mg/next/proof'
SOURCE=ROOT/'src/runtime/parallel_wave20261104/main-arm-large/next'
CONTRACT=['name','program','processor','module','mode','address','bytes','source','sourceSha256','sourceDependencies','targetSha256','compiler','compilerSha256','compilerFlags','nativeSymbolEntries']


def source_policy(entry):
    paths=[ROOT/entry['source'],*[ROOT/p['path'] for p in entry['sourceDependencies']]]
    pins={entry['source']:entry['sourceSha256'],**{p['path']:p['sha256'] for p in entry['sourceDependencies']}}
    includes=set()
    for path in paths:
        text=path.read_text()
        if not path.resolve().is_relative_to(SOURCE) or sha256(path)!=pins[path.relative_to(ROOT).as_posix()]:raise ValueError('Frozen ordinary C/include identity differs')
        if len(text.splitlines())>500 or '/*' in text or '//' in text or re.search(r'\b(?:asm|__asm|__asm__|INCBIN)\b',text):raise ValueError('Ordinary C/source policy failed')
        if re.search(r'^\s*#\s*include\s*<',text,re.M):raise ValueError('Implicit system include forbidden')
        includes.update((path.parent/name).resolve() for name in re.findall(r'^\s*#\s*include\s*"([^"<>]+)"',text,re.M))
    if includes!={p.resolve() for p in paths[1:]}:raise ValueError('Actual include closure differs')
    return dict(ordinaryC=True,commentFree=True,maximumFileLines=max(len(p.read_text().splitlines()) for p in paths),actualIncludesPinned=True)



def main():
    parser=argparse.ArgumentParser();parser.add_argument('--inputs-sha256',required=True);args=parser.parse_args()
    path=LANE/'inputs.json'
    if sha256(path)!=args.inputs_sha256:raise ValueError('Explicit immutable packet manifest changed')
    inputs=read_json(path)
    for pin in inputs['files']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Immutable packet input changed: '+pin['path'])
    matches=[]
    for entry in inputs['entries']:
        source_policy(entry)
        row,body=build(ROOT/entry['source'],WORK/format(int(entry['address'],0),'08x'))
        if any(row.get(k)!=entry.get(k) for k in CONTRACT):raise ValueError(('Fresh complete source/compiler/native/binding contract differs',row['address']))
        row.update(sourceLanguage='C',ordinaryCOnly=True,ordinaryCBytes=row['bytes'],justifiedAssemblyBytes=0,originalObjectScaffolding=False,originalDataSourceCredit=0,wholeModuleLinked=False,sourcePolicy=source_policy(entry),oracle=dict(supported=False,nativeAndCompiledReturningCalls=0,actualNativeHelperExecutions=0,limitations=['Exact ordinary C complete caller plus genuine link and original callsite module proofs; complete callers/callees/devices unexecuted.']))
        matches.append(row)
        print(dict(address=row['address'],bytes=row['bytes'],exactRealMwLink=True),flush=True)
    controls=binding_controls(matches);fixtures=data_fixtures(matches)
    full=read_json(LANE/'limit-fixtures.json')
    for row in matches:
        vectors=[v for v in full['records'] if v['address']==row['address']]
        if vectors:row['oracle']=dict(supported=True,supportedReturningVectors=len(vectors),nativeAndCompiledReturningCalls=2*len(vectors),actualNativeCalleeBodiesExecuted=0,nativeDevicesOrScenesExecuted=0,proof=(LANE/'limit-fixtures.json').relative_to(ROOT).as_posix(),traceSha256=fixtures['traceSha256'],helperCodeAndExtentCredit=0,originalDataStorageExtentAuthorshipCredit=0,limitations=fixtures['limits'])
    write_json(LANE/'binding-layout-controls.json',controls)
    report=dict(schemaVersion=1,createdUtc=now(),romSha256=configuration()['romSha256'],program='',processor='arm9',module='main',matches=matches,exactFunctions=len(matches),exactInitializedBytes=sum(r['bytes'] for r in matches),allPassed=True,acceptedSourceCredit=0,wholeModuleLinked=False,sourceReconstructionComplete=False,inputManifest=path.relative_to(ROOT).as_posix(),inputManifestSha256=sha256(path),generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=inputs['generatorSources'],actualNativeAndSourceCallerReturns=fixtures['nativeAndCompiledReturningCalls'],nativeCalleeBodiesExecuted=fixtures['actualNativeCalleeBodiesExecuted'],limitFixtureTraceSha256=fixtures['traceSha256'],replayCanonicalReportRefreshed=True,replayRoot=str(ROOT),sourceContractsUnchanged=True,wholeCNegativeControlsRejected=1,limits=['One complete1612B ordinary C floating-to-wide-text formatter compiles under pinned2.0/sp1p5 O4,p/file-IPA/inline-on-noauto and genuinely MW-links exactly. No object or instruction patch; compiler-emitted _dls symbol/actual canonical ARM target preserved.','Nine exact original wide-class/UTF16 literal ABS32 origins/words/zero-addends/data kinds and complete original array bytes/hash/element geometry qualify. Native decimal has32digits,size38; wide class masks0x200,bounds128. Original data storage/extent/authorship0credit.','Twenty-three actual compiler geometry checks,wrong36digit record,10branch/helper,108pointer and9changed-array controls reject. Wrong complete1612B C genuinely links, fails nativebytes and12 actual returning-null models while preserving ABI/memory.','Only60original/source precision>509 guard vectors120topreturns execute. Floating payload/conversion/rounding/copy/strlen/mbstowcs body, data array reads, callbacks, hardware and game scenes remain unexecuted.','Whole shared module/ROM/source acceptance remains coordinator-owned and separate.'])
    write_json(LANE/'match.json',report)
    print(dict(functions=len(matches),bytes=report['exactInitializedBytes'],inputsSha256=sha256(path)),flush=True)


if __name__=='__main__':main()
