import copy
import os
import shutil
import subprocess
from project import ROOT
from elftools.elf.elffile import ELFFile
from wave20261106_game_main_arm_next_fifth_bindings import verify_original,negative_controls
from wave20261106_game_main_arm_next_compiler import COMPILER

SOURCE=ROOT/'src/runtime/parallel_wave20261105/game-main-arm-next/fifth'
WORK=ROOT/'work/w6gm/fifth-controls'


def sections(path):
    with path.open('rb') as stream:return [(s.name,s.data().hex()) for s in ELFFile(stream).iter_sections() if s['sh_flags']&4]


def compile_source(source,obj,flags):
    return subprocess.run([str(COMPILER),*flags,'-c',str(source),'-o',str(obj)],cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))


def execute(rows):
    if SOURCE!=ROOT/'src/runtime/parallel_wave20261105/game-main-arm-next/fifth' or WORK!=ROOT/'work/w6gm/fifth-controls':raise ValueError('Exact initializer control paths differ')
    cases=[]
    for row in rows:
        verify_original(row,row['nativeSymbolEntries'])
        for symbol,binding in row['nativeSymbolEntries'].items():
            if binding['kind']!='function':continue
            for label,key,value in [('wrong-mode','mode','thumb'),('wrong-CPU','processor','arm7'),('wrong-program','program','child'),('wrong-overlay','module','ov000'),('wrong-address','address',hex(int(binding['address'],0)+4)),('function-as-data','kind','data')]:
                wrong=copy.deepcopy(row['nativeSymbolEntries']);wrong[symbol][key]=value
                try:verify_original(row,wrong)
                except ValueError as error:cases.append(dict(caller=row['address'],symbol=symbol,case=label,rejected=True,reason=str(error)))
                else:raise ValueError('Wrong initializer provider admitted')
    row=rows[0];folder=WORK/'prototypes';folder.mkdir(parents=True,exist_ok=True);obj=folder/'explicit.o';flags=[*row['compilerFlags'],'-requireprotos','-w','error'];positive=compile_source(ROOT/row['source'],obj,flags)
    if positive.returncode or sections(obj)!=sections(ROOT/row['object']):raise ValueError(('Initializer prototypes failed or executable changed',positive.stdout,positive.stderr))
    text=(SOURCE/'initializer.h').read_text();symbol='native_fn_02065730'
    if text.count(symbol+'(')!=1:raise ValueError('Missing allocator prototype mutation ambiguous')
    (folder/'initializer.h').write_text(text.replace(symbol+'(','missing_callable_declaration(',1));wrong=folder/'missing.c';shutil.copyfile(ROOT/row['source'],wrong);badobj=folder/'missing.o';bad=compile_source(wrong,badobj,flags)
    if bad.returncode==0 or badobj.exists() or 'no prototype' not in bad.stdout:raise ValueError(('Missing actual allocator prototype admitted',bad.stdout,bad.stderr))
    declarations=dict(positiveExitCode=0,executableSectionsUnchanged=True,missingActualProvider=symbol,negativeExitCode=bad.returncode,negativeStdout=bad.stdout,diagnosticFlags=flags)
    folder=WORK/'layout';folder.mkdir(exist_ok=True);source=folder/'layout.c';checks=['sizeof(void*)==4','sizeof(Layout)==12','(u32)&((ContextPrefix*)0)->rows[1]==0x1c','(u32)&((ContextPrefix*)0)->cursor25c==0x25c','sizeof(ContextPrefix)==0x260','sizeof(native_data_020de394)==22']
    source.write_text('#include "initializer.h"\n'+'\n'.join('typedef char Geometry'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(checks)));obj=folder/'layout.o';layouts=[]
    for label,header,success in [('positive',text,True),('wrong-row-stride',text.replace('words[3]','words[4]'),False),('wrong-cursor-offset',text.replace('gap88[0x1d4]','gap88[0x1d8]'),False),('wrong-name-prefix',text.replace('020de394[22]','020de394[21]'),False)]:
        (folder/'initializer.h').write_text(header);process=compile_source(source,obj,row['compilerFlags'])
        if (process.returncode==0)!=success:raise ValueError(('Initializer geometry assertion differs',label,process.stdout,process.stderr))
        layouts.append(dict(case=label,exitCode=process.returncode,accepted=success,stdout=process.stdout))
    return dict(status='passed',sourceCredit=0,originalBindingRejections=cases,originalDataRejections=negative_controls(rows),requiredPrototypeDiagnostics=declarations,actualGeometryChecks=checks,actualCompilerLayouts=layouts,completeOriginalAllocationExtent=None,externalStorageCredit=0)
