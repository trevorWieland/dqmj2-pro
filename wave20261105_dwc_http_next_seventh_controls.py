import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261105_dwc_http_next_seventh_build import build
from wave20261105_dwc_http_next_seventh_fixtures import run
from wave20261105_dwc_http_next_seventh_models import cases

LAYOUT=[('sizeof(u32)',4),('sizeof(void*)',4),('sizeof(long)',4),('sizeof(DWCHttpParam)',28),('OFF(DWCHttpParam,alloc)',12),('OFF(DWCHttpParam,free)',16),('OFF(DWCHttpParam,ignoreca)',20),('OFF(DWCHttpParam,timeout)',24),('sizeof(DWCHttp)',7188),('OFF(DWCHttp,initflag)',4096),('OFF(DWCHttp,param)',4100),('OFF(DWCHttp,error)',4128),('OFF(DWCHttp,url)',4132),('OFF(DWCHttp,hostname)',4388),('OFF(DWCHttp,filepath)',4392),('OFF(DWCHttp,port)',4404),('OFF(DWCHttp,lowrecvbuf)',6604),('OFF(DWCHttp,lowsendbuf)',6608),('OFF(DWCHttp,lowentropydata)',6612),('OFF(DWCHttp,num_postitem)',6644),('OFF(DWCHttp,req)',6648),('OFF(DWCHttp,rep)',6664),('OFF(DWCHttp,content_len_mutex)',6680),('OFF(DWCHttp,content_len)',6704),('OFF(DWCHttp,receivedbody_len)',6708),('OFF(DWCHttp,labelvalue)',6712),('OFF(DWCHttp,thread)',6968),('OFF(DWCHttp,thread.id)',7076),('OFF(DWCHttp,mutex)',7160),('OFF(DWCHttp,abort)',7184),('sizeof(Thread)',192),('sizeof(Mutex)',24),('sizeof(DWCHttpBuffer)',16)]
LAYOUT += [('sizeof(DWCSvlResult)',372),('sizeof(DWCSvlIntWorkarea)',7200),('OFF(DWCSvlIntWorkarea,alloc)',0),('OFF(DWCSvlIntWorkarea,free)',4),('OFF(DWCSvlIntWorkarea,http)',8),('OFF(DWCSvlIntWorkarea,result)',7196),('OFF(DWCSvlIntWorkarea,http.thread.id)',7084),('OFF(DWCSvlIntWorkarea,http.error)',4136)]
LAYOUT += [('sizeof(Scheduler)',8),('OFF(Scheduler,current)',4),('OFF(DWCSvlResult,status)',0),('OFF(DWCSvlResult,svlhost)',4),('OFF(DWCSvlResult,svltoken)',69)]


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
    if address==0x2099df4:return [('receive-length','source','param.len_recvbuf=4096;','param.len_recvbuf=4095;','Change the supplied receive-buffer length'),('priority','source','native_data_020e33e4.current)-1','native_data_020e33e4.current)-2','Change the current-thread priority decrement'),('cal-return','source','native_fn_02097dc4(cal)==0','native_fn_02097dc4(cal)!=0','Invert the measured Cal return-word boundary')]
    if address==0x209a03c:return [('errno','source','native_data_020ec9b0==34','native_data_020ec9b0==0','Reject errno zero instead of actual34'),('return-code','source','status>=100','status>100','Accept the original error boundary100'),('zero-host','source','svlhost,64)<0','svlhost,64)<=0','Reject a zero-length host decode accepted by native caller')]
    raise ValueError('Outside SVL request/result')


def wrong_source(row,directory):
    source=ROOT/row['source'];text=source.read_text();image=(ROOT/'extract/arm9/arm9.bin').read_bytes();out=[]
    for name,owner,before,after,meaning in changes(int(row['address'],0)):
        folder=directory/name;folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        wrong=folder/source.name;wrong.write_text(text);target=folder/'context.h'if owner=='header'else wrong;old=target.read_text()
        expected=2 if name=='errno'else 1
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
