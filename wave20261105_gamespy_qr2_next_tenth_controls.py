import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261105_gamespy_qr2_next_tenth_build import build
from wave20261105_gamespy_qr2_next_tenth_fixtures import run
from wave20261105_gamespy_qr2_next_tenth_models import cases

LAYOUT=[('sizeof(unsigned short)',2),('sizeof(int)',4),('sizeof(void*)',4),('sizeof(struct sockaddr)',8),('sizeof(struct sockaddr_in)',8),('OFF(struct sockaddr_in,sin_family)',1),('OFF(struct sockaddr_in,sin_port)',2),('OFF(struct sockaddr_in,sin_addr)',4),('sizeof(struct _NATNegotiator)',84),('sizeof(DArray)',4)]
FIELDS={}


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


MUTATIONS={0x20b6100:('if (gsiSocketIsError(ret))','if (ret < 0)','Reject every negative status instead of only native-1'),0x20b66e0:('if (gsiSocketIsError(ret))','if (ret < 0)','Reject every negative status instead of only native-1'),0x20b65a4:('sizeof(_neg), 4, NULL','sizeof(_neg), 5, NULL','Forward wrong initial array capacity while preserving record size')}


def wrong_source(row,directory):
    directory.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
    source=ROOT/row['source'];text=source.read_text()
    if int(row['address'],0)==0x20b6128:
        altered=text.replace('{','{\nif(theMap)((AddressMapping*)theMap)->privateIp=0;',1);meaning='Write caller memory despite original debug-disabled no-op'
    else:
        before,after,meaning=MUTATIONS[int(row['address'],0)]
        if text.count(before)!=1:raise ValueError('NAT whole-source mutation is not unique')
        altered=text.replace(before,after)
    wrong=directory/source.name;wrong.write_text(altered);bad,body=build(wrong,directory/'build',negative=True)
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();violations=[]
    for seed,vector in enumerate(cases(int(row['address'],0))):
        record=run(image,row,body,vector,seed)
        if not record['modelPassed']:
            violations.append(dict(vector=vector,seed=seed,actualReturningModelViolation=record))
            if len(violations)==4:break
    if not violations:raise ValueError(('Wrong complete NAT C passed independent caller model',row['address']))
    return dict(address=row['address'],meaning=meaning,sourceSha256=sha256(wrong),objectSha256=bad['objectSha256'],compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],sourceDependencies=bad['sourceDependencies'],rejectedByCompleteNativeComparison=True,actualReturningModelRejections=len(violations),witnesses=violations,sourceOrExecutionCredit=0)
