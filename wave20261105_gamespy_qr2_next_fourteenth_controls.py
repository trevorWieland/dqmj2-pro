import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261105_gamespy_qr2_next_fourteenth_build import build
from wave20261105_gamespy_qr2_next_fourteenth_fixtures import run
from wave20261105_gamespy_qr2_next_fourteenth_models import cases

LAYOUT=[('sizeof(NAT)',216),('sizeof(gsi_bool)',4),('sizeof(void*)',4),('sizeof(NatType)',4),('sizeof(NatMappingScheme)',4),('sizeof(struct NativeStatus)',32),('sizeof(struct NativePorts)',12),('sizeof(struct NativeNatTail)',20),('(0x21d2c70-0x21d2bf0)',128)]
FIELDS={'NAT':{'natType':140,'mappingScheme':144},'struct NativeStatus':{'scheme':8,'callback':12,'start':16},'struct NativePorts':{'kind':0,'ert':4,'mapping':8},'struct NativeNatTail':{'kind':12,'scheme':16}}


def layouts(row,directory,wrong=False):
    directory.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
    checks=LAYOUT+[(f'OFF({name},{field})',value) for name,fields in FIELDS.items() for field,value in fields.items()]
    text='#include "context.h"\n#undef activeNatify\n#undef mappingSock\n#undef ertSock\n#undef matchup1ip\n#undef matchup2ip\n#undef matchup3ip\n#define OFF(T,m) ((size_t)&(((T*)0)->m))\n'
    text+='\n'.join('typedef char check_%d[(%s)==%d?1:-1];'%(index,expression,expected+(1 if wrong and index==0 else 0)) for index,(expression,expected) in enumerate(checks))+'\n'
    source=directory/'layout.c';source.write_text(text);obj=directory/'layout.o'
    command=[str(ROOT/row['compilerPath']),*row['compilerFlags'],'-c',str(source),'-o',str(obj)]
    process=subprocess.run(command,cwd=ROOT,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=60)
    if (process.returncode==0)==wrong:raise ValueError(('Pinned C layout result differs',wrong,process.stdout,process.stderr))
    return dict(checks=len(checks),allPassed=not wrong,rejected=wrong,sourceSha256=sha256(source),compilerSha256=row['compilerSha256'],flags=row['compilerFlags'],stdout=process.stdout,stderr=process.stderr)


def changes(address):
    if address!=0x20b6aa8:raise ValueError('No selected aggregate-status mutation family')
    return [('timeout-equality','source','< NATIFY_TIMEOUT','<= NATIFY_TIMEOUT','Treat native10000 timeout equality as active'),('callback-success-word','source','natifyCallback(success, nat);','natifyCallback(!success, nat);','Normalize/invert the full Determine result word before aggregate callback'),('post-callback-kind','source','native_data_020e172c.kind = native_data_021d2c70.kind;','native_data_020e172c.kind = native_data_021d2c70.scheme;','Read live mapping-scheme word into kind output'),('close-validity','source','if (mappingSock != INVALID_SOCKET)','if (mappingSock == INVALID_SOCKET)','Close the invalid mapping socket and retain a valid mapping socket')]


def wrong_source(row,directory):
    source=ROOT/row['source'];text=source.read_text();image=(ROOT/'extract/arm9/arm9.bin').read_bytes();out=[]
    for name,owner,before,after,meaning in changes(int(row['address'],0)):
        folder=directory/name;folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        wrong=folder/source.name;wrong.write_text(text);target=folder/'context.h'if owner=='header'else wrong;old=target.read_text()
        if old.count(before)!=1:raise ValueError(('Twelfth exact source mutation changed',name))
        target.write_text(old.replace(before,after));bad,body=build(wrong,folder/'build',negative=True);violations=[]
        for seed,vector in enumerate(cases(int(row['address'],0))):
            record=run(image,row,body,vector,seed)
            if not record['modelPassed']:
                violations.append(dict(vector=vector,seed=seed,actualReturningModelViolation=record))
                if len(violations)==4:break
        if not violations:raise ValueError(('Wrong SDK packet C passed independent caller oracle',name))
        out.append(dict(address=row['address'],case=name,meaning=meaning,sourceSha256=sha256(wrong),objectSha256=bad['objectSha256'],compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],sourceDependencies=bad['sourceDependencies'],rejectedByCompleteNativeComparison=True,actualReturningModelRejections=len(violations),witnesses=violations,sourceOrExecutionCredit=0))
    return out
