#include "context.h"
#include "string.h"
#include "wchar.h"
unsigned long native_main_02097fac(DWCHttp*http,char*cal,int include_ssid)
{
 char buffer[36];
 size_t length;
 OS_SNPrintf(buffer,33,native_data_020decac,3,1);
 length=strlen(buffer);
 if(DWC_Http_Add_PostBase64Item(http,native_data_020decb8,buffer,length)!=0)return 0;
 length=strlen(cal+0);
 if(DWC_Http_Add_PostBase64Item(http,native_data_020decc0,cal+0,length)!=0)return 0;
 length=strlen(cal+14);
 if(DWC_Http_Add_PostBase64Item(http,native_data_020decc8,cal+14,length)!=0)return 0;
 length=strlen(cal+65);
 if(DWC_Http_Add_PostBase64Item(http,native_data_020decd0,cal+65,length)!=0)return 0;
 length=strlen(cal+111);
 if(DWC_Http_Add_PostBase64Item(http,native_data_020decd8,cal+111,length)!=0)return 0;
 length=strlen(cal+21);
 if(DWC_Http_Add_PostBase64Item(http,native_data_020dece0,cal+21,length)!=0)return 0;
 length=strlen(cal+26);
 if(DWC_Http_Add_PostBase64Item(http,native_data_020dece8,cal+26,length)!=0)return 0;
 length=strlen(cal+29);
 if(DWC_Http_Add_PostBase64Item(http,native_data_020decf0,cal+29,length)!=0)return 0;
 length=strlen(cal+31);
 if(DWC_Http_Add_PostBase64Item(http,native_data_020decf8,cal+31,length)!=0)return 0;
 length=strlen(cal+44);
 if(DWC_Http_Add_PostBase64Item(http,native_data_020ded00,cal+44,length)!=0)return 0;
 length=strlen(cal+47);
 if(DWC_Http_Add_PostBase64Item(http,native_data_020ded08,cal+47,length)!=0)return 0;
 length=strlen(cal+52);
 if(DWC_Http_Add_PostBase64Item(http,native_data_020ded10,cal+52,length)!=0)return 0;
 length=wcslen((wchar_t*)(cal+126));
 if(DWC_Http_Add_PostBase64Item(http,native_data_020ded18,cal+126,length<<1)!=0)return 0;
 if(include_ssid==1){
  length=strlen(cal+78);
  if(DWC_Http_Add_PostBase64Item(http,native_data_020ded20,cal+78,length)!=0)return 0;
 }
 OS_SNPrintf(buffer,33,native_data_020ded28,3,1);
 if(DWC_Http_Add_HeaderItem(http,native_data_020ded40,buffer)!=0)return 0;
 if(DWC_Http_Add_HeaderItem(http,native_data_020ded4c,cal+21)!=0)return 0;
 return 1;
}
