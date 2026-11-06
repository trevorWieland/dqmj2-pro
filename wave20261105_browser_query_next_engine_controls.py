import os
import shutil
import subprocess
from project import ROOT,write_json,sha256
from wave20261105_browser_query_next_engine_compiler import COMPILER
from wave20261105_browser_query_next_engine_bindings import verify_original,negative_controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/browser-query-next/engine'


def geometry(row):
    folder=ROOT/'work/w5bq/engine/geometry'/format(int(row['address'],0),'08x');folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    text=(folder/'context.h').read_text();checks=['sizeof(int)==4','sizeof(void*)==4','sizeof(u8)==1','sizeof(u16)==2','sizeof(u32)==4','sizeof(struct Server)==44','sizeof(((struct Server*)0)->publicport)==2','sizeof(((struct Server*)0)->privateport)==2','(u32)&((struct Server*)0)->state==20','(u32)&((struct Server*)0)->flags==21','(u32)&((struct Server*)0)->keyvals==24','(u32)&((struct Server*)0)->querychallenge==32','(u32)&((struct Server*)0)->next==36','(u32)&((struct Server*)0)->splitResponseBitmap==40','sizeof(SBServerFIFO)==12','sizeof(SBQueryEngine)==76','(u32)&((SBQueryEngine*)0)->querylist==8','(u32)&((SBQueryEngine*)0)->pendinglist==20','(u32)&((SBQueryEngine*)0)->querysock==32','(u32)&((SBQueryEngine*)0)->mypublicip==40','(u32)&((SBQueryEngine*)0)->serverkeys==44','(u32)&((SBQueryEngine*)0)->numserverkeys==64','(u32)&((SBQueryEngine*)0)->ListCallback==68','(u32)&((SBQueryEngine*)0)->instance==72']
    if row['address'] in ('0x20a5b74','0x20a5d1c','0x20a5a74'):checks.extend(['sizeof(struct sockaddr_in)==8','(u32)&((struct sockaddr_in*)0)->sin_port==2','(u32)&((struct sockaddr_in*)0)->sin_addr==4'])
    if row['address']=='0x20a5b74':checks.append('sizeof(native_data_020e277c[0])==4')
    source=folder/'layout.c';source.write_text('#include "context.h"\n'+'\n'.join('typedef char Layout'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(checks)));obj=folder/'layout.o';command=[str(COMPILER),*row['compilerFlags'],'-c',str(source),'-o',str(obj)]
    def compile_layout():return subprocess.run(command,cwd=ROOT,capture_output=True,text=True,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),timeout=60)
    process=compile_layout()
    if process.returncode:raise ValueError(('Actual Thumb structure geometry failed',row['address'],process.stdout,process.stderr))
    result=dict(address=row['address'],checks=checks,positiveExitCode=0,objectSha256=sha256(obj))
    if True:
        wrong=text.replace('u16 publicport;','u32 publicport;',1) if row['address'] in ('0x20a5894','0x20a5afc','0x20a5b74','0x20a5cb0','0x20a5f98') else text.replace('int queryversion,maxupdates;','int gap,queryversion,maxupdates;',1)
        if wrong==text:raise ValueError('Wrong browser version/layout did not mutate')
        (folder/'context.h').write_text(wrong);bad=compile_layout()
        if bad.returncode==0:raise ValueError('Wrong browser version/layout accepted')
        result.update(wrongLayoutRejected=True,negativeExitCode=bad.returncode,negativeStdout=bad.stdout)
    return result


def execute(rows):
    for row in rows:verify_original(row,row['nativeSymbolEntries'])
    result=dict(status='passed',actualCompilerGeometry=[geometry(r) for r in rows],nativeThumbBindingControls=negative_controls(rows),oldNormalizerAndHelperParsersUnchanged=True,actualNativeAndCompilerRelocationsUnmodified=True,sourceCredit=0)
    write_json(LANE/'binding-layout-controls.json',result);return result
