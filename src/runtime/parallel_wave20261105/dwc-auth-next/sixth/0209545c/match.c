#include "context.h"
#include "string.h"
u8 native_main_0209545c(WMBssDesc*desc)
{
 tagACWORK*work=DWCi_AC_GetMemPtr(16);
 if((work->connectType==0||work->connectType==6)&&strncmp((const char*)desc->ssid,(const char*)FREESPOT_SSID,8)==0)return 8;
 return 0;
}
