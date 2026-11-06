from wave20261106_dwc_match_next_second_paths import assert_owned,EVIDENCE,SOURCE as OWN_SOURCE,WORK as OWN_WORK
import os
import shutil
import subprocess
from project import ROOT,write_json,sha256
from wave20261106_dwc_match_next_second_compiler import COMPILER
from wave20261106_dwc_match_next_second_bindings import verify_original,negative_controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/dwc-match-next/second'


def geometry(row):
    assert_owned(LANE,OWN_SOURCE)
    if not (ROOT/row["source"]).resolve().is_relative_to(OWN_SOURCE.resolve()):raise ValueError("Record layout source escaped exact own directory")
    folder=ROOT/'work/w6dm/second/geometry'/format(int(row['address'],0),'08x');folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    text=(folder/'context.h').read_text();checks=['sizeof(void*)==4','sizeof(u16)==2','sizeof(u32)==4','sizeof(OSTick)==8','sizeof(DWCLoginControl)==640','sizeof(DWCAccLoginId)==12','sizeof(DWCUserData)==64','sizeof(GPConnectResponseArg)==32','sizeof(DWCLoginGlobals)==12','(u32)&((DWCLoginGlobals*)0)->remoteCallback==0','(u32)&((DWCLoginGlobals*)0)->control==4','(u32)&((DWCLoginGlobals*)0)->remoteParam==8','(u32)&((DWCLoginControl*)0)->pGpObj==0','(u32)&((DWCLoginControl*)0)->state==4','(u32)&((DWCLoginControl*)0)->productID==8','(u32)&((DWCLoginControl*)0)->gamecode==12','(u32)&((DWCLoginControl*)0)->playerName==16','(u32)&((DWCLoginControl*)0)->callback==20','(u32)&((DWCLoginControl*)0)->param==24','(u32)&((DWCLoginControl*)0)->userdata==28','(u32)&((DWCLoginControl*)0)->http==36','(u32)&((DWCLoginControl*)0)->startTick==0x28','(u32)&((DWCLoginControl*)0)->connectFlag==0x30','(u32)&((DWCLoginControl*)0)->connectTick==0x34','(u32)&((DWCLoginControl*)0)->tempLoginId==0x3c','(u32)&((DWCLoginControl*)0)->authToken==0x48','(u32)&((DWCLoginControl*)0)->partnerChallenge==0x148','(u32)&((DWCLoginControl*)0)->username==0x248','(u32)&((DWCLoginControl*)0)->gpconnectresponsearg==0x260','(u32)&((DWCUserData*)0)->gs_profile_id==0x1c','(u32)&((DWCUserData*)0)->gamecode==0x24','(u32)&((GPConnectResponseArg*)0)->result==0','(u32)&((GPConnectResponseArg*)0)->profile==4','(u32)&((GPConnectResponseArg*)0)->uniquenick==8','DWC_LOGIN_STATE_CONNECTING==2','DWC_LOGIN_STATE_GPGETINFO==3','DWC_LOGIN_STATE_CONNECTED==5','DWC_LOGIN_GPCONNECT_TIMEOUT==60000']
    source=folder/'layout.c';source.write_text('#include "context.h"\n#undef serverreqs\n'+'\n'.join('typedef char Layout'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(checks)));obj=folder/'layout.o';command=[str(COMPILER),*row['compilerFlags'],'-c',str(source),'-o',str(obj)]
    def compile_layout():return subprocess.run(command,cwd=ROOT,capture_output=True,text=True,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),timeout=60)
    process=compile_layout()
    if process.returncode:raise ValueError(('Actual Thumb structure geometry failed',row['address'],process.stdout,process.stderr))
    result=dict(address=row['address'],checks=checks,positiveExitCode=0,objectSha256=sha256(obj))
    wrong=text.replace('DWCLoginState state;','u32 wrongExtra;DWCLoginState state;',1)
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
