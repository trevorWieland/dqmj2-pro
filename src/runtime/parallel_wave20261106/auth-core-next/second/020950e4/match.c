#include "context.h"
BOOL native_main_020950e4(ACWORK*wk,int type,WCMWepDesc*wep)
{
 DWCMemPage*page=wk->userInfo;
 switch(type){
 case 0:goto normal0;
 case 1:goto normal1;
 case 2:page++;
 normal1:page++;
 normal0:wep->mode=page->ap.wepMode;MI_CpuCopy8(page->ap.wep[0],wep->key,16);break;
 case 3:goto alternate0;
 case 4:goto alternate1;
 case 5:page++;
 alternate1:page++;
 alternate0:wep->mode=1;MI_CpuCopy8(page->ap.wep2[0],wep->key,5);break;
 case 6:wep->mode=2;DWCi_AC_GetNintendoUSBWepKey((const char*)wk->bssDesc[wk->connectNo].ssid,wep->key);break;
 case 7:wep->mode=2;DWCi_AC_GetNintendoShopWepKey((const char*)wk->bssDesc[wk->connectNo].ssid,wep->key);break;
 case 8:break;
 case 9:break;
 }
 return wep->mode!=0;
}
