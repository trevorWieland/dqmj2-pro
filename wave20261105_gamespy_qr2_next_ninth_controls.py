import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261105_gamespy_qr2_next_ninth_build import build
from wave20261105_gamespy_qr2_next_ninth_fixtures import run
from wave20261105_gamespy_qr2_next_ninth_models import cases

MUTATIONS=[('minimum-room','AVAILABLE_BUFFER_LEN(buf) < sizeof(cttemp)','AVAILABLE_BUFFER_LEN(buf) <= sizeof(cttemp)','Reject the allowed2-byte count prefix capacity'),('row-index','pindex++','pindex += 2','Skip a requested player/team row'),('callback-context','qrec->udata','NULL','Lose measured full-word callback userdata'),('empty-fallback','if(len == buf->len)','if(len != buf->len)','Suppress necessary empty value placeholder after no-output callback')]


def layouts(row,directory,wrong=False):
    directory.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
    checks=[('sizeof(int)',4),('sizeof(unsigned short)',2),('sizeof(void*)',4),('sizeof(uchar)',1),('OFF(struct qr2_implementation_s,server_key_callback)',136),('OFF(struct qr2_implementation_s,player_key_callback)',140),('OFF(struct qr2_implementation_s,team_key_callback)',144),('OFF(struct qr2_implementation_s,key_list_callback)',148),('OFF(struct qr2_implementation_s,playerteam_count_callback)',152),('OFF(struct qr2_implementation_s,udata)',268),('sizeof(struct qr2_implementation_s)',272),('sizeof(struct qr2_keybuffer_s)',260),('OFF(struct qr2_keybuffer_s,numkeys)',256),('OFF(struct qr2_buffer_s,len)',1400),('sizeof(native_data_020e25b4)',1),('sizeof(native_data_020e25ac)',8)]
    text='#include "context.h"\n#define OFF(T,m) ((size_t)&(((T*)0)->m))\n'
    text+='\n'.join('typedef char check_%d[(%s)==%d?1:-1];'%(index,expression,276 if wrong and index==9 else expected) for index,(expression,expected) in enumerate(checks))+'\n'
    source=directory/'layout.c';source.write_text(text);obj=directory/'layout.o'
    process=subprocess.run([str(ROOT/row['compilerPath']),*row['compilerFlags'],'-c',str(source),'-o',str(obj)],cwd=ROOT,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=60)
    if (process.returncode==0)==wrong:raise ValueError(('Pinned partial QR2 callback layout differs',wrong,process.stdout,process.stderr))
    return dict(checks=len(checks),allPassed=not wrong,rejected=wrong,sourceSha256=sha256(source),compilerSha256=row['compilerSha256'],flags=row['compilerFlags'],stdout=process.stdout,stderr=process.stderr,
        measuredViewOnly=True,opaqueBytes=[172,268],completeObjectStorageCredit=0)


def wrong_source(row,directory):
    source=ROOT/row['source'];text=source.read_text();image=(ROOT/'extract/arm9/arm9.bin').read_bytes();out=[]
    for name,before,after,meaning in MUTATIONS:
        folder=directory/name;folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        count=text.count(before)
        if count!=({'callback-context':6,'empty-fallback':2}.get(name,1)):raise ValueError(('Scoped split reply mutation count differs',name,count))
        wrong=folder/source.name;wrong.write_text(text.replace(before,after));bad,body=build(wrong,folder/'build',negative=True);violations=[]
        for seed,vector in enumerate(cases(int(row['address'],0))):
            record=run(image,row,body,vector,seed)
            if not record['modelPassed']:
                violations.append(dict(vector=vector,seed=seed,actualReturningModelViolation=record))
                if len(violations)==4:break
        if not violations:raise ValueError(('Wrong split reply C passed independent caller oracle',name))
        out.append(dict(address=row['address'],case=name,meaning=meaning,sourceSha256=sha256(wrong),objectSha256=bad['objectSha256'],compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],sourceDependencies=bad['sourceDependencies'],rejectedByCompleteNativeComparison=True,actualReturningModelRejections=len(violations),witnesses=violations,sourceOrExecutionCredit=0))
    return out
