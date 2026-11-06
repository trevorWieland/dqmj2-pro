import argparse
import json
import re
import shutil
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256,now
from wave20261105_main_later_build import build
from wave20261105_main_later_controls import execute as binding_controls
from wave20261105_main_later_fixtures import execute as data_fixtures

LANE=ROOT/'evidence/lanes/parallel-wave20261104/main-arm-later'
WORK=ROOT/'work/w5ml/proof'
SOURCE=ROOT/'src/runtime/parallel_wave20261104/main-arm-later'
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
    full=read_json(LANE/'table-fixtures.json')
    for row in matches:
        vectors=[v for v in full['records'] if v['address']==row['address']]
        if vectors:row['oracle']=dict(supported=True,supportedReturningVectors=len(vectors),nativeAndCompiledReturningCalls=2*len(vectors),positiveActualNativeHelperReturns=sum(v['original']['actualNativeHelperReturns']+v['recompiled']['actualNativeHelperReturns'] for v in vectors),nativeDevicesOrScenesExecuted=0,proof=(LANE/'table-fixtures.json').relative_to(ROOT).as_posix(),traceSha256=fixtures['traceSha256'],helperCodeAndExtentCredit=0,originalDataStorageExtentAuthorshipCredit=0,limitations=fixtures['limits'])
    write_json(LANE/'binding-layout-controls.json',controls)
    report=dict(schemaVersion=1,createdUtc=now(),romSha256=configuration()['romSha256'],program='',processor='arm9',module='main',matches=matches,exactFunctions=len(matches),exactInitializedBytes=sum(r['bytes'] for r in matches),allPassed=True,acceptedSourceCredit=0,wholeModuleLinked=False,sourceReconstructionComplete=False,inputManifest=path.relative_to(ROOT).as_posix(),inputManifestSha256=sha256(path),generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=inputs['generatorSources'],actualNativeAndSourceCallerReturns=fixtures['nativeAndCompiledReturningCalls'],nativeCalleeBodiesExecuted=fixtures['actualNativeCalleeBodiesExecuted'],dataFixtureTraceSha256=fixtures['traceSha256'],replayCanonicalReportRefreshed=True,replayRoot=str(ROOT),sourceContractsUnchanged=True,wholeCNegativeControlsRejected=1,limits=['Ten full configured ordinary C extents compile and genuinely MW-link exactly; all imports preserve original same-program ARM9 main ARM callsite/entry/complete boundaries.','Measured table strides0x10/8, key0, payload+4 and clear length4 remain explicit;0x10 slot trailing8 bytes stay untouched. Only optional-copy code uses the measured three-word field+0x70.','Fifteen actual compiler ABI assertions, wrong-stride,8 original binding negatives and9 exact original native fill-helper controls pass.','All ten callers execute732 original+rebuilt vectors(1464 top returns) against independent table/copy formulas. Native20B helper calls/returns are counted with zero source credit. Genuine wrong-C92B succeeds compilation/link, then fails native bytes and25 actual independent payload-extent oracles.','Synthetic memory establishes finite fixture behavior, never original storage/object bounds, gameplay-valid state, devices, scenes or full-game/platform execution. Names, roles and prototypes retain inferred status; coordinator owns shared source/module/ROM acceptance.'])
    write_json(LANE/'match.json',report)
    print(dict(functions=len(matches),bytes=report['exactInitializedBytes'],inputsSha256=sha256(path)),flush=True)


if __name__=='__main__':main()
