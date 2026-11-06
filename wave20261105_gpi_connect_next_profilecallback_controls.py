from wave20261105_gpi_connect_next_profilecallback_paths import assert_owned,EVIDENCE,SOURCE as OWN_SOURCE,WORK as OWN_WORK
import os
import shutil
import subprocess
from project import ROOT,write_json,sha256
from wave20261105_gpi_connect_next_profilecallback_compiler import COMPILER,compare
from wave20261105_gpi_connect_next_profilecallback_bindings import verify_original,negative_controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gpi-connect-next/profilecallback'


def geometry(row):
    assert_owned(LANE,OWN_SOURCE)
    if not (ROOT/row["source"]).resolve().is_relative_to(OWN_SOURCE.resolve()):raise ValueError("Record layout source escaped exact own directory")
    folder=ROOT/'work/w5gc/profilecallback/geometry'/format(int(row['address'],0),'08x');folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    text=(folder/'context.h').read_text();checks=['sizeof(void*)==4','sizeof(GPIConnection)==0x5d8','(u32)&((GPIConnection*)0)->profileList==0x5c8']
    checks+=['sizeof(GPConnectResponseArg)==32','sizeof(GPNewProfileResponseArg)==8','sizeof(GPDeleteProfileResponseArg)==8','sizeof(GPGetInfoResponseArg)==516','sizeof(GPProfileSearchResponseArg)==16','sizeof(GPIOperation)==36','(u32)&((GPIOperation*)0)->callback==12','(u32)&((GPIOperation*)0)->result==28'] if int(row['address'],0)==0x20af7f8 else ['sizeof(GPIProfile)==32','(u32)&((GPIProfile*)0)->profileId==0','(u32)&((GPIProfile*)0)->userId==4']
    source=folder/'layout.c';source.write_text('#include "context.h"\n#undef serverreqs\n'+'\n'.join('typedef char Layout'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(checks)));obj=folder/'layout.o';command=[str(COMPILER),*row['compilerFlags'],'-c',str(source),'-o',str(obj)]
    def compile_layout():return subprocess.run(command,cwd=ROOT,capture_output=True,text=True,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),timeout=60)
    process=compile_layout()
    if process.returncode:raise ValueError(('Actual Thumb structure geometry failed',row['address'],process.stdout,process.stderr))
    result=dict(address=row['address'],checks=checks,positiveExitCode=0,objectSha256=sha256(obj))
    wrong=text.replace('GPResult result;GPProfile profile;}GPDeleteProfileResponseArg','GPResult result;GPProfile profile;int wrongExtra;}GPDeleteProfileResponseArg',1) if int(row['address'],0)==0x20af7f8 else text.replace('int profileId,userId;','int wrongPrefix,profileId,userId;',1)
    if wrong==text:raise ValueError('Wrong GP callback-prefix layout did not mutate')
    (folder/'context.h').write_text(wrong);bad=compile_layout()
    if bad.returncode==0:raise ValueError('Wrong GP callback-prefix layout accepted')
    result.update(wrongLayoutRejected=True,negativeExitCode=bad.returncode,negativeStdout=bad.stdout)
    return result


def intrinsic_context_control(row):
    folder=ROOT/'work/w5gc/profilecallback/intrinsic-context-negative';folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    source=folder/'match.c';shutil.copyfile(ROOT/row['source'],source)
    header=folder/'context.h';text=header.read_text();prototype=(folder/'string.h').read_text()
    if '#include "string.h"' not in text:raise ValueError('Real standard-header declaration absent')
    header.write_text(text.replace('#include "string.h"',prototype,1));rows,unused=compare(source,folder/'compile');bad=rows[0]
    if bad.get('compileFailed') or bad['compiledBytes']!=108 or bad['exactAfterDeclaredRelocation'] or not any(r['symbol']=='memset' for r in bad['relocations']):raise ValueError('Measured declaration-header negative did not reproduce external memset108B mismatch')
    return dict(status='rejected-nonmatching-context',sameActualPrototype=True,originalHeader='string.h',negativeDeclarationHeader='context.h',negativeCompiledBytes=bad['compiledBytes'],negativeObject=bad['object'],negativeObjectSha256=bad['objectSha256'],oldSourceOrCompilerFlagsChanged=False,sourceCredit=0)


def execute(rows):
    assert_owned(LANE,OWN_SOURCE)
    for row in rows:verify_original(row,row['nativeSymbolEntries'])
    result=dict(status='passed',actualCompilerGeometry=[geometry(r) for r in rows],standardDeclarationHeaderControl=intrinsic_context_control(next(r for r in rows if int(r['address'],0)==0x20b09e0)),nativeThumbBindingControls=negative_controls(rows),oldNormalizerAndHelperParsersUnchanged=True,actualNativeAndCompilerRelocationsUnmodified=True,sourceCredit=0)
    write_json(LANE/'binding-layout-controls.json',result);return result
