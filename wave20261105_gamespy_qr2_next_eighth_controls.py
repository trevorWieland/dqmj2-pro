import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261105_gamespy_qr2_next_eighth_build import build
from wave20261105_gamespy_qr2_next_eighth_fixtures import run
from wave20261105_gamespy_qr2_next_eighth_models import cases

LAYOUT=[('sizeof(GT2Byte)',1),('sizeof(unsigned short)',2),('sizeof(GT2Bool)',4),('sizeof(GTI2Connection)',160),('sizeof(GTI2Socket)',76),('sizeof(GTI2ProtocolType)',4),('GTI2VdpProtocol',2),('GTI2_MAGIC_STRING_LEN',2),('MAX_PROTOCOL_OFFSET',2),('GTI2MsgAck',100),('GTI2MsgNack',101),('GTI2MsgClosed',104)]
FIELDS={'GTI2Connection':{'socket':8,'expectedSerialNumber':102,'lastSend':136,'pendingAck':144},'GTI2Socket':{'protocolType':64}}


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


MUTATIONS={0x20b57a0:('connection->pendingAck = GT2False;','connection->pendingAck = GT2True;','Successful ACK retains pending flag'),0x20b5810:('SNMin != SNMax','SNMin == SNMax','Wrong equal-range rule appends the extra serial word'),0x20b58ac:('GTI2MsgClosed','GTI2MsgPong','Wrong control packet discriminator')}


def wrong_source(row,directory):
    source=ROOT/row['source'];text=source.read_text();image=(ROOT/'extract/arm9/arm9.bin').read_bytes();out=[]
    ordinary=MUTATIONS[int(row['address'],0)]
    for name,owner,before,after,meaning in [('caller','source',*ordinary),('copy-width','header','else if(n==2){d[0]=s[0];d[1]=s[1];}','else if(n==2){d[0]=s[0];d[1]=s[0];}','Fixed2 primitive duplicates low byte instead of preserving unaligned byte1')]:
        folder=directory/name;folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        wrong=folder/source.name;wrong.write_text(text);target=folder/'context.h' if owner=='header' else wrong;old=target.read_text()
        if old.count(before)!=1:raise ValueError(('Unique packet primitive mutation changed',name))
        target.write_text(old.replace(before,after));bad,body=build(wrong,folder/'build',negative=True);violations=[]
        for seed,vector in enumerate(cases(int(row['address'],0))):
            record=run(image,row,body,vector,seed)
            if not record['modelPassed']:
                violations.append(dict(vector=vector,seed=seed,actualReturningModelViolation=record))
                if len(violations)==4:break
        if not violations:raise ValueError(('Wrong complete C passed caller oracle',row['address'],name))
        out.append(dict(address=row['address'],case=name,meaning=meaning,sourceSha256=sha256(wrong),objectSha256=bad['objectSha256'],compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],sourceDependencies=bad['sourceDependencies'],rejectedByCompleteNativeComparison=True,actualReturningModelRejections=len(violations),witnesses=violations,sourceOrExecutionCredit=0))
    return out
