import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261105_gamespy_qr2_followup_seventh_build import build
from wave20261105_gamespy_qr2_followup_seventh_fixtures import run
from wave20261105_gamespy_qr2_followup_seventh_models import cases

LAYOUT=[('sizeof(u32)',4),('sizeof(void*)',4),('sizeof(int)',4),('sizeof(char)',1),('((char)-1)<0',1),('sizeof(State)',4816),('sizeof(Control)',2292),('sizeof(Result)',40),('OFF(State,f0)',0),('OFF(State,f4)',4),('OFF(State,f34)',52),('OFF(State,text38)',56),('OFF(State,f40)',64),('OFF(State,gap44)',68),('OFF(State,error1b8)',440),('OFF(State,mutex1bc)',444),('OFF(State,gapa0c)',2572),('OFF(State,threada10)',2576),('sizeof(((State*)0)->error1b8)',4)]


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
        0x20b9068:[('callback-word','source','->gapa0c=callback','->gapa0c=callback^1','Alter stored raw function-word mode bit')],
        0x20b9364:[('entry-gate','source','if(native_data_021d3028->f4==1&&native_data_021d3028->f34==3)','if(native_data_021d3028->f4==2&&native_data_021d3028->f34==3)','Alter entry raw state gate'),('status-volatile','header','volatile u32 f34','u32 f34','Remove measured repeated status read contract')],
        0x20b9404:[('entry-gate','source','if(native_data_021d3028->f4==1&&native_data_021d3028->f40==3)','if(native_data_021d3028->f4==2&&native_data_021d3028->f40==3)','Alter entry raw state gate'),('status-volatile','header','volatile u32 f40','u32 f40','Remove measured repeated status read contract')],
        0x20b95d8:[('signed-zero-handle','source','handle>=0','handle>0','Reject original valid zero handle'),('retry-value','source','result==-26','result==-25','Stop at original close retry result')]}
    return value[address]




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
