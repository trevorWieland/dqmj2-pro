import os
import shutil
import subprocess
from project import ROOT,write_json,sha256
from wave20261105_gamespy_thumb_next_sorting_compiler import COMPILER
from wave20261105_gamespy_thumb_next_sorting_bindings import verify_original,negative_controls,slot_negative_controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-thumb-next/sorting'


def geometry(row):
    folder=ROOT/'work/w5gt/sorting/geometry'/format(int(row['address'],0),'08x');folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    text=(folder/'context.h').read_text();checks=['sizeof(int)==4','sizeof(void*)==4','sizeof(char)==1','sizeof(SortGlobal)==8','(u32)&((SortGlobal*)0)->active==4','sizeof(native_data_020e0350)==1','sizeof(u32)==4','sizeof(u16)==2','sizeof(u8)==1','sizeof(struct Server)==44','(u32)&((struct Server*)0)->state==20','(u32)&((struct Server*)0)->flags==21','sizeof(GOACryptState)==261','sizeof(SortInfo)==260','sizeof(SBQueryEngine)==76','sizeof(SBServerList)==2012','sizeof(struct _ServerBrowser)==2112','(u32)&((SBQueryEngine*)0)->querylist.count==16','(u32)&((SBQueryEngine*)0)->numserverkeys==64','(u32)&((struct _ServerBrowser*)0)->list==76','(u32)&((struct _ServerBrowser*)0)->dontUpdate==2092','(u32)&((struct _ServerBrowser*)0)->triggerIP==2096','(u32)&((struct _ServerBrowser*)0)->triggerPort==2100','(u32)&((struct _ServerBrowser*)0)->BrowserCallback==2104','(u32)&((struct _ServerBrowser*)0)->instance==2108']
    source=folder/'layout.c';source.write_text('#include "context.h"\n'+'\n'.join('typedef char Layout'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(checks)));obj=folder/'layout.o';command=[str(COMPILER),*row['compilerFlags'],'-c',str(source),'-o',str(obj)]
    def compile_layout():return subprocess.run(command,cwd=ROOT,capture_output=True,text=True,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),timeout=60)
    process=compile_layout()
    if process.returncode:raise ValueError(('Actual Thumb structure geometry failed',row['address'],process.stdout,process.stderr))
    result=dict(address=row['address'],checks=checks,positiveExitCode=0,objectSha256=sha256(obj))
    if row['address'] in ('0x20a6cc0','0x20a69f8'):
        wrong=text.replace('u32 uninterpreted;SBServerList*active;','SBServerList*active;u32 uninterpreted;',1) if row['address']=='0x20a6cc0' else text.replace('char sortkey[255];','char sortkey[251];',1)
        if wrong==text:raise ValueError('Wrong browser version/layout did not mutate')
        (folder/'context.h').write_text(wrong);bad=compile_layout()
        if bad.returncode==0:raise ValueError('Wrong browser version/layout accepted')
        result.update(wrongLayoutRejected=True,negativeExitCode=bad.returncode,negativeStdout=bad.stdout)
    return result


def execute(rows):
    for row in rows:verify_original(row,row['nativeSymbolEntries'])
    result=dict(status='passed',actualCompilerGeometry=[geometry(r) for r in rows],nativeThumbBindingControls=negative_controls(rows),typedSortSlotNegativeControls=slot_negative_controls(rows),oldNormalizerAndHelperParsersUnchanged=True,actualNativeAndCompilerRelocationsUnmodified=True,sourceCredit=0)
    write_json(LANE/'binding-layout-controls.json',result);return result
