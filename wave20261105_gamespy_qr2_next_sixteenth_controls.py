import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261105_gamespy_qr2_next_sixteenth_build import build
from wave20261105_gamespy_qr2_next_sixteenth_fixtures import run
from wave20261105_gamespy_qr2_next_sixteenth_models import cases

LAYOUT=[('sizeof(NegotiateError)',4),('sizeof(SOCKET)',4),('sizeof(void*)',4),('sizeof(NegotiateProgressFunc)',4),('sizeof(NegotiateCompletedFunc)',4),('sizeof(struct _NATNegotiator)',84),('AF_INET',2),('SOCK_DGRAM',2),('IPPROTO_UDP',0)]
FIELDS={'struct _NATNegotiator':{'negotiateSock':0,'gameSock':4,'cookie':8,'clientindex':12,'retryCount':36,'maxRetryCount':40,'guessedIP':48,'guessedPort':52,'gotRemoteData':54,'sendGotRemoteData':55,'progressCallback':56,'completedCallback':60,'userdata':64,'result':68}}


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
    if address!=0x20b6c08:raise ValueError('No selected six-word constructor mutation family')
    return [('socket-protocol','header','#define IPPROTO_UDP 0','#define IPPROTO_UDP 17','Forward provisional generic17 instead of measured socket thirdword0'),('cookie-word','source','neg->cookie = cookie;','neg->cookie = clientindex;','Store client word into cookie field'),('completion-word','source','neg->completedCallback = completedcallback;','neg->completedCallback = NULL;','Drop the fifth incoming callback word'),('userdata-word','source','neg->userdata = userdata;','neg->userdata = NULL;','Drop the sixth incoming context word')]


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
