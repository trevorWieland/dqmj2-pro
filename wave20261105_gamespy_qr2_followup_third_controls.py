import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261105_gamespy_qr2_followup_third_build import build
from wave20261105_gamespy_qr2_followup_third_fixtures import run
from wave20261105_gamespy_qr2_followup_third_models import cases

COMMON=[('sizeof(u32)',4),('sizeof(void*)',4),('sizeof(unsigned long)',4),('sizeof(long)',4),('sizeof(ThreadInfo)',8),('OFF(ThreadInfo,current)',4)]
CONTROL=[('sizeof(Control)',2292),('OFF(Control,active)',36),('OFF(Control,callback)',40),('OFF(Control,completion)',44),('OFF(Control,boundary)',48),('OFF(Control,thread)',52),('OFF(Control,stack)',244),('sizeof(((Control*)0)->thread)',192),('sizeof(((Control*)0)->stack)',2048)]
STATE=[('sizeof(State)',4816),('sizeof(Alloc)',4),('sizeof(Free)',4),('sizeof(Mask)',4),('sizeof(Pair)',8),('sizeof(((State*)0)->threada10)',192),('sizeof(((State*)0)->stackad0)',2048)]
STATE_FIELDS={'f0':0,'f4':4,'mutex8':8,'alloc':40,'free':44,'f30':48,'f34':52,'text38':56,'f40':64,'error1b8':440,'mutex1bc':444,'f9d4':2516,'mask9e4':2532,'config9e8':2536,'flag9ec':2540,'paira04':2564,'threada10':2576,'stackad0':2768}



def layouts(row,directory,wrong=False):
    directory.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
    checks=COMMON+(CONTROL if row['address']=='0x20b86cc'else STATE+[(f'OFF(State,{name})',value)for name,value in STATE_FIELDS.items()])
    text='#include "context.h"\n#define OFF(T,m) ((size_t)&(((T*)0)->m))\n'
    text+='\n'.join('typedef char check_%d[(%s)==%d?1:-1];'%(index,expression,expected+(1 if wrong and index==0 else 0)) for index,(expression,expected) in enumerate(checks))+'\n'
    source=directory/'layout.c';source.write_text(text);obj=directory/'layout.o'
    command=[str(ROOT/row['compilerPath']),*row['compilerFlags'],'-c',str(source),'-o',str(obj)]
    process=subprocess.run(command,cwd=ROOT,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=60)
    if (process.returncode==0)==wrong:raise ValueError(('Pinned C layout result differs',wrong,process.stdout,process.stderr))
    return dict(checks=len(checks),allPassed=not wrong,rejected=wrong,sourceSha256=sha256(source),compilerSha256=row['compilerSha256'],flags=row['compilerFlags'],stdout=process.stdout,stderr=process.stderr)


def changes(address):
    value={
        0x20b86cc:('clear-span','source','sizeof(Control)','sizeof(Control)-4','Clear four fewer bytes than measured initialized caller view'),
        0x20b8e74:('initial-flag','source','->flag9ec=1','->flag9ec=2','Publish wrong initial configuration flag'),
        0x20b8f64:('incoming-word','source','->f30=value','->f30=value+1','Store altered incoming word'),
        0x20b90bc:('old-status-read','source','(void)native_data_021d3028->f4;','','Remove actual old status read before locking'),
        0x20b90ec:('old-phase-read','source','(void)native_data_021d3028->f0;','','Remove actual old phase read before storing'),
        0x20b92b4:('shared-phase-reads','header','volatile u32 f0,f4;','u32 f0,f4;','Coalesce independently measured guard/switch phase reads')}
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
