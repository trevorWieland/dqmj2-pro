import copy
import os
import shutil
import subprocess
import match_runtime as C
from project import ROOT,sha256
from wave20261104_main_tail_compiler import COMPILER
from wave20261105_main_later_next_bindings import verify_original,negative_controls


def layout_checks():
    directory=ROOT/'work/w5ml/next/controls/layout';directory.mkdir(parents=True,exist_ok=True)
    header=ROOT/'src/runtime/parallel_wave20261104/main-arm-later/next/context.h';shutil.copyfile(header,directory/'context.h')
    conditions=['sizeof(int)==4','sizeof(u32)==4','sizeof(void*)==4','(u32)&((CounterParent*)0)->field11c==0x11c','sizeof(((CounterParent*)0)->field11c)==4','(u32)&((QueueNode*)0)->field8==8','sizeof(((QueueNode*)0)->field8)==4','sizeof(Object150)==0x150','(u32)&((Object150*)0)->field110==0x110','sizeof(((Object150*)0)->field110)==4','(u32)&((Object150*)0)->field14c==0x14c','sizeof(Heap58)==0x58','(u32)&((Heap58*)0)->field0==0','(u32)&((Heap58*)0)->field8==8','sizeof(Allocator12)==12','(u32)&((Allocator12*)0)->base==0','(u32)&((Allocator12*)0)->limit==4','(u32)&((Allocator12*)0)->used==8','sizeof(GlobalSlot10)==16','(u32)&((GlobalSlot10*)0)->key==0','sizeof(((GlobalSlot10*)0)->key)==4','sizeof(ModeState)==8','(u32)&((ModeState*)0)->field4==4','sizeof(((ModeState*)0)->field4)==4']
    source=directory/'layout.c';source.write_text('#include "context.h"\n'+'\n'.join('typedef char NativeLayout'+str(i)+'[('+condition+')?1:-1];' for i,condition in enumerate(conditions))+'\n');output=directory/'layout.o'
    command=[str(COMPILER),*C.FLAGS,'-opt','speed','-c',str(source),'-o',str(output)];environment=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'))
    process=subprocess.run(command,cwd=ROOT,env=environment,capture_output=True,text=True,timeout=60)
    if process.returncode:raise ValueError(('Actual native ABI witnesses failed',process.stdout,process.stderr))
    positive=dict(checks=conditions,compilerSha256=sha256(COMPILER),headerSha256=sha256(header),sourceSha256=sha256(source),objectSha256=sha256(output),exitCode=process.returncode)
    wrong=header.read_text().replace('u32 reservedc;','u32 reservedc[2];')
    if wrong==header.read_text():raise ValueError('Typed stride mutation did not apply')
    (directory/'context.h').write_text(wrong);failed=subprocess.run(command,cwd=ROOT,env=environment,capture_output=True,text=True,timeout=60)
    if failed.returncode==0 or 'illegal constant expression' not in failed.stdout:raise ValueError('Actual compiler accepted incompatible stride')
    return dict(positive=positive,wrongStrideRejected=True,wrongStrideExitCode=failed.returncode,wrongHeaderSha256=sha256(directory/'context.h'),wrongCompileOutput=failed.stdout+failed.stderr,sourceCredit=0)


def execute(rows):
    row=next(r for r in rows if r['address']=='0x203a77c');name='native_fn_02007ff4';checks=[]
    changes=[('target-address','binding','address','0x2008008'),('target-module','binding','module','ov000'),('target-mode','binding','mode','thumb'),('target-CPU','binding','processor','arm7'),('target-program','binding','program','dwc/utility.bin/move/child.srl'),('target-kind','binding','kind','data'),('caller-mode','row','mode','thumb'),('caller-module','row','module','ov000')]
    for label,owner,key,value in changes:
        changed=copy.deepcopy(row);bindings=copy.deepcopy(row['nativeSymbolEntries'])
        (bindings[name] if owner=='binding' else changed)[key]=value
        try:verify_original(changed,bindings)
        except ValueError as error:checks.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Invalid original function binding accepted: '+label)
    for entry in rows:verify_original(entry,entry['nativeSymbolEntries'])
    return dict(status='passed',negativeBindingCases=checks,dataLoadQualification=negative_controls(rows),actualCompilerLayoutWitnesses=layout_checks(),allOriginalBranchesAndRelocationsUnchanged=True,externalStorageExtentAuthorshipCredit=0)
