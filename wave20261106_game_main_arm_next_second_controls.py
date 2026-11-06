import copy
import os
import shutil
import subprocess
from project import ROOT,sha256
from elftools.elf.elffile import ELFFile
from wave20261106_game_main_arm_next_second_bindings import verify_original,negative_controls
from wave20261106_game_main_arm_next_compiler import COMPILER

SOURCE=ROOT/'src/runtime/parallel_wave20261105/game-main-arm-next/second'
WORK=ROOT/'work/w6gm/second-controls'


def sections(path):
    with path.open('rb') as stream:return [(s.name,s.data().hex()) for s in ELFFile(stream).iter_sections() if s['sh_flags']&4]


def compile_source(source,obj,flags):
    return subprocess.run([str(COMPILER),*flags,'-c',str(source),'-o',str(obj)],cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))


def execute(rows):
    if SOURCE!=ROOT/'src/runtime/parallel_wave20261105/game-main-arm-next/second' or WORK!=ROOT/'work/w6gm/second-controls':raise ValueError('Exclusive second control paths differ')
    cases=[]
    for row in rows:
        verify_original(row,row['nativeSymbolEntries'])
        for symbol,binding in row['nativeSymbolEntries'].items():
            if binding['kind']!='function':continue
            for label,key,value in [('wrong-mode','mode','thumb'),('wrong-CPU','processor','arm7'),('wrong-program','program','child'),('same-address-wrong-overlay','module','ov000'),('wrong-address','address','0x2061948'),('function-as-data','kind','data')]:
                bindings=copy.deepcopy(row['nativeSymbolEntries']);bindings[symbol][key]=value
                try:verify_original(row,bindings)
                except ValueError as error:cases.append(dict(caller=row['address'],symbol=symbol,case=label,rejected=True,reason=str(error)))
                else:raise ValueError('Wrong original second provider identity admitted')
    declarations=[];providers={'02072568':'native_fn_0206de44','020728ec':'native_fn_02049ad0','02072de8':'native_fn_0204b53c'}
    for row in rows:
        name=format(int(row['address'],0),'08x');folder=WORK/'prototypes'/name;folder.mkdir(parents=True,exist_ok=True);obj=folder/'explicit.o';flags=[*row['compilerFlags'],'-requireprotos','-w','error'];positive=compile_source(ROOT/row['source'],obj,flags)
        if positive.returncode or sections(obj)!=sections(ROOT/row['object']):raise ValueError(('Explicit second C99 prototypes failed or changed code',positive.stdout,positive.stderr))
        text=(SOURCE/'context.h').read_text();selected=providers[name]
        if text.count(selected+'(')!=1:raise ValueError('Missing actual second provider mutation ambiguous')
        (folder/'context.h').write_text(text.replace(selected+'(','missing_callable_declaration(',1));wrong=folder/'missing.c';shutil.copyfile(ROOT/row['source'],wrong);badobj=folder/'missing.o';bad=compile_source(wrong,badobj,flags)
        if bad.returncode==0 or badobj.exists() or 'no prototype' not in bad.stdout:raise ValueError(('Missing second provider prototype admitted',bad.stdout,bad.stderr))
        declarations.append(dict(caller=row['address'],positiveExitCode=0,executableSectionsUnchanged=True,missingActualProvider=selected,negativeExitCode=bad.returncode,negativeStdout=bad.stdout,diagnosticFlags=flags))
    folder=WORK/'layout';folder.mkdir(exist_ok=True);header=(SOURCE/'context.h').read_text();source=folder/'layout.c';checks=['sizeof(void*)==4','sizeof(u32)==4','sizeof(Point)==4','sizeof(ByteColumn)==9','sizeof(SignedColumn)==9','(u32)&((WidgetPrefix*)0)->field5==5','(u32)&((Point*)0)->x==0','(u32)&((Point*)0)->y==2']
    source.write_text('#include "context.h"\n'+'\n'.join('typedef char Geometry'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(checks)));flags=rows[0]['compilerFlags'];obj=folder/'layout.o';layout=[]
    for label,text,success in [('positive',header,True),('wrong-column-stride',header.replace('gap[8]','gap[7]'),False),('wrong-widget-field',header.replace('prefix[5]','prefix[6]'),False),('wrong-halfword-order',header.replace('s16 x,y','s16 y,x'),False)]:
        (folder/'context.h').write_text(text);process=compile_source(source,obj,flags)
        if (process.returncode==0)!=success:raise ValueError(('Actual second layout assertion differs',label,process.stdout,process.stderr))
        layout.append(dict(case=label,exitCode=process.returncode,stdout=process.stdout,accepted=success))
    return dict(status='passed',sourceCredit=0,originalBindingRejections=cases,originalDataRejections=negative_controls(rows),requiredPrototypeDiagnostics=declarations,actualCompilerGeometryChecks=checks,actualCompilerLayout=layout,completeOriginalAllocationExtent=None,externalStorageCredit=0)
