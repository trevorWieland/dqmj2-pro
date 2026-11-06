from wave20261105_gpi_connect_next_peer_init_paths import assert_owned,EVIDENCE,SOURCE as OWN_SOURCE,WORK as OWN_WORK
import os
import shutil
import subprocess
from project import ROOT,write_json,sha256
from wave20261105_gpi_connect_next_peer_init_compiler import COMPILER
from wave20261105_gpi_connect_next_peer_init_build import build
from wave20261105_gpi_connect_next_peer_init_bindings import verify_original,negative_controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gpi-connect-next/peer-init'


def geometry(row):
    assert_owned(LANE,OWN_SOURCE)
    if not (ROOT/row["source"]).resolve().is_relative_to(OWN_SOURCE.resolve()):raise ValueError("Record layout source escaped exact own directory")
    folder=ROOT/'work/w5gc/peer-init/geometry'/format(int(row['address'],0),'08x');folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    text=(folder/'context.h').read_text();checks=['sizeof(void*)==4','sizeof(GPIConnection)==0x600','(u32)&((GPIConnection*)0)->peerList==0x5d4','sizeof(GPIPeer)==80','(u32)&((GPIPeer*)0)->inputBuffer==28','(u32)&((GPIPeer*)0)->outputBuffer==44','(u32)&((GPIPeer*)0)->nackCount==24','(u32)&((GPIPeer*)0)->profile==16','(u32)&((GPIPeer*)0)->pnext==76','(u32)&((GPIProfile*)0)->peerSig==28']
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


def standard_context_control(row):
    folder=ROOT/'work/w5gc/peer-init/standard-header-negative';folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    source=folder/'match.c';shutil.copyfile(ROOT/row['source'],source);header=folder/'context.h';text=header.read_text();declarations=(folder/'string.h').read_text()
    if '#include "string.h"' not in text:raise ValueError('Actual standard declaration header absent')
    header.write_text(text.replace('#include "string.h"',declarations,1));bad,body=build(source,folder/'genuine-link',negative=True)
    if bad['compiledBytes']!=row['bytes'] or bad['realLink']['exactCallerBytes']:raise ValueError('Same-prototype moved-header negative failed to change original code')
    return dict(status='rejected-nonmatching-context',identicalStandardPrototypes=True,negativeDeclarationHeader='context.h',positiveDeclarationHeader='string.h',compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],sourceSha256=sha256(source),objectSha256=bad['objectSha256'],calleeExecutions=0,callerBehaviorDifferenceClaimed=False,sourceCredit=0)


def execute(rows):
    assert_owned(LANE,OWN_SOURCE)
    for row in rows:verify_original(row,row['nativeSymbolEntries'])
    result=dict(status='passed',actualCompilerGeometry=[geometry(r) for r in rows],standardHeaderContext=standard_context_control(rows[0]),nativeThumbBindingControls=negative_controls(rows),oldNormalizerAndHelperParsersUnchanged=True,actualNativeAndCompilerRelocationsUnmodified=True,sourceCredit=0)
    write_json(LANE/'binding-layout-controls.json',result);return result
