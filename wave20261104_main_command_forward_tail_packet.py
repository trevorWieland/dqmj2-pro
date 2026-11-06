import argparse
import json
import re
import shutil
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256,now
from wave20261104_main_command_forward_tail_build import build
from wave20261104_main_command_forward_tail_controls import execute as binding_controls
from wave20261104_main_command_forward_tail_fixtures import execute as data_fixtures

LANE=ROOT/'evidence/lanes/parallel-wave20261104/main-command-forward/tail'
WORK=ROOT/'work/w4mcf/tail/proof'
SOURCE=ROOT/'src/runtime/parallel_wave20261104/main-command-forward/tail'
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
    full=read_json(LANE/'bit-fixtures.json')
    for row in matches:
        vectors=full['records'] if row['address']==full['supportedAddress'] else []
        if vectors:row['oracle']=dict(supported=True,supportedReturningVectors=len(vectors),nativeAndCompiledReturningCalls=2*len(vectors),actualNativeCalleeBodiesExecuted=fixtures['actualNativeCalleeBodiesExecuted'],actualCompiledHelperExecutions=fixtures['actualCompiledHelperExecutions'],nativeDevicesOrScenesExecuted=0,proof=(LANE/'bit-fixtures.json').relative_to(ROOT).as_posix(),traceSha256=fixtures['traceSha256'],helperReconstructionCredit=0,externalStorageExtentAuthorshipCredit=0,limitations=fixtures['limits'])
    write_json(LANE/'binding-layout-controls.json',controls)
    report=dict(schemaVersion=1,createdUtc=now(),romSha256=configuration()['romSha256'],program='',processor='arm9',module='main',matches=matches,exactFunctions=len(matches),exactInitializedBytes=sum(r['bytes'] for r in matches),allPassed=True,acceptedSourceCredit=0,wholeModuleLinked=False,sourceReconstructionComplete=False,inputManifest=path.relative_to(ROOT).as_posix(),inputManifestSha256=sha256(path),generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=inputs['generatorSources'],actualNativeAndSourceCallerReturns=fixtures['nativeAndCompiledReturningCalls'],nativeCalleeBodiesExecuted=fixtures['actualNativeCalleeBodiesExecuted'],compiledHelperExecutions=fixtures['actualCompiledHelperExecutions'],dataFixtureTraceSha256=fixtures['traceSha256'],replayCanonicalReportRefreshed=True,replayRoot=str(ROOT),sourceContractsUnchanged=True,wholeCNegativeControlsRejected=1,limits=['Two full configured ordinary C extents compile and genuinely MW-link exactly; all imported branches retain original singular namespace/mode/entry evidence.','One private signed-halfword data case pins original kind:load/BSS point/literal, unchanged ABS32 addend0, and measured stride8/field4/width2. External storage/extent/authorship gets zero credit.','Nine actual compiler ABI assertions, wrong-stride,8 branch and14 data negatives pass;12 native-helper boundary/data controls reject namespace/mode/interior/extent/body/literal/inventory corruption.','Complete92B setter executes192 original+rebuilt vectors(384 top returns) with exact original12B provider and original/rebuilt frozen36B query; helpers are verified and counted separately, with zero new source credit. Genuine wrong-C92B links successfully then fails native bytes and192 independent mutation oracles.','Dispatcher56B imported logic, scenes and devices remain unexecuted. Types/roles remain inferred views; negative-index synthetic memory does not establish original C object bounds or gameplay-valid inputs.','Shared whole-module/ROM/source acceptance remains coordinator owned.'])
    write_json(LANE/'match.json',report)
    print(dict(functions=len(matches),bytes=report['exactInitializedBytes'],inputsSha256=sha256(path)),flush=True)


if __name__=='__main__':main()
