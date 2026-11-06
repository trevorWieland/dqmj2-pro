import os,shutil,subprocess
from project import ROOT,sha256
from wave20261106_wcm_manager_next_cps_second_build import build
from wave20261106_wcm_manager_next_cps_second_fixtures import run
from wave20261106_wcm_manager_next_cps_second_models import cases

LAYOUT=[('sizeof(u8)',1),('sizeof(u16)',2),('sizeof(u32)',4),('sizeof(void*)',4),('sizeof(CPSGlobalView)',96),('OFF(CPSGlobalView,putpnt)',40),('OFF(CPSGlobalView,getpnt)',48),('OFF(CPSGlobalView,myip)',80),('OFF(CPSGlobalView,recvthread)',84),('OFF(CPSGlobalView,buf)',88),('OFF(CPSGlobalView,buflen)',92),('sizeof(CPSArpCache)',12),('OFF(CPSArpCache,ip)',0),('OFF(CPSArpCache,mac)',4),('OFF(CPSArpCache,when)',10),('sizeof(native_data_021cfd78)',96),('sizeof(ThreadInfoView)',8),('OFF(ThreadInfoView,current)',4)]


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
  0x208bd24:('blocklen=(size+9)&~1;','blocklen=(size+11)&~1;'),
  0x208be40:('if(!native_fn_020068c0','if(native_fn_020068c0'),
  0x208be70:('*len=blocklen-2;','*len=blocklen-3;'),
  0x208bee4:('G.getpnt>=G.buflen','G.getpnt>G.buflen'),
  0x208bf10:('i<8;i++','i<7;i++'),
  0x208bf98:('buf[15]=1;','buf[15]=2;'),
  0x208c080:('if(new_entry){','if(!new_entry){'),
  0x208c140:('hdr[-12]=0x5e;','hdr[-12]=0x5f;')
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
