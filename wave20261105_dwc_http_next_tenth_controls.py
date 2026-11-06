import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261105_dwc_http_next_tenth_build import build
from wave20261105_dwc_http_next_tenth_fixtures import run
from wave20261105_dwc_http_next_tenth_models import cases

LAYOUT=[('sizeof(u32)',4),('sizeof(void*)',4),('sizeof(size_t)',4),('sizeof(int)',4),('sizeof(DWCiAllocHeader)',32),('OFF(DWCiAllocHeader,signature)',0),('OFF(DWCiAllocHeader,size)',4),('sizeof(DWCErrorState)',8),('OFF(DWCErrorState,last)',0),('OFF(DWCErrorState,code)',4),('sizeof(DWCAllocatorState)',8),('OFF(DWCAllocatorState,free)',0),('OFF(DWCAllocatorState,alloc)',4)]


def layouts(row,directory,wrong=False):
    directory.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
    checks=LAYOUT
    text='#include "context.h"\n#define OFF(T,m) ((size_t)&(((T*)0)->m))\n'
    text+='\n'.join('typedef char check_%d[(%s)==%d?1:-1];'%(index,expression,expected+(1 if wrong and index==0 else 0)) for index,(expression,expected) in enumerate(checks))+'\n'
    source=directory/'layout.c';source.write_text(text);obj=directory/'layout.o'
    command=[str(ROOT/row['compilerPath']),*row['compilerFlags'],'-c',str(source),'-o',str(obj)]
    process=subprocess.run(command,cwd=ROOT,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=60)
    if (process.returncode==0)==wrong:raise ValueError(('Pinned C layout result differs',wrong,process.stdout,process.stderr))
    return dict(checks=len(checks),allPassed=not wrong,rejected=wrong,sourceSha256=sha256(source),compilerSha256=row['compilerSha256'],flags=row['compilerFlags'],stdout=process.stdout,stderr=process.stderr)


def changes(address):
    values={0x209a944:('raw-error-domain','source','case 21:','case 22:','Change the measured extra raw error case'),0x209a9d0:('fatal-guard','source','!= DWC_ERROR_FATAL','!= DWC_ERROR_FATAL-1','Preserve the wrong fatal code'),0x209aa44:('header-span','source','size + sizeof(DWCiAllocHeader)','size + sizeof(DWCiAllocHeader)-1','Underallocate the imported32B header by one byte'),0x209aa64:('null-test','source','if (ptr == NULL)','if (ptr != NULL)','Skip nonnull free paths'),0x209aa88:('alignment','source','newsize, 32','newsize, 16','Change forwarded default alignment'),0x209aa98:('copy-bound','source','oldsize > newsize','oldsize < newsize','Copy the larger allocation length instead of the minimum'),0x209b26c:('format-cap','header','DWC_COMMONSTR_MAX_KEY_VALUE_LEN 4096','DWC_COMMONSTR_MAX_KEY_VALUE_LEN 4095','Change the measured formatter capacity'),0x209b2bc:('key-delimiter','source','strlen(key) + 1','strlen(key) + 0','Check the key terminal byte instead of its following separator')}
    return[values[address]]


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
