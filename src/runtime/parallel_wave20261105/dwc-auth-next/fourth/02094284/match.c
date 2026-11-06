#include "context.h"
BOOL native_main_02094284(DWCACConfig*config)
{
 tagACHOLD*hold;
 tagACWORK*work;
 DWCNetcheckParam*check;
 int result;
 acHold=config->alloc(1,sizeof(tagACHOLD));
 MI_CpuClear32(acHold,36);
 hold=acHold;
 acHold->alloc=config->alloc;
 hold->free=config->free;
 hold->phase=1;
 hold->endSequence=1;
 hold->allocState=1;
 acWork=DWCi_AC_Alloc(16,sizeof(tagACWORK));
 wcmBuffer=DWCi_AC_Alloc(2,0x2300);
 socConfig=DWCi_AC_Alloc(4,sizeof(SOCConfig));
 netCheck=DWCi_AC_Alloc(8,sizeof(DWCNetcheckParam));
 MI_CpuClear32(acWork,3352);
 MI_CpuClear32(wcmBuffer,0x2300);
 MI_CpuClear32(socConfig,88);
 MI_CpuClear32(netCheck,12);
 work=acWork;
 acWork->dmaNo=config->dmaNo;
 work->powerMode=config->powerMode;
 check=netCheck;
 netCheck->alloc=config->alloc;
 check->free=config->free;
 check->bmworkarea=NULL;
 work->connectType=config->option.connectType;
 work->skipNetCheck=config->option.skipNetCheck;
 native_fn_020a4640(work->userInfo);
 result=native_fn_02089aa4(wcmBuffer,0x2300);
 if(result==1||result>4){DWCi_AC_FreeAll();return FALSE;}
 return TRUE;
}
