import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261105_gamespy_qr2_next_twentieth_build import build
from wave20261105_gamespy_qr2_next_twentieth_fixtures import run
from wave20261105_gamespy_qr2_next_twentieth_models import cases

QR_LAYOUT=[('sizeof(unsigned char)',1),('sizeof(unsigned short)',2),('sizeof(void*)',4),('sizeof(GTI2Buffer)',12),('sizeof(GTI2Socket)',76),('sizeof(GTI2Connection)',160),('sizeof(GTI2IncomingBufferMessage)',16),('sizeof(GTI2OutgoingBufferMessage)',16),('sizeof(GTI2MessageType)',4)]
QR_FIELDS={'GTI2Socket':{'protocolType':64,'protocolOffset':68},'GTI2Connection':{'socket':8,'state':12,'callbacks.ping':52,'incomingBuffer':68,'incomingBuffer.len':76,'incomingBufferMessages':92,'outgoingBufferMessages':96,'expectedSerialNumber':102,'response':104,'pendingAck':144,'receiveFilters':156},'GTI2IncomingBufferMessage':{'start':0,'len':4,'type':8,'serialNumber':12},'GTI2OutgoingBufferMessage':{'serialNumber':8,'lastSend':12}}


def layouts(row,directory,wrong=False):
    directory.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
    layout,fields=QR_LAYOUT,QR_FIELDS
    checks=layout+[(f'OFF({name},{field})',value) for name,members in fields.items() for field,value in members.items()]
    text='#include "context.h"\n#undef activeNatify\n#undef mappingSock\n#undef ertSock\n#undef matchup1ip\n#undef matchup2ip\n#undef matchup3ip\n#define OFF(T,m) ((size_t)&(((T*)0)->m))\n'
    text+='\n'.join('typedef char check_%d[(%s)==%d?1:-1];'%(index,expression,expected+(1 if wrong and index==0 else 0)) for index,(expression,expected) in enumerate(checks))+'\n'
    source=directory/'layout.c';source.write_text(text);obj=directory/'layout.o'
    command=[str(ROOT/row['compilerPath']),*row['compilerFlags'],'-c',str(source),'-o',str(obj)]
    process=subprocess.run(command,cwd=ROOT,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=60)
    if (process.returncode==0)==wrong:raise ValueError(('Pinned C layout result differs',wrong,process.stdout,process.stderr))
    return dict(checks=len(checks),allPassed=not wrong,rejected=wrong,sourceSha256=sha256(source),compilerSha256=row['compilerSha256'],flags=row['compilerFlags'],stdout=process.stdout,stderr=process.stderr)


def changes(address):
    specs={
        0x20b45b0:[('low-byte','source','s |= buffer[pos];','s |= buffer[pos]+1;','Alter decoded unsigned-short low byte')],
        0x20b475c:[('phase-gate','source','connection->state != GTI2Closing','connection->state != GTI2Closed','Treat closing state as communication error')],
        0x20b47c8:[('challenge-length','source','len < GTI2_CHALLENGE_LEN','len < GTI2_CHALLENGE_LEN-1','Accept31-byte challenge'),('next-phase','source','connection->state = GTI2AwaitingClientResponse;','connection->state = GTI2Connected;','Publish wrong post-send phase')],
        0x20b49b8:[('phase-gate','source','connection->state != GTI2AwaitingAcceptance','connection->state != GTI2AwaitingClientChallenge','Reject correct acceptance phase')],
        0x20b4a00:[('close-reason','source','connection->state == GTI2Closing','connection->state == GTI2Closed','Invert observed local-close classification')],
        0x20b4a30:[('serial-step','source','connection->expectedSerialNumber++;','connection->expectedSerialNumber+=2;','Advance sequence word by two')],
        0x20b4ad4:[('capacity-edge','source','(&connection->incomingBuffer) < len','(&connection->incomingBuffer) <= len','Reject exact available capacity'),('stored-serial','source','messageInfo.serialNumber = SN;','messageInfo.serialNumber = SN+1;','Insert wrong incoming serial word')],
        0x20b4c40:[('quiescent-result','source','return GT2True;','return GT2False;','Report failure after successful/quiescent drain')],
        0x20b4cb0:[('overflow-gate','source','if(overflow)','if(!overflow)','Invert memory-error propagation')],
        0x20b4df0:[('wire-width','source','if(len == 2)','if(len == 3)','Reject valid one-serial NACK body')],
        0x20b4e8c:[('wire-length','source','len != (4 + sizeof(gsi_time))','len != (5 + sizeof(gsi_time))','Reject measured8-byte ping body')],
        0x20b4ee8:[('already-closed','source','connection->state == GTI2Closed','connection->state == GTI2Closing','Suppress wrong closure phase')],
        0x20b4f10:[('data-start','source','GTI2_MAGIC_STRING_LEN + 1','GTI2_MAGIC_STRING_LEN + 2','Shift ACK/NACK/PONG payload one byte')]
    }
    return specs[address]


def wrong_source(row,directory):
    source=ROOT/row['source'];text=source.read_text();image=(ROOT/'extract/arm9/arm9.bin').read_bytes();out=[]
    for name,owner,before,after,meaning in changes(int(row['address'],0)):
        folder=directory/name;folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        wrong=folder/source.name;wrong.write_text(text);target=folder/'context.h'if owner=='header'else wrong;old=target.read_text()
        expected=1
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
