import os,shutil,subprocess
from project import ROOT,sha256
from wave20261106_wcm_manager_next_cps_first_build import build
from wave20261106_wcm_manager_next_cps_first_fixtures import run
from wave20261106_wcm_manager_next_cps_first_models import cases

LAYOUT=[('sizeof(u8)',1),('sizeof(u16)',2),('sizeof(u32)',4),('sizeof(void*)',4),('sizeof(CPSSoc)',100),('OFF(CPSSoc,state)',8),('OFF(CPSSoc,local_port)',10),('OFF(CPSSoc,remote_port)',24),('OFF(CPSSoc,remote_ip)',28),('OFF(CPSSoc,sndbuf.data)',76),('sizeof(CPSGlobalView)',84),('OFF(CPSGlobalView,my_ip)',80)]


def layouts(row,directory,wrong=False):
 directory.mkdir(parents=True,exist_ok=True)
 for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
 text='#include "context.h"\n#define OFF(T,m) ((unsigned long)&(((T*)0)->m))\n'
 text+='\n'.join('typedef char check_%d[(%s)==%d?1:-1];'%(i,e,n+(1 if wrong and i==5 else 0))for i,(e,n)in enumerate(LAYOUT))+'\n';source=directory/'layout.c';source.write_text(text);obj=directory/'layout.o';cmd=[str(ROOT/row['compilerPath']),*row['compilerFlags'],'-c',str(source),'-o',str(obj)]
 result=subprocess.run(cmd,cwd=ROOT,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=60)
 if (result.returncode==0)==wrong:raise ValueError(('Pinned WCM layout result differs',wrong,result.stdout,result.stderr))
 return dict(checks=len(LAYOUT),allPassed=not wrong,rejected=wrong,sourceSha256=sha256(source),compilerSha256=row['compilerSha256'],flags=row['compilerFlags'],stdout=result.stdout,stderr=result.stderr,onlyConsumedCpsFieldsQualified=True)


def mutation(address):
 return {
  0x208bb08:('sum+=(u32)*s<<8;','sum+=(u32)*s<<7;'),
  0x208bb84:('sum^=0xffff;','sum^=0xfffe;'),
  0x208bbac:('return sum!=0xffff;','return sum!=0xfffe;'),
  0x208bc58:('==0xe0000000','==0xd0000000'),
  0x208bcc4:('if(*a++!=*b++)return 1;','if(*a++!=*b++)return 0;'),
  0x208c1e0:('hdr_len+20+body_len','hdr_len+21+body_len'),
  0x208c488:('hdr+4,len+8','hdr+4,len+9')
 }[address]



def wrong_source(row,directory):
 directory.mkdir(parents=True,exist_ok=True);source=ROOT/row['source'];text=source.read_text();a=int(row['address'],0);before,after=mutation(a);count=text.count(before)
 if count!=1:raise ValueError(('WCM semantic mutation occurrence differs',hex(a),before,count))
 for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
 wrong=directory/source.name;wrong.write_text(text.replace(before,after));bad,body=build(wrong,directory/'build',negative=True);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();violations=[]
 for seed,v in enumerate(cases(a)):
  record=run(image,row,body,v,seed)
  if not record['modelPassed']:
   violations.append(dict(vector=v,seed=seed,actualReturningModelViolation=record))
   if len(violations)==2:break
 if not violations:raise ValueError(('Meaningfully changed WCM C passed model',hex(a)))
 return [dict(address=row['address'],sourceSha256=sha256(wrong),objectSha256=bad['objectSha256'],genuineLink=bad['realLink'],compiledBytes=bad['compiledBytes'],rejectedByCompleteNativeComparison=True,actualReturningModelRejections=len(violations),witnesses=violations,sourceOrExecutionCredit=0)]
