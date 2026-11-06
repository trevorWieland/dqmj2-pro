import os
import subprocess
from project import ROOT
from elftools.elf.elffile import ELFFile
from wave20261106_socl_continuation_next_fourth_bindings import negative_controls
from wave20261106_socl_continuation_next_fourth_compiler import COMPILER

SOURCE=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/fourth'
WORK=ROOT/'work/w6sc/fourth-controls'
ARGUMENTS={n:args for n,args in [('020938b8','(u16*)0,(u16*)0,(u16*)0,4'),('02093930','(u16*)0,(u16*)0,1,4'),('02093998','(u16*)0,(u16*)0,(u16*)0,4'),('02093a18','(u16*)0,(u16*)0,1,4'),('02093a6c','(u16*)0,(u16*)0,4'),('02093ac0','(u16*)0,(u16*)0,(u16*)0,4'),('02093b2c','(u16*)0,(u16*)0,1,4'),('02093b7c','(u16*)0,(u16*)0,4')]}


def sections(path):
    with path.open('rb') as stream:return [(s.name,s.data().hex()) for s in ELFFile(stream).iter_sections() if s['sh_flags']&4]


def compile_source(source,obj,flags):
    return subprocess.run([str(COMPILER),*flags,'-c',str(source),'-o',str(obj)],cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))


def execute(rows):
    if SOURCE!=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/fourth' or WORK!=ROOT/'work/w6sc/fourth-controls':raise ValueError('Exact new third control paths differ')
    text=(SOURCE/'context.h').read_text();prototypes=[]
    for row in rows:
        name=format(int(row['address'],0),'08x');folder=WORK/'prototypes'/name;folder.mkdir(parents=True,exist_ok=True);obj=folder/'explicit.o';flags=[*row['compilerFlags'],'-requireprotos','-w','error'];positive=compile_source(ROOT/row['source'],obj,flags)
        if positive.returncode or sections(obj)!=sections(ROOT/row['object']):raise ValueError(('Actual C99 prototypes failed or executable sections changed',positive.stdout,positive.stderr))
        symbol='native_main_'+name;header=folder/'context.h';header.write_text(text);call=folder/'callsite.c';call.write_text('#include "context.h"\nextern void diagnostic(void);\nvoid diagnostic(void){'+symbol+'('+ARGUMENTS[name]+');}\n');good=compile_source(call,folder/'callsite.o',flags)
        if good.returncode:raise ValueError(('Typed actual-entry callsite failed',good.stdout,good.stderr))
        if text.count(symbol+'(')!=1:raise ValueError('Missing actual callable prototype mutation ambiguous')
        header.write_text(text.replace(symbol+'(','missing_callable_declaration(',1));badobj=folder/'missing.o';bad=compile_source(call,badobj,flags)
        if bad.returncode==0 or badobj.exists() or 'no prototype' not in bad.stdout:raise ValueError(('Missing callable declaration admitted',bad.stdout,bad.stderr))
        prototypes.append(dict(caller=row['address'],positiveExitCode=0,executableSectionsUnchanged=True,typedActualEntryCallsitePassed=True,missingActualEntry=symbol,negativeExitCode=bad.returncode,negativeStdout=bad.stdout,diagnosticFlags=flags,diagnosticCallerSourceCredit=0))
    folder=WORK/'layout';folder.mkdir(exist_ok=True);source=folder/'layout.c';checks=['sizeof(void*)==4','sizeof(u16)==2','sizeof(u32)==4','sizeof(s32)==4','((s32)-1)<0','((u16)-1)==65535','((u32)-1)==0xffffffff']
    source.write_text('#include "context.h"\n'+'\n'.join('typedef char Geometry'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(checks)));obj=folder/'layout.o';layouts=[]
    for label,header,success in [('positive',text,True),('wrong-halfword-width',text.replace('unsigned short u16','unsigned char u16'),False),('wrong-word-width',text.replace('unsigned long u32','unsigned long long u32'),False),('wrong-signed-length',text.replace('typedef int s32','typedef unsigned int s32'),False)]:
        if not success and header==text:raise ValueError('Geometry mutation did not change actual header')
        (folder/'context.h').write_text(header);process=compile_source(source,obj,rows[0]['compilerFlags'])
        if (process.returncode==0)!=success:raise ValueError(('Actual compiler geometry assertion differs',label,process.stdout,process.stderr))
        layouts.append(dict(case=label,exitCode=process.returncode,accepted=success,stdout=process.stdout))
    providers=[]
    for symbol in ['native_fn_02093874','native_fn_02008d78','native_fn_02093aa0']:
        row=next(r for r in rows if symbol in r['nativeSymbolEntries']);folder=WORK/'providers'/symbol;folder.mkdir(parents=True,exist_ok=True);source=folder/'source.c';source.write_text((ROOT/row['source']).read_text());(folder/'context.h').write_text(text.replace(symbol+'(','missing_callable_declaration(',1));obj=folder/'missing.o';flags=[*row['compilerFlags'],'-requireprotos','-w','error'];process=compile_source(source,obj,flags)
        if process.returncode==0 or obj.exists() or 'no prototype' not in process.stdout:raise ValueError(('Missing actual provider declaration admitted',symbol,process.stdout,process.stderr))
        providers.append(dict(caller=row['address'],provider=symbol,negativeExitCode=process.returncode,negativeStdout=process.stdout,diagnosticFlags=flags))
    return dict(status='passed',sourceCredit=0,originalBindings=negative_controls(rows),requiredPrototypeDiagnostics=prototypes,requiredProviderDiagnostics=providers,actualGeometryChecks=checks,actualCompilerLayouts=layouts,externalStorageCredit=0)
