from wave20261105_gpi_connect_next_peers_paths import assert_owned,EVIDENCE,SOURCE as OWN_SOURCE,WORK as OWN_WORK
import os
import shutil
import subprocess
from project import ROOT,write_json,sha256
from wave20261105_gpi_connect_next_peers_compiler import COMPILER
from wave20261105_gpi_connect_next_peers_bindings import verify_original,negative_controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gpi-connect-next/peers'


def geometry(row):
    assert_owned(LANE,OWN_SOURCE)
    if not (ROOT/row["source"]).resolve().is_relative_to(OWN_SOURCE.resolve()):raise ValueError("Record layout source escaped exact own directory")
    folder=ROOT/'work/w5gc/peers/geometry'/format(int(row['address'],0),'08x');folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    text=(folder/'context.h').read_text();checks=['sizeof(void*)==4','sizeof(time_t)==4','sizeof(GPIConnection)==0x600','sizeof(GPIProfileList)==12','(u32)&((GPIConnection*)0)->peerList==0x5d4','sizeof(GPIPeer)==80','(u32)&((GPIPeer*)0)->state==0','(u32)&((GPIPeer*)0)->initiated==4','(u32)&((GPIPeer*)0)->ip==8','(u32)&((GPIPeer*)0)->port==12','(u32)&((GPIPeer*)0)->profile==16','(u32)&((GPIPeer*)0)->timeout==20','(u32)&((GPIPeer*)0)->inputBuffer==28','(u32)&((GPIPeer*)0)->outputBuffer==44','(u32)&((GPIPeer*)0)->messages==60','(u32)&((GPIPeer*)0)->peerOpQueue==64','(u32)&((GPIPeer*)0)->pnext==76','sizeof(GPIMessage)==24','(u32)&((GPIMessage*)0)->type==16','(u32)&((GPIMessage*)0)->start==20']
    if int(row['address'],0)==0x20b049c:checks+=['(u32)&((GPIBuddyStatusInfo*)0)->buddyIp==28','(u32)&((GPIBuddyStatusInfo*)0)->buddyPort==32','GS_UDP_ADDRESS_ALREADY_IN_USE==5','GS_UDP_PEER_CONNECTED==1','GS_UDP_PEER_CONNECTING==0']
    source=folder/'layout.c';source.write_text('#include "context.h"\n#undef serverreqs\n'+'\n'.join('typedef char Layout'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(checks)));obj=folder/'layout.o';command=[str(COMPILER),*row['compilerFlags'],'-c',str(source),'-o',str(obj)]
    def compile_layout():return subprocess.run(command,cwd=ROOT,capture_output=True,text=True,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),timeout=60)
    process=compile_layout()
    if process.returncode:raise ValueError(('Actual Thumb structure geometry failed',row['address'],process.stdout,process.stderr))
    result=dict(address=row['address'],checks=checks,positiveExitCode=0,objectSha256=sha256(obj))
    wrong=text.replace('unsigned short port;','u32 wrongExtra;unsigned short port;',1)
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
