import os
import shutil
import subprocess
from project import ROOT
from elftools.elf.elffile import ELFFile
from wave20261106_socl_continuation_next_bindings import negative_controls
from wave20261106_socl_continuation_next_compiler import COMPILER

SOURCE=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/first'
WORK=ROOT/'work/w6sc/first-controls'


def sections(path):
    with path.open('rb') as stream:return [(s.name,s.data().hex()) for s in ELFFile(stream).iter_sections() if s['sh_flags']&4]


def compile_source(source,obj,flags):
    return subprocess.run([str(COMPILER),*flags,'-c',str(source),'-o',str(obj)],cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))


def execute(rows):
    if SOURCE!=ROOT/'src/runtime/parallel_wave20261105/socl-continuation-next/first' or WORK!=ROOT/'work/w6sc/first-controls':raise ValueError('Exact new continuation control paths differ')
    text=(SOURCE/'context.h').read_text();prototypes=[];missing={'0209075c':'0209009c','02090794':'020061ac','0209088c':'020908f0','0209302c':'02092cb8','020930ac':'0209302c','020936f4':'02093180','02093774':'020936f4'}
    for row in rows:
        name=format(int(row['address'],0),'08x');folder=WORK/'prototypes'/name;folder.mkdir(parents=True,exist_ok=True);obj=folder/'explicit.o';flags=[*row['compilerFlags'],'-requireprotos','-w','error'];positive=compile_source(ROOT/row['source'],obj,flags)
        if positive.returncode or sections(obj)!=sections(ROOT/row['object']):raise ValueError(('Actual C99 prototypes failed or executable sections changed',name,positive.stdout,positive.stderr))
        symbol='native_fn_'+missing[name]
        if text.count(symbol+'(')!=1:raise ValueError('Missing actual callable prototype mutation ambiguous')
        (folder/'context.h').write_text(text.replace(symbol+'(','missing_callable_declaration(',1));wrong=folder/'missing.c';shutil.copyfile(ROOT/row['source'],wrong);badobj=folder/'missing.o';bad=compile_source(wrong,badobj,flags)
        if bad.returncode==0 or badobj.exists() or 'no prototype' not in bad.stdout:raise ValueError(('Missing callable declaration admitted',name,bad.stdout,bad.stderr))
        prototypes.append(dict(caller=row['address'],positiveExitCode=0,executableSectionsUnchanged=True,missingActualProvider=symbol,negativeExitCode=bad.returncode,negativeStdout=bad.stdout,diagnosticFlags=flags))
    folder=WORK/'layout';folder.mkdir(exist_ok=True);source=folder/'layout.c';checks=['sizeof(void*)==4','sizeof(u64)==8','sizeof(Address)==4','sizeof(PollEntry)==8','(u32)&((PollEntry*)0)->events==4','(u32)&((PollEntry*)0)->revents==6','(u32)&((SocketPrefix*)0)->state==0x70','(u32)&((SocketPrefix*)0)->mode==0x73','sizeof(SocketPrefix)==116','sizeof(Md5View)==88','(u32)&((Md5View*)0)->low==16','(u32)&((Md5View*)0)->high==20','(u32)&((Md5View*)0)->buffer==24','sizeof(Sha1View)==92','(u32)&((Sha1View*)0)->high==20','(u32)&((Sha1View*)0)->low==24','(u32)&((Sha1View*)0)->buffer==28','sizeof(native_data_020de81c)==12','sizeof(native_data_020de8d8)==64','sizeof(native_data_020dea18)==64']
    checks+=['sizeof(((Md5View*)0)->buffer)==64','sizeof(((Sha1View*)0)->buffer)==64']
    source.write_text('#include "context.h"\n'+'\n'.join('typedef char Geometry'+str(i)+'[('+c+')?1:-1];' for i,c in enumerate(checks)));obj=folder/'layout.o';layouts=[]
    for label,header,success in [('positive',text,True),('wrong-socket-mode-offset',text.replace('s8 block,mode','s8 mode,block'),False),('wrong-counter-word-order',text.replace('state[4],low,high','state[4],high,low'),False),('wrong-block-size',text.replace('buffer[64]','buffer[63]'),False),('wrong-format-prefix',text.replace('020de81c[12]','020de81c[11]'),False)]:
        (folder/'context.h').write_text(header);process=compile_source(source,obj,rows[0]['compilerFlags'])
        if (process.returncode==0)!=success:raise ValueError(('Actual compiler geometry assertion differs',label,process.stdout,process.stderr))
        layouts.append(dict(case=label,exitCode=process.returncode,accepted=success,stdout=process.stdout))
    return dict(status='passed',sourceCredit=0,originalBindings=negative_controls(rows),requiredPrototypeDiagnostics=prototypes,actualGeometryChecks=checks,actualCompilerLayouts=layouts,completeOriginalObjectExtents=None,externalStorageCredit=0)
