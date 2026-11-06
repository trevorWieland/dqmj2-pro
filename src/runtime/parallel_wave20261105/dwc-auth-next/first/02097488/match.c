#include "context.h"
DWCAuthError native_main_02097488(DWCAuthParam*param,void*http)
{
    DWCAuth*temp;
    DWCAuthAlloc alloc=param->alloc;
    if(DWCauth!=NULL)
        return DWCAUTH_E_MEMERR;
    temp=alloc((unsigned long)native_data_020deb70,sizeof(DWCAuth));
    DWCauth=temp;
    if(temp==NULL)
        return DWCAUTH_E_MEMERR;
    MI_CpuFill8(DWCauth,0,sizeof(DWCAuth));
    DWCauth->http=(DWCHttp*)http;
    native_data_021d18f0.unknownReset0=0;
    MI_CpuFill8(&DWCauth->result,0,sizeof(DWCAuthResult));
    DWCauth->result.returncode=20100;
    DWCauth->param=*param;
    DWCauth->param.ingamesn[25]=0;
    DWCauth->param.gsbrcd[11]=0;
    DWCauth->error=DWCi_Auth_Start(TRUE);
    if(DWCauth->error!=DWCAUTH_E_NOERR)
        return DWCauth->error;
    native_data_021d18f0.unknownReset4=0;
    DWCi_Auth_StartThread();
    return DWCAUTH_E_NOERR;
}
