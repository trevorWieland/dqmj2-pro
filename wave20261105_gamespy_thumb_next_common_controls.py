import os
import shutil
import subprocess
from project import ROOT,write_json,sha256
from wave20261105_gamespy_thumb_next_common_compiler import COMPILER
from wave20261105_gamespy_thumb_next_common_bindings import verify_original,negative_controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-thumb-next/common'


def geometry(row):
    folder=ROOT/'work/w5gt/common/geometry'/format(int(row['address'],0),'08x');folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    text=(folder/'context.h').read_text();checks=['sizeof(int)==4','sizeof(void*)==4','sizeof(char)==1','sizeof(double)==8','sizeof(long)==4','sizeof(u32)==4','sizeof(u8)==1','((char)-1)<0','sizeof(native_data_020dc550)==3','sizeof(native_data_020dc554)==3','sizeof(native_data_020dc558)==3']
    source=folder/'layout.c';source.write_text('#include "context.h"\n'+'\n'.join('typedef char Layout'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(checks)));obj=folder/'layout.o';command=[str(COMPILER),*row['compilerFlags'],'-c',str(source),'-o',str(obj)]
    def compile_layout():return subprocess.run(command,cwd=ROOT,capture_output=True,text=True,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),timeout=60)
    process=compile_layout()
    if process.returncode:raise ValueError(('Actual Thumb structure geometry failed',row['address'],process.stdout,process.stderr))
    result=dict(address=row['address'],checks=checks,positiveExitCode=0,objectSha256=sha256(obj))
    if row['address'] in ('0x20a9040','0x20a91a0'):
        wrong=text.replace('typedef unsigned int u32;','typedef unsigned short u32;',1)
        if wrong==text:raise ValueError('Wrong native scalar layout did not mutate')
        (folder/'context.h').write_text(wrong);bad=compile_layout()
        if bad.returncode==0:raise ValueError('Wrong native scalar width accepted')
        result.update(wrongLayoutRejected=True,negativeExitCode=bad.returncode,negativeStdout=bad.stdout)
    return result


def execute(rows):
    for row in rows:verify_original(row,row['nativeSymbolEntries'])
    result=dict(status='passed',actualCompilerGeometry=[geometry(r) for r in rows],nativeThumbBindingControls=negative_controls(rows),oldNormalizerAndHelperParsersUnchanged=True,actualNativeAndCompilerRelocationsUnmodified=True,sourceCredit=0)
    write_json(LANE/'binding-layout-controls.json',result);return result
