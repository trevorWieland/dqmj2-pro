#include "context.h"
void native_main_020948d0(WMBssDesc*desc)
{
 ACWORK*wk;
 tagACHOLD*hold;
 int found=-1,pos;
 u8 channel;
 u8 phase;
 wk=DWCi_AC_GetMemPtr(16);
 hold=DWCi_AC_GetMemPtr(1);
 hold->findAP=1;
 phase=DWCi_AC_GetPhase();
 switch(phase){
 case 3:
  channel=wk->searchChannel;
  if(desc->ssidLength==0||desc->ssid[0]==0)DWCi_AC_SetStealthChannel(desc->channel);
  else if(desc->ssidLength==1&&desc->ssid[0]==' '){DWCi_AC_SetStealthChannel(desc->channel);found=CompareList(desc,wk->searchListNum,wk->searchList);}
  else found=CompareList(desc,wk->searchListNum,wk->searchList);
  break;
 case 4:
  channel=(wk->bssDesc[wk->searchListNo].channel-1)&255;
  found=CompareListDiff(desc,wk);
  if(found>=0)wk->findList[wk->searchListNo].find=1;
  break;
 case 5:
  channel=(u8)wk->searchChannel;
  found=CompareList(desc,1,&wk->searchList[wk->searchListNo]);
  if(found>=0)wk->searchList[wk->searchListNo].find=1;
  break;
 default:return;
 }
 if(found>=0){pos=AddList(found,desc,(u8)channel,wk);SortList(pos,wk);}
}
