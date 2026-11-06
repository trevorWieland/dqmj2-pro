import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261105_gamespy_qr2_followup_fifth_build import build
from wave20261105_gamespy_qr2_followup_fifth_fixtures import run
from wave20261105_gamespy_qr2_followup_fifth_models import cases

COMMON=[('sizeof(u32)',4),('sizeof(int)',4),('sizeof(unsigned short)',2),('sizeof(void*)',4),('sizeof(Result)',40)]
CONTROL=[('sizeof(Control)',2292),('OFF(Control,thread)',52),('OFF(Control,stack)',244),('sizeof(((Control*)0)->thread)',192),('sizeof(((Control*)0)->stack)',2048)]
TRANSPORT=[('sizeof(State)',4816),('OFF(State,error1b8)',440),('OFF(State,threada10)',2576),('OFF(State,stackad0)',2768),('sizeof(((State*)0)->threada10)',192),('sizeof(((State*)0)->stackad0)',2048),('sizeof(Packet)',1044),('OFF(Packet,length)',0),('OFF(Packet,magic)',4),('OFF(Packet,code)',8),('OFF(Packet,tail)',12)]



def layouts(row,directory,wrong=False):
    directory.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
    checks=COMMON+(TRANSPORT if row['address']in ['0x20b9128','0x20b91a0','0x20b9270']else CONTROL)
    text='#include "context.h"\n#define OFF(T,m) ((size_t)&(((T*)0)->m))\n'
    text+='\n'.join('typedef char check_%d[(%s)==%d?1:-1];'%(index,expression,expected+(1 if wrong and index==0 else 0)) for index,(expression,expected) in enumerate(checks))+'\n'
    source=directory/'layout.c';source.write_text(text);obj=directory/'layout.o'
    command=[str(ROOT/row['compilerPath']),*row['compilerFlags'],'-c',str(source),'-o',str(obj)]
    process=subprocess.run(command,cwd=ROOT,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=60)
    if (process.returncode==0)==wrong:raise ValueError(('Pinned C layout result differs',wrong,process.stdout,process.stderr))
    return dict(checks=len(checks),allPassed=not wrong,rejected=wrong,sourceSha256=sha256(source),compilerSha256=row['compilerSha256'],flags=row['compilerFlags'],stdout=process.stdout,stderr=process.stderr)


def changes(address):
    value={
        0x20b8780:('message-word','source','native_fn_02006e24(native_data_021d3020,r,0)','native_fn_02006e24(native_data_021d3020,0,0)','Lose actual incoming result pointer forwarded as message'),
        0x20b87a8:('restore-ime','source','*ime=previous;','*ime=previous+1;','Restore wrong16-bit modeled register word'),
        0x20b9270:('restore-ime','source','*ime=previous;','*ime=previous+1;','Restore wrong16-bit modeled register word'),
        0x20b9d2c:('status-word','source','return result;','return result+1;','Alter returned provider status word'),
        0x20b9d40:('cleanup-guard','source','if(!native_fn_0209a930(&output))','if(native_fn_0209a930(&output))','Invoke cleanup for wrong provider result'),
        0x20b9128:('zero-progress','source','else if(result<0)','else if(result<=0)','Treat a finite zero-progress write as fatal instead of retrying'),
        0x20b91a0:('minimum-header','source','received<3*sizeof(u32)','received<2*sizeof(u32)','Accept incomplete three-word header')}
    if address==0x20b91a0:return [value[address],('partial-header-error','source','received>0||result!=0','received>0&&result!=0','Drop error notification on zero partial-header or first negative read')]
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
