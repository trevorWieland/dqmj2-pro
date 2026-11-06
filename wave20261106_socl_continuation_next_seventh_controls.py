import os
import subprocess
import copy
from project import ROOT
from elftools.elf.elffile import ELFFile
from wave20261106_socl_continuation_next_seventh_bindings import negative_controls
from wave20261106_socl_continuation_next_seventh_compiler import COMPILER
import wave20261106_socl_continuation_next_seventh_bindings as bindings

SOURCE=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/seventh'
WORK=ROOT/'work/w6sc/seventh-controls'
ARGUMENTS={'020909c8':'(ConnectionPrefix*)0,1,2','02090a3c':'(ConnectionPrefix*)0,1,2','02090ae8':'(ConnectionPrefix*)0'}


def sections(path):
    with path.open('rb') as stream:return [(s.name,s.data().hex()) for s in ELFFile(stream).iter_sections() if s['sh_flags']&4]


def compile_source(source,obj,flags):
    return subprocess.run([str(COMPILER),*flags,'-c',str(source),'-o',str(obj)],cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))


def bss_controls(rows):
    value,image,inventory,records,imports=bindings.inputs();view=bindings.VIEWS[0x021d1748];cases=[]
    for row in rows:
        rel=next(r for r in row['relocations'] if r['target']=='0x21d1748');binding=row['nativeSymbolEntries'][rel['symbol']]
        for key,wrong in [('minimumBytes',368),('layoutBytes',367),('recordBytes',88),('records',5),('initializedBytes',1),('storage','data')]:
            bad=dict(view);bad[key]=wrong
            try:bindings.bss_view(row,image,bad)
            except ValueError as error:cases.append(dict(caller=row['address'],case='access-view-'+key,rejected=True,reason=str(error)))
            else:raise ValueError('Incorrect BSS access/layout/storage view admitted')
        wrong=inventory.replace('data_021d1748 kind:bss','data_021d1748 kind:data(any)')
        try:bindings.validate(row,rel,binding,value,image,wrong,records,imports)
        except ValueError as error:cases.append(dict(caller=row['address'],case='initialized-vs-bss-kind',rejected=True,reason=str(error)))
        else:raise ValueError('Initialized source bytes substituted for configured BSS')
        for offset,label in [(0,'record-stride'),(1,'slot-count')]:
            origins={'0x20909c8':[0x2090a28,0x2090a2a],'0x2090a3c':[0x2090aaa,0x2090aac],'0x2090ae8':[0x2090b1c,0x2090b1e]};changed=bytearray(image);changed[origins[row['address']][offset]-0x02000000]^=1
            try:bindings.bss_view(row,bytes(changed),view)
            except ValueError as error:cases.append(dict(caller=row['address'],case='original-'+label,rejected=True,reason=str(error)))
            else:raise ValueError('Changed actual BSS loop stride/bound accepted')
    return dict(status='passed',negativeCases=cases,sourceCredit=0,minimumAccessedSpanBytes=367,chosenArrayLayoutBytes=368,originalCompleteAllocationBytes=None,bssOrInitializedStorageCredit=0)


def execute(rows):
    if SOURCE!=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/seventh' or WORK!=ROOT/'work/w6sc/seventh-controls':raise ValueError('Exact new third control paths differ')
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
    folder=WORK/'layout';folder.mkdir(exist_ok=True);source=folder/'layout.c';checks=['sizeof(void*)==4','sizeof(u16)==2','sizeof(u32)==4','sizeof(u64)==8','sizeof(ConnectionPrefix)==148','(u32)&((ConnectionPrefix*)0)->cached==48','(u32)&((ConnectionPrefix*)0)->session==116','sizeof(SessionView)==92','(u32)&((SessionView*)0)->master==32','(u32)&((SessionView*)0)->when==80','(u32)&((SessionView*)0)->ip==84','(u32)&((SessionView*)0)->port==88','(u32)&((SessionView*)0)->valid==90','(u32)&((SessionView*)0)->padding==91','sizeof(native_data_021d1748)==368']
    source.write_text('#include "context.h"\n'+'\n'.join('typedef char Geometry'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(checks)));obj=folder/'layout.o';layouts=[]
    for label,header,success in [('positive-access-layout',text,True),('wrong-slot-count',text.replace('021d1748[4]','021d1748[3]'),False),('wrong-word-width',text.replace('unsigned long u32','unsigned long long u32'),False),('wrong-port-width',text.replace('u16 port','u32 port'),False),('wrong-tick-width',text.replace('unsigned long long u64','unsigned long u64'),False)]:
        if not success and header==text:raise ValueError('Geometry mutation did not change actual header')
        (folder/'context.h').write_text(header);process=compile_source(source,obj,rows[0]['compilerFlags'])
        if (process.returncode==0)!=success:raise ValueError(('Actual compiler geometry assertion differs',label,process.stdout,process.stderr))
        layouts.append(dict(case=label,exitCode=process.returncode,accepted=success,stdout=process.stdout))
    providers=[]
    for symbol in sorted({symbol for row in rows for symbol,binding in row['nativeSymbolEntries'].items() if binding['kind']=='function'}):
        row=next(r for r in rows if symbol in r['nativeSymbolEntries']);folder=WORK/'providers'/symbol;folder.mkdir(parents=True,exist_ok=True);source=folder/'source.c';source.write_text((ROOT/row['source']).read_text());(folder/'context.h').write_text(text.replace(symbol+'(','missing_callable_declaration(',1));obj=folder/'missing.o';flags=[*row['compilerFlags'],'-requireprotos','-w','error'];process=compile_source(source,obj,flags)
        if process.returncode==0 or obj.exists() or 'no prototype' not in process.stdout:raise ValueError(('Missing actual provider declaration admitted',symbol,process.stdout,process.stderr))
        providers.append(dict(caller=row['address'],provider=symbol,negativeExitCode=process.returncode,negativeStdout=process.stdout,diagnosticFlags=flags))
    return dict(status='passed',sourceCredit=0,originalBindings=negative_controls(rows),bssAccessViewControls=bss_controls(rows),requiredPrototypeDiagnostics=prototypes,requiredProviderDiagnostics=providers,actualGeometryChecks=checks,actualCompilerLayouts=layouts,externalStorageCredit=0,originalCompleteBssAllocationBytes=None)
