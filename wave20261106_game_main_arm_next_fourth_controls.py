import copy
import os
import shutil
import subprocess
from project import ROOT
from elftools.elf.elffile import ELFFile
from wave20261106_game_main_arm_next_fourth_bindings import verify_original,negative_controls
from wave20261106_game_main_arm_next_compiler import COMPILER

SOURCE=ROOT/'src/runtime/parallel_wave20261105/game-main-arm-next/fourth'
WORK=ROOT/'work/w6gm/fourth-controls'


def sections(path):
    with path.open('rb') as stream:return [(s.name,s.data().hex()) for s in ELFFile(stream).iter_sections() if s['sh_flags']&4]


def compile_source(source,obj,flags):
    return subprocess.run([str(COMPILER),*flags,'-c',str(source),'-o',str(obj)],cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))


def execute(rows):
    if SOURCE!=ROOT/'src/runtime/parallel_wave20261105/game-main-arm-next/fourth' or WORK!=ROOT/'work/w6gm/fourth-controls':raise ValueError('Exact fourth control paths differ')
    cases=[]
    for row in rows:
        verify_original(row,row['nativeSymbolEntries'])
        for symbol,binding in row['nativeSymbolEntries'].items():
            if binding['kind']!='function':continue
            for label,key,value in [('wrong-mode','mode','thumb'),('wrong-CPU','processor','arm7'),('wrong-program','program','child'),('same-address-wrong-overlay','module','ov000'),('wrong-address','address',hex(int(binding['address'],0)+4)),('function-as-data','kind','data')]:
                wrong=copy.deepcopy(row['nativeSymbolEntries']);wrong[symbol][key]=value
                try:verify_original(row,wrong)
                except ValueError as error:cases.append(dict(caller=row['address'],symbol=symbol,case=label,rejected=True,reason=str(error)))
                else:raise ValueError('Wrong rectangle provider identity admitted')
    row=rows[0];folder=WORK/'prototypes';folder.mkdir(parents=True,exist_ok=True);obj=folder/'explicit.o';flags=[*row['compilerFlags'],'-requireprotos','-w','error'];positive=compile_source(ROOT/row['source'],obj,flags)
    if positive.returncode or sections(obj)!=sections(ROOT/row['object']):raise ValueError(('Actual rectangle prototype failed or changed executable sections',positive.stdout,positive.stderr))
    text=(SOURCE/'context.h').read_text();symbol='native_fn_02072ed4'
    if text.count(symbol+'(')!=1:raise ValueError('Missing actual rectangle provider mutation ambiguous')
    (folder/'context.h').write_text(text.replace(symbol+'(','missing_callable_declaration(',1));wrong=folder/'missing.c';shutil.copyfile(ROOT/row['source'],wrong);badobj=folder/'missing.o';bad=compile_source(wrong,badobj,flags)
    if bad.returncode==0 or badobj.exists() or 'no prototype' not in bad.stdout:raise ValueError(('Missing byte-index predicate prototype admitted',bad.stdout,bad.stderr))
    declarations=dict(positiveExitCode=0,executableSectionsUnchanged=True,missingActualProvider=symbol,negativeExitCode=bad.returncode,negativeStdout=bad.stdout,diagnosticFlags=flags)
    folder=WORK/'layout';folder.mkdir(exist_ok=True);source=folder/'layout.c';checks=['sizeof(void*)==4','sizeof(Row)==9','sizeof(native_data_021c5a11)==18','(u32)&((Row*)0)->x==2','(u32)&((Row*)0)->y==3','(u32)&((Row*)0)->enabled==5','sizeof(Sample)==3','(u32)&((Sample*)0)->x==1','(u32)&((Sample*)0)->y==2','sizeof(Hit)==7','(u32)&((Hit*)0)->index==2','(u32)&((Hit*)0)->field6==6']
    source.write_text('#include "context.h"\n'+'\n'.join('typedef char Geometry'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(checks)));obj=folder/'layout.o';layouts=[]
    for label,header,success in [('positive',text,True),('wrong-row-stride',text.replace('field8;} Row','field8,extra;} Row'),False),('wrong-hit-index',text.replace('u8 gap1,index','u8 gap1[2],index'),False),('wrong-sample-axis',text.replace('u8 field0,x,y','u8 field0,y,x'),False)]:
        (folder/'context.h').write_text(header);process=compile_source(source,obj,row['compilerFlags'])
        if (process.returncode==0)!=success:raise ValueError(('Actual rectangle geometry assertion differs',label,process.stdout,process.stderr))
        layouts.append(dict(case=label,exitCode=process.returncode,accepted=success,stdout=process.stdout))
    return dict(status='passed',sourceCredit=0,originalBindingRejections=cases,originalDataRejections=negative_controls(rows),requiredPrototypeDiagnostics=declarations,actualGeometryChecks=checks,actualCompilerLayouts=layouts,completeOriginalAllocationExtent=None,externalStorageCredit=0)
