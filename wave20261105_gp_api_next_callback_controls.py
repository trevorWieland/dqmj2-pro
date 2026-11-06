from wave20261105_gp_api_next_callback_paths import assert_owned,EVIDENCE,SOURCE as OWN_SOURCE,WORK as OWN_WORK
import os
import shutil
import subprocess
from project import ROOT,write_json,sha256
from wave20261105_gp_api_next_callback_compiler import COMPILER
from wave20261105_gp_api_next_callback_bindings import verify_original,negative_controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gp-api-next/callback'


def geometry(row):
    assert_owned(LANE,OWN_SOURCE)
    if not (ROOT/row["source"]).resolve().is_relative_to(OWN_SOURCE.resolve()):raise ValueError("Record layout source escaped exact own directory")
    folder=ROOT/'work/w5gp/callback/geometry'/format(int(row['address'],0),'08x');folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    text=(folder/'context.h').read_text();checks=['sizeof(int)==4','sizeof(void*)==4','sizeof(GPICallback)==8','sizeof(GPICallbackData)==24','(u32)&((GPICallbackData*)0)->arg==8','(u32)&((GPICallbackData*)0)->type==12','(u32)&((GPICallbackData*)0)->operationID==16','(u32)&((GPICallbackData*)0)->pnext==20','sizeof(GPIConnection)==0x5e0','(u32)&((GPIConnection*)0)->errorCode==0x5b8','(u32)&((GPIConnection*)0)->fatalError==0x5bc','(u32)&((GPIConnection*)0)->callbackList==0x5d8','(u32)&((GPIConnection*)0)->lastCallback==0x5dc','sizeof(GPErrorArg)==16','(u32)&((GPErrorArg*)0)->fatal==12','(u32)&((struct GPIOperation_s*)0)->id==24']
    source=folder/'layout.c';source.write_text('#include "context.h"\n'+'\n'.join('typedef char Layout'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(checks)));obj=folder/'layout.o';command=[str(COMPILER),*row['compilerFlags'],'-c',str(source),'-o',str(obj)]
    def compile_layout():return subprocess.run(command,cwd=ROOT,capture_output=True,text=True,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),timeout=60)
    process=compile_layout()
    if process.returncode:raise ValueError(('Actual Thumb structure geometry failed',row['address'],process.stdout,process.stderr))
    result=dict(address=row['address'],checks=checks,positiveExitCode=0,objectSha256=sha256(obj))
    wrong=text.replace('struct GPICallbackData*callbackList,*lastCallback;','int incorrectPeerField;struct GPICallbackData*callbackList,*lastCallback;',1)
    if wrong==text:raise ValueError('Wrong GP callback-prefix layout did not mutate')
    (folder/'context.h').write_text(wrong);bad=compile_layout()
    if bad.returncode==0:raise ValueError('Wrong GP callback-prefix layout accepted')
    result.update(wrongLayoutRejected=True,negativeExitCode=bad.returncode,negativeStdout=bad.stdout)
    return result


def execute(rows):
    assert_owned(LANE,OWN_SOURCE)
    for row in rows:verify_original(row,row['nativeSymbolEntries'])
    result=dict(status='passed',actualCompilerGeometry=[geometry(r) for r in rows],nativeThumbBindingControls=negative_controls(rows),oldNormalizerAndHelperParsersUnchanged=True,actualNativeAndCompilerRelocationsUnmodified=True,sourceCredit=0)
    write_json(LANE/'binding-layout-controls.json',result);return result
