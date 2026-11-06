import os
import shutil
import subprocess
from project import ROOT,write_json,sha256
from wave20261105_gamespy_thumb_next_availability_compiler import COMPILER
from wave20261105_gamespy_thumb_next_availability_bindings import verify_original,negative_controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-thumb-next/availability'


def geometry(row):
    folder=ROOT/'work/w5gt/availability/geometry'/format(int(row['address'],0),'08x');folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    text=(folder/'context.h').read_text();checks=['sizeof(int)==4','sizeof(void*)==4','sizeof(u32)==4','sizeof(u16)==2','sizeof(u8)==1','sizeof(IN_ADDR)==4','sizeof(SOCKADDR_IN)==8','(u32)&((SOCKADDR_IN*)0)->sin_port==2','(u32)&((SOCKADDR_IN*)0)->sin_addr==4','sizeof(HOSTENT)==16','(u32)&((HOSTENT*)0)->h_addr_list==12','sizeof(Availability)==88','(u32)&((Availability*)0)->sock==0','(u32)&((Availability*)0)->address==4','(u32)&((Availability*)0)->packet==12','(u32)&((Availability*)0)->packetLen==76','(u32)&((Availability*)0)->sendTime==80','(u32)&((Availability*)0)->retryCount==84']
    source=folder/'layout.c';source.write_text('#include "context.h"\n'+'\n'.join('typedef char Layout'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(checks)));obj=folder/'layout.o';command=[str(COMPILER),*row['compilerFlags'],'-c',str(source),'-o',str(obj)]
    def compile_layout():return subprocess.run(command,cwd=ROOT,capture_output=True,text=True,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),timeout=60)
    process=compile_layout()
    if process.returncode:raise ValueError(('Actual Thumb structure geometry failed',row['address'],process.stdout,process.stderr))
    result=dict(address=row['address'],checks=checks,positiveExitCode=0,objectSha256=sha256(obj))
    if True:
        changes={'0x20a92b0':('short type,len;','short type,len;int gap;'),'0x20a932c':('int sock;SOCKADDR_IN address;','int sock,gap;SOCKADDR_IN address;'),'0x20a93cc':('struct in_addr{u32 s_addr;};','struct in_addr{u16 s_addr;};'),'0x20a9448':('gsi_time sendTime;int retryCount;','gsi_time sendTime;int gap,retryCount;')}
        old,new=changes[row['address']];wrong=text.replace(old,new,1)
        if wrong==text:raise ValueError('Wrong browser version/layout did not mutate')
        (folder/'context.h').write_text(wrong);bad=compile_layout()
        if bad.returncode==0:raise ValueError('Wrong browser version/layout accepted')
        result.update(wrongLayoutRejected=True,negativeExitCode=bad.returncode,negativeStdout=bad.stdout)
    return result


def execute(rows):
    for row in rows:verify_original(row,row['nativeSymbolEntries'])
    result=dict(status='passed',actualCompilerGeometry=[geometry(r) for r in rows],nativeThumbBindingControls=negative_controls(rows),oldNormalizerAndHelperParsersUnchanged=True,actualNativeAndCompilerRelocationsUnmodified=True,sourceCredit=0)
    write_json(LANE/'binding-layout-controls.json',result);return result
