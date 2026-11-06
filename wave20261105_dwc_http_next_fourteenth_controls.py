import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261105_dwc_http_next_fourteenth_build import build
from wave20261105_dwc_http_next_fourteenth_fixtures import run
from wave20261105_dwc_http_next_fourteenth_models import cases

LAYOUT=[('sizeof(void*)',4),('sizeof(u16)',2),('sizeof(DWCInetControl)',100),('OFF(DWCInetControl,ac_state)',0),('OFF(DWCInetControl,state)',4),('OFF(DWCInetControl,online)',6),('OFF(DWCInetControl,dmaNo)',8),('OFF(DWCInetControl,powerMode)',10),('OFF(DWCInetControl,wontExecuteWDS)',12),('OFF(DWCInetControl,processWDSstate)',16),('OFF(DWCInetControl,nspotInfo)',20),('OFF(DWCInetControl,nspotInfo.ssid)',20),('OFF(DWCInetControl,nspotInfo.wep)',52),('OFF(DWCInetControl,nspotInfo.wepMode)',84),('OFF(DWCInetControl,nspotInfo.apnum)',88),('sizeof(DWCWDSData)',80),('sizeof(DWCACConfig)',12),('OFF(DWCACConfig,alloc)',0),('OFF(DWCACConfig,free)',4),('OFF(DWCACConfig,dmaNo)',8),('OFF(DWCACConfig,powerMode)',9),('OFF(DWCACConfig,option)',10),('sizeof(InetGlobals)',8),('OFF(InetGlobals,old)',0),('OFF(InetGlobals,current)',4),('DWC_ERROR_AC_ANY',5),('DWC_ERROR_FATAL',9),('WCM_PHASE_DCF',9)]


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
    if address==0x209ab18:return [('power-mode','source','inetCntl->powerMode = DWC_CONNECTINET_POWERMODE_ACTIVE;','inetCntl->powerMode = 0;','Change forced active power-mode field')]
    if address==0x209ab84:return [('operating-state','source','stpInetCntl->state = DWC_CONNECTINET_STATE_OPERATING;','stpInetCntl->state = DWC_CONNECTINET_STATE_CONNECTED;','Change state before AC provider creation'),('error-code','source','-50199','-50198','Change exact fatal provider error code')]
    if address==0x209ac5c:return [('raw-WDS5','source','case 5:','case 6:','Misroute measured extra raw WDS state5'),('AC-reset','source','stpInetCntl->ac_state = 0;','stpInetCntl->ac_state = 1;','Change state cleared before WDS process provider')]
    if address==0x209ad08:return [('WDS-second-word','source','native_fn_02096900(&(stpInetCntl->nspotInfo),1);','native_fn_02096900(&(stpInetCntl->nspotInfo),0);','Change actual second startup word from1to0'),('raw-WDS-result','source','return 5;','return 6;','Change raw WDS5 result')]
    raise ValueError('Outside four internet-control callers')



def wrong_source(row,directory):
    source=ROOT/row['source'];text=source.read_text();image=(ROOT/'extract/arm9/arm9.bin').read_bytes();out=[]
    for name,owner,before,after,meaning in changes(int(row['address'],0)):
        folder=directory/name;folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        wrong=folder/source.name;wrong.write_text(text);target=folder/'context.h'if owner=='header'else wrong;old=target.read_text()
        expected=2 if int(row['address'],0)==0x209ab84 and name=='error-code'else 1
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
