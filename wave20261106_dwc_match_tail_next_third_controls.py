import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261106_dwc_match_tail_next_third_build import build
from wave20261106_dwc_match_tail_next_third_fixtures import run
from wave20261106_dwc_match_tail_next_third_models import cases

LAYOUT=[('sizeof(u32)', 4), ('sizeof(OSTick)', 8), ('sizeof(DWCSBMessageHeader)', 20), ('sizeof(DWCSBMessage)', 148), ('sizeof(DWCMatchCommandControl)', 152), ('OFF(DWCMatchControl,pGpObj)', 0), ('OFF(DWCMatchControl,gt2NumValidConn)', 14), ('OFF(DWCMatchControl,qr2Obj)', 16), ('OFF(DWCMatchControl,qr2NNFinishCount)', 20), ('OFF(DWCMatchControl,qr2MatchType)', 21), ('OFF(DWCMatchControl,qr2NumEntry)', 22), ('OFF(DWCMatchControl,qr2Port)', 26), ('OFF(DWCMatchControl,qr2IP)', 28), ('OFF(DWCMatchControl,qr2IPList)', 36), ('OFF(DWCMatchControl,qr2PortList)', 164), ('OFF(DWCMatchControl,sbObj)', 228), ('OFF(DWCMatchControl,sbPidList)', 244), ('OFF(DWCMatchControl,distantFriend)', 422), ('OFF(DWCMatchControl,cmdResendFlag)', 444), ('OFF(DWCMatchControl,cmdResendTick)', 448), ('OFF(DWCMatchControl,cmdTimeoutTime)', 456), ('OFF(DWCMatchControl,cmdTimeoutStartTick)', 460), ('OFF(DWCMatchControl,profileID)', 512), ('OFF(DWCMatchControl,reqProfileID)', 516), ('OFF(DWCMatchControl,priorProfileID)', 520), ('OFF(DWCMatchControl,validAidBitmap)', 752), ('OFF(DWCMatchControl,cmdCnt)', 972), ('OFF(DWCMatchCommandControl,data)', 8), ('OFF(DWCMatchCommandControl,profileID)', 136), ('OFF(DWCMatchCommandControl,len)', 140), ('OFF(DWCMatchCommandControl,sendTime)', 144)]


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
    entries={
      0x20a00ac:('recorded-profile','source','cmdCnt.profileID = profileID;','cmdCnt.profileID = profileID+1;','Alter recorded command profile'),
      0x20a020c:('wire-version','source','header.version = DWC_MATCHING_VERSION;','header.version = DWC_MATCHING_VERSION+1;','Change serialized protocol version'),
      0x209f110:('dummy-command','source','cmdCnt.command = DWC_MATCH_COMMAND_DUMMY;','cmdCnt.command = DWC_MATCH_COMMAND_DUMMY-1;','Change stopped command sentinel'),
      0x209f640:('valid-count','source','int count = -1;','int count = 0;','Count one extra valid connection'),
      0x209f1c0:('entry-reset','source','qr2NumEntry = 0;','qr2NumEntry = 1;','Fail to clear entry count'),
      0x20a1278:('deferred-request','source','reqProfileID=0;','reqProfileID=1;','Retain wrong deferred request profile')}
    return [entries[address]]


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
