from wave20261106_dwc_match_next_third_paths import assert_owned,EVIDENCE,SOURCE as OWN_SOURCE,WORK as OWN_WORK
import os
import shutil
import subprocess
from project import ROOT,write_json,sha256
from wave20261106_dwc_match_next_third_compiler import COMPILER
from wave20261106_dwc_match_next_third_bindings import verify_original,negative_controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/dwc-match-next/third'


def geometry(row):
    assert_owned(LANE,OWN_SOURCE)
    if not (ROOT/row["source"]).resolve().is_relative_to(OWN_SOURCE.resolve()):raise ValueError("Record layout source escaped exact own directory")
    folder=ROOT/'work/w6dm/third/geometry'/format(int(row['address'],0),'08x');folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    text=(folder/'context.h').read_text();checks=['sizeof(void*)==4','sizeof(u16)==2','sizeof(u32)==4','sizeof(OSTick)==8','sizeof(DWCLoginControl)==640','sizeof(DWCUserData)==64','sizeof(DWCLoginGlobals)==12','(u32)&((DWCLoginGlobals*)0)->remoteParam==0','(u32)&((DWCLoginGlobals*)0)->control==4','(u32)&((DWCLoginGlobals*)0)->remoteCallback==8','(u32)&((DWCLoginControl*)0)->authToken==0x48','(u32)&((DWCLoginControl*)0)->partnerChallenge==0x148','(u32)&((DWCLoginControl*)0)->username==0x248','(u32)&((DWCLoginControl*)0)->userdata==0x1c','sizeof(DWCAuthParam)==72','(u32)&((DWCAuthParam*)0)->gsbrcd==52','(u32)&((DWCAuthParam*)0)->alloc==64','(u32)&((DWCAuthParam*)0)->free==68','sizeof(DWCHttp)==7188','sizeof(DWCAuthResult)==452','(u32)&((DWCAuthResult*)0)->token==74','(u32)&((DWCAuthResult*)0)->challenge==375','sizeof(MATHRandContext32)==24','DWC_ACC_USERNAME_GSBRCD_OFFSET==9','DWC_ALLOCTYPE_AUTH==0','DWC_LOGIN_AUTH_TIMEOUT==10000','DWCAUTH_E_FINISH==21']
    if 'GPGetInfoResponseArg;' in text:checks+=['sizeof(GPGetInfoResponseArg)==516','(u32)&((GPGetInfoResponseArg*)0)->lastname==142','GP_LASTNAME==1797']
    source=folder/'layout.c';source.write_text('#include "context.h"\n#undef serverreqs\n'+'\n'.join('typedef char Layout'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(checks)));obj=folder/'layout.o';command=[str(COMPILER),*row['compilerFlags'],'-c',str(source),'-o',str(obj)]
    def compile_layout():return subprocess.run(command,cwd=ROOT,capture_output=True,text=True,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),timeout=60)
    process=compile_layout()
    if process.returncode:raise ValueError(('Actual Thumb structure geometry failed',row['address'],process.stdout,process.stderr))
    result=dict(address=row['address'],checks=checks,positiveExitCode=0,objectSha256=sha256(obj))
    wrong=text.replace('u16 ingamesn[26];','u16 ingamesn[25];',1)
    if wrong==text:raise ValueError('Wrong GP callback-prefix layout did not mutate')
    (folder/'context.h').write_text(wrong);bad=compile_layout()
    if bad.returncode==0:raise ValueError('Wrong GP callback-prefix layout accepted')
    result.update(wrongLayoutRejected=True,negativeExitCode=bad.returncode,negativeStdout=bad.stdout)
    return result


def prototype_presence(row):
    from elftools.elf.elffile import ELFFile
    assert_owned(LANE,OWN_SOURCE)
    folder=ROOT/'work/w6dm/third/required-prototypes'/format(int(row['address'],0),'08x');folder.mkdir(parents=True,exist_ok=True)
    def code_sections(path):
        with path.open('rb') as stream:return [(s.name,s.data().hex()) for s in ELFFile(stream).iter_sections() if s['sh_flags']&4]
    flags=[*row['compilerFlags'],'-requireprotos','-w','error'];source=ROOT/row['source'];obj=folder/'explicit.o';command=[str(COMPILER),*flags,'-c',str(source),'-o',str(obj)];env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'));positive=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if positive.returncode or code_sections(obj)!=code_sections(ROOT/row['object']):raise ValueError(('Required real prototypes failed or changed caller executable sections',row['address'],positive.stdout,positive.stderr))
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    wrong=folder/'missing-provider.c';shutil.copyfile(source,wrong);header=folder/'context.h';text=header.read_text();name={0x209c81c:'native_fn_02008d78',0x209c940:'native_fn_02097674',0x209caa0:'native_fn_02096ffc'}[int(row['address'],0)];changed=text.replace(name+'(','missing_callable_declaration(',1)
    if changed==text:raise ValueError('Actual provider declaration negative did not mutate')
    header.write_text(changed);negative_obj=folder/'missing.o';negative_command=[str(COMPILER),*flags,'-c',str(wrong),'-o',str(negative_obj)];negative=subprocess.run(negative_command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if negative.returncode==0 or negative_obj.exists() or 'no prototype' not in negative.stdout:raise ValueError(('Actual missing provider declaration admitted',negative.stdout,negative.stderr))
    return dict(address=row['address'],positiveExitCode=0,actualExecutableSectionsUnchanged=True,diagnosticFlags=flags,missingActualProvider=name,negativeExitCode=negative.returncode,negativeStdout=negative.stdout,primaryFlagsUnchanged=True,sourceCredit=0)


def execute(rows):
    assert_owned(LANE,OWN_SOURCE)
    for row in rows:verify_original(row,row['nativeSymbolEntries'])
    declarations=[prototype_presence(r) for r in rows]
    result=dict(status='passed',actualCompilerGeometry=[geometry(r) for r in rows],requiredPrototypeDiagnostics=declarations,nativeThumbBindingControls=negative_controls(rows),oldNormalizerAndHelperParsersUnchanged=True,actualNativeAndCompilerRelocationsUnmodified=True,sourceCredit=0)
    write_json(LANE/'binding-layout-controls.json',result);return result
