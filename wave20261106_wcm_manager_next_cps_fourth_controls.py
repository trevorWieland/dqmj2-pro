import os,shutil,subprocess
from project import ROOT,sha256
from wave20261106_wcm_manager_next_cps_fourth_build import build
from wave20261106_wcm_manager_next_cps_fourth_fixtures import run
from wave20261106_wcm_manager_next_cps_fourth_models import cases

LAYOUT=[('sizeof(u16)',2),('sizeof(u32)',4),('sizeof(void*)',4),('sizeof(ThreadInfoView)',12),('OFF(ThreadInfoView,current)',4),('OFF(ThreadInfoView,head)',8),('sizeof(ThreadPrefix)',168),('OFF(ThreadPrefix,next)',104),('OFF(ThreadPrefix,cps)',164),('sizeof(CPSSoc)',100),('OFF(CPSSoc,thread)',0),('OFF(CPSSoc,block_type)',4),('OFF(CPSSoc,state)',8),('OFF(CPSSoc,local_port)',10),('OFF(CPSSoc,when)',16),('OFF(CPSSoc,local_ip_real)',20),('OFF(CPSSoc,remote_port)',24),('OFF(CPSSoc,remote_ip)',28),('OFF(CPSSoc,ackno)',36),('OFF(CPSSoc,seqno)',40),('OFF(CPSSoc,remote_win)',44),('OFF(CPSSoc,remote_mss)',46),('OFF(CPSSoc,remote_ackno)',48),('OFF(CPSSoc,ackrcvd)',52),('OFF(CPSSoc,rcvbuf.size)',60),('OFF(CPSSoc,rcvbuf.data)',64),('OFF(CPSSoc,rcvbufp)',68),('sizeof(ResetView)',168),('OFF(ResetView,reset)',68),('OFF(ResetView,reset.local_port)',78),('OFF(ResetView,reset.remote_port)',92),('OFF(ResetView,reset.remote_ip)',96)]


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
  0x208ca9c:('soc->state!=10','soc->state!=9'),
  0x208cbc4:('NULL,0,soc,flag,urgent','NULL,0,soc,flag,0'),
  0x208cc24:('R.reset.local_port=CPS_GETUSHORT2(tcphdr+2);','R.reset.local_port=CPS_GETUSHORT2(tcphdr);'),
  0x208ccec:('soc->state=3;','soc->state=2;'),
  0x208cd80:('soc->seqno--;','soc->seqno++;'),
  0x208cdd0:('if(native_fn_0208cd80','if(!native_fn_0208cd80'),
  0x208ce58:('soc->state=4;','soc->state=3;'),
  0x208cef0:('if(len==0)break;','if(len!=0)break;')
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
