import argparse
import json
import re
import shutil
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256,now
from wave20261105_gamespy_thumb_next_list_build import build
from wave20261105_gamespy_thumb_next_list_controls import execute as binding_controls
from wave20261105_gamespy_thumb_next_list_fixtures import execute as data_fixtures

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-thumb-next/list'
WORK=ROOT/'work/w5gt/list/proof'
SOURCE=ROOT/'src/runtime/parallel_wave20261105/gamespy-thumb-next/list'
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
    full=read_json(LANE/'caller-fixtures.json')
    for row in matches:
        vectors=[v for v in full['records'] if v['address']==row['address']]
        if vectors:row['oracle']=dict(supported=True,supportedReturningVectors=len(vectors),nativeAndCompiledReturningCalls=2*len(vectors),actualNativeCalleeBodiesExecuted=2*sum(v['actualOriginalHelperInvocations'] for v in vectors),nativeDevicesOrScenesExecuted=0,proof=(LANE/'caller-fixtures.json').relative_to(ROOT).as_posix(),traceSha256=fixtures['traceSha256'],helperCodeAndExtentCredit=0,originalDataStorageExtentAuthorshipCredit=0,limitations=fixtures['limits'])
    write_json(LANE/'binding-layout-controls.json',controls)
    report=dict(schemaVersion=1,createdUtc=now(),romSha256=configuration()['romSha256'],program='',processor='arm9',module='main',mode='thumb',matches=matches,exactFunctions=len(matches),exactInitializedBytes=sum(r['bytes'] for r in matches),allPassed=True,acceptedSourceCredit=0,wholeModuleLinked=False,sourceReconstructionComplete=False,inputManifest=path.relative_to(ROOT).as_posix(),inputManifestSha256=sha256(path),generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=inputs['generatorSources'],actualNativeAndSourceCallerReturns=fixtures['nativeAndCompiledReturningCalls'],nativeCalleeBodiesExecuted=fixtures['actualNativeCalleeBodiesExecuted'],callerFixtureTraceSha256=fixtures['traceSha256'],replayCanonicalReportRefreshed=True,replayRoot=str(ROOT),sourceContractsUnchanged=True,wholeCNegativeControlsRejected=fixtures['wholeCNegativeControlsRejected'],actualStandaloneOriginalEntryExecutions=controls.get('actualStandaloneOriginalEntryExecutions',0),limits=['Eight complete ordinary C GameSpy server-list append/search/dead-list/removal/reference-string routines genuinely MW-link under measured2.0/base Thumb O4,p/file-IPA/inline-on-noauto. Full extents and original canonical Thumb call payloads remain unchanged.','Actual compiler geometry checks2012-byte list,44-byte server,next pointer offset36,callback/instance slots1160/1172,dead-list slot2008 and8-byte reference-string view. Two wrong field-layout controls reject; unused field meanings remain comparative.','Independent bounded models exercise first pointer/IP-and-port matches in0..4 arrays including duplicates, raw native port values, empty/nonempty dead-list insertion and empty dead-list free. Three same-extent full wrong C units genuinely link and actually return model violations.','Actual allocation, nonempty heap frees, reference-table/count mutation and dynamic append/remove callback dispatch remain unexecuted, as do devices/network/scenes and complete external storage extent/authorship. Existing native helper bodies carry0 additional source credit; shared acceptance remains coordinator-owned.'])
    write_json(LANE/'match.json',report)
    print(dict(functions=len(matches),bytes=report['exactInitializedBytes'],inputsSha256=sha256(path)),flush=True)


if __name__=='__main__':main()
