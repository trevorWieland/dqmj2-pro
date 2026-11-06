import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261106_dwc_match_tail_next_sixth_build import build
from wave20261106_dwc_match_tail_next_sixth_fixtures import run
from wave20261106_dwc_match_tail_next_sixth_models import cases

LAYOUT=[('sizeof(u64)', 8), ('sizeof(GPBuddyStatus)', 532), ('OFF(GPBuddyStatus,profile)', 0), ('OFF(GPBuddyStatus,status)', 4), ('OFF(GPBuddyStatus,statusString)', 8), ('OFF(GPBuddyStatus,locationString)', 264), ('OFF(GPBuddyStatus,ip)', 520), ('OFF(GPBuddyStatus,port)', 524), ('OFF(GPBuddyStatus,quietModeFlags)', 528), ('sizeof(DWCFriendData)', 12), ('OFF(DWCMatchControl,gt2NumConnection)', 13), ('OFF(DWCMatchControl,qr2MatchType)', 21), ('OFF(DWCMatchControl,qr2NumEntry)', 22), ('OFF(DWCMatchControl,state)', 416), ('OFF(DWCMatchControl,friendCount)', 421), ('OFF(DWCMatchControl,resvWaitCount)', 423), ('OFF(DWCMatchControl,synResendCount)', 427), ('OFF(DWCMatchControl,clWaitTimeoutCount)', 429), ('OFF(DWCMatchControl,baseLatency)', 432), ('OFF(DWCMatchControl,cancelBaseLatency)', 434), ('OFF(DWCMatchControl,cmdResendFlag)', 444), ('OFF(DWCMatchControl,cmdTimeoutTime)', 456), ('OFF(DWCMatchControl,cmdTimeoutStartTick)', 460), ('OFF(DWCMatchControl,synAckBit)', 468), ('OFF(DWCMatchControl,cancelSynAckBit)', 472), ('OFF(DWCMatchControl,lastSynSent)', 480), ('OFF(DWCMatchControl,lastCancelSynSent)', 488), ('OFF(DWCMatchControl,reqProfileID)', 516), ('OFF(DWCMatchControl,priorProfileID)', 520), ('OFF(DWCMatchControl,friendList)', 764), ('OFF(DWCMatchControl,friendIdxList)', 772), ('OFF(DWCMatchControl,friendIdxListLen)', 836), ('OS_SYSTEM_CLOCK', 33514000), ('DWC_GP_PROCESS_INTERVAL', 300)]


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
    entries={
      0x20a1608:('retry-prior-reset','source','priorProfileID = 0;','priorProfileID = 1;','Retain prior profile during retry'),
      0x20a13d8:('friend-required-version','source','== DWC_MATCHING_VERSION)','== DWC_MATCHING_VERSION+1)','Require another peer version'),
      0x20a2544:('sync-timeout-boundary','source','if (passTime > DWC_MATCH_SYN_ACK_WAIT_TIME)','if (passTime >= DWC_MATCH_SYN_ACK_WAIT_TIME)','Timeout one boundary value early'),
      0x20a277c:('cancel-process-interval','header','#define DWC_GP_PROCESS_INTERVAL 300','#define DWC_GP_PROCESS_INTERVAL 301','Subtract an altered cancel process interval')}
    return [entries[address]]


def wrong_source(row,directory):
    source=ROOT/row['source'];text=source.read_text();image=(ROOT/'extract/arm9/arm9.bin').read_bytes();out=[]
    for name,owner,before,after,meaning in changes(int(row['address'],0)):
        folder=directory/name;folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        wrong=folder/source.name;wrong.write_text(text);target=folder/'context.h'if owner=='header'else wrong;old=target.read_text()
        expected=2 if name=='sync-timeout-boundary'else 1
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
