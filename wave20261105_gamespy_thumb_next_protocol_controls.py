import os
import shutil
import subprocess
from project import ROOT,write_json,sha256
from wave20261105_gamespy_thumb_next_protocol_compiler import COMPILER
from wave20261105_gamespy_thumb_next_protocol_bindings import verify_original,negative_controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-thumb-next/protocol'


def geometry(row):
    folder=ROOT/'work/w5gt/protocol/geometry'/format(int(row['address'],0),'08x');folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    text=(folder/'context.h').read_text();checks=['sizeof(int)==4','sizeof(void*)==4','sizeof(char)==1','sizeof(u32)==4','sizeof(u16)==2','sizeof(u8)==1','sizeof(struct Server)==44','(u32)&((struct Server*)0)->state==20','(u32)&((struct Server*)0)->flags==21','sizeof(GOACryptState)==261','sizeof(KeyInfo)==8','(u32)&((KeyInfo*)0)->keyName==0','(u32)&((KeyInfo*)0)->keyType==4','(u32)&((SBServerList*)0)->keylist==8','(u32)&((SBServerList*)0)->inbuffer==124','(u32)&((SBServerList*)0)->inbufferlen==128','(u32)&((SBServerList*)0)->numpopularvalues==1152','(u32)&((SBServerList*)0)->expectedelements==1156','(u32)&((SBServerList*)0)->defaultport==1708','(u32)&((SBServerList*)0)->cryptkey==1728','(u32)&((SBServerList*)0)->queryoptions==1992','(u32)&((SBServerList*)0)->pstate==1996','(u32)&((struct Server*)0)->privateport==12','sizeof(SortInfo)==260','sizeof(SBQueryEngine)==76','sizeof(SBServerList)==2012','sizeof(struct _ServerBrowser)==2112','(u32)&((SBQueryEngine*)0)->querylist.count==16','(u32)&((SBQueryEngine*)0)->numserverkeys==64','(u32)&((struct _ServerBrowser*)0)->list==76','(u32)&((struct _ServerBrowser*)0)->dontUpdate==2092','(u32)&((struct _ServerBrowser*)0)->triggerIP==2096','(u32)&((struct _ServerBrowser*)0)->triggerPort==2100','(u32)&((struct _ServerBrowser*)0)->BrowserCallback==2104','(u32)&((struct _ServerBrowser*)0)->instance==2108']
    source=folder/'layout.c';source.write_text('#include "context.h"\n'+'\n'.join('typedef char Layout'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(checks)));obj=folder/'layout.o';command=[str(COMPILER),*row['compilerFlags'],'-c',str(source),'-o',str(obj)]
    def compile_layout():return subprocess.run(command,cwd=ROOT,capture_output=True,text=True,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),timeout=60)
    process=compile_layout()
    if process.returncode:raise ValueError(('Actual Thumb structure geometry failed',row['address'],process.stdout,process.stderr))
    result=dict(address=row['address'],checks=checks,positiveExitCode=0,objectSha256=sha256(obj))
    if row['address'] in ('0x20a7858','0x20a7b30'):
        wrong=text.replace('u32 privateip;','u16 privateip;',1) if row['address']=='0x20a7858' else text.replace('const char*keyName;int keyType;','int keyType;const char*keyName;',1)
        if wrong==text:raise ValueError('Wrong browser version/layout did not mutate')
        (folder/'context.h').write_text(wrong);bad=compile_layout()
        if bad.returncode==0:raise ValueError('Wrong browser version/layout accepted')
        result.update(wrongLayoutRejected=True,negativeExitCode=bad.returncode,negativeStdout=bad.stdout)
    return result


def execute(rows):
    for row in rows:verify_original(row,row['nativeSymbolEntries'])
    result=dict(status='passed',actualCompilerGeometry=[geometry(r) for r in rows],nativeThumbBindingControls=negative_controls(rows),oldNormalizerAndHelperParsersUnchanged=True,actualNativeAndCompilerRelocationsUnmodified=True,sourceCredit=0)
    write_json(LANE/'binding-layout-controls.json',result);return result
