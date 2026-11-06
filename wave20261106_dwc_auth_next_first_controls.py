from wave20261106_dwc_auth_next_first_paths import assert_owned,EVIDENCE,SOURCE as OWN_SOURCE,WORK as OWN_WORK
import os
import shutil
import subprocess
from project import ROOT,write_json,sha256
from wave20261106_dwc_auth_next_first_compiler import COMPILER
from wave20261106_dwc_auth_next_first_bindings import verify_original,negative_controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/dwc-auth-next/first'


def geometry(row):
    assert_owned(LANE,OWN_SOURCE)
    if not (ROOT/row["source"]).resolve().is_relative_to(OWN_SOURCE.resolve()):raise ValueError("Record layout source escaped exact own directory")
    folder=ROOT/'work/w6da/first/geometry'/format(int(row['address'],0),'08x');folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    text=(folder/'context.h').read_text();checks=['sizeof(void*)==4','sizeof(u32)==4','sizeof(DWCAuthParam)==72','(u32)&((DWCAuthParam*)0)->alloc==64','(u32)&((DWCAuthParam*)0)->free==68','sizeof(DWCAuthResult)==452','sizeof(OSThread)==192','(u32)&((OSThread*)0)->activityWord108==108','sizeof(OSMutex)==24','sizeof(DWCAuth)==5108','(u32)&((DWCAuth*)0)->stack==0','(u32)&((DWCAuth*)0)->error==0x1004','(u32)&((DWCAuth*)0)->result==0x1008','(u32)&((DWCAuth*)0)->param==0x11cc','(u32)&((DWCAuth*)0)->http==0x1314','(u32)&((DWCAuth*)0)->thread==0x1318','(u32)&((DWCAuth*)0)->mutex==0x13d8','(u32)&((DWCAuth*)0)->abort==0x13f0','sizeof(DWCAuthGlobals)==12','(u32)&((DWCAuthGlobals*)0)->auth==8']
    source=folder/'layout.c';source.write_text('#include "context.h"\n#undef serverreqs\n'+'\n'.join('typedef char Layout'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(checks)));obj=folder/'layout.o';command=[str(COMPILER),*row['compilerFlags'],'-c',str(source),'-o',str(obj)]
    def compile_layout():return subprocess.run(command,cwd=ROOT,capture_output=True,text=True,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),timeout=60)
    process=compile_layout()
    if process.returncode:raise ValueError(('Actual Thumb structure geometry failed',row['address'],process.stdout,process.stderr))
    result=dict(address=row['address'],checks=checks,positiveExitCode=0,objectSha256=sha256(obj))
    wrong=text.replace('stack[4096]','stack[4092]',1)
    if wrong==text:raise ValueError('Wrong GP callback-prefix layout did not mutate')
    (folder/'context.h').write_text(wrong);bad=compile_layout()
    if bad.returncode==0:raise ValueError('Wrong GP callback-prefix layout accepted')
    result.update(wrongLayoutRejected=True,negativeExitCode=bad.returncode,negativeStdout=bad.stdout)
    return result


def prototype_presence(row):
    from elftools.elf.elffile import ELFFile
    assert_owned(LANE,OWN_SOURCE)
    folder=ROOT/'work/w6da/first/required-prototypes'/format(int(row['address'],0),'08x');folder.mkdir(parents=True,exist_ok=True)
    def code_sections(path):
        with path.open('rb') as stream:return [(s.name,s.data().hex()) for s in ELFFile(stream).iter_sections() if s['sh_flags']&4]
    flags=[*row['compilerFlags'],'-requireprotos','-w','error'];source=ROOT/row['source'];obj=folder/'explicit.o';command=[str(COMPILER),*flags,'-c',str(source),'-o',str(obj)];env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'));positive=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
    if positive.returncode or code_sections(obj)!=code_sections(ROOT/row['object']):raise ValueError(('Required real prototypes failed or changed caller executable sections',row['address'],positive.stdout,positive.stderr))
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    wrong=folder/'missing-provider.c';shutil.copyfile(source,wrong);header=folder/'context.h';text=header.read_text();name={0x2097488:'native_fn_02008d78',0x20975b8:'OS_LockMutex',0x2097618:'DWC_Http_Destroy',0x2097654:'OS_JoinThread'}[int(row['address'],0)];changed=text.replace(name+'(','missing_callable_declaration(',1)
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
