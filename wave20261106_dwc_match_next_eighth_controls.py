from wave20261106_dwc_match_next_eighth_paths import assert_owned,EVIDENCE,SOURCE as OWN_SOURCE,WORK as OWN_WORK
import os
import shutil
import subprocess
from project import ROOT,write_json,sha256
from wave20261106_dwc_match_next_eighth_compiler import COMPILER
from wave20261106_dwc_match_next_eighth_bindings import verify_original,negative_controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/dwc-match-next/eighth'


def geometry(row):
    assert_owned(LANE,OWN_SOURCE)
    if not (ROOT/row["source"]).resolve().is_relative_to(OWN_SOURCE.resolve()):raise ValueError("Record layout source escaped exact own directory")
    folder=ROOT/'work/w6dm/eighth/geometry'/format(int(row['address'],0),'08x');folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    text=(folder/'context.h').read_text();checks=['sizeof(void*)==4','sizeof(u32)==4']+(['sizeof(GPRecvBuddyMessageArg)==12','(u32)&((GPRecvBuddyMessageArg*)0)->profile==0','(u32)&((GPRecvBuddyMessageArg*)0)->date==4','(u32)&((GPRecvBuddyMessageArg*)0)->message==8','(u32)&((DWCCorePrefix*)0)->state==0x24','(u32)&((DWCCorePrefix*)0)->matchcnt.qr2MatchType==0x38d','DWC_MATCHING_VERSION==3'] if int(row['address'],0)==0x209c188 else ['sizeof(DWCFriendData)==12','sizeof(DWCFriendGlobals)==16','(u32)&((DWCFriendGlobals*)0)->control==12','(u32)&((DWCFriendPrefix*)0)->friendListChanged==29','(u32)&((DWCFriendPrefix*)0)->deleteCallback==60','(u32)&((DWCFriendPrefix*)0)->deleteParam==64'])
    source=folder/'layout.c';source.write_text('#include "context.h"\n#undef serverreqs\n'+'\n'.join('typedef char Layout'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(checks)));obj=folder/'layout.o';command=[str(COMPILER),*row['compilerFlags'],'-c',str(source),'-o',str(obj)]
    def compile_layout():return subprocess.run(command,cwd=ROOT,capture_output=True,text=True,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),timeout=60)
    process=compile_layout()
    if process.returncode:raise ValueError(('Actual Thumb structure geometry failed',row['address'],process.stdout,process.stderr))
    result=dict(address=row['address'],checks=checks,positiveExitCode=0,objectSha256=sha256(obj))
    wrong=text.replace('int profile;unsigned int date;char*message;','int profile;char*message;unsigned int date;',1) if int(row['address'],0)==0x209c188 else text.replace('u32 gpProcessCount;','u32 wrongPadding,gpProcessCount;',1)
    if wrong==text:raise ValueError('Wrong GP callback-prefix layout did not mutate')
    (folder/'context.h').write_text(wrong);bad=compile_layout()
    if bad.returncode==0:raise ValueError('Wrong GP callback-prefix layout accepted')
    result.update(wrongLayoutRejected=True,negativeExitCode=bad.returncode,negativeStdout=bad.stdout)
    return result


def prototype_presence(row):
    from elftools.elf.elffile import ELFFile
    assert_owned(LANE,OWN_SOURCE)
    folder=ROOT/'work/w6dm/eighth/required-prototypes'/format(int(row['address'],0),'08x');folder.mkdir(parents=True,exist_ok=True)
    def code_sections(path):
        with path.open('rb') as stream:return [(s.name,s.data().hex()) for s in ELFFile(stream).iter_sections() if s['sh_flags']&4]
    flags=[*row['compilerFlags'],'-requireprotos','-w','error'];source=ROOT/row['source'];obj=folder/'explicit.o';command=[str(COMPILER),*flags,'-c',str(source),'-o',str(obj)];env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'));positive=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if positive.returncode or code_sections(obj)!=code_sections(ROOT/row['object']):raise ValueError(('Required real prototypes failed or changed caller executable sections',row['address'],positive.stdout,positive.stderr))
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    wrong=folder/'missing-provider.c';shutil.copyfile(source,wrong);header=folder/'context.h';text=header.read_text();name='DWCi_MatchGPRecvBuddyMsgCallback' if int(row['address'],0)==0x209c188 else 'DWC_GetFriendDataType';changed=text.replace(name+'(','missing_callable_declaration(',1)
    if changed==text:raise ValueError('Actual provider declaration negative did not mutate')
    header.write_text(changed);negative_obj=folder/'missing.o';negative_command=[str(COMPILER),*flags,'-c',str(wrong),'-o',str(negative_obj)];negative=subprocess.run(negative_command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if negative.returncode==0 or negative_obj.exists() or 'no prototype' not in negative.stdout:raise ValueError(('Actual missing provider declaration admitted',negative.stdout,negative.stderr))
    return dict(address=row['address'],positiveExitCode=0,actualExecutableSectionsUnchanged=True,diagnosticFlags=flags,missingActualProvider=name,negativeExitCode=negative.returncode,negativeStdout=negative.stdout,primaryFlagsUnchanged=True,sourceCredit=0)


def execute(rows):
    assert_owned(LANE,OWN_SOURCE)
    for row in rows:verify_original(row,row['nativeSymbolEntries'])
    from wave20261106_dwc_match_next_eighth_helpers import execute as helpers
    helper=helpers()
    declarations=[prototype_presence(r) for r in rows]
    result=dict(status='passed',actualStandaloneOriginalEntryExecutions=helper['standaloneOriginalEntries'],helperQualificationProof='evidence/lanes/parallel-wave20261105/dwc-match-next/eighth/helpers-proof.json',actualCompilerGeometry=[geometry(r) for r in rows],requiredPrototypeDiagnostics=declarations,nativeThumbBindingControls=negative_controls(rows),oldNormalizerAndHelperParsersUnchanged=True,actualNativeAndCompilerRelocationsUnmodified=True,sourceCredit=0)
    write_json(LANE/'binding-layout-controls.json',result);return result
