#include "context.h"
#include "string.h"
DWCAuthError native_main_02097ab0(void)
{
 char *end = NULL;
 int code;
 long result;
 size_t length;
 end = DWC_Http_GetResult(DWCauth->http,native_data_020debcc);
 if(end != NULL) DWC_Auth_SetNasTimeDiff(end);
 errno=0;
 end=NULL;
 code=atoi(DWC_Http_GetResult(DWCauth->http,native_data_020debd4));
 if(errno==34){DWCauth->result.returncode=20101;return 12;}
 if(code!=200){DWCauth->result.returncode=code+23000;return 18;}
 if(DWC_Http_GetBase64DecodedResult(DWCauth->http,native_data_020debe0,DWCauth->result.retcode,4)<=0){DWCauth->result.returncode=20101;return 14;}
 result=strtol(DWCauth->result.retcode,&end,10);
 length=strlen(DWCauth->result.retcode);
 if(end!=DWCauth->result.retcode+length){DWCauth->result.returncode=20101;return 12;}
 DWCauth->result.returncode=result+20000;
 if(result<100){
  DWCauth->result.token[0]=0;
  DWCauth->result.locator[0]=0;
  DWCauth->result.challenge[0]=0;
  DWCauth->result.datetime[0]=0;
  DWCauth->result.cookie[0]=0;
  DWC_Http_GetBase64DecodedResult(DWCauth->http,native_data_020debec,DWCauth->result.token,301);
  DWC_Http_GetBase64DecodedResult(DWCauth->http,native_data_020debf4,DWCauth->result.locator,51);
  DWC_Http_GetBase64DecodedResult(DWCauth->http,native_data_020debfc,DWCauth->result.challenge,9);
  DWC_Http_GetBase64DecodedResult(DWCauth->http,native_data_020dec08,DWCauth->result.datetime,15);
  DWC_Http_GetRawResult(DWCauth->http,native_data_020dec14,DWCauth->result.cookie,65);
  DWCauth->result.cookie[43]=0;
  if(result!=40) DWCauthingamesncheckresult=1;else DWCauthingamesncheckresult=2;
 }
 return 0;
}
