#include "context.h"
u32 native_main_02094d9c(ACWORK*wk)
{
 WMBssDesc*desc=&wk->bssDesc[wk->connectNo];
 wk->connectApType=GetConnectType(wk);
 MI_CpuClear8(&wk->wepKey,82);
 if(GetWepKey(wk,wk->connectApType,&wk->wepKey)!=FALSE){
  wk->authMode=1;
  if(((desc->capaInfo>>4)&1)==0){wk->findList[wk->connectNo].state=3;return 9;}
  if(wk->connectApType==6&&desc->ssid[9]==0){wk->findList[wk->connectNo].state=3;return 9;}
 }else{
  wk->authMode=0;
  if(((desc->capaInfo>>4)&1)==1){wk->findList[wk->connectNo].state=3;return 9;}
 }
 wk->count=0;
 wk->connectResult=0;
 return 8;
}
