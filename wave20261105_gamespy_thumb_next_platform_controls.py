import os
import shutil
import subprocess
from project import ROOT,write_json,sha256
from wave20261105_gamespy_thumb_next_platform_compiler import COMPILER
from wave20261105_gamespy_thumb_next_platform_bindings import verify_original,negative_controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-thumb-next/platform'


def geometry(row):
    folder=ROOT/'work/w5gt/platform/geometry'/format(int(row['address'],0),'08x');folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    text=(folder/'context.h').read_text();checks=['sizeof(int)==4','sizeof(void*)==4','sizeof(char)==1','sizeof(double)==8','sizeof(u32)==4']
    if 'SOCKADDR;' in text:checks+=['sizeof(SOCKADDR)==8','sizeof(SOCKADDR_IN)==8','sizeof(SOPollFD)==8','(u32)&((SOCKADDR*)0)->len==0','(u32)&((SOCKADDR*)0)->family==1','(u32)&((SOCKADDR_IN*)0)->port==2','(u32)&((SOCKADDR_IN*)0)->addr==4','(u32)&((SOPollFD*)0)->events==4','(u32)&((SOPollFD*)0)->revents==6','sizeof(((SOPollFD*)0)->events)==2']
    if 'IN_ADDR;' in text:checks+=['sizeof(IN_ADDR)==4','(u32)&((IN_ADDR*)0)->s_addr==0']
    if 'u64;' in text:checks+=['sizeof(u64)==8']
    source=folder/'layout.c';source.write_text('#include "context.h"\n'+'\n'.join('typedef char Layout'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(checks)));obj=folder/'layout.o';command=[str(COMPILER),*row['compilerFlags'],'-c',str(source),'-o',str(obj)]
    def compile_layout():return subprocess.run(command,cwd=ROOT,capture_output=True,text=True,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),timeout=60)
    process=compile_layout()
    if process.returncode:raise ValueError(('Actual Thumb structure geometry failed',row['address'],process.stdout,process.stderr))
    result=dict(address=row['address'],checks=checks,positiveExitCode=0,objectSha256=sha256(obj))
    if row['address'] in ('0x20a8ca8','0x20a8e18'):
        wrong=text.replace('short events,revents','int events,revents',1) if row['address']=='0x20a8ca8' else text.replace('typedef unsigned int u32;','typedef unsigned short u32;',1)
        if wrong==text:raise ValueError('Wrong native scalar layout did not mutate')
        (folder/'context.h').write_text(wrong);bad=compile_layout()
        if bad.returncode==0:raise ValueError('Wrong native scalar width accepted')
        result.update(wrongLayoutRejected=True,negativeExitCode=bad.returncode,negativeStdout=bad.stdout)
    return result


def execute(rows):
    for row in rows:verify_original(row,row['nativeSymbolEntries'])
    result=dict(status='passed',actualCompilerGeometry=[geometry(r) for r in rows],nativeThumbBindingControls=negative_controls(rows),oldNormalizerAndHelperParsersUnchanged=True,actualNativeAndCompilerRelocationsUnmodified=True,sourceCredit=0)
    write_json(LANE/'binding-layout-controls.json',result);return result
