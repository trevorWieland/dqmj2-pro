#include "context.h"
u32 native_main_02094e68(ACWORK*wk)
{
 int phase=WCM_GetPhase();
 WMBssDesc*desc=&wk->bssDesc[wk->connectNo];
 if(phase==3){
  u32 power=GetPowerMode(wk),auth;
  wk->count++;
  if(wk->count>3){wk->count=0;wk->findList[wk->connectNo].state=1;return 9;}
  if(wk->count!=1){
   if(wk->connectResult==1)wk->authMode=0;
   else{
    if(wk->connectResult==2){wk->count=0;wk->findList[wk->connectNo].state=3;return 9;}
    if(wk->connectResult==3){wk->count=0;wk->findList[wk->connectNo].state=4;return 9;}
    if(wk->count==3)wk->authMode=0;
   }
  }
  auth=GetAuthMode(wk);
  WCM_ConnectAsync(desc,&wk->wepKey,power|auth);
 }else if(phase==9){wk->count=0;wk->timeOut=OS_GetTick();return 10;}
 return 8;
}
