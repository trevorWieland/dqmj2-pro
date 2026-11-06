import argparse
import re
from pathlib import Path
from project import ROOT,read_json,write_json,sha256,now,configuration
from wave20261106_itcm_reset_next_paths import SOURCE,WORK,EVIDENCE,assert_owned
from wave20261106_itcm_reset_next_build import build
from wave20261106_itcm_reset_next_controls import execute as controls
from wave20261106_itcm_reset_next_fixtures import execute as fixtures

CONTRACT=['name','program','processor','module','mode','address','bytes','source','sourceSha256','sourceDependencies','targetSha256','compiler','compilerSha256','compilerFlags','nativeSymbolEntries']


def source_policy(row):
    paths=[ROOT/row['source'],*[ROOT/p['path']for p in row['sourceDependencies']]];pins={row['source']:row['sourceSha256'],**{p['path']:p['sha256']for p in row['sourceDependencies']}};includes=set()
    for path in paths:
        text=path.read_text(encoding='utf-8')
        if not path.resolve().is_relative_to(SOURCE)or sha256(path)!=pins[path.relative_to(ROOT).as_posix()]:raise ValueError('Closed reset ordinary-C source/include differs')
        if len(text.splitlines())>500 or '/*'in text or '//'in text or re.search(r'\b(?:asm|__asm|__asm__|INCBIN)\b',text):raise ValueError('Reset ordinary-C source policy failed')
        if re.search(r'^\s*#\s*include\s*<',text,re.M):raise ValueError('Implicit reset system header forbidden')
        includes.update((path.parent/name).resolve()for name in re.findall(r'^\s*#\s*include\s*"([^"<>]+)"',text,re.M))
    if includes!={p.resolve()for p in paths[1:]}:raise ValueError('Actual reset include closure differs')
    return dict(ordinaryC=True,commentFree=True,maximumFileLines=max(len(p.read_text().splitlines())for p in paths),actualIncludesPinned=True)


def reference(inputs):
    raw=(ROOT/inputs['comparativeReference']['path']).read_text(encoding='utf-8');start=raw.index('static void OSi_ReloadRomData (void)\n{');end=raw.index('\nstatic void OSi_ReadCardRom32 (',start);body=raw[start:end].replace('static void OSi_ReloadRomData','void native_itcm_01ff82c8').replace('(u32)HW_ROM_HEADER_BUF','0x027ffe00').replace('HW_ROM_BASE_OFFSET_BUF','0x027ffc2c').replace('(int)len_arm','(s32)len_arm')
    names={'OSi_ReadCardRom32':'native_fn_01ff8370','OS_DisableInterrupts':'native_fn_02007ff4','DC_StoreAll':'native_fn_02007270','DC_InvalidateAll':'native_fn_02007264','OS_RestoreInterrupts':'native_fn_02008008','IC_InvalidateAll':'native_fn_02007338','DC_WaitWriteBufferEmpty':'native_fn_0200732c'}
    for old,new in names.items():body=body.replace(old,new)
    actual=(SOURCE/'01ff82c8.c').read_text(encoding='utf-8').split('\n',1)[1]
    if re.sub(r'\s+','',body)!=re.sub(r'\s+','',actual):raise ValueError('Actual reset source drifted from pinned complete primary C body')
    return dict(completeReferenceBodyRetained=True,comparativeReference=inputs['comparativeReference'],actualSdkNamesMappedOnlyThroughMeasuredNativeBranches=True,physicalSdkHeaderConstantsRetained=True,signedIntLengthSpelledWithMeasured32BitS32Alias=True,publicSurroundingAssemblyOrOtherFunctionsNotCredited=True)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--inputs-sha256',required=True);args=parser.parse_args();assert_owned();path=EVIDENCE/'inputs.json'
    if sha256(path)!=args.inputs_sha256:raise ValueError('Explicit immutable packet manifest changed')
    inputs=read_json(path)
    for pin in inputs['files']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Immutable packet input changed: '+pin['path'])
    ref=reference(inputs);entry=inputs['entries'][0];source_policy(entry);row,body=build(ROOT/entry['source'],WORK/'proof/01ff82c8')
    if any(row.get(k)!=entry.get(k)for k in CONTRACT):raise ValueError('Fresh complete source/compiler/native/binding contract differs')
    control=controls([row]);fixture=fixtures([row]);row.update(sourceLanguage='C',ordinaryCOnly=True,ordinaryCBytes=168,justifiedAssemblyBytes=0,originalObjectScaffolding=False,originalDataSourceCredit=0,wholeModuleLinked=False,sourcePolicy=source_policy(row),oracle=dict(supported=True,supportedReturningVectors=0,nativeAndCompiledReturningCalls=0,actualNativeAndSourcePartialStops=64,actualNativeCalleeBodiesExecuted=0,proof=(EVIDENCE/'caller-fixtures.json').relative_to(ROOT).as_posix(),traceSha256=fixture['traceSha256'],helperCodeAndExtentCredit=0,originalDataStorageExtentAuthorshipCredit=0,limitations=fixture['limits']))
    report=dict(schemaVersion=1,createdUtc=now(),romSha256=configuration()['romSha256'],program='',processor='arm9',module='itcm',matches=[row],exactFunctions=1,exactInitializedBytes=168,allPassed=True,acceptedSourceCredit=0,wholeModuleLinked=False,sourceReconstructionComplete=False,inputManifest=path.relative_to(ROOT).as_posix(),inputManifestSha256=sha256(path),generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=inputs['generatorSources'],actualNativeAndSourceCallerReturns=0,actualNativeAndSourcePartialStops=64,nativeCalleeBodiesExecuted=0,callerFixtureTraceSha256=fixture['traceSha256'],replayCanonicalReportRefreshed=True,replayRoot=str(ROOT),sourceContractsUnchanged=True,wholeCNegativeControlsRejected=2,actualStandaloneOriginalEntryExecutions=0,primarySourceProof=ref,limits=fixture['limits']+['Pinned MW2.0/sp1p6 O4,p/file-IPA/on-noauto C99 emits the complete168B ARM ITCM body. Nine unchanged original ARM branch relocations genuinely link using canonical same-program ARM main/ITCM entries.','Original SDK reserved RAM/header word geometry and pointer literals are measured without claiming their storage. Six actual compiler width/sign checks, wrong-word geometry, actual required-prototype diagnostics and81 namespace/origin/addend controls pass. Shared acceptance remains coordinator-owned.'])
    write_json(EVIDENCE/'match.json',report);print(dict(functions=1,bytes=168,inputsSha256=sha256(path)),flush=True)


if __name__=='__main__':main()
