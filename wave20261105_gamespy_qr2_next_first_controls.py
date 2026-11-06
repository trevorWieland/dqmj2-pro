import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261105_gamespy_qr2_next_first_build import build
from wave20261105_gamespy_qr2_next_first_fixtures import run
from wave20261105_gamespy_qr2_next_first_models import cases

LAYOUT=[('sizeof(GT2Byte)',1),('sizeof(GT2Bool)',4),('sizeof(void*)',4),('sizeof(gsi_time)',4),('sizeof(GTI2ConnectionState)',4),('sizeof(GTI2ProtocolType)',4),('sizeof(GTI2Buffer)',12),('sizeof(GTI2Connection)',160),('sizeof(GTI2Socket)',76),('sizeof(GTI2OutgoingBufferMessage)',16)]
FIELDS={'GTI2Connection':{'socket':8,'state':12,'initiated':16,'freeAtAcceptReject':20,'startTime':28,'timeout':32,'incomingBuffer':68,'outgoingBuffer':80,'outgoingBufferMessages':96,'serialNumber':100,'expectedSerialNumber':102,'lastSend':136,'challengeTime':140,'pendingAck':144,'pendingAckTime':148},'GTI2Socket':{'connections':12,'closedConnections':16,'receiveDumpCallback':44,'protocolType':64,'protocolOffset':68},'GTI2OutgoingBufferMessage':{'start':0,'len':4,'serialNumber':8,'lastSend':12},'GTI2Buffer':{'buffer':0,'size':4,'len':8}}


def layouts(row,directory,wrong=False):
    directory.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
    checks=LAYOUT+[(f'OFF({name},{field})',value) for name,fields in FIELDS.items() for field,value in fields.items()]
    text='#include "context.h"\n#define OFF(T,m) ((size_t)&(((T*)0)->m))\n'
    text+='\n'.join('typedef char check_%d[(%s)==%d?1:-1];'%(index,expression,expected+(1 if wrong and index==0 else 0)) for index,(expression,expected) in enumerate(checks))+'\n'
    source=directory/'layout.c';source.write_text(text);obj=directory/'layout.o'
    command=[str(ROOT/row['compilerPath']),*row['compilerFlags'],'-c',str(source),'-o',str(obj)]
    process=subprocess.run(command,cwd=ROOT,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=60)
    if (process.returncode==0)==wrong:raise ValueError(('Pinned C layout result differs',wrong,process.stdout,process.stderr))
    return dict(checks=len(checks),allPassed=not wrong,rejected=wrong,sourceSha256=sha256(source),compilerSha256=row['compilerSha256'],flags=row['compilerFlags'],stdout=process.stdout,stderr=process.stderr)


MUTATIONS={0x20b4134:('> connection->timeout','>= connection->timeout','Timeout boundary becomes inclusive'),0x20b4194:('> GTI2_RESEND_TIME','>= GTI2_RESEND_TIME','Retry boundary becomes inclusive'),0x20b41d8:('> GTI2_PENDING_ACK_TIME','>= GTI2_PENDING_ACK_TIME','Pending ACK boundary becomes inclusive'),0x20b4204:('> GTI2_KEEP_ALIVE_TIME','>= GTI2_KEEP_ALIVE_TIME','Keepalive boundary becomes inclusive'),0x20b4270:('>= GTI2Closed','> GTI2Closed','Already-closed hard close invokes helpers'),0x20b42a4:('== GTI2Closed','== GTI2Closing','Closed-state idempotence tests the wrong enum'),0x20b4330:('callback, GTI2UdpProtocol','callback, GTI2VdpProtocol','Sixth constructor word changes protocol'),0x20b45dc:('== GTI2AwaitingAcceptReject','== GTI2AwaitingClientResponse','Wrong connection phase publishes freeAtAcceptReject'),0x20b514c:('< connection->timeout','<= connection->timeout','Connection reset timeout equality is suppressed'),0x20b51dc:('GT2TimedOut, GT2RemoteClose','GT2Rejected, GT2RemoteClose','Host-unreachable reports the wrong result'),0x20b5390:('connection->serialNumber++','connection->serialNumber--','Reliable-message serial publication decrements'),0x20b5900:('type == GTI2MsgServerChallenge','type == GTI2MsgClientChallenge','Resending wrong challenge type publishes challengeTime')}


def wrong_source(row,directory):
    directory.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
    source=ROOT/row['source'];before,after,meaning=MUTATIONS[int(row['address'],0)];text=source.read_text()
    if text.count(before)!=1:raise ValueError('Scoped whole-C mutation no longer identifies exactly one expression')
    wrong=directory/source.name;wrong.write_text(text.replace(before,after));bad,body=build(wrong,directory/'build',negative=True)
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();violations=[]
    for seed,vector in enumerate(cases(int(row['address'],0))):
        record=run(image,row,body,vector,seed)
        if not record['modelPassed']:
            violations.append(dict(vector=vector,seed=seed,actualReturningModelViolation=record))
            if len(violations)==4:break
    if not violations:raise ValueError(('Wrong complete C passed independent caller model',row['address']))
    return dict(address=row['address'],meaning=meaning,sourceSha256=sha256(wrong),objectSha256=bad['objectSha256'],compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],sourceDependencies=bad['sourceDependencies'],rejectedByCompleteNativeComparison=True,actualReturningModelRejections=len(violations),witnesses=violations,sourceOrExecutionCredit=0)
