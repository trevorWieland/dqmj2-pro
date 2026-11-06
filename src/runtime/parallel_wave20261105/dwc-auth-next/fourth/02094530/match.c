#include "context.h"
void native_main_02094530(const void*ssid,const void*wep,int wepMode)
{
 tagACWORK*work=DWCi_AC_GetMemPtr(16);
 int i;
 const u8*source=ssid;
 u32 size;
 work->connectType=1;
 native_fn_02008d78(work,0,240);
 for(i=0;i<32;i++){u8 value=source[i];if(value==0)break;work->userInfo[0].ap.ssid[0][i]=value;}
 if(wep==NULL||wepMode==0)work->userInfo[0].ap.wepMode=0;
 else{
  if(wepMode==1)size=5;else if(wepMode==2)size=13;else size=16;
  native_fn_02008e0c(wep,work->userInfo[0].ap.wep,size);
  work->userInfo[0].ap.wepMode=wepMode;
 }
}
