import os
import subprocess
from project import ROOT
from elftools.elf.elffile import ELFFile
from wave20261106_socl_continuation_next_eleventh_naming_v2_bindings import negative_controls
from wave20261106_socl_continuation_next_eleventh_naming_v2_compiler import COMPILER

SOURCE=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/eleventh-naming-v2'
WORK=ROOT/'work/w6sc/eleventh-naming-v2-controls'
ARGUMENTS={'020911b0':'(ConnectionView*)0','02091c5c':'(ConnectionView*)0,(u8*)0'}


def sections(path):
    with path.open('rb') as stream:return [(s.name,s.data().hex()) for s in ELFFile(stream).iter_sections() if s['sh_flags']&4]


def compile_source(source,obj,flags):
    return subprocess.run([str(COMPILER),*flags,'-c',str(source),'-o',str(obj)],cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))


def execute(rows):
    if SOURCE!=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/eleventh-naming-v2' or WORK!=ROOT/'work/w6sc/eleventh-naming-v2-controls':raise ValueError('Exact new third control paths differ')
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
    folder=WORK/'layout';folder.mkdir(exist_ok=True);source=folder/'layout.c';checks=['sizeof(void*)==4', 'sizeof(u32)==4', 'sizeof(s32)==4', '((s32)-1)<0', 'sizeof(Md5View)==88', 'sizeof(Sha1View)==92', 'sizeof(ConnectionView)==2076', '(u32)&((ConnectionView*)0)->receive_secret==468', '(u32)&((ConnectionView*)0)->sequence==740', 'sizeof(((ConnectionView*)0)->sequence)==8', '(u32)&((ConnectionView*)0)->sha1tmp==840', '(u32)&((ConnectionView*)0)->md5tmp==1020', '(u32)&((ConnectionView*)0)->state==1109', '(u32)&((ConnectionView*)0)->certificate_algorithm==1112', '(u32)&((ConnectionView*)0)->pub_algorithm==1116', '(u32)&((ConnectionView*)0)->hash_start==1120', '(u32)&((ConnectionView*)0)->hash_end==1124', '(u32)&((ConnectionView*)0)->certificate_hash==1128', '(u32)&((ConnectionView*)0)->certificate_hash_length==1148', '(u32)&((ConnectionView*)0)->date_ok==1455', '(u32)&((ConnectionView*)0)->issuer==1456']
    source.write_text('#include "context.h"\n'+'\n'.join('typedef char Geometry'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(checks)));obj=folder/'layout.o';layouts=[]
    for label,header,success in [('positive-access-layout',text,True),('wrong-secret-pointer-offset',text.replace('before_secret[320]','before_secret[316]'),False),('wrong-word-width',text.replace('unsigned long u32','unsigned long long u32'),False),('wrong-server-field',text.replace('u8 server,state','u8 state,server'),False),('wrong-certificate-flag-offset',text.replace('before_flag[303]','before_flag[304]'),False)]:
        if not success and header==text:raise ValueError('Geometry mutation did not change actual header')
        (folder/'context.h').write_text(header);process=compile_source(source,obj,rows[0]['compilerFlags'])
        if (process.returncode==0)!=success:raise ValueError(('Actual compiler geometry assertion differs',label,process.stdout,process.stderr))
        layouts.append(dict(case=label,exitCode=process.returncode,accepted=success,stdout=process.stdout))
    providers=[]
    for symbol in sorted({symbol for row in rows for symbol,binding in row['nativeSymbolEntries'].items() if binding['kind']=='function'}):
        row=next(r for r in rows if symbol in r['nativeSymbolEntries']);folder=WORK/'providers'/symbol;folder.mkdir(parents=True,exist_ok=True);source=folder/'source.c';source.write_text((ROOT/row['source']).read_text());(folder/'context.h').write_text(text.replace(symbol+'(','missing_callable_declaration(',1));obj=folder/'missing.o';flags=[*row['compilerFlags'],'-requireprotos','-w','error'];process=compile_source(source,obj,flags)
        if process.returncode==0 or obj.exists() or 'no prototype' not in process.stdout:raise ValueError(('Missing actual provider declaration admitted',symbol,process.stdout,process.stderr))
        providers.append(dict(caller=row['address'],provider=symbol,negativeExitCode=process.returncode,negativeStdout=process.stdout,diagnosticFlags=flags))
    return dict(status='passed',sourceCredit=0,originalBindings=negative_controls(rows),requiredPrototypeDiagnostics=prototypes,requiredProviderDiagnostics=providers,actualGeometryChecks=checks,actualCompilerLayouts=layouts,externalStorageCredit=0)
