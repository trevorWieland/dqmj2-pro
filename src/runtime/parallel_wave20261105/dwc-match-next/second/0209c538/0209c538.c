#include "context.h"
void native_main_0209c538(void)
{
    DWC_Printf(DWC_REPORTFLAG_LOGIN, "Login Async\n");
    DWCi_RemoteLogin(DWCi_RemoteAuthCallback, NULL);

    stpLoginCnt->state = DWC_LOGIN_STATE_REMOTE_AUTH;
    stpLoginCnt->connectFlag = FALSE;
}