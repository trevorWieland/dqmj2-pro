import copy
import os
import shutil
import subprocess
from project import ROOT,sha256
from elftools.elf.elffile import ELFFile
from wave20261104_main_tail_bindings import verify_original
from wave20261106_game_main_arm_next_compiler import COMPILER

SOURCE=ROOT/'src/runtime/parallel_wave20261105/game-main-arm-next/first'
WORK=ROOT/'work/w6gm/first-controls'


def sections(path):
    with path.open('rb') as stream:return [(s.name,s.data().hex()) for s in ELFFile(stream).iter_sections() if s['sh_flags']&4]


def compile_source(source,obj,flags):
    return subprocess.run([str(COMPILER),*flags,'-c',str(source),'-o',str(obj)],cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))


def execute(rows):
    if SOURCE!=ROOT/'src/runtime/parallel_wave20261105/game-main-arm-next/first' or WORK!=ROOT/'work/w6gm/first-controls':raise ValueError('Exclusive control directories differ')
    cases=[]
    for row in rows:
        verify_original(row,row['nativeSymbolEntries'])
        for symbol in row['nativeSymbolEntries']:
            for label,key,value in [('wrong-mode','mode','thumb'),('wrong-CPU','processor','arm7'),('wrong-program','program','utility'),('same-address-wrong-overlay','module','ov000'),('wrong-address','address','0x2061948'),('function-as-data','kind','data')]:
                bindings=copy.deepcopy(row['nativeSymbolEntries']);bindings[symbol][key]=value
                try:verify_original(row,bindings)
                except ValueError as error:cases.append(dict(caller=row['address'],symbol=symbol,case=label,rejected=True,reason=str(error)))
                else:raise ValueError('Wrong original provider identity accepted')
    declarations=[]
    for row in rows:
        name=format(int(row['address'],0),'08x');folder=WORK/'prototypes'/name;folder.mkdir(parents=True,exist_ok=True);obj=folder/'explicit.o';flags=[*row['compilerFlags'],'-requireprotos','-w','error']
        positive=compile_source(ROOT/row['source'],obj,flags)
        if positive.returncode or sections(obj)!=sections(ROOT/row['object']):raise ValueError(('Explicit real C99 prototypes failed or changed code',positive.stdout,positive.stderr))
        text=(SOURCE/'context.h').read_text();selected='native_fn_0207211c' if name=='020720a4' else 'native_main_'+name
        if text.count(selected+'(')!=1:raise ValueError('Missing actual prototype mutation ambiguous')
        (folder/'context.h').write_text(text.replace(selected+'(','missing_callable_declaration(',1));wrong=folder/'missing.c';shutil.copyfile(ROOT/row['source'],wrong);badobj=folder/'missing.o';bad=compile_source(wrong,badobj,flags)
        if bad.returncode==0 or badobj.exists() or 'no prototype' not in bad.stdout:raise ValueError(('Required actual prototype was not rejected',bad.stdout,bad.stderr))
        declarations.append(dict(caller=row['address'],positiveExitCode=0,executableSectionsUnchanged=True,negativeDeclaration=selected,negativeExitCode=bad.returncode,negativeStdout=bad.stdout,diagnosticFlags=flags))
    row=next(r for r in rows if r['address']=='0x20720a4');folder=WORK/'layout';folder.mkdir(exist_ok=True);header=(SOURCE/'context.h').read_text();source=folder/'layout.c';source.write_text('#include "context.h"\n');commandFlags=row['compilerFlags'];obj=folder/'layout.o';layout=[]
    for label,text,success in [('positive',header,True),('wrong-stride',header.replace('words[3]','words[4]'),False),('wrong-prefix',header.replace('prefix[16]','prefix[20]'),False)]:
        (folder/'context.h').write_text(text);process=compile_source(source,obj,commandFlags)
        if (process.returncode==0)!=success:raise ValueError(('Actual layout assertion status differs',label,process.stdout,process.stderr))
        layout.append(dict(case=label,exitCode=process.returncode,stdout=process.stdout,accepted=success))
    return dict(status='passed',sourceCredit=0,originalBindingRejections=cases,requiredPrototypeDiagnostics=declarations,actualCompilerLayout=layout,layoutScope='12-byte record stride and16-byte prefix/136-byte ABI view only; original complete allocation unknown and storage credit zero')
