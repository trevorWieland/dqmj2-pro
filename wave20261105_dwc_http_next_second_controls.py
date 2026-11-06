import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261105_dwc_http_next_second_build import build
from wave20261105_dwc_http_next_second_fixtures import run
from wave20261105_dwc_http_next_second_models import cases

LAYOUT=[('sizeof(u32)',4),('sizeof(void*)',4),('sizeof(long)',4),('sizeof(DWCHttpParam)',28),('OFF(DWCHttpParam,alloc)',12),('OFF(DWCHttpParam,free)',16),('OFF(DWCHttpParam,ignoreca)',20),('OFF(DWCHttpParam,timeout)',24),('sizeof(DWCHttp)',7188),('OFF(DWCHttp,initflag)',4096),('OFF(DWCHttp,param)',4100),('OFF(DWCHttp,error)',4128),('OFF(DWCHttp,url)',4132),('OFF(DWCHttp,hostname)',4388),('OFF(DWCHttp,filepath)',4392),('OFF(DWCHttp,port)',4404),('OFF(DWCHttp,lowrecvbuf)',6604),('OFF(DWCHttp,lowsendbuf)',6608),('OFF(DWCHttp,lowentropydata)',6612),('OFF(DWCHttp,num_postitem)',6644),('OFF(DWCHttp,req)',6648),('OFF(DWCHttp,rep)',6664),('OFF(DWCHttp,content_len_mutex)',6680),('OFF(DWCHttp,content_len)',6704),('OFF(DWCHttp,receivedbody_len)',6708),('OFF(DWCHttp,labelvalue)',6712),('OFF(DWCHttp,thread)',6968),('OFF(DWCHttp,thread.state)',7076),('OFF(DWCHttp,mutex)',7160),('OFF(DWCHttp,abort)',7184),('sizeof(Thread)',192),('sizeof(Mutex)',24),('sizeof(DWCHttpBuffer)',16)]


def layouts(row,directory,wrong=False):
    directory.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
    checks=LAYOUT
    text='#include "context.h"\n#define OFF(T,m) ((size_t)&(((T*)0)->m))\n'
    text+='\n'.join('typedef char check_%d[(%s)==%d?1:-1];'%(index,expression,expected+(1 if wrong and index==0 else 0)) for index,(expression,expected) in enumerate(checks))+'\n'
    source=directory/'layout.c';source.write_text(text);obj=directory/'layout.o'
    command=[str(ROOT/row['compilerPath']),*row['compilerFlags'],'-c',str(source),'-o',str(obj)]
    process=subprocess.run(command,cwd=ROOT,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=60)
    if (process.returncode==0)==wrong:raise ValueError(('Pinned C layout result differs',wrong,process.stdout,process.stderr))
    return dict(checks=len(checks),allPassed=not wrong,rejected=wrong,sourceSha256=sha256(source),compilerSha256=row['compilerSha256'],flags=row['compilerFlags'],stdout=process.stdout,stderr=process.stderr)


def changes(address):
    values={
        0x209820c:('clear-span','source','sizeof(*http)','sizeof(*http)-4','Leave final HTTP abort word uncleared'),
        0x20982e4:('body-presence','source','if(length)','if(!length)','Generate content length for empty body instead of nonempty body'),
        0x209834c:('exact-ignoreca','source','ignoreca==1','ignoreca!=0','Normalize arbitrary nonzero word instead of original exact one'),
        0x20987b0:('clear-span','source','sizeof(*http)','sizeof(*http)-4','Leave final HTTP abort word uncleared'),
        0x2098954:('post-counter','source','num_postitem++','num_postitem+=2','Increment original post-item counter twice')}
    result=[values[address]]
    if address==0x209820c:result.append(('returned-error','source','return http->error;','return 1;','Discard original returned error word'))
    return result




def wrong_source(row,directory):
    source=ROOT/row['source'];text=source.read_text();image=(ROOT/'extract/arm9/arm9.bin').read_bytes();out=[]
    for name,owner,before,after,meaning in changes(int(row['address'],0)):
        folder=directory/name;folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        wrong=folder/source.name;wrong.write_text(text);target=folder/'context.h'if owner=='header'else wrong;old=target.read_text()
        expected=2 if int(row['address'],0)==0x20b70c8 and name=='cookie-endian'else 1
        if old.count(before)!=expected:raise ValueError(('Expected source mutation count changed',name,old.count(before),expected))
        target.write_text(old.replace(before,after));bad,body=build(wrong,folder/'build',negative=True);violations=[]
        for seed,vector in enumerate(cases(int(row['address'],0))):
            record=run(image,row,body,vector,seed)
            if not record['modelPassed']:
                violations.append(dict(vector=vector,seed=seed,actualReturningModelViolation=record))
                if len(violations)==4:break
        if not violations:raise ValueError(('Wrong SDK packet C passed independent caller oracle',name))
        out.append(dict(address=row['address'],case=name,meaning=meaning,sourceSha256=sha256(wrong),objectSha256=bad['objectSha256'],compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],sourceDependencies=bad['sourceDependencies'],rejectedByCompleteNativeComparison=True,actualReturningModelRejections=len(violations),witnesses=violations,sourceOrExecutionCredit=0))
    return out
