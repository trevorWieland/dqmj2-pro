import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261105_gamespy_qr2_followup_second_build import build
from wave20261105_gamespy_qr2_followup_second_fixtures import run
from wave20261105_gamespy_qr2_followup_second_models import cases

LAYOUT=[('sizeof(u32)',4),('sizeof(void*)',4),('sizeof(Callback)',4),('sizeof(BoundaryCallback)',4),('sizeof(Result)',40),('sizeof(Control)',48),('sizeof(Event)',20),('OFF(Control,active)',36),('OFF(Control,callback)',40),('OFF(Control,completion)',44),('OFF(Result,words)',0),('sizeof(((Result*)0)->words)',40),('OFF(Event,payload)',20)]


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
        0x20b8878:('result-clear','source','words[7]=0','words[7]=1','Publish wrong cleared result word'),
        0x20b88a8:('result-mark','source','words[7]=1','words[7]=2','Publish wrong dequeued marker'),
        0x20b88d0:('result-flag','source','words[8]=1','words[8]=2','Publish wrong completion flag'),
        0x20b8d14:('default-result','source','int result=1','int result=0','Lose default completion result'),
        0x20b8d44:('success-word','source','return 1;','return 2;','Return wrong successful registration word'),
        0x20b8d80:('poll-duration','source','(100)','(101)','Pass wrong poll interval'),
        0x20b8da0:('completion-word','source','completion=1','completion=2','Publish wrong completion word'),
        0x20b8dd8:('message-code','source','case 201:','case 200:','Handle wrong response discriminator'),
        0x20b8dfc:('response-class','source','words[3]==3','words[3]==4','Accept wrong second response class'),
        0x20b87e4:('dispatch-class','source','case 1:','case 11:','Route wrong dispatch discriminator'),
        0x20b85d8:('registry-edge','header','#define MAX_REGISTERED_KEYS 254','#define MAX_REGISTERED_KEYS 255','Allow index255 outside measured upper registration boundary')}
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
