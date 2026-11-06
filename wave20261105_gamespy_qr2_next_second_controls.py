import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261105_gamespy_qr2_next_second_build import build
from wave20261105_gamespy_qr2_next_second_fixtures import run
from wave20261105_gamespy_qr2_next_second_models import cases

MUTATIONS={0x20b5f38:('^= 1','^= 0','Suppress alternating static output-buffer selection'),0x20b72f8:('qrec->nn_callback = nncallback','qrec->cm_callback = (qr2_clientmessagecallback_t)nncallback','Store natneg callback bits in the client-message slot'),0x20b730c:('qrec->cm_callback = cmcallback','qrec->pa_callback = (qr2_publicaddresscallback_t)cmcallback','Store client-message callback bits in the public-address slot'),0x20b7320:('qrec->pa_callback = pacallback','qrec->nn_callback = (qr2_natnegcallback_t)pacallback','Store public-address callback bits in the natneg slot'),0x20b753c:('keyid < 1','keyid < 2','Reject the valid minimum key identifier'),0x20b7588:('native_fn_0201d69c(value) + 1','native_fn_0201d69c(value) + 2','Copy an extra byte and publish an extra buffer byte'),0x20b76bc:('>> 2','>> 3','Encode the first quartet from the wrong bit position'),0x20b7848:('native_fn_0201d69c(buf->buffer + buf->len) + 1','native_fn_0201d69c(buf->buffer + buf->len) + 2','Publish an extra challenge-output length byte')}


def layouts(row,directory,wrong=False):
    directory.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
    checks=[('sizeof(int)',4),('sizeof(void*)',4),('sizeof(uchar)',1),('sizeof(qr2_t)',4),('sizeof(struct qr2_keybuffer_s)',260),('sizeof(struct qr2_buffer_s)',1404),('OFF(struct qr2_keybuffer_s,numkeys)',256),('OFF(struct qr2_buffer_s,len)',1400),('OFF(struct qr2_implementation_s,secret_key)',68),('OFF(struct qr2_implementation_s,nn_callback)',160),('OFF(struct qr2_implementation_s,cm_callback)',164),('OFF(struct qr2_implementation_s,pa_callback)',168),('sizeof(qr2_natnegcallback_t)',4)]
    text='#include "context.h"\n#define OFF(T,m) ((size_t)&(((T*)0)->m))\n'
    text+='\n'.join('typedef char check_%d[(%s)==%d?1:-1];'%(index,expression,expected+(1 if wrong and index==2 else 0)) for index,(expression,expected) in enumerate(checks))+'\n'
    source=directory/'layout.c';source.write_text(text);obj=directory/'layout.o'
    process=subprocess.run([str(ROOT/row['compilerPath']),*row['compilerFlags'],'-c',str(source),'-o',str(obj)],cwd=ROOT,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=60)
    if (process.returncode==0)==wrong:raise ValueError(('Pinned QR2 C layout proof differs',wrong,process.stdout,process.stderr))
    return dict(checks=len(checks),allPassed=not wrong,rejected=wrong,sourceSha256=sha256(source),compilerSha256=row['compilerSha256'],flags=row['compilerFlags'],stdout=process.stdout,stderr=process.stderr,scope='Measured accessed QR2 prefix fields and buffers; complete implementation object storage remains uncredited')


def wrong_source(row,directory):
    directory.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
    source=ROOT/row['source'];before,after,meaning=MUTATIONS[int(row['address'],0)];text=source.read_text()
    if text.count(before)!=1:raise ValueError(('Scoped QR2 whole-C mutation no longer unique',row['address'],before))
    wrong=directory/source.name;wrong.write_text(text.replace(before,after));bad,body=build(wrong,directory/'build',negative=True)
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();violations=[]
    for seed,vector in enumerate(cases(int(row['address'],0))):
        record=run(image,row,body,vector,seed)
        if not record['modelPassed']:
            violations.append(dict(vector=vector,seed=seed,actualReturningModelViolation=record))
            if len(violations)==4:break
    if not violations:raise ValueError(('Wrong complete QR2 C passed caller oracle',row['address']))
    return dict(address=row['address'],meaning=meaning,sourceSha256=sha256(wrong),objectSha256=bad['objectSha256'],compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],sourceDependencies=bad['sourceDependencies'],rejectedByCompleteNativeComparison=True,actualReturningModelRejections=len(violations),witnesses=violations,sourceOrExecutionCredit=0)
