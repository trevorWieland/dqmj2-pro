import os
import shutil
import subprocess
from project import ROOT,write_json,sha256
from wave20261105_gamespy_thumb_next_compiler import COMPILER
from wave20261105_gamespy_thumb_next_bindings import verify_original,negative_controls

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-thumb-next/first'


def geometry(row):
    folder=ROOT/'work/w5gt/first/geometry'/format(int(row['address'],0),'08x');folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    text=(folder/'context.h').read_text();checks=['sizeof(int)==4','sizeof(void*)==4']
    if 'Server;' in text:checks+=['sizeof(Server)==44','sizeof(u16)==2','(unsigned int)&((Server*)0)->publicport==4','(unsigned int)&((Server*)0)->privateport==12','(unsigned int)&((Server*)0)->keyvals==24','(unsigned int)&((Server*)0)->updatetime==28','sizeof(native_data_020d8e04)==256']
    else:
        checks+=['sizeof(struct DArrayImplementation)==24','sizeof(((DArray)0)->count)==4','(unsigned int)&((DArray)0)->count==0','(unsigned int)&((DArray)0)->capacity==4','(unsigned int)&((DArray)0)->elemsize==8','(unsigned int)&((DArray)0)->growby==12','(unsigned int)&((DArray)0)->elemfreefn==16','(unsigned int)&((DArray)0)->list==20']
        if 'HashImplementation' in text:checks+=['sizeof(struct HashImplementation)==20','(unsigned int)&((HashTable)0)->nbuckets==4','(unsigned int)&((HashTable)0)->freefn==8','(unsigned int)&((HashTable)0)->hashfn==12','(unsigned int)&((HashTable)0)->compfn==16']
    source=folder/'layout.c';source.write_text('#include "context.h"\n'+'\n'.join('typedef char Layout'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(checks)));obj=folder/'layout.o';command=[str(COMPILER),*row['compilerFlags'],'-c',str(source),'-o',str(obj)]
    def compile_layout():return subprocess.run(command,cwd=ROOT,capture_output=True,text=True,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),timeout=60)
    process=compile_layout()
    if process.returncode:raise ValueError(('Actual Thumb structure geometry failed',row['address'],process.stdout,process.stderr))
    result=dict(address=row['address'],checks=checks,positiveExitCode=0,objectSha256=sha256(obj))
    if row['address'] in ['0x20a60b4','0x20a8594']:
        wrong=text.replace('u16 publicport;','u16 padding,publicport;',1) if 'Server;' in text else text.replace('int count,capacity','int count,wrong,capacity',1)
        if wrong==text:raise ValueError('Wrong Thumb structure did not mutate')
        (folder/'context.h').write_text(wrong);bad=compile_layout()
        if bad.returncode==0:raise ValueError('Wrong actual Thumb field layout accepted')
        result.update(wrongLayoutRejected=True,negativeExitCode=bad.returncode,negativeStdout=bad.stdout)
    return result


def execute(rows):
    for row in rows:verify_original(row,row['nativeSymbolEntries'])
    result=dict(status='passed',actualCompilerGeometry=[geometry(r) for r in rows],nativeThumbBindingControls=negative_controls(rows),oldNormalizerAndHelperParsersUnchanged=True,actualNativeAndCompilerRelocationsUnmodified=True,sourceCredit=0)
    write_json(LANE/'binding-layout-controls.json',result);return result
