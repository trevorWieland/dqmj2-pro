import os
import subprocess
import copy
from project import ROOT
from elftools.elf.elffile import ELFFile
from wave20261106_socl_continuation_next_sixth_bindings import negative_controls
from wave20261106_socl_continuation_next_sixth_compiler import COMPILER
import wave20261106_socl_continuation_next_sixth_compiler as compiler
import wave20261106_socl_continuation_next_sixth_bindings as bindings

SOURCE=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/sixth'
WORK=ROOT/'work/w6sc/sixth-controls'
ARGUMENTS={'02091518':'(u8*)0,1,2,4','0209158c':'(ConnectionView*)0,(u8*)0','020917f8':'(u8*)0,(char*)0,(ConnectionView*)0','02091864':'(ConnectionView*)0'}


def sections(path):
    with path.open('rb') as stream:return [(s.name,s.data().hex()) for s in ELFFile(stream).iter_sections() if s['sh_flags']&4]


def compile_source(source,obj,flags):
    return subprocess.run([str(COMPILER),*flags,'-c',str(source),'-o',str(obj)],cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))


def helper_controls(rows):
    row=next(r for r in rows if r['address']=='0x209158c');rel=next(r for r in row['relocations'] if r['symbol']=='_s32_div_f');binding=row['nativeSymbolEntries'][rel['symbol']];value,image,inventory,records,imports=bindings.inputs();cases=[]
    for label,key,wrong in [('compiler','compilerSha256','0'*64),('frontend','compilerFlags',[s if s!='c99' else 'c++' for s in row['compilerFlags']]),('processor-profile','compilerFlags',[s if s!='arm946e' else 'arm7tdmi' for s in row['compilerFlags']])]:
        bad=copy.deepcopy(row);bad[key]=wrong
        try:bindings.validate(bad,rel,binding,value,image,inventory,records,imports)
        except ValueError as error:cases.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong compiler-helper profile admitted')
    for name in ['_u32_div_f','_s32_div']:
        bad=dict(rel,symbol=name)
        try:bindings.validate(row,bad,binding,value,image,inventory,records,imports)
        except ValueError as error:cases.append(dict(case='helper-name-'+name,rejected=True,reason=str(error)))
        else:raise ValueError('Different ELF helper name admitted')
    for caller in ['02091518','020917f8','02091864','02093180']:
        try:compiler.helper_address('_s32_div_f',caller,compiler.C.symbol_address)
        except ValueError as error:cases.append(dict(case='resolver-caller-'+caller,rejected=True,reason=str(error)))
        else:raise ValueError('Helper resolver escaped exact caller scope')
    before=compiler.C.FLAGS,compiler.C.WORK,compiler.C.symbol_address,compiler.C.compare
    def failure(*args,**kwargs):
        if compiler.C.symbol_address('_s32_div_f')!=0x02026144:raise AssertionError('Delegated helper identity differs')
        raise RuntimeError('controlled-private-frontend-failure')
    compiler.C.compare=failure
    try:
        try:compiler.compare(SOURCE/'0209158c.c',WORK/'failure-restoration')
        except RuntimeError as error:
            if str(error)!='controlled-private-frontend-failure':raise
        else:raise ValueError('Controlled delegate failure did not propagate')
    finally:compiler.C.compare=before[3]
    if compiler.C.FLAGS is not before[0] or compiler.C.WORK!=before[1] or compiler.C.symbol_address is not before[2]:raise ValueError('Private delegation did not restore original frontend state')
    return dict(status='passed',cases=cases,exactElfHelperName='_s32_div_f',canonicalOriginalArmEntry='0x02026144',controlledFailureRestoredAllOriginalGlobals=True,objectBytesOrSymbolsEdited=False,calleeSourceCredit=0)


def execute(rows):
    if SOURCE!=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/sixth' or WORK!=ROOT/'work/w6sc/sixth-controls':raise ValueError('Exact new third control paths differ')
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
    folder=WORK/'layout';folder.mkdir(exist_ok=True);source=folder/'layout.c';checks=['sizeof(void*)==4','sizeof(u16)==2','sizeof(u32)==4','sizeof(s32)==4','((s32)-1)<0','sizeof(ConnectionView)==1112','sizeof(((ConnectionView*)0)->randoms)==64','sizeof(((ConnectionView*)0)->before_sha1)==692','(u32)&((ConnectionView*)0)->cached==48','(u32)&((ConnectionView*)0)->method==50','(u32)&((ConnectionView*)0)->randoms==52','(u32)&((ConnectionView*)0)->session==116','(u32)&((ConnectionView*)0)->sha1tmp==840','(u32)&((ConnectionView*)0)->md5tmp==1020','(u32)&((ConnectionView*)0)->state==1109','sizeof(native_data_020de87c)==2','sizeof(native_data_020de880)==3','sizeof(native_data_020de884)==4']
    source.write_text('#include "context.h"\n'+'\n'.join('typedef char Geometry'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(checks)));obj=folder/'layout.o';layouts=[]
    for label,header,success in [('positive-access-prefix',text,True),('wrong-method-width',text.replace('u16 method','u32 method'),False),('wrong-word-width',text.replace('unsigned long u32','unsigned long long u32'),False),('wrong-random-extent',text.replace('randoms[64]','randoms[63]'),False),('wrong-context-field-offset',text.replace('before_sha1[692]','before_sha1[688]'),False)]:
        if not success and header==text:raise ValueError('Geometry mutation did not change actual header')
        (folder/'context.h').write_text(header);process=compile_source(source,obj,rows[0]['compilerFlags'])
        if (process.returncode==0)!=success:raise ValueError(('Actual compiler geometry assertion differs',label,process.stdout,process.stderr))
        layouts.append(dict(case=label,exitCode=process.returncode,accepted=success,stdout=process.stdout))
    providers=[]
    for symbol in sorted({symbol for row in rows for symbol,binding in row['nativeSymbolEntries'].items() if binding['kind']=='function' and symbol.startswith('native_fn_')}):
        row=next(r for r in rows if symbol in r['nativeSymbolEntries']);folder=WORK/'providers'/symbol;folder.mkdir(parents=True,exist_ok=True);source=folder/'source.c';source.write_text((ROOT/row['source']).read_text());(folder/'context.h').write_text(text.replace(symbol+'(','missing_callable_declaration(',1));obj=folder/'missing.o';flags=[*row['compilerFlags'],'-requireprotos','-w','error'];process=compile_source(source,obj,flags)
        if process.returncode==0 or obj.exists() or 'no prototype' not in process.stdout:raise ValueError(('Missing actual provider declaration admitted',symbol,process.stdout,process.stderr))
        providers.append(dict(caller=row['address'],provider=symbol,negativeExitCode=process.returncode,negativeStdout=process.stdout,diagnosticFlags=flags))
    return dict(status='passed',sourceCredit=0,originalBindings=negative_controls(rows),compilerHelperScope=helper_controls(rows),requiredPrototypeDiagnostics=prototypes,requiredProviderDiagnostics=providers,actualGeometryChecks=checks,actualCompilerLayouts=layouts,externalStorageCredit=0,originalCompleteConnectionAllocationBytes=None)
