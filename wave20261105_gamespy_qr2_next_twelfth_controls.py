import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261105_gamespy_qr2_next_twelfth_build import build
from wave20261105_gamespy_qr2_next_twelfth_fixtures import run
from wave20261105_gamespy_qr2_next_twelfth_models import cases

LAYOUT=[('sizeof(unsigned short)',2),('sizeof(unsigned int)',4),('sizeof(void*)',4),('sizeof(struct sockaddr_in)',8),('sizeof(struct _NATNegotiator)',84),('INITPACKET_SIZE',21),('PARTNER_WAIT_TIME',10000),('INIT_RETRY_TIME',500),('INIT_RETRY_COUNT',10),('NN_PROTVER',3),('sizeof(struct NativeIPs)',44)]
FIELDS={'struct _NATNegotiator':{'gameSock':4,'cookie':8,'clientindex':12,'state':16,'initAckRecv':20,'maxRetryCount':40,'retryTime':44,'progressCallback':56,'completedCallback':60,'userdata':64,'result':68,'connectedSocket':72,'remoteaddr':76},'InitPacket':{'porttype':0,'clientindex':1,'usegameport':2},'struct NativeIPs':{'matchup3ip':32,'matchup2ip':36,'matchup1ip':40}}


def layouts(row,directory,wrong=False):
    directory.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
    checks=LAYOUT+[(f'OFF({name},{field})',value) for name,fields in FIELDS.items() for field,value in fields.items()]
    text='#include "context.h"\n#undef activeNatify\n#undef mappingSock\n#undef ertSock\n#undef matchup1ip\n#undef matchup2ip\n#undef matchup3ip\n#define OFF(T,m) ((size_t)&(((T*)0)->m))\n'
    text+='\n'.join('typedef char check_%d[(%s)==%d?1:-1];'%(index,expression,expected+(1 if wrong and index==0 else 0)) for index,(expression,expected) in enumerate(checks))+'\n'
    source=directory/'layout.c';source.write_text(text);obj=directory/'layout.o'
    command=[str(ROOT/row['compilerPath']),*row['compilerFlags'],'-c',str(source),'-o',str(obj)]
    process=subprocess.run(command,cwd=ROOT,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=60)
    if (process.returncode==0)==wrong:raise ValueError(('Pinned C layout result differs',wrong,process.stdout,process.stderr))
    return dict(checks=len(checks),allPassed=not wrong,rejected=wrong,sourceSha256=sha256(source),compilerSha256=row['compilerSha256'],flags=row['compilerFlags'],stdout=process.stdout,stderr=process.stderr)


def changes(address):
    if address==0x20b6840:return [('magic-six','header','d[4]=s[4];d[5]=s[5];','d[4]=s[4];d[5]=s[4];','Duplicate the fifth magic byte instead of preserve sixth'),('single-ip-read','source','localip = ntohl(native_fn_020b66a4());','localip = native_fn_020b66a4(); localip = ntohl(localip);','Collapse four measured original IP helper calls to one'),('single-port-read','source','localport = ntohs(native_fn_020b66e0((p->Packet.Init.usegameport) ?  neg->gameSock : neg->negotiateSock));','localport = native_fn_020b66e0((p->Packet.Init.usegameport) ? neg->gameSock : neg->negotiateSock); localport = ntohs(localport);','Collapse two measured original port helper calls to one'),('ip-word','header','#define matchup1ip native_data_021d2bc4.matchup1ip','#define matchup1ip (*((unsigned int*)((char*)&native_data_021d2bc4+36)))','Forward endpoint2 word for first endpoint')]
    return [('partner-wait','header','#define PARTNER_WAIT_TIME 10000','#define PARTNER_WAIT_TIME 60000','Use newer public SDK60000 value rather than measured10000'),('allowed-port3','source','> NN_PT_NN3','>= NN_PT_NN3','Reject allowed port-type3 ACK')]


def wrong_source(row,directory):
    source=ROOT/row['source'];text=source.read_text();image=(ROOT/'extract/arm9/arm9.bin').read_bytes();out=[]
    for name,owner,before,after,meaning in changes(int(row['address'],0)):
        folder=directory/name;folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        wrong=folder/source.name;wrong.write_text(text);target=folder/'context.h'if owner=='header'else wrong;old=target.read_text()
        if old.count(before)!=1:raise ValueError(('Twelfth exact source mutation changed',name))
        target.write_text(old.replace(before,after));bad,body=build(wrong,folder/'build',negative=True);violations=[]
        for seed,vector in enumerate(cases(int(row['address'],0))):
            record=run(image,row,body,vector,seed)
            if not record['modelPassed']:
                violations.append(dict(vector=vector,seed=seed,actualReturningModelViolation=record))
                if len(violations)==4:break
        if not violations:raise ValueError(('Wrong SDK packet C passed independent caller oracle',name))
        out.append(dict(address=row['address'],case=name,meaning=meaning,sourceSha256=sha256(wrong),objectSha256=bad['objectSha256'],compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],sourceDependencies=bad['sourceDependencies'],rejectedByCompleteNativeComparison=True,actualReturningModelRejections=len(violations),witnesses=violations,sourceOrExecutionCredit=0))
    return out
