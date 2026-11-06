import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261105_dwc_http_next_first_build import build
from wave20261105_dwc_http_next_first_fixtures import run
from wave20261105_dwc_http_next_first_models import cases

LAYOUT=[('sizeof(u32)',4),('sizeof(void*)',4),('sizeof(long)',4),('sizeof(int)',4),('sizeof(DWCHttpBuffer)',16),('OFF(DWCHttpBuffer,buffer)',0),('OFF(DWCHttpBuffer,write_index)',4),('OFF(DWCHttpBuffer,buffer_tail)',8),('OFF(DWCHttpBuffer,length)',12),('sizeof(DWCHttpLabelValue)',8),('sizeof(DWCHttpParseResult)',12),('OFF(DWCHttpParseResult,len)',4),('OFF(DWCHttpParseResult,index)',8),('OFF(DWCHttp,initflag)',4096),('OFF(DWCHttp,param)',4100),('OFF(DWCHttp,param.alloc)',4112),('OFF(DWCHttp,param.free)',4116),('OFF(DWCHttp,labelvalue)',6712),('OFF(DWCHttp,thread)',6968),('OFF(DWCHttp,thread.state)',7076),('OFF(DWCHttp,mutex)',7160),('OFF(DWCHttp,abort)',7184),('sizeof(DWCHttp)',7188),('sizeof(Thread)',192),('sizeof(Mutex)',24)]


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
    values={
        0x20983d0:('init-gate','source','initflag==255','initflag==254','Alter exact native initialization byte guard'),
        0x2098a7c:('published-length','source','buf->length=len;','buf->length=len+1;','Publish wrong allocated length word'),
        0x2098ab4:('clear-span','source','sizeof(*buf)','sizeof(*buf)-4','Leave final buffer length word uncleared'),
        0x2098adc:('zero-growth','source','len<=0','len<0','Allocate and copy at original rejected zero growth'),
        0x2098c38:('inclusive-index','source','aResult->index>aResult->len','aResult->index>=aResult->len','Reject original inclusive result index boundary'),
        0x2098ed8:('table-last-entry','source','i<32','i<31','Skip final published32-entry slot'),
        0x2098f14:('terminator-boundary','source','result<size','result<=size','Write terminator at original excluded equality'),
        0x2098f48:('equal-capacity','source','native_fn_0201d69c(value)>=size','native_fn_0201d69c(value)>size','Copy at original rejected equality'),
        0x2098f74:('entry-count','source','i<count','i<=count','Free an extra label/value entry')}
    return [values[address]]




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
