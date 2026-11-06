import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261105_gamespy_qr2_next_third_build import build
from wave20261105_gamespy_qr2_next_third_fixtures import run
from wave20261105_gamespy_qr2_next_third_models import cases

MUTATIONS={0x20b5970:('connection->ip * connection->port','connection->ip + connection->port','Hash adds the raw fields instead of wrapped uint32 multiplication'),0x20b5984:('(int)(short)(connection1->port','(int)(unsigned short)(connection1->port','Port ordering loses signed16 difference extension'),0x20b59ac:('return *connectionPtrPtr;','return NULL;','Present lookup entry loses its returned connection word'),0x20b5cd0:('connection->freeAtAcceptReject || connection->callbackLevel','connection->freeAtAcceptReject && connection->callbackLevel','One active callback/free-at-accept guard no longer blocks disposal'),0x20b5e8c:('&& !connection->freeAtAcceptReject','&& connection->freeAtAcceptReject','Closed connection disposal tests the opposite free-at-accept condition'),0x20b5f14:('socket->error = GT2True','socket->error = GT2False','Error flag is not published before callbacks')}


def layouts(row,directory,wrong=False):
    directory.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
    checks=[('sizeof(int)',4),('sizeof(void*)',4),('sizeof(unsigned short)',2),('sizeof(GTI2Connection)',160),('sizeof(GTI2Socket)',76),('OFF(GTI2Connection,ip)',0),('OFF(GTI2Connection,port)',4),('OFF(GTI2Connection,socket)',8),('OFF(GTI2Connection,state)',12),('OFF(GTI2Connection,freeAtAcceptReject)',20),('OFF(GTI2Connection,callbackLevel)',36),('OFF(GTI2Socket,connections)',12),('OFF(GTI2Socket,closedConnections)',16),('OFF(GTI2Socket,error)',24)]
    text='#include "context.h"\n#define OFF(T,m) ((size_t)&(((T*)0)->m))\n'
    text+='\n'.join('typedef char check_%d[(%s)==%d?1:-1];'%(index,expression,expected+(1 if wrong and index==2 else 0)) for index,(expression,expected) in enumerate(checks))+'\n'
    source=directory/'layout.c';source.write_text(text);obj=directory/'layout.o'
    process=subprocess.run([str(ROOT/row['compilerPath']),*row['compilerFlags'],'-c',str(source),'-o',str(obj)],cwd=ROOT,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=60)
    if (process.returncode==0)==wrong:raise ValueError(('Pinned socket caller layout differs',wrong,process.stdout,process.stderr))
    return dict(checks=len(checks),allPassed=not wrong,rejected=wrong,sourceSha256=sha256(source),compilerSha256=row['compilerSha256'],flags=row['compilerFlags'],stdout=process.stdout,stderr=process.stderr)


def wrong_source(row,directory):
    directory.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
    source=ROOT/row['source'];before,after,meaning=MUTATIONS[int(row['address'],0)];text=source.read_text()
    if text.count(before)!=1:raise ValueError(('Scoped socket whole-C mutation no longer unique',row['address']))
    wrong=directory/source.name;wrong.write_text(text.replace(before,after));bad,body=build(wrong,directory/'build',negative=True)
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();violations=[]
    for seed,vector in enumerate(cases(int(row['address'],0))):
        record=run(image,row,body,vector,seed)
        if not record['modelPassed']:
            violations.append(dict(vector=vector,seed=seed,actualReturningModelViolation=record))
            if len(violations)==4:break
    if not violations:raise ValueError(('Wrong complete socket C passed caller oracle',row['address']))
    return dict(address=row['address'],meaning=meaning,sourceSha256=sha256(wrong),objectSha256=bad['objectSha256'],compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],sourceDependencies=bad['sourceDependencies'],rejectedByCompleteNativeComparison=True,actualReturningModelRejections=len(violations),witnesses=violations,sourceOrExecutionCredit=0)
