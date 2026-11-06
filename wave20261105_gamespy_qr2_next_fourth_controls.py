import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261105_gamespy_qr2_next_fourth_build import build
from wave20261105_gamespy_qr2_next_fourth_fixtures import run
from wave20261105_gamespy_qr2_next_fourth_models import cases

MUTATIONS=[('minimum-length','if (len < 3)','if (len < 4)','Reject the valid three-count query'),('all-server-keys','serverkeycount != 0xFF','serverkeycount != 0xFE','Change the all-server-keys byte sentinel'),('split-return-status','gsi_true == native_fn_020b7b00','gsi_false == native_fn_020b7b00','Treat false reply-builder status as another packet'),('split-prefix','buf->len = 5','buf->len = 6','Restore the wrong split-packet prefix length'),('split-limit','> QR2_SPLITNUM_MAX','>= QR2_SPLITNUM_MAX','Stop on the allowed maximum packet ordinal')]


def layouts(row,directory,wrong=False):
    directory.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
    checks=[('sizeof(int)',4),('sizeof(void*)',4),('sizeof(uchar)',1),('sizeof(SOCKET)',4),('sizeof(struct sockaddr_in)',8),('OFF(struct sockaddr_in,sin_family)',1),('OFF(struct sockaddr_in,sin_port)',2),('OFF(struct sockaddr_in,sin_addr)',4),('sizeof(struct qr2_buffer_s)',1404),('OFF(struct qr2_buffer_s,len)',1400),('sizeof(struct QRSplitQueryProgress)',280),('OFF(struct QRSplitQueryProgress,mCurPacketNum)',4),('OFF(struct QRSplitQueryProgress,mKeyBuffer)',20),('OFF(struct qr2_keybuffer_s,numkeys)',256),('OFF(struct qr2_implementation_s,hbsock)',0)]
    text='#include "context.h"\n#define OFF(T,m) ((size_t)&(((T*)0)->m))\n'
    text+='\n'.join('typedef char check_%d[(%s)==%d?1:-1];'%(index,expression,16 if wrong and index==4 else expected) for index,(expression,expected) in enumerate(checks))+'\n'
    source=directory/'layout.c';source.write_text(text);obj=directory/'layout.o'
    process=subprocess.run([str(ROOT/row['compilerPath']),*row['compilerFlags'],'-c',str(source),'-o',str(obj)],cwd=ROOT,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=60)
    if (process.returncode==0)==wrong:raise ValueError(('Pinned QR2 dispatcher layout proof differs',wrong,process.stdout,process.stderr))
    return dict(checks=len(checks),allPassed=not wrong,rejected=wrong,sourceSha256=sha256(source),compilerSha256=row['compilerSha256'],flags=row['compilerFlags'],stdout=process.stdout,stderr=process.stderr,wrongControl='POSIX16-byte address substituted for measured Nintendo8-byte address' if wrong else None)


def wrong_source(row,directory):
    source=ROOT/row['source'];text=source.read_text();image=(ROOT/'extract/arm9/arm9.bin').read_bytes();out=[]
    for name,before,after,meaning in MUTATIONS:
        folder=directory/name;folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        if text.count(before)!=1:raise ValueError(('Scoped dispatcher mutation is no longer unique',name))
        wrong=folder/source.name;wrong.write_text(text.replace(before,after));bad,body=build(wrong,folder/'build',negative=True);violations=[]
        for seed,vector in enumerate(cases(int(row['address'],0))):
            record=run(image,row,body,vector,seed)
            if not record['modelPassed']:
                violations.append(dict(vector=vector,seed=seed,actualReturningModelViolation=record))
                if len(violations)==4:break
        if not violations:raise ValueError(('Wrong complete dispatcher C passed independent caller oracle',name))
        out.append(dict(address=row['address'],case=name,meaning=meaning,sourceSha256=sha256(wrong),objectSha256=bad['objectSha256'],compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],sourceDependencies=bad['sourceDependencies'],rejectedByCompleteNativeComparison=True,actualReturningModelRejections=len(violations),witnesses=violations,sourceOrExecutionCredit=0))
    return out
