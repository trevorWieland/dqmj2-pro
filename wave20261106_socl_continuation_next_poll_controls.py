import os
import shutil
import subprocess
from project import ROOT
from elftools.elf.elffile import ELFFile
from wave20261106_socl_continuation_next_poll_bindings import negative_controls
from wave20261106_socl_continuation_next_poll_compiler import COMPILER

SOURCE=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/second'
WORK=ROOT/'work/w6sc/poll-controls'


def sections(path):
    with path.open('rb') as stream:return [(s.name,s.data().hex()) for s in ELFFile(stream).iter_sections() if s['sh_flags']&4]


def compile_source(source,obj,flags):
    return subprocess.run([str(COMPILER),*flags,'-c',str(source),'-o',str(obj)],cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))


def execute(rows):
    if SOURCE!=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/second' or WORK!=ROOT/'work/w6sc/poll-controls':raise ValueError('Exact new poll control paths differ')
    text=(SOURCE/'poll.h').read_text();prototypes=[];row=rows[0]
    for symbol in ['native_fn_02090138','native_fn_02006b7c']:
        folder=WORK/'prototypes'/symbol;folder.mkdir(parents=True,exist_ok=True);obj=folder/'explicit.o';flags=[*row['compilerFlags'],'-requireprotos','-w','error'];positive=compile_source(ROOT/row['source'],obj,flags)
        if positive.returncode or sections(obj)!=sections(ROOT/row['object']):raise ValueError(('Actual C99 prototypes failed or executable sections changed',positive.stdout,positive.stderr))
        if text.count(symbol+'(')!=1:raise ValueError('Missing actual callable prototype mutation ambiguous')
        (folder/'poll.h').write_text(text.replace(symbol+'(','missing_callable_declaration(',1));wrong=folder/'missing.c';shutil.copyfile(ROOT/row['source'],wrong);badobj=folder/'missing.o';bad=compile_source(wrong,badobj,flags)
        if bad.returncode==0 or badobj.exists() or 'no prototype' not in bad.stdout:raise ValueError(('Missing callable declaration admitted',bad.stdout,bad.stderr))
        prototypes.append(dict(caller=row['address'],positiveExitCode=0,executableSectionsUnchanged=True,missingActualProvider=symbol,negativeExitCode=bad.returncode,negativeStdout=bad.stdout,diagnosticFlags=flags))
    folder=WORK/'layout';folder.mkdir(exist_ok=True);source=folder/'layout.c';checks=['sizeof(void*)==4','sizeof(u64)==8','sizeof(s64)==8','sizeof(s32)==4','sizeof(PollEntry)==8','(u32)&((PollEntry*)0)->events==4','(u32)&((PollEntry*)0)->revents==6','sizeof(((PollEntry*)0)->events)==2','sizeof(((PollEntry*)0)->revents)==2']
    source.write_text('#include "poll.h"\n'+'\n'.join('typedef char Geometry'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(checks)));obj=folder/'layout.o';layouts=[]
    for label,header,success in [('positive',text,True),('wrong-event-field-order',text.replace('events,revents','revents,events'),False),('wrong-event-width',text.replace('s16 events,revents','s32 events,revents'),False),('wrong-descriptor-width',text.replace('s32 fd','s16 fd'),False)]:
        if not success and header==text:raise ValueError('Geometry mutation did not change actual header')
        (folder/'poll.h').write_text(header);process=compile_source(source,obj,row['compilerFlags'])
        if (process.returncode==0)!=success:raise ValueError(('Actual compiler geometry assertion differs',label,process.stdout,process.stderr))
        layouts.append(dict(case=label,exitCode=process.returncode,accepted=success,stdout=process.stdout))
    return dict(status='passed',sourceCredit=0,originalBindings=negative_controls(rows),requiredPrototypeDiagnostics=prototypes,actualGeometryChecks=checks,actualCompilerLayouts=layouts,externalStorageCredit=0)
