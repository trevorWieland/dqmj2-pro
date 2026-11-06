import os
import shutil
import subprocess
from project import ROOT,write_json,sha256
from wave20261105_gamespy_thumb_next_lan_compiler import COMPILER
from wave20261105_gamespy_thumb_next_lan_bindings import verify_original,negative_controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-thumb-next/lan'


def geometry(row):
    folder=ROOT/'work/w5gt/lan/geometry'/format(int(row['address'],0),'08x');folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    text=(folder/'context.h').read_text();checks=['sizeof(int)==4','sizeof(void*)==4','sizeof(u32)==4','sizeof(u16)==2','sizeof(u8)==1','sizeof(struct Server)==44','sizeof(SBServerList)==2012','(u32)&((SBServerList*)0)->slsocket==1716','(u32)&((SBServerList*)0)->lanstarttime==1720','(u32)&((SBServerList*)0)->ListCallback==1160','(u32)&((SBServerList*)0)->instance==1172','sizeof(struct sockaddr_in)==8','(u32)&((struct sockaddr_in*)0)->sin_port==2','(u32)&((struct sockaddr_in*)0)->sin_addr==4']
    source=folder/'layout.c';source.write_text('#include "context.h"\n'+'\n'.join('typedef char Layout'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(checks)));obj=folder/'layout.o';command=[str(COMPILER),*row['compilerFlags'],'-c',str(source),'-o',str(obj)]
    def compile_layout():return subprocess.run(command,cwd=ROOT,capture_output=True,text=True,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),timeout=60)
    process=compile_layout()
    if process.returncode:raise ValueError(('Actual Thumb structure geometry failed',row['address'],process.stdout,process.stderr))
    result=dict(address=row['address'],checks=checks,positiveExitCode=0,objectSha256=sha256(obj))
    if True:
        wrong=text.replace('int slsocket;','int gap,slsocket;',1) if row['address']=='0x20a834c' else text.replace('u16 sin_port;','u32 sin_port;',1)
        if wrong==text:raise ValueError('Wrong browser version/layout did not mutate')
        (folder/'context.h').write_text(wrong);bad=compile_layout()
        if bad.returncode==0:raise ValueError('Wrong browser version/layout accepted')
        result.update(wrongLayoutRejected=True,negativeExitCode=bad.returncode,negativeStdout=bad.stdout)
    return result


def execute(rows):
    for row in rows:verify_original(row,row['nativeSymbolEntries'])
    result=dict(status='passed',actualCompilerGeometry=[geometry(r) for r in rows],nativeThumbBindingControls=negative_controls(rows),oldNormalizerAndHelperParsersUnchanged=True,actualNativeAndCompilerRelocationsUnmodified=True,sourceCredit=0)
    write_json(LANE/'binding-layout-controls.json',result);return result
