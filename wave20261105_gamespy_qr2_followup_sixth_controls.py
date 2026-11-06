import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261105_gamespy_qr2_followup_sixth_build import build
from wave20261105_gamespy_qr2_followup_sixth_fixtures import run
from wave20261105_gamespy_qr2_followup_sixth_models import cases

LAYOUT=[('sizeof(u32)',4),('sizeof(void*)',4),('sizeof(int)',4),('sizeof(long)',4),('sizeof(char)',1),('((char)-1)<0',1),('sizeof(Status)',72),('sizeof(Result)',40),('sizeof(Completion)',4),('sizeof(Peer8)',8),('sizeof(HOSTENT)',16),('OFF(Status,request)',20),('OFF(Status,callback)',60),('OFF(Status,extra40)',64),('OFF(Status,extra44)',68),('OFF(Peer8,length)',0),('OFF(Peer8,family)',1),('OFF(Peer8,port)',2),('OFF(Peer8,address)',4),('OFF(HOSTENT,h_addrtype)',8),('OFF(HOSTENT,h_length)',10),('OFF(HOSTENT,h_addr_list)',12),('OFF(State,mutex1bc)',444),('sizeof(State)',4816),('sizeof(Control)',2292),('ROUNDUP32(1u)',32),('ROUNDUP32(31u)',32),('ROUNDUP32(0xffffffe1u)',0)]


def layouts(row,directory,wrong=False):
    directory.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
    checks=LAYOUT
    text='#include "context.h"\n#define OFF(T,m) ((size_t)&(((T*)0)->m))\n'
    text+='\n'.join('typedef char check_%d[(%s)==%d?1:-1];'%(index,expression,expected+(1 if wrong and index==0 else 0)) for index,(expression,expected) in enumerate(checks))+'\n'
    source=directory/'layout.c';source.write_text(text);obj=directory/'layout.o'
    command=[str(ROOT/row['compilerPath']),*row['compilerFlags'],'-c',str(source),'-o',str(obj)]
    process=subprocess.run(command,cwd=ROOT,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=60)
    if (process.returncode==0)==wrong:raise ValueError(('Pinned C layout result differs',wrong,process.stdout,process.stderr))
    return dict(checks=len(checks),allPassed=not wrong,rejected=wrong,sourceSha256=sha256(source),compilerSha256=row['compilerSha256'],flags=row['compilerFlags'],stdout=process.stdout,stderr=process.stderr)


def changes(address):
    value={
        0x20b9848:('phase-result','source','return 1;','return 2;','Alter exact raw phase-predicate result'),
        0x20b9868:('length-edge','source','length<=64','length<64','Reject original upper-inclusive length boundary'),
        0x20b9898:('peer-width','source','peer->length=8','peer->length=16','Publish wrong Nintendo peer byte width'),
        0x20b9914:('header-clear','source','native_fn_02008d78(base,0,sizeof(Status))','native_fn_02008d78(base,0,sizeof(Status)-4)','Leave final cleared header word unchanged'),
        0x20b9998:('consumed-marker','source','request.words[7]=0','request.words[7]=1','Leave consumed shared marker set'),
        0x20b99ec:('published-phase','source','->prefix[0]=2','->prefix[0]=3','Publish wrong raw start phase'),
        0x20b9c2c:('rounding-edge','header','#define ROUNDUP32(n) ((((n)+31)>>5)<<5)','#define ROUNDUP32(n) ((((n)+30)>>5)<<5)','Round one-byte provider views below original boundary')}
    if address==0x20b9998:return [value[address],('callback-order','source','native_data_021d3030->request.words[9],native_data_021d3030->extra44','native_data_021d3030->extra44,native_data_021d3030->request.words[9]','Swap measured callback words1/2')]
    return [value[address]]



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
