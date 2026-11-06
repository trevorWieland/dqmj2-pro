import os,shutil,subprocess
from project import ROOT,sha256
from wave20261106_wcm_manager_next_sixth_build import build
from wave20261106_wcm_manager_next_sixth_fixtures import run
from wave20261106_wcm_manager_next_sixth_models import cases

LAYOUT=[('sizeof(WCMWork)',0x2300),('sizeof(OSAlarm)',44),('sizeof(WCMConfig)',16),('sizeof(WCMApListHeader)',12),('sizeof(WCMNotice)',16),('OFF(WCMWork,phase)',0x2260),('OFF(WCMWork,option)',0x2264),('OFF(WCMWork,maxScanTime)',0x2268),('OFF(WCMWork,apListLock)',0x226a),('OFF(WCMWork,resetting)',0x226b),('OFF(WCMWork,config)',0x226c),('OFF(WCMWork,notify)',0x227c),('OFF(WCMWork,notifyId)',0x2280),('OFF(WCMWork,authId)',0x2282),('OFF(WCMWork,scanCount)',0x2284),('OFF(WCMWork,keepAliveAlarm)',0x22cc),('OFF(WCMWork,wlStatusOnConnectFail)',0x22f8),('OFF(WCMNotice,result)',2),('OFF(WCMNotice,parameter)',4),('sizeof(WMStatusPrefix)',2),('sizeof(WMCallback)',8),('sizeof(WMIndCallback)',8),('OFF(WMStatusPrefix,state)',0),('OFF(WMCallback,errcode)',2),('OFF(WMIndCallback,errcode)',2),('OFF(WMIndCallback,state)',4),('OFF(WMIndCallback,reason)',6),('OFF(WCMWork,wmWork)',0),('sizeof(WMBssDesc)',192),('OFF(WMBssDesc,rateSet.support)',48),('OFF(WCMWork,bssDesc)',0x2140),('OFF(WCMWork,wepDesc)',0x2200),('OFF(WCMWork,wepDesc.mode)',0x2250),('OFF(WCMWork,wepDesc.keyId)',0x2251),('sizeof(WMScanExParam)',68),('OFF(WMScanExParam,scanBuf)',0),('OFF(WMScanExParam,scanBufSize)',4),('OFF(WMScanExParam,ssidMatchLength)',52),('sizeof(WMDcfRecvBuf)',48),('OFF(WMDcfRecvBuf,rate_rssi)',14),('OFF(WMDcfRecvBuf,data)',44),('sizeof(WMStartDCFCallback)',12),('OFF(WMStartDCFCallback,recvBuf)',8),('sizeof(WCMWepDesc)',82),('OFF(WCMWepDesc,key)',2),('sizeof(WCMApList)',208),('OFF(WCMApList,linkLevel)',2),('OFF(WCMApList,data)',16),('sizeof(WMStartScanExCallback)',112),('OFF(WMStartScanExCallback,state)',8),('OFF(WMStartScanExCallback,channelList)',10),('OFF(WMStartScanExCallback,bssDescCount)',14),('OFF(WMStartScanExCallback,bssDesc)',16),('OFF(WMStartScanExCallback,linkLevel)',80),('OFF(WCMWork,sendBuf)',0xf00),('OFF(WCMWork,recvBuf)',0x1500),('OFF(WMBssDesc,gameInfoLength)',60),('sizeof(WMStartConnectCallback)',26),('OFF(WMStartConnectCallback,state)',8),('OFF(WMStartConnectCallback,aid)',10),('OFF(WMStartConnectCallback,wlStatus)',14),('sizeof(OSThreadQueue)',8),('sizeof(OSMutex)',24),('OFF(OSMutex,thread)',8),('OFF(OSMutex,count)',12),('sizeof(WCMCpsifWork)',44),('OFF(WCMCpsifWork,sendQ)',4),('OFF(WCMCpsifWork,sendMutex)',12),('OFF(WCMCpsifWork,sendResult)',36),('OFF(WCMCpsifWork,recvCallback)',40)]


def layouts(row,directory,wrong=False):
 directory.mkdir(parents=True,exist_ok=True)
 for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
 text='#include "context.h"\n#define OFF(T,m) ((unsigned long)&(((T*)0)->m))\n'
 text+='\n'.join('typedef char check_%d[(%s)==%d?1:-1];'%(i,e,n+(1 if wrong and i==5 else 0))for i,(e,n)in enumerate(LAYOUT))+'\n';source=directory/'layout.c';source.write_text(text);obj=directory/'layout.o';cmd=[str(ROOT/row['compilerPath']),*row['compilerFlags'],'-c',str(source),'-o',str(obj)]
 result=subprocess.run(cmd,cwd=ROOT,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=60)
 if (result.returncode==0)==wrong:raise ValueError(('Pinned WCM layout result differs',wrong,result.stdout,result.stderr))
 return dict(checks=len(LAYOUT),allPassed=not wrong,rejected=wrong,sourceSha256=sha256(source),compilerSha256=row['compilerSha256'],flags=row['compilerFlags'],stdout=result.stdout,stderr=result.stderr,opaqueWorkAndScanAlarmInternalsUnqualified=True)


def mutation(address):
 return {0x208b580:('return headerLen + bodyLen;','return headerLen;')}[address]



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
