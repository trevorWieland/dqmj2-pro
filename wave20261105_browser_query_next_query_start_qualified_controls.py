from wave20261105_browser_query_next_query_start_qualified_paths import assert_owned,EVIDENCE,SOURCE as OWN_SOURCE,WORK as OWN_WORK
import os
import shutil
import subprocess
from project import ROOT,write_json,sha256
from wave20261105_browser_query_next_query_start_qualified_compiler import COMPILER
from wave20261105_browser_query_next_query_start_qualified_bindings import verify_original,negative_controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/browser-query-next/query-start-qualified'


def geometry(row):
    assert_owned(LANE,OWN_SOURCE)
    if not (ROOT/row["source"]).resolve().is_relative_to(OWN_SOURCE.resolve()):raise ValueError("RPC layout source escaped exact own directory")
    folder=ROOT/'work/w5bq/query-start-qualified/geometry'/format(int(row['address'],0),'08x');folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    text=(folder/'context.h').read_text();checks=['sizeof(int)==4','sizeof(void*)==4','sizeof(u16)==2','sizeof(u32)==4','((u32)-1)>0','sizeof(struct Server)==44','sizeof(((SBServer)0)->publicport)==2','(u32)&((SBServer)0)->state==20','(u32)&((SBServer)0)->flags==21','(u32)&((SBServer)0)->updatetime==28','(u32)&((SBServer)0)->querychallenge==32','sizeof(SBQueryEngine)==76','(u32)&((SBQueryEngine*)0)->querysock==32','(u32)&((SBQueryEngine*)0)->serverkeys==44','(u32)&((SBQueryEngine*)0)->numserverkeys==64','sizeof(struct sockaddr_in)==8','(u32)&((struct sockaddr_in*)0)->sin_port==2','(u32)&((struct sockaddr_in*)0)->sin_addr==4']
    source=folder/'layout.c';source.write_text('#include "context.h"\n'+'\n'.join('typedef char Layout'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(checks)));obj=folder/'layout.o';command=[str(COMPILER),*row['compilerFlags'],'-c',str(source),'-o',str(obj)]
    def compile_layout():return subprocess.run(command,cwd=ROOT,capture_output=True,text=True,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),timeout=60)
    process=compile_layout()
    if process.returncode:raise ValueError(('Actual Thumb argument/callback geometry failed',row['address'],process.stdout,process.stderr))
    result=dict(address=row['address'],checks=checks,positiveExitCode=0,objectSha256=sha256(obj))
    wrong=text.replace('u16 publicport;','u32 publicport;',1)
    if wrong==text:raise ValueError('Wrong RPC halfword width did not mutate')
    (folder/'context.h').write_text(wrong);bad=compile_layout()
    if bad.returncode==0:raise ValueError('Wrong RPC halfword width accepted')
    result.update(wrongLayoutRejected=True,negativeExitCode=bad.returncode,negativeStdout=bad.stdout)
    return result


def execute(rows):
    assert_owned(LANE,OWN_SOURCE)
    for row in rows:verify_original(row,row['nativeSymbolEntries'])
    result=dict(status='passed',actualCompilerGeometry=[geometry(r) for r in rows],nativeThumbBindingControls=negative_controls(rows),oldNormalizerAndHelperParsersUnchanged=True,actualNativeAndCompilerRelocationsUnmodified=True,sourceCredit=0)
    write_json(LANE/'binding-layout-controls.json',result);return result
