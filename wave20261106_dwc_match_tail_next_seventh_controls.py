import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261106_dwc_match_tail_next_seventh_build import build
from wave20261106_dwc_match_tail_next_seventh_fixtures import run
from wave20261106_dwc_match_tail_next_seventh_models import cases

LAYOUT=[('sizeof(u32)', 4), ('sizeof(struct sockaddr_in)', 8), ('OFF(struct sockaddr_in,sin_len)', 0), ('OFF(struct sockaddr_in,sin_family)', 1), ('OFF(struct sockaddr_in,sin_port)', 2), ('OFF(struct sockaddr_in,sin_addr)', 4), ('sizeof(native_data_021d1b88)', 4), ('sizeof(DWCMatchOptMinCompleteIn)', 32), ('OFF(DWCMatchOptMinCompleteIn,valid)', 0), ('OFF(DWCMatchOptMinCompleteIn,timeout)', 4), ('OFF(DWCMatchOptMinCompleteIn,recvBit)', 8), ('OFF(DWCMatchOptMinCompleteIn,timeoutBit)', 12), ('OFF(DWCMatchOptMinCompleteIn,startTime)', 16), ('OFF(DWCMatchControl,nnFinishTime)', 396), ('OFF(DWCMatchControl,nnInfo)', 404), ('OFF(DWCMatchControl,clLinkProgress)', 420), ('OFF(DWCMatchControl,resvWaitCount)', 423), ('OFF(DWCMatchControl,cmdResendFlag)', 444), ('OFF(DWCMatchControl,cmdResendTick)', 448), ('OFF(DWCMatchControl,cmdTimeoutStartTick)', 460), ('OFF(DWCMatchControl,profileID)', 512), ('OFF(DWCMatchControl,reqProfileID)', 516), ('OFF(DWCMatchControl,priorProfileID)', 520), ('OFF(DWCMatchControl,cbEventPid)', 524), ('OFF(DWCMatchControl,cmdCnt)', 972)]


def layouts(row,directory,wrong=False):
    directory.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
    checks=LAYOUT
    text='#include "context.h"\n#define OFF(T,m) ((unsigned long)&(((T*)0)->m))\n'
    text+='\n'.join('typedef char check_%d[(%s)==%d?1:-1];'%(index,expression,expected+((-4 if index==1 else 1)if wrong and index==(1 if row['address']=='0x20a13d8'else 0)else 0)) for index,(expression,expected) in enumerate(checks))+'\n'
    source=directory/'layout.c';source.write_text(text);obj=directory/'layout.o'
    command=[str(ROOT/row['compilerPath']),*row['compilerFlags'],'-c',str(source),'-o',str(obj)]
    process=subprocess.run(command,cwd=ROOT,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=60)
    if (process.returncode==0)==wrong:raise ValueError(('Pinned C layout result differs',wrong,process.stdout,process.stderr))
    return dict(checks=len(checks),allPassed=not wrong,rejected=wrong,sourceSha256=sha256(source),compilerSha256=row['compilerSha256'],flags=row['compilerFlags'],stdout=process.stdout,stderr=process.stderr)


def changes(address):
    assert address==0x20a039c
    return [('address-byte-order','header','#define SO_HtoNs(n) ((unsigned char)((n)>>8)|(((n)<<8)&0xff00))','#define SO_HtoNs(n) (n)','Forward host port bytes without network conversion'),('resend-wait-reset','source','resvWaitCount = 0;','resvWaitCount = 1;','Preserve a wrong reservation wait count')]


def wrong_source(row,directory):
    source=ROOT/row['source'];text=source.read_text();image=(ROOT/'extract/arm9/arm9.bin').read_bytes();out=[]
    for name,owner,before,after,meaning in changes(int(row['address'],0)):
        folder=directory/name;folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        wrong=folder/source.name;wrong.write_text(text);target=folder/'context.h'if owner=='header'else wrong;old=target.read_text()
        expected=3 if name=='resend-wait-reset'else 1
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
