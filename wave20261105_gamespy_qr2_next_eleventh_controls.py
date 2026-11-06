import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261105_gamespy_qr2_next_eleventh_build import build
from wave20261105_gamespy_qr2_next_eleventh_fixtures import run
from wave20261105_gamespy_qr2_next_eleventh_models import cases

LAYOUT=[('sizeof(unsigned short)',2),('sizeof(unsigned long)',4),('sizeof(void*)',4),('sizeof(struct sockaddr_in)',8),('OFF(struct sockaddr_in,sin_family)',1),('OFF(struct sockaddr_in,sin_port)',2),('OFF(struct sockaddr_in,sin_addr)',4),('sizeof(struct _NATNegotiator)',84),('sizeof(NegotiateState)',4),('sizeof(NegotiateResult)',4),('sizeof(struct NativeBss)',32),('OFF(struct NativeBss,activeNatify)',28),('sizeof(struct NativeData)',12),('OFF(struct NativeData,ertSock)',4),('OFF(struct NativeData,mappingSock)',8)]
FIELDS={'struct _NATNegotiator':{'negotiateSock':0,'gameSock':4,'cookie':8,'state':16,'retryCount':36,'maxRetryCount':40,'retryTime':44,'guessedIP':48,'guessedPort':52,'gotRemoteData':54,'sendGotRemoteData':55,'progressCallback':56,'completedCallback':60,'userdata':64,'result':68,'connectedSocket':72,'remoteaddr':76},'NatNegPacket':{'Packet.Connect.remoteIP':12,'Packet.Connect.remotePort':16,'Packet.Connect.gotyourdata':18,'Packet.Connect.finished':19}}


def layouts(row,directory,wrong=False):
    directory.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
    checks=LAYOUT+[(f'OFF({name},{field})',value) for name,fields in FIELDS.items() for field,value in fields.items()]
    text='#include "context.h"\n#undef activeNatify\n#undef mappingSock\n#undef ertSock\n#define OFF(T,m) ((size_t)&(((T*)0)->m))\n'
    text+='\n'.join('typedef char check_%d[(%s)==%d?1:-1];'%(index,expression,expected+(1 if wrong and index==0 else 0)) for index,(expression,expected) in enumerate(checks))+'\n'
    source=directory/'layout.c';source.write_text(text);obj=directory/'layout.o'
    command=[str(ROOT/row['compilerPath']),*row['compilerFlags'],'-c',str(source),'-o',str(obj)]
    process=subprocess.run(command,cwd=ROOT,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=60)
    if (process.returncode==0)==wrong:raise ValueError(('Pinned C layout result differs',wrong,process.stdout,process.stderr))
    return dict(checks=len(checks),allPassed=not wrong,rejected=wrong,sourceSha256=sha256(source),compilerSha256=row['compilerSha256'],flags=row['compilerFlags'],stdout=process.stdout,stderr=process.stderr)


MUTATIONS={0x20b6670:('htons(toport)','toport','Omit measured scalar endian conversion'),0x20b6b74:('sizeof(hostnameBuffer)','sizeof(hostnameBuffer)-1','Forward wrong formatter capacity'),0x20b6c90:('!= INVALID_SOCKET','== INVALID_SOCKET','Close exactly the invalid socket instead of valid values'),0x20b6cb4:('> neg->retryTime','>= neg->retryTime','Make all four measured timer expiration boundaries inclusive'),0x20b6f3c:('== FINISHED_NOERROR','!= FINISHED_NOERROR','Acknowledge failure packets instead of successful connect packets'),0x20b6fa8:('neg->gotRemoteData = 1;','neg->gotRemoteData = 0;','Suppress the measured received-data state byte')}


def wrong_source(row,directory):
    directory.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
    source=ROOT/row['source'];text=source.read_text();before,after,meaning=MUTATIONS[int(row['address'],0)]
    if text.count(before)!=(4 if int(row['address'],0)==0x20b6cb4 else 1):raise ValueError('NAT protocol whole-source mutation no longer unique')
    wrong=directory/source.name;wrong.write_text(text.replace(before,after));bad,body=build(wrong,directory/'build',negative=True)
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();violations=[]
    for seed,vector in enumerate(cases(int(row['address'],0))):
        record=run(image,row,body,vector,seed)
        if not record['modelPassed']:
            violations.append(dict(vector=vector,seed=seed,actualReturningModelViolation=record))
            if len(violations)==4:break
    if not violations:raise ValueError(('Wrong protocol C passed independent caller model',row['address']))
    return dict(address=row['address'],meaning=meaning,sourceSha256=sha256(wrong),objectSha256=bad['objectSha256'],compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],sourceDependencies=bad['sourceDependencies'],rejectedByCompleteNativeComparison=True,actualReturningModelRejections=len(violations),witnesses=violations,sourceOrExecutionCredit=0)
