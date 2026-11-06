import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261106_dwc_match_tail_next_fifth_build import build
from wave20261106_dwc_match_tail_next_fifth_fixtures import run
from wave20261106_dwc_match_tail_next_fifth_models import cases

LAYOUT=[('sizeof(u32)', 4), ('sizeof(DWCError)', 4), ('sizeof(DWCState)', 4), ('OFF(DWCMatchControl,pGt2Socket)', 4), ('OFF(DWCMatchControl,gt2NumConnection)', 13), ('OFF(DWCMatchControl,qr2MatchType)', 21), ('OFF(DWCMatchControl,qr2NumEntry)', 22), ('OFF(DWCMatchControl,sbPidList)', 244), ('OFF(DWCMatchControl,nnInfo)+OFF(DWCNNInfo,cookie)', 412), ('OFF(DWCMatchControl,state)', 416), ('OFF(DWCMatchControl,closeState)', 424), ('OFF(DWCMatchControl,cancelState)', 425), ('OFF(DWCMatchControl,clWaitTimeoutCount)', 429), ('OFF(DWCMatchControl,baseLatency)', 432), ('OFF(DWCMatchControl,synAckBit)', 468), ('OFF(DWCMatchControl,lastSynSent)', 480), ('OFF(DWCMatchControl,closedTime)', 496), ('OFF(DWCMatchControl,profileID)', 512), ('OFF(DWCMatchControl,priorProfileID)', 520), ('OFF(DWCMatchControl,cbEventPid)', 524), ('OFF(DWCMatchControl,aidList)', 720), ('DWC_MATCH_COMMAND_ADD_MESSAGE_NUM', 128), ('DWC_MATCH_SYN_DATA_BODY_SIZE', 4), ('DWC_SEND_TYPE_MATCH_SYN', 2), ('DWC_SEND_TYPE_MATCH_SYN_ACK', 3), ('DWC_SEND_TYPE_MATCH_ACK', 4)]


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
      0x209f0c4:('received-word-count','source','data, i);','data, i+1);','Forward an extra unparsed word'),
      0x209f460:('closing-exclusion','source','closeState != DWC_MATCH_CLOSE_STATE_TIMEOUT','closeState == DWC_MATCH_CLOSE_STATE_TIMEOUT','Cancel preconnection in the excluded close state'),
      0x209f47c:('profile-search','source','sbPidList[i] == profileID','sbPidList[i] != profileID','Delete the wrong profile index'),
      0x209f724:('advertised-entry-count','source','qr2NumEntry + 1','qr2NumEntry + 2','Advertise an extra entry'),
      0x209f1e8:('syn-event-clear','source','data[0] == 1','data[0] == 2','Clear event for the wrong wire flag'),
      0x20a249c:('syn-last-peer-flag','source','senddata[0] = 1;','senddata[0] = 2;','Transmit an altered defined handshake flag'),
      0x209f334:('closing-aid-clear','source','aidList[0] = 0;','aidList[0] = 1;','Leave wrong first aid after close')}
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
