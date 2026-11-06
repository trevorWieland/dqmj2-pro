import argparse
import json
import re
import shutil
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256,now
from wave20261105_main_math_next_build import build
from wave20261105_main_math_next_controls import execute as binding_controls
from wave20261105_main_math_next_fixtures import execute as data_fixtures

LANE=ROOT/'evidence/lanes/parallel-wave20261105/main-math-next'
WORK=ROOT/'work/w5mn/proof'
SOURCE=ROOT/'src/runtime/parallel_wave20261105/main-math-next'
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
        if vectors:row['oracle']=dict(supported=True,supportedReturningVectors=len(vectors),nativeAndCompiledReturningCalls=2*len(vectors),actualNativeCalleeBodiesExecuted=0,nativeDevicesOrScenesExecuted=0,proof=(LANE/'caller-fixtures.json').relative_to(ROOT).as_posix(),traceSha256=fixtures['traceSha256'],helperCodeAndExtentCredit=0,originalDataStorageExtentAuthorshipCredit=0,limitations=fixtures['limits'])
    write_json(LANE/'binding-layout-controls.json',controls)
    report=dict(schemaVersion=1,createdUtc=now(),romSha256=configuration()['romSha256'],program='',processor='arm9',module='main',matches=matches,exactFunctions=len(matches),exactInitializedBytes=sum(r['bytes'] for r in matches),allPassed=True,acceptedSourceCredit=0,wholeModuleLinked=False,sourceReconstructionComplete=False,inputManifest=path.relative_to(ROOT).as_posix(),inputManifestSha256=sha256(path),generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=inputs['generatorSources'],actualNativeAndSourceCallerReturns=fixtures['nativeAndCompiledReturningCalls'],nativeCalleeBodiesExecuted=fixtures['actualNativeCalleeBodiesExecuted'],callerFixtureTraceSha256=fixtures['traceSha256'],replayCanonicalReportRefreshed=True,replayRoot=str(ROOT),sourceContractsUnchanged=True,wholeCNegativeControlsRejected=fixtures['wholeCNegativeControlsRejected'],actualStandaloneOriginalEntryExecutions=controls['actualStandaloneOriginalEntryExecutions'],limits=['Three complete ordinary C routines total 1832 B: unsigned64-to-decimal 204 B, decimal-to-double 1572 B and lazy runtime-state getter 56 B. Pinned 2.0/sp1p5 O4,p/file-IPA/inline-on-noauto genuinely links all full extents with 40 unchanged original relocations and measured same-program ARM namespaces.','MSL decimal has 32 digit bytes and size 38. Pure C sequencing preserves original length increment before the typed remainder call. Seven compiler-emitted floating helpers retain actual canonical entries; the explicit numeric unsigned64 alternate entry revalidates its unchanged existing certificate. No new alias, algorithm ASM or object/instruction patch.','Original binary32 infinity, double[8] powers and char[37] max-digit arrays preserve exact bytes, typed geometry and ABS32 origins/addends/kinds. The BSS runtime-state view declares only measured fields at offsets 4 and 20, with original storage extent/authorship uncredited. A separate original caller/callee instruction and full-body proof establishes incoming R0=1 consumed through signed low-eight-bit conversion.','25 actual compiler layout checks and wrong layouts, 69 helper/entry namespace controls, 48 pointer controls, 3 changed-array controls and 8 argument-provenance controls pass. Three wrong complete C bodies preserve their original extents, genuinely link and produce 48 actual returning model violations.','128 original/source vectors and 256 caller returns cover zero-input decimal output, signed quiet-NaN decimal return and already-initialized runtime getter state. Another 16 standalone original unsigned64 entry controls execute independently. No finite decimal payload, nonzero unsigned64 caller-helper path, lazy initialization call, array read, hardware or scene execution is claimed; all callee and external storage source credit remains zero. Shared acceptance is coordinator-owned.'])
    write_json(LANE/'match.json',report)
    print(dict(functions=len(matches),bytes=report['exactInitializedBytes'],inputsSha256=sha256(path)),flush=True)


if __name__=='__main__':main()
