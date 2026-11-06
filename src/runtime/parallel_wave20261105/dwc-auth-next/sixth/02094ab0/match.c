#include "context.h"
#include "string.h"
u32 native_main_02094ab0(WMBssDesc*desc,tagACWORK*work)
{
 u32 found;
 int i;
 if(desc->ssidLength!=32||(found=native_fn_020949e4(desc),(int)found<=0)){
  for(i=0;i<work->findListNum;i++){
   if(desc->ssidLength==work->bssDesc[i].ssidLength&&strncmp((const char*)desc->ssid,(const char*)work->bssDesc[i].ssid,desc->ssidLength)==0)return work->findList[i].type;
  }
  found=0xffffffff;
 }
 return found;
}
