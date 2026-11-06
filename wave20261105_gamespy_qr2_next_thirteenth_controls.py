import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261105_gamespy_qr2_next_thirteenth_build import build
from wave20261105_gamespy_qr2_next_thirteenth_fixtures import run
from wave20261105_gamespy_qr2_next_thirteenth_models import cases

LAYOUT=[('sizeof(NatType)',4),('sizeof(NatMappingScheme)',4),('sizeof(unsigned char)',1),('sizeof(void*)',4),('sizeof(ReportPacket)',61),('REPORTPACKET_SIZE',73),('sizeof(struct _NATNegotiator)',84),('sizeof(struct NativeIPs)',44)]
FIELDS={'ReportPacket':{'porttype':0,'clientindex':1,'negResult':2,'natType':3,'natMappingScheme':7,'gamename':11},'NatNegPacket':{'Packet.Report':12},'struct _NATNegotiator':{'cookie':8,'clientindex':12,'result':68},'struct NativeIPs':{'matchup1ip':40}}


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
    if address!=0x20b6708:raise ValueError('No selected report mutation family')
    return [('success-byte','source','neg->result==nr_success','neg->result!=nr_success','Invert measured report success byte'),('cookie-byteorder','source','p.cookie = (int)htonl(neg->cookie);','p.cookie = neg->cookie;','Lose original cookie byte order'),('enum-word','source','&native_data_020e172c,4','&native_data_021d2bcc,4','Copy mapping-scheme word into NAT-type wire field'),('name-copy-count','source','sizeof(p.Packet.Report.gamename)','sizeof(p.Packet.Report.gamename)-1','Forward49 rather than original50 name bytes')]


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
