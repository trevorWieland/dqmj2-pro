import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261105_gamespy_qr2_followup_fourth_build import build
from wave20261105_gamespy_qr2_followup_fourth_fixtures import run
from wave20261105_gamespy_qr2_followup_fourth_models import cases

LAYOUT=[('sizeof(u32)',4),('sizeof(int)',4),('sizeof(void*)',4),('sizeof(Result)',40),('sizeof(Status)',72),('sizeof(ErrorPair)',8),('sizeof(State)',4816),('OFF(Status,prefix)',0),('OFF(Status,request)',20),('OFF(Status,callback)',60),('OFF(Status,extra40)',64),('OFF(Status,extra44)',68),('sizeof(((Status*)0)->prefix)',20),('sizeof(((Status*)0)->request)',40),('OFF(State,error1b8)',440),('OFF(State,mutex1bc)',444),('OFF(ErrorPair,detail)',4)]


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
        0x20b8fd8:('shared-error-read','header','volatile int error1b8;','int error1b8;','Coalesce actual post-lock check and provider argument reads'),
        0x20b909c:('status-guard','source','->f4!=2','->f4==2','Forward two incoming words in wrong protected status'),
        0x20b9a98:('returned-word','source','->request.words[6];','->request.words[6]+1;','Return altered stored result word'),
        0x20b9bf4:('phase-result','source','case 2:case 3:return 1;','case 2:case 3:return 0;','Lose positive cases in native dense switch'),
        0x20b9c4c:('callback-word','source','->callback(value)','->callback(value+1)','Forward altered one-word callback argument'),
        0x20b9cd8:('sticky-guard','source','.code!=9','.code==9','Reset wrong sticky-error class'),
        0x20b9a48:('first-cleanup-result','source','if(!native_fn_020b8748())ok=0;','if(native_fn_020b8748())ok=0;','Reverse first cleanup result while preserving both provider calls'),
        0x20b9c74:('large-id-edge','source','id>255','id>254','Reject original upper-inclusive id boundary'),
        0x20b9ab4:('request-id-prefix','source','id+1024','id+2048','Publish wrong measured request-id offset'),
        0x20b9b24:('request-kind','source','request.words[0]=2','request.words[0]=3','Publish wrong second request discriminator'),
        0x20b9b90:('request-kind','source','request.words[0]=3','request.words[0]=4','Publish wrong third request discriminator')}
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
