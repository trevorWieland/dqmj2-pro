import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261105_gamespy_qr2_next_eighteenth_build import build
from wave20261105_gamespy_qr2_next_eighteenth_fixtures import run
from wave20261105_gamespy_qr2_next_eighteenth_models import cases

QR_LAYOUT=[('sizeof(unsigned char)',1),('sizeof(unsigned short)',2),('sizeof(void*)',4),('sizeof(struct sockaddr_in)',8),('sizeof(struct qr2_implementation_s)',3476),('sizeof(struct qr2_ipverify_info_s)',16),('sizeof(((qr2_t)0)->ipverify)',3200),('sizeof(struct hostent)',16),('sizeof(struct in_addr)',4)]
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
    specs={
        0x20b70c8:[('length-gate','source','len < CONNECTPACKET_SIZE','len < CONNECTPACKET_SIZE-1','Accept undersized CONNECT packet'),('cookie-endian','source','(int)ntohl((unsigned int)p.cookie)','(int)p.cookie','Forward wrong cookie byte order')],
        0x20b718c:[('listed-phase','source','cr->listed_state = 1;','cr->listed_state = 0;','Lose initialized first-list phase'),('instance-width','source','i < REQUEST_KEY_LEN','i < REQUEST_KEY_LEN-1','Generate only three instance bytes')],
        0x20b7334:[('public-gate','source','if (qrec->ispublic)','if (!qrec->ispublic)','Invert measured heartbeat gate')],
        0x20b7360:[('receive-bound','source','(INBUF_LEN - 1)','(INBUF_LEN - 2)','Change actual receive capacity'),('socket-error','header','#define gsiSocketIsNotError(s) ((s)!=-1)','#define gsiSocketIsNotError(s) ((s)>=0)','Reject raw-2 instead of exact-1 gate')],
        0x20b73c0:[('first-count','source','MAX_FIRST_COUNT','(MAX_FIRST_COUNT-1)','Fire error one retry too soon'),('keepalive-edge','source','KA_TIME','(KA_TIME-1)','Change strict keepalive deadline edge')],
        0x20b748c:[('state-edge','source','MIN_STATECHANGED_HB_TIME','(MIN_STATECHANGED_HB_TIME+1)','Queue exact deadline instead of publishing')],
        0x20b74d4:[('close-gate','source','INVALID_SOCKET != qrec->hbsock','INVALID_SOCKET == qrec->hbsock','Invert original close ownership gate'),('heartbeat-kind','source','(qrec, 2)','(qrec, 1)','Send statechange instead of shutdown kind')],
        0x20b75cc:[('list-cap','source','native_data_021d2ec8 < MAX_LOCAL_IP','native_data_021d2ec8 < MAX_LOCAL_IP-1','Drop fifth available address'),('list-start','source','native_data_021d2ec8 = 0','native_data_021d2ec8 = 1','Skip first address')],
        0x20b760c:[('peer-family','source','saddr->sin_family = AF_INET;','saddr->sin_family = AF_INET+1;','Publish wrong peer family byte'),('port-endian','source','htons((unsigned short)port)','((unsigned short)port)','Lose measured port byte order')],
        0x20b78ac:[('port-truncate','source','(unsigned short)portTemp','(unsigned short)(portTemp+1)','Change public-port truncation'),('zero-gate','source','(ip == 0) || (port == 0)','(ip == 0) && (port == 0)','Publish invalid one-zero endpoint')]
    }
    return specs[address]


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
