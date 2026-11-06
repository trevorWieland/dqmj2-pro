from wave20261106_dwc_auth_next_third_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
import copy
import hashlib
import os
import shutil
import subprocess
from project import ROOT,write_json,sha256
from wave20261106_dwc_auth_next_third_compiler import COMPILER,compare
from wave20261106_dwc_auth_next_third_bindings import verify_original,negative_controls
from recover_linked_runtime import qualified_bindings
from elftools.elf.elffile import ELFFile


def geometry(row):
    assert_owned(LANE,SOURCE,WORK);folder=WORK/'geometry'/format(int(row['address'],0),'08x');folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    text=(folder/'context.h').read_text();checks=['sizeof(void*)==4','sizeof(u32)==4']
    if row['address']=='0x2097fac':checks+=['sizeof(wchar_t)==2','sizeof(size_t)==4'];wrong=text.replace('typedef unsigned short wchar_t;','typedef unsigned long wchar_t;',1)
    else:
        checks+=['sizeof(DWCAuthParam)==72','(u32)&((DWCAuthParam*)0)->alloc==64','(u32)&((DWCAuthParam*)0)->free==68','sizeof(DWCAuthResult)==452','sizeof(DWCAuth)==5108','(u32)&((DWCAuth*)0)->result==0x1008','(u32)&((DWCAuth*)0)->param==0x11cc','(u32)&((DWCAuth*)0)->http==0x1314','(u32)&((DWCAuthGlobals*)0)->auth==8'];wrong=text.replace('stack[4096]','stack[4092]',1)
    if row['address']=='0x20977cc':checks+=['sizeof(DWCHttp)==7188','(u32)&((DWCHttp*)0)->error==4128','(u32)&((DWCHttp*)0)->thread==6968','(u32)&((DWCHttp*)0)->thread.activityWord108==7076','sizeof(OSTick)==8']
    source=folder/'layout.c';source.write_text('#include "context.h"\n'+'\n'.join('typedef char Layout'+str(i)+'[('+condition+')?1:-1];' for i,condition in enumerate(checks)));obj=folder/'layout.o';command=[str(COMPILER),*row['compilerFlags'],'-c',str(source),'-o',str(obj)];env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'))
    positive=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,env=env,timeout=60)
    if positive.returncode:raise ValueError(('Actual consumed Auth/CAL layout failed',positive.stdout,positive.stderr))
    if wrong==text:raise ValueError('Meaningful wrong layout did not mutate')
    (folder/'context.h').write_text(wrong);negative=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,env=env,timeout=60)
    if negative.returncode==0:raise ValueError('Wrong actual Auth/CAL layout admitted')
    return dict(address=row['address'],checks=checks,positiveExitCode=0,wrongLayoutRejected=True,negativeExitCode=negative.returncode,negativeStdout=negative.stdout)


def prototype_presence(row):
    folder=WORK/'required-prototypes'/format(int(row['address'],0),'08x');folder.mkdir(parents=True,exist_ok=True)
    def allocated(path):
        with path.open('rb') as stream:return [(s.name,s['sh_flags'],s.data().hex()) for s in ELFFile(stream).iter_sections() if s['sh_flags']&2]
    flags=[*row['compilerFlags'],'-requireprotos','-w','error'];source=ROOT/row['source'];obj=folder/'explicit.o';command=[str(COMPILER),*flags,'-c',str(source),'-o',str(obj)];env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'));positive=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if positive.returncode or allocated(obj)!=allocated(ROOT/row['object']):raise ValueError(('Required actual prototypes failed or changed allocated caller/context',positive.stdout,positive.stderr))
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    wrong=folder/'missing-provider.c';shutil.copyfile(source,wrong);header=folder/'context.h';text=header.read_text();name={'0x20977cc':'OS_GetTick','0x209798c':'native_fn_02098d0c'}[row['address']];changed=text.replace(name+'(','missing_callable_declaration(',1)
    if changed==text:raise ValueError('Actual provider declaration did not mutate')
    header.write_text(changed);negative_obj=folder/'missing.o'
    if negative_obj.exists():negative_obj.unlink()
    negative=subprocess.run([str(COMPILER),*flags,'-c',str(wrong),'-o',str(negative_obj)],cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if negative.returncode==0 or negative_obj.exists() or 'no prototype' not in negative.stdout:raise ValueError(('Actual missing provider declaration admitted',negative.stdout,negative.stderr))
    return dict(address=row['address'],positiveExitCode=0,actualExecutableAndInitializedContextSectionsUnchanged=True,diagnosticFlags=flags,missingActualProvider=name,negativeExitCode=negative.returncode,negativeStdout=negative.stdout,primaryFlagsUnchanged=True,sourceCredit=0)


def execute(rows):
    assert_owned(LANE,SOURCE,WORK)
    for row in rows:verify_original(row,row['nativeSymbolEntries'])
    result=dict(status='passed',actualCompilerGeometry=[geometry(r) for r in rows],requiredPrototypeDiagnostics=[prototype_presence(r) for r in rows],nativeThumbBindingControls=negative_controls(rows),oldNormalizerAndHelperParsersUnchanged=True,actualNativeAndCompilerRelocationsUnmodified=True,sourceCredit=0)
    write_json(LANE/'binding-layout-controls.json',result);return result
