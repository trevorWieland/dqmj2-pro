import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261105_gamespy_qr2_next_fifth_build import build
from wave20261105_gamespy_qr2_next_fifth_fixtures import run,vectors


def layouts(row,directory,wrong=False):
    directory.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
    checks=[('sizeof(short)',2),('sizeof(uchar)',1),('sizeof(int)',4),('sizeof(void*)',4),('sizeof(uchar[256])',256)]
    text='#include "context.h"\n'+'\n'.join('typedef char check_%d[(%s)==%d?1:-1];'%(index,expression,4 if wrong and index==0 else expected) for index,(expression,expected) in enumerate(checks))+'\n'
    source=directory/'layout.c';source.write_text(text);obj=directory/'layout.o'
    process=subprocess.run([str(ROOT/row['compilerPath']),*row['compilerFlags'],'-c',str(source),'-o',str(obj)],cwd=ROOT,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=60)
    if (process.returncode==0)==wrong:raise ValueError(('Pinned signed16 cipher layout differs',wrong,process.stdout,process.stderr))
    return dict(checks=len(checks),allPassed=not wrong,rejected=wrong,sourceSha256=sha256(source),compilerSha256=row['compilerSha256'],flags=row['compilerFlags'],stdout=process.stdout,stderr=process.stderr)


def wrong_source(row,directory):
    source=ROOT/row['source'];text=source.read_text();image=(ROOT/'extract/arm9/arm9.bin').read_bytes();out=[]
    changes=[('counter-width','short counter;','int counter;',False,'Generic public int counter removes three native signed16 narrowing pairs; bounded cipher meaning is intentionally unchanged'),('cipher-operator','buffer_ptr[counter] ^= state[xorIndex]','buffer_ptr[counter] += state[xorIndex]',True,'Cipher substitutes addition for XOR'),('state-step','x + buffer_ptr[counter] + 1','x + buffer_ptr[counter] + 2',True,'Cipher advances its byte index by the wrong constant')]
    for name,before,after,semantic,meaning in changes:
        folder=directory/name;folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        if text.count(before)!=1:raise ValueError(('Cipher mutation expression is no longer unique',name))
        wrong=folder/source.name;wrong.write_text(text.replace(before,after));bad,body=build(wrong,folder/'build',negative=True);violations=[];equivalent=[]
        for seed,vector in enumerate(vectors()):
            record=run(image,row,body,vector,seed)
            if not record['modelPassed']:violations.append(dict(seed=seed,vector=vector,actualReturningModelViolation=record))
            else:equivalent.append(record['traceSha256'])
            if semantic and len(violations)==4:break
        if semantic and not violations:raise ValueError(('Wrong cipher algorithm passed independent arithmetic oracle',name))
        if not semantic and (violations or len(equivalent)!=len(vectors())):raise ValueError('Representation-only counter control unexpectedly changes bounded algorithm')
        out.append(dict(address=row['address'],case=name,meaning=meaning,sourceSha256=sha256(wrong),objectSha256=bad['objectSha256'],compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],sourceDependencies=bad['sourceDependencies'],
            rejectedByCompleteNativeComparison=True,actualReturningModelRejections=len(violations),boundedSemanticallyEquivalentReturns=len(equivalent) if not semantic else 0,witnesses=violations,sourceOrExecutionCredit=0))
    return out
