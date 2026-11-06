import os,shutil,subprocess
from project import ROOT,sha256
from wave20261106_wcm_manager_next_second_build import build
from wave20261106_wcm_manager_next_second_fixtures import run
from wave20261106_wcm_manager_next_second_models import cases

LAYOUT=[('sizeof(WCMWork)',0x2300),('sizeof(OSAlarm)',44),('sizeof(WCMConfig)',16),('sizeof(WCMApListHeader)',12),('sizeof(WCMNotice)',16),('OFF(WCMWork,phase)',0x2260),('OFF(WCMWork,option)',0x2264),('OFF(WCMWork,maxScanTime)',0x2268),('OFF(WCMWork,apListLock)',0x226a),('OFF(WCMWork,resetting)',0x226b),('OFF(WCMWork,config)',0x226c),('OFF(WCMWork,notify)',0x227c),('OFF(WCMWork,notifyId)',0x2280),('OFF(WCMWork,authId)',0x2282),('OFF(WCMWork,scanCount)',0x2284),('OFF(WCMWork,keepAliveAlarm)',0x22cc),('OFF(WCMWork,wlStatusOnConnectFail)',0x22f8),('OFF(WCMNotice,result)',2),('OFF(WCMNotice,parameter)',4),('sizeof(WMStatusPrefix)',2),('sizeof(WMCallback)',8),('sizeof(WMIndCallback)',8),('OFF(WMStatusPrefix,state)',0),('OFF(WMCallback,errcode)',2),('OFF(WMIndCallback,errcode)',2),('OFF(WMIndCallback,state)',4),('OFF(WMIndCallback,reason)',6),('OFF(WCMWork,wmWork)',0)]


def layouts(row,directory,wrong=False):
 directory.mkdir(parents=True,exist_ok=True)
 for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
 text='#include "context.h"\n#define OFF(T,m) ((unsigned long)&(((T*)0)->m))\n'
 text+='\n'.join('typedef char check_%d[(%s)==%d?1:-1];'%(i,e,n+(1 if wrong and i==5 else 0))for i,(e,n)in enumerate(LAYOUT))+'\n';source=directory/'layout.c';source.write_text(text);obj=directory/'layout.o';cmd=[str(ROOT/row['compilerPath']),*row['compilerFlags'],'-c',str(source),'-o',str(obj)]
 result=subprocess.run(cmd,cwd=ROOT,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=60)
 if (result.returncode==0)==wrong:raise ValueError(('Pinned WCM layout result differs',wrong,result.stdout,result.stderr))
 return dict(checks=len(LAYOUT),allPassed=not wrong,rejected=wrong,sourceSha256=sha256(source),compilerSha256=row['compilerSha256'],flags=row['compilerFlags'],stdout=result.stdout,stderr=result.stderr,opaqueWorkAndScanAlarmInternalsUnqualified=True)


def mutation(address):
 return {0x2089ba0:('WCM_NOTIFY_STARTUP','WCM_NOTIFY_CLEANUP'),0x2089cf4:('WCM_NOTIFY_CLEANUP','WCM_NOTIFY_STARTUP'),0x208a060:('WCM_NOTIFY_DISCONNECT','WCM_NOTIFY_CONNECT'),0x208a114:('wmResult == WM_ERRCODE_SUCCESS','wmResult != WM_ERRCODE_SUCCESS'),0x208a6d8:('WM_APIID_AUTO_DISCONNECT','(WM_APIID_AUTO_DISCONNECT+1)'),0x208ab0c:('WCM_RESULT_SUCCESS','WCM_RESULT_FAILURE')}[address]



def wrong_source(row,directory):
 directory.mkdir(parents=True,exist_ok=True);source=ROOT/row['source'];text=source.read_text();a=int(row['address'],0);before,after=mutation(a);count=text.count(before)
 if count!=(2 if a==0x208a060 else 1):raise ValueError(('WCM semantic mutation occurrence differs',hex(a),before,count))
 for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
 wrong=directory/source.name;wrong.write_text(text.replace(before,after));bad,body=build(wrong,directory/'build',negative=True);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();violations=[]
 for seed,v in enumerate(cases(a)):
  record=run(image,row,body,v,seed)
  if not record['modelPassed']:
   violations.append(dict(vector=v,seed=seed,actualReturningModelViolation=record))
   if len(violations)==2:break
 if not violations:raise ValueError(('Meaningfully changed WCM C passed model',hex(a)))
 return [dict(address=row['address'],sourceSha256=sha256(wrong),objectSha256=bad['objectSha256'],genuineLink=bad['realLink'],compiledBytes=bad['compiledBytes'],rejectedByCompleteNativeComparison=True,actualReturningModelRejections=len(violations),witnesses=violations,sourceOrExecutionCredit=0)]
