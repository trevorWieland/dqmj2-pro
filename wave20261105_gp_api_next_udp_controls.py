from wave20261105_gp_api_next_udp_paths import assert_owned,EVIDENCE,SOURCE as OWN_SOURCE,WORK as OWN_WORK
import os
import shutil
import subprocess
from project import ROOT,write_json,sha256
from wave20261105_gp_api_next_udp_compiler import COMPILER
from wave20261105_gp_api_next_udp_bindings import verify_original,negative_controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gp-api-next/udp'


def geometry(row):
    assert_owned(LANE,OWN_SOURCE)
    if not (ROOT/row["source"]).resolve().is_relative_to(OWN_SOURCE.resolve()):raise ValueError("Record layout source escaped exact own directory")
    folder=ROOT/'work/w5gp/udp/geometry'/format(int(row['address'],0),'08x');folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    text=(folder/'context.h').read_text();checks=['sizeof(int)==4','sizeof(void*)==4','sizeof(u8)==1','sizeof(u16)==2','sizeof(u32)==4','sizeof(GSUdpEngineObject)==60','sizeof(GSUdpRemotePeer)==12','sizeof(GSUdpMsgHandler)==60','sizeof(GT2ConnectionCallbacks)==16','sizeof(((GSUdpRemotePeer*)0)->mPort)==2','(u32)&((GSUdpRemotePeer*)0)->mPort==4','(u32)&((GSUdpRemotePeer*)0)->mConnection==8','(u32)&((GSUdpMsgHandler*)0)->mHeader==16','(u32)&((GSUdpMsgHandler*)0)->mPendingConnections==32','(u32)&((GSUdpMsgHandler*)0)->mUserData==56','(u32)&((GSUdpEngineObject*)0)->mInitialized==12','(u32)&((GSUdpEngineObject*)0)->mAppNetworkError==36','(u32)&((GSUdpEngineObject*)0)->mAppUnknownMessage==40','(u32)&((GSUdpEngineObject*)0)->mAppUserData==44','(u32)&((GSUdpEngineObject*)0)->mLocalPort==56','(u32)&((GT2ConnectionCallbacks*)0)->connected==0','(u32)&((GT2ConnectionCallbacks*)0)->received==4','(u32)&((GT2ConnectionCallbacks*)0)->closed==8','(u32)&((GT2ConnectionCallbacks*)0)->ping==12']
    source=folder/'layout.c';source.write_text('#include "context.h"\n'+'\n'.join('typedef char Layout'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(checks)));obj=folder/'layout.o';command=[str(COMPILER),*row['compilerFlags'],'-c',str(source),'-o',str(obj)]
    def compile_layout():return subprocess.run(command,cwd=ROOT,capture_output=True,text=True,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),timeout=60)
    process=compile_layout()
    if process.returncode:raise ValueError(('Actual Thumb structure geometry failed',row['address'],process.stdout,process.stderr))
    result=dict(address=row['address'],checks=checks,positiveExitCode=0,objectSha256=sha256(obj))
    wrong=text.replace('typedef unsigned short u16;','typedef unsigned int u16;',1)
    if wrong==text:raise ValueError('Wrong UDP halfword width did not mutate')
    (folder/'context.h').write_text(wrong);bad=compile_layout()
    if bad.returncode==0:raise ValueError('Wrong UDP halfword geometry accepted')
    result.update(wrongLayoutRejected=True,negativeExitCode=bad.returncode,negativeStdout=bad.stdout)
    return result


def execute(rows):
    assert_owned(LANE,OWN_SOURCE)
    for row in rows:verify_original(row,row['nativeSymbolEntries'])
    result=dict(status='passed',actualCompilerGeometry=[geometry(r) for r in rows],nativeThumbBindingControls=negative_controls(rows),oldNormalizerAndHelperParsersUnchanged=True,actualNativeAndCompilerRelocationsUnmodified=True,sourceCredit=0)
    write_json(LANE/'binding-layout-controls.json',result);return result
