#include "context.h"
void native_main_020947b4(u8 type)
{
 u8 selected;
 const u8*ssid;
 int i;
 if(acHold->overrideType==0)selected=native_fn_02094818(type);else selected=acHold->overrideType;
 acHold->type=selected;
 ssid=native_fn_0208b524(NULL);
 if(ssid!=NULL){native_fn_020072d0(ssid,32);native_fn_02096174((const char*)ssid,(u8*)acHold->apSpotInfo);}
 for(i=0;i<10;i++){
  if(acHold->apSpotInfo[i]<32||acHold->apSpotInfo[i]>126){native_fn_02008d78(acHold->apSpotInfo,0,10);return;}
 }
}
