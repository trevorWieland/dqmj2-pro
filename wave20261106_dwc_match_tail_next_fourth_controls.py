import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261106_dwc_match_tail_next_fourth_build import build
from wave20261106_dwc_match_tail_next_fourth_fixtures import run
from wave20261106_dwc_match_tail_next_fourth_models import cases

LAYOUT=[('sizeof(u32)', 4), ('sizeof(DWCError)', 4), ('sizeof(DWCMatchResetLevel)', 4), ('sizeof(GT2Connection)', 4), ('OFF(DWCMatchControl,pGt2Socket)', 4), ('OFF(DWCMatchControl,gt2NumConnection)', 13), ('OFF(DWCMatchControl,qr2Obj)', 16), ('OFF(DWCMatchControl,qr2NNFinishCount)', 20), ('OFF(DWCMatchControl,qr2MatchType)', 21), ('OFF(DWCMatchControl,qr2IsReserved)', 23), ('OFF(DWCMatchControl,qr2Reservation)', 32), ('OFF(DWCMatchControl,sbUpdateFlag)', 232), ('OFF(DWCMatchControl,sbUpdateTick)', 236), ('OFF(DWCMatchControl,sbPidList)', 244), ('OFF(DWCMatchControl,nnInfo)+OFF(DWCNNInfo,cookie)', 412), ('OFF(DWCMatchControl,state)', 416), ('OFF(DWCMatchControl,distantFriend)', 422), ('OFF(DWCMatchControl,closeState)', 424), ('OFF(DWCMatchControl,cancelBaseLatency)', 434), ('OFF(DWCMatchControl,cancelSynAckBit)', 472), ('OFF(DWCMatchControl,lastCancelSynSent)', 488), ('OFF(DWCMatchControl,profileID)', 512), ('OFF(DWCMatchControl,reqProfileID)', 516), ('OFF(DWCMatchControl,priorProfileID)', 520), ('OFF(DWCMatchControl,cbEventPid)', 524), ('OFF(DWCMatchControl,svDataBak)', 840), ('sizeof(((DWCMatchControl*)0)->svDataBak)', 132), ('OFF(DWCMatchControl,cmdCnt)', 972)]


def layouts(row,directory,wrong=False):
    directory.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
    checks=LAYOUT
    text='#include "context.h"\n#define OFF(T,m) ((unsigned long)&(((T*)0)->m))\n'
    text+='\n'.join('typedef char check_%d[(%s)==%d?1:-1];'%(index,expression,expected+(1 if wrong and index==0 else 0)) for index,(expression,expected) in enumerate(checks))+'\n'
    source=directory/'layout.c';source.write_text(text);obj=directory/'layout.o'
    command=[str(ROOT/row['compilerPath']),*row['compilerFlags'],'-c',str(source),'-o',str(obj)]
    process=subprocess.run(command,cwd=ROOT,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=60)
    if (process.returncode==0)==wrong:raise ValueError(('Pinned C layout result differs',wrong,process.stdout,process.stderr))
    return dict(checks=len(checks),allPassed=not wrong,rejected=wrong,sourceSha256=sha256(source),compilerSha256=row['compilerSha256'],flags=row['compilerFlags'],stdout=process.stdout,stderr=process.stderr)


def changes(address):
    entries={
      0x20a1edc:('friend-bypass-state','source','state == DWC_MATCH_STATE_CL_WAIT_RESV','state == DWC_MATCH_STATE_CL_SEARCH_OWN','Bypass friend validation in the wrong state'),
      0x20a2290:('server-timeout-exclusion','source','qr2MatchType == DWC_MATCH_TYPE_SC_SV','qr2MatchType == DWC_MATCH_TYPE_SC_CL','Restart a protected server match'),
      0x20a22b4:('resume-reservation','source','qr2Reservation = 0;','qr2Reservation = 1;','Leave reservation id after resume'),
      0x20a233c:('close-event-profile','source','cbEventPid = profileID;','cbEventPid = profileID+1;','Alter close event profile word'),
      0x20a2724:('cancel-payload-kind','source','command == DWC_MATCH_COMMAND_CANCEL_SYN','command == DWC_MATCH_COMMAND_CANCEL_SYN_ACK','Attach cancellation word to wrong command'),
      0x20a1908:('client-reservation','source','qr2Reservation = 0;','qr2Reservation = 1;','Leave reservation id when changing to client'),
      0x20a16e4:('cancel-request','source','reqProfileID = 0;','reqProfileID = 1;','Retain a request after cancellation')}
    return [entries[address]]


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
