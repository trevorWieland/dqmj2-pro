import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261105_gamespy_qr2_followup_first_build import build
from wave20261105_gamespy_qr2_followup_first_fixtures import run
from wave20261105_gamespy_qr2_followup_first_models import cases

QR_LAYOUT=[('sizeof(unsigned char)',1),('sizeof(unsigned short)',2),('sizeof(void*)',4),('sizeof(struct sockaddr_in)',8),('sizeof(struct qr2_implementation_s)',3476),('sizeof(struct qr2_ipverify_info_s)',16),('sizeof(((qr2_t)0)->ipverify)',3200),('sizeof(struct hostent)',16),('sizeof(struct in_addr)',4),('sizeof(struct qr2_buffer_s)',1404),('MAX_DATA_SIZE',1400),('OFF(struct qr2_buffer_s,len)',1400)]
QR_FIELDS={'struct sockaddr_in':{'sin_family':1,'sin_port':2,'sin_addr':4},'struct hostent':{'h_addr_list':12},'struct qr2_implementation_s':{'instance_key':132,'server_key_callback':136,'adderror_callback':156,'nn_callback':160,'cm_callback':164,'pa_callback':168,'lastheartbeat':172,'lastka':176,'userstatechangerequested':180,'listed_state':184,'ispublic':188,'qport':192,'read_socket':196,'nat_negotiate':200,'hbaddr':204,'cdkeyprocess':212,'client_message_keys':216,'cur_message_key':256,'publicip':260,'publicport':264,'udata':268,'backendoptions':272,'ipverify':276}}
N_LAYOUT=[('sizeof(unsigned char)',1),('sizeof(unsigned short)',2),('sizeof(void*)',4),('sizeof(struct sockaddr_in)',8),('INITPACKET_SIZE',21),('CONNECTPACKET_SIZE',20)]
N_FIELDS={'NatNegPacket':{'packettype':7,'cookie':8,'Packet':12},'struct sockaddr_in':{'sin_port':2,'sin_addr':4}}


def layouts(row,directory,wrong=False):
    directory.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
    layout,fields=(N_LAYOUT,N_FIELDS)if int(row['address'],0)==0x20b70c8 else(QR_LAYOUT,QR_FIELDS)
    checks=layout+[(f'OFF({name},{field})',value) for name,members in fields.items() for field,value in members.items()]
    text='#include "context.h"\n#undef activeNatify\n#undef mappingSock\n#undef ertSock\n#undef matchup1ip\n#undef matchup2ip\n#undef matchup3ip\n#define OFF(T,m) ((size_t)&(((T*)0)->m))\n'
    text+='\n'.join('typedef char check_%d[(%s)==%d?1:-1];'%(index,expression,expected+(1 if wrong and index==0 else 0)) for index,(expression,expected) in enumerate(checks))+'\n'
    source=directory/'layout.c';source.write_text(text);obj=directory/'layout.o'
    command=[str(ROOT/row['compilerPath']),*row['compilerFlags'],'-c',str(source),'-o',str(obj)]
    process=subprocess.run(command,cwd=ROOT,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=60)
    if (process.returncode==0)==wrong:raise ValueError(('Pinned C layout result differs',wrong,process.stdout,process.stderr))
    return dict(checks=len(checks),allPassed=not wrong,rejected=wrong,sourceSha256=sha256(source),compilerSha256=row['compilerSha256'],flags=row['compilerFlags'],stdout=process.stdout,stderr=process.stderr)


def changes(address):
    if address==0x20b8010:return [('match-result','source','return gsi_true;','return gsi_false;','Lose successful challenge-match result'),('consumed-address','source','qrec->ipverify[i].addr.sin_addr.s_addr = 0;','qrec->ipverify[i].addr.sin_addr.s_addr = 1;','Leave wrong consumed endpoint word')]
    if address==0x20b8334:return [('packet-kind','source','PACKET_KEEPALIVE','PACKET_HEARTBEAT','Forward wrong packet discriminator'),('clock-word','source','qrec->lastka = native_fn_020a8ef8();','qrec->lastka = native_fn_020a8ef8()+1;','Publish wrong keepalive timestamp')]
    if address!=0x20b8380:raise ValueError('Unselected first follow-up source mutation')
    return [('fallback-edge','source','AVAILABLE_BUFFER_LEN(&temp) < 1','AVAILABLE_BUFFER_LEN(&temp) < 0','Lose exact-full-buffer server-only fallback'),('trailer-edge','source','AVAILABLE_BUFFER_LEN(&buf) >= 1','AVAILABLE_BUFFER_LEN(&buf) > 1','Drop trailer at one-byte remaining capacity'),('requested-clear','source','statechanged != 0','statechanged == 0','Clear user request in wrong statechange class')]


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
