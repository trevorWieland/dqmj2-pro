import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261105_gamespy_qr2_next_seventh_build import build
from wave20261105_gamespy_qr2_next_seventh_fixtures import run
from wave20261105_gamespy_qr2_next_seventh_models import cases


def layouts(row,directory,wrong=False):
    directory.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
    checks=[('sizeof(char)',1),('(char)0x80<0',1),('sizeof(unsigned short)',2),('sizeof(unsigned int)',4),('sizeof(void*)',4),('sizeof(IN_ADDR)',4),('sizeof(HOSTENT)',16),('OFF(HOSTENT,h_addr_list)',12),('sizeof(native_data_020d8e04)',256),('GTI2_STACK_HOSTLEN_MAX',256)]
    text='#include "context.h"\n#define OFF(T,m) ((size_t)&(((T*)0)->m))\n'
    text+='\n'.join('typedef char check_%d[(%s)==%d?1:-1];'%(index,expression,1 if wrong and index==2 else expected) for index,(expression,expected) in enumerate(checks))+'\n'
    source=directory/'layout.c';source.write_text(text);obj=directory/'layout.o'
    process=subprocess.run([str(ROOT/row['compilerPath']),*row['compilerFlags'],'-c',str(source),'-o',str(obj)],cwd=ROOT,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=60)
    if (process.returncode==0)==wrong:raise ValueError(('Pinned address/character view layout differs',wrong,process.stdout,process.stderr))
    return dict(checks=len(checks),allPassed=not wrong,rejected=wrong,sourceSha256=sha256(source),compilerSha256=row['compilerSha256'],flags=row['compilerFlags'],stdout=process.stdout,stderr=process.stderr)


def wrong_source(row,directory):
    source=ROOT/row['source'];text=source.read_text();image=(ROOT/'extract/arm9/arm9.bin').read_bytes();out=[]
    changes=[('classification-mask','header','native_data_020d8e04[c]&8','native_data_020d8e04[c]&4','Use the control-character mask instead of measured digit bit8'),('port-maximum','source','temp > 0xFFFF','temp > 0xFFFE','Reject the valid maximum65535 port'),('dns-word','source','srcIP = *(unsigned int *)hostent->h_addr_list[0];','srcIP = 0;','Discard the resolved full IP word'),('port-narrowing','source','*port = srcPort;','*port = (unsigned char)srcPort;','Lose the high eight port bits')]
    for name,owner,before,after,meaning in changes:
        folder=directory/name;folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        wrong=folder/source.name;wrong.write_text(text);target=folder/'context.h' if owner=='header' else wrong;old=target.read_text()
        if old.count(before)!=1:raise ValueError(('Address primitive mutation is no longer unique',name))
        target.write_text(old.replace(before,after));bad,body=build(wrong,folder/'build',negative=True);violations=[]
        for seed,vector in enumerate(cases(int(row['address'],0))):
            record=run(image,row,body,vector,seed)
            if not record['modelPassed']:
                violations.append(dict(vector=vector,seed=seed,actualReturningModelViolation=record))
                if len(violations)==4:break
        if not violations:raise ValueError(('Wrong address parsing C passed independent caller oracle',name))
        out.append(dict(address=row['address'],case=name,meaning=meaning,sourceSha256=sha256(wrong),objectSha256=bad['objectSha256'],compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],sourceDependencies=bad['sourceDependencies'],rejectedByCompleteNativeComparison=True,actualReturningModelRejections=len(violations),witnesses=violations,sourceOrExecutionCredit=0))
    return out
