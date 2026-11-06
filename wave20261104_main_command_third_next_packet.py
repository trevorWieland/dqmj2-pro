import argparse
import json
import re
import shutil
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256,now
from wave20261104_main_command_third_build import build
from wave20261104_main_command_third_next_controls import execute as binding_controls
from wave20261104_main_tail_bindings import verify_original
from wave20261104_main_command_third_next_data import execute as data_controls

LANE=ROOT/'evidence/lanes/parallel-wave20261104/main-command-third/next'
WORK=ROOT/'work/w4mc3/next/proof'
SOURCE=ROOT/'src/runtime/parallel_wave20261104/main-command-third/next'
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


def wrong_control(row):
    directory=WORK/'wrong-status'
    source=ROOT/row['source'];text=source.read_text()
    if text.count('status=0;')!=1:raise ValueError('Semantic wrong-status mutation not isolated')
    target=directory/'source.c';target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(text.replace('status=0;','status=1;'))
    shutil.copyfile(source.with_name('context.h'),target.with_name('context.h'))
    bad,body=build(target,directory/'build',True)
    verify_original(bad,bad['nativeSymbolEntries'])
    attempt=bad['realLink']['linkerAttempt']
    if attempt['exitCode']!=0 or bad['compiledBytes']!=row['bytes'] or bad['realLink'].get('exactCallerBytes') or sha256(directory/'build/l/caller.bin')==row['targetSha256']:
        raise ValueError('Wrong C did not genuinely compile/link same complete extent and fail native bytes')
    return dict(status='passed',positiveAddress=row['address'],mutation='Selected banked command status0 replaced by status1',wrongSource=target.relative_to(ROOT).as_posix(),wrongSourceSha256=sha256(target),compiledCompleteBytes=bad['compiledBytes'],genuineMwLinkExitCode=attempt['exitCode'],nativeByteGateRejected=True,originalBranchesAndModulesVerified=True,negativeCompilerResult=bad,executionCredit=0)


def wrong_flag_control(row):
    directory=WORK/'wrong-flag'
    target=directory/'source.c';target.parent.mkdir(parents=True,exist_ok=True)
    source=ROOT/row['source'];shutil.copyfile(source,target)
    text=source.with_name('context.h').read_text()
    if text.count('0x02102d78')!=1:raise ValueError('Measured original flag expression not isolated')
    target.with_name('context.h').write_text(text.replace('0x02102d78','0x02102d7c'))
    bad,body=build(target,directory/'build',True)
    verify_original(bad,bad['nativeSymbolEntries'])
    attempt=bad['realLink']['linkerAttempt']
    if attempt['exitCode']!=0 or bad['compiledBytes']!=row['bytes'] or bad['realLink'].get('exactCallerBytes') or sha256(directory/'build/l/caller.bin')==row['targetSha256']:
        raise ValueError('Wrong flag C did not genuinely compile/link complete extent and fail native')
    return dict(status='passed',address=row['address'],mutation='Measured byte flag data address02102d78 replaced by02102d7c',wrongHeaderSha256=sha256(target.with_name('context.h')),compiledCompleteBytes=bad['compiledBytes'],genuineMwLinkExitCode=attempt['exitCode'],nativeByteGateRejected=True,originalBranchesAndModulesVerified=True,negativeCompilerResult=bad,executionCredit=0)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--inputs-sha256',required=True);args=parser.parse_args()
    path=LANE/'inputs.json'
    if sha256(path)!=args.inputs_sha256:raise ValueError('Explicit immutable packet manifest changed')
    inputs=read_json(path)
    for pin in inputs['files']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Immutable packet input changed: '+pin['path'])
    context_origin=ROOT/'src/runtime/parallel_wave20261104/main-runtime-tail/context.h'
    if not (SOURCE/'context.h').read_text().startswith(context_origin.read_text()):raise ValueError('Measured frozen context contract not preserved')
    matches=[]
    for entry in inputs['entries']:
        source_policy(entry)
        row,body=build(ROOT/entry['source'],WORK/format(int(entry['address'],0),'08x'))
        if any(row.get(k)!=entry.get(k) for k in CONTRACT):raise ValueError(('Fresh complete source/compiler/native/binding contract differs',row['address']))
        row.update(sourceLanguage='C',ordinaryCOnly=True,ordinaryCBytes=row['bytes'],justifiedAssemblyBytes=0,originalObjectScaffolding=False,originalDataSourceCredit=0,wholeModuleLinked=False,sourcePolicy=source_policy(entry),oracle=dict(supported=False,nativeAndCompiledReturningCalls=0,actualNativeHelperExecutions=0,limitations=['Exact ordinary C complete caller plus genuine link and original callsite module proofs; complete callers/callees/devices unexecuted.']))
        matches.append(row)
        print(dict(address=row['address'],bytes=row['bytes'],exactRealMwLink=True),flush=True)
    negative=wrong_control(next(row for row in matches if row['address']=='0x204de70'));controls=binding_controls(matches);controls['measuredOriginalDataReferences']=data_controls();negative['wrongFlagControl']=wrong_flag_control(matches[0])
    write_json(LANE/'whole-c-controls.json',negative)
    write_json(LANE/'binding-layout-controls.json',controls)
    report=dict(schemaVersion=1,createdUtc=now(),romSha256=configuration()['romSha256'],program='',processor='arm9',module='main',matches=matches,exactFunctions=len(matches),exactInitializedBytes=sum(r['bytes'] for r in matches),allPassed=True,acceptedSourceCredit=0,wholeModuleLinked=False,sourceReconstructionComplete=False,inputManifest=path.relative_to(ROOT).as_posix(),inputManifestSha256=sha256(path),generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=inputs['generatorSources'],actualNativeAndSourceCallerReturns=0,nativeCalleeBodiesExecuted=0,replayCanonicalReportRefreshed=True,replayRoot=str(ROOT),sourceContractsUnchanged=True,wholeCNegativeControlsRejected=2,limits=['Complete configured native extents, ordinary readable C, actual pinned compiler and genuine MW links are exact.','Original relocation records independently qualify every imported address/module/mode; plural-overlay records remain refused, never guessed.','Sixteen actual compiler ABI assertions, wrong-stride and8 binding negatives, plus successfully compiled and real-linked semantic wrong-C status are separate controls.','No complete callers, native callees, hardware, scenes or game domains execute in this packet; behavioral execution and original storage credits remain zero.','Names, field roles and comparative interfaces retain inferred status; shared whole-module/ROM/source acceptance remains coordinator owned.'])
    write_json(LANE/'match.json',report)
    print(dict(functions=len(matches),bytes=report['exactInitializedBytes'],inputsSha256=sha256(path)),flush=True)


if __name__=='__main__':main()
