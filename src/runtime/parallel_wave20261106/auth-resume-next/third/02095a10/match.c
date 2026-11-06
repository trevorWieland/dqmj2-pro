#include "context.h"
u8 native_main_02095a10(ACWORK*wk)
{
 OSTick time=OS_GetTick();
 time=time-wk->timeOut;
 time=OS_TicksToMilliSeconds(time);
 if(time>=SEARCH_CHANNEL_TIME_OUT||wk->findList[wk->searchListNo].find==TRUE){
  wk->findList[wk->searchListNo].find=TRUE;
  for(;wk->searchListNo<wk->findListNum;wk->searchListNo++){if(wk->findList[wk->searchListNo].find==FALSE)break;}
  if(wk->findListNum<=wk->searchListNo){wk->searchListNo=0;return NextSearchCheck(wk,AC_PHASE_SEARCH_DIFFER_CHANNEL);}
  else{
   wk->timeOut=OS_GetTick();
   ScanStart(wk->bssDesc[wk->searchListNo].bssid,wk->bssDesc[wk->searchListNo].ssid,wk->bssDesc[wk->searchListNo].channel-1,WCM_OPTION_SCANTYPE_ACTIVE);
  }
 }
 return AC_PHASE_SEARCH_DIFFER_CHANNEL;
}
