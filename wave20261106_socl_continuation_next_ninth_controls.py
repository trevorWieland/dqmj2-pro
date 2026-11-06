import os
import subprocess
import copy
from project import ROOT
from elftools.elf.elffile import ELFFile
from wave20261106_socl_continuation_next_ninth_bindings import negative_controls
from wave20261106_socl_continuation_next_ninth_compiler import COMPILER
import wave20261106_socl_continuation_next_ninth_bindings as bindings

SOURCE=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/ninth'
WORK=ROOT/'work/w6sc/ninth-controls'
ARGUMENTS={'02092778':'(SocketView*)0','02092b50':'(SocketView*)0','02092bf0':'1'}


def sections(path):
    with path.open('rb') as stream:return [(s.name,s.data().hex()) for s in ELFFile(stream).iter_sections() if s['sh_flags']&4]


def compile_source(source,obj,flags):
    return subprocess.run([str(COMPILER),*flags,'-c',str(source),'-o',str(obj)],cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))


def bss_controls(rows):
    value,image,inventory,records,imports=bindings.inputs();view=bindings.VIEWS[0x021d1748];cases=[]
    row=next(r for r in rows if r['address']=='0x2092bf0')
    rel=next(r for r in row['relocations'] if r['target']=='0x21d1748');binding=row['nativeSymbolEntries'][rel['symbol']]
    for key,wrong in [('minimumBytes',368),('layoutBytes',367),('recordBytes',88),('records',5),('initializedBytes',1),('storage','data')]:
        bad=dict(view);bad[key]=wrong
        try:bindings.bss_view(row,image,bad)
        except ValueError as error:cases.append(dict(caller=row['address'],case='access-view-'+key,rejected=True,reason=str(error)))
        else:raise ValueError('Incorrect BSS access/layout/storage view admitted')
    for target,function in [(0x21d1748,bindings.bss_view),(0x20e33e4,bindings.thread_view)]:
        rel=next(r for r in row['relocations']if int(r['target'],0)==target);binding=row['nativeSymbolEntries'][rel['symbol']];wrong=inventory.replace('data_'+format(target,'08x')+' kind:bss','data_'+format(target,'08x')+' kind:data(any)')
        try:bindings.validate(row,rel,binding,value,image,wrong,records,imports)
        except ValueError as error:cases.append(dict(case='initialized-vs-bss-kind-'+hex(target),rejected=True,reason=str(error)))
        else:raise ValueError('Initialized data substituted for configured BSS')
    for origin in [0x2092c1a,0x2092c1c,0x2092c26,0x2092c32,0x2092c34,0x2092c6c]:
        function=bindings.bss_view if origin<0x2092c20 else bindings.thread_view;target=0x21d1748 if origin<0x2092c20 else 0x20e33e4;changed=bytearray(image);changed[origin-0x02000000]^=1
        try:function(row,bytes(changed),bindings.VIEWS[target])
        except ValueError as error:cases.append(dict(case='original-typed-field-instruction-'+hex(origin),rejected=True,reason=str(error)))
        else:raise ValueError('Changed original BSS loop/thread field admitted')
    for key,wrong in [('minimumBytes',8),('width',2),('initializedBytes',1),('storage','data'),('type','whole-thread-allocation')]:
        view=dict(bindings.VIEWS[0x20e33e4]);view[key]=wrong
        try:bindings.thread_view(row,image,view)
        except ValueError as error:cases.append(dict(case='thread-view-'+key,rejected=True,reason=str(error)))
        else:raise ValueError('Incorrect thread access view admitted')
    return dict(status='passed',negativeCases=cases,sourceCredit=0,minimumAccessedSpanBytes=367,chosenArrayLayoutBytes=368,originalCompleteAllocationBytes=None,bssOrInitializedStorageCredit=0)


def execute(rows):
    if SOURCE!=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/ninth' or WORK!=ROOT/'work/w6sc/ninth-controls':raise ValueError('Exact new third control paths differ')
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
    folder=WORK/'layout';folder.mkdir(exist_ok=True);source=folder/'layout.c';checks=['sizeof(void*)==4', 'sizeof(u8)==1', 'sizeof(u16)==2', 'sizeof(u32)==4', 'sizeof(ConnectionView)==2076', '(u32)&((ConnectionView*)0)->cached==48', '(u32)&((ConnectionView*)0)->reuse==49', '(u32)&((ConnectionView*)0)->state==1109', 'sizeof(SocketView)==32', '(u32)&((SocketView*)0)->ssl==12', '(u32)&((SocketView*)0)->when==16', '(u32)&((SocketView*)0)->port==24', '(u32)&((SocketView*)0)->ip==28', 'sizeof(SessionView)==92', '(u32)&((SessionView*)0)->when==80', '(u32)&((SessionView*)0)->valid==90', 'sizeof(native_data_021d1748)==368', 'sizeof(ThreadView)==168', '(u32)&((ThreadView*)0)->next==104', '(u32)&((ThreadView*)0)->socket==164', 'sizeof(ThreadInfoView)==12', '(u32)&((ThreadInfoView*)0)->first==8']
    source.write_text('#include "context.h"\n'+'\n'.join('typedef char Geometry'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(checks)));obj=folder/'layout.o';layouts=[]
    for label,header,success in [('positive-access-layout',text,True),('wrong-slot-count',text.replace('021d1748[4]','021d1748[3]'),False),('wrong-word-width',text.replace('unsigned long u32','unsigned long long u32'),False),('wrong-port-width',text.replace('u16 port','u32 port'),False),('wrong-thread-field-offset',text.replace('before_socket[56]','before_socket[60]'),False)]:
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
