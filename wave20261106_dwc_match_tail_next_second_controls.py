import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261106_dwc_match_tail_next_second_build import build
from wave20261106_dwc_match_tail_next_second_fixtures import run
from wave20261106_dwc_match_tail_next_second_models import cases

LAYOUT=[('sizeof(u32)',4),('sizeof(OSTick)',8),('sizeof(DWCGameMatchKeyData)',12),('OFF(DWCGameMatchKeyData,keyID)',0),('OFF(DWCGameMatchKeyData,isStr)',1),('OFF(DWCGameMatchKeyData,pad)',2),('OFF(DWCGameMatchKeyData,keyStr)',4),('OFF(DWCGameMatchKeyData,value)',8),('sizeof(MatchGlobalsView)',12),('OFF(MatchGlobalsView,addFilter)',8),('DWC_QR2_GAME_RESERVED_KEYS',154),('MAX_FILTER_LEN',256),('OFF(DWCMatchControl,sbObj)',0xe4),('OFF(DWCMatchControl,state)',0x1a0),('OFF(DWCMatchControl,qr2MatchType)',0x15),('OFF(DWCMatchControl,qr2NumEntry)',0x16),('OFF(DWCMatchControl,profileID)',0x200),('OFF(DWCMatchControl,reqProfileID)',0x204),('OFF(DWCMatchControl,priorProfileID)',0x208),('OFF(DWCMatchControl,sbUpdateRequestTick)',0x174),('OFF(DWCMatchControl,svDataBak)',0x348),('sizeof(((DWCMatchControl*)0)->svDataBak)',132)]


def layouts(row,directory,wrong=False):
    directory.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
    checks=LAYOUT
    text='#include "context.h"\n#define OFF(T,m) ((unsigned long)&(((T*)0)->m))\n'
    text+='\n'.join('typedef char check_%d[(%s)==%d?1:-1];'%(index,expression,expected+(1 if wrong and index==0 else 0)) for index,(expression,expected) in enumerate(checks))+'\n'
    source=directory/'layout.c';source.write_text(text);obj=directory/'layout.o'
    command=[str(ROOT/row['compilerPath']),*row['compilerFlags'],'-c',str(source),'-o',str(obj)]
    process=subprocess.run(command,cwd=ROOT,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=60)
    if (process.returncode==0)==wrong:raise ValueError(('Pinned C layout result differs',wrong,process.stdout,process.stderr))
    return dict(checks=len(checks),allPassed=not wrong,rejected=wrong,sourceSha256=sha256(source),compilerSha256=row['compilerSha256'],flags=row['compilerFlags'],stdout=process.stdout,stderr=process.stderr)


def changes(address):
    if address==0x20a121c:return [('backup-profile','source','svDataBak[1] = (u32)profileID;','svDataBak[1] = (u32)profileID+1;','Alter recorded backup profile word'),('backup-length','source','len = data[0] + 2;','len = data[0] + 3;','Copy an extra backup word')]
    if address==0x209fc38:return [('DNS-retry','header','#define DWC_DNS_ERROR_RETRY_MAX 5','#define DWC_DNS_ERROR_RETRY_MAX 4','Retry one fewer supplied DNS error'),('first-key','header','#define NUMPLAYERS_KEY 8','#define NUMPLAYERS_KEY 9','Change first requested key id')]
    raise ValueError('Outside backup/SB pair')



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
