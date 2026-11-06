#include "context.h"
void native_main_0209c55c(void)
{
    if (!stpLoginCnt || DWCi_IsError()) return;

    switch (stpLoginCnt->state) {
    case DWC_LOGIN_STATE_REMOTE_AUTH:
        DWCi_RemoteLoginProcess();
        break;
    case DWC_LOGIN_STATE_CONNECTING:
    case DWC_LOGIN_STATE_GPGETINFO:
    case DWC_LOGIN_STATE_GPSETINFO:
        if (stpLoginCnt->pGpObj && *stpLoginCnt->pGpObj) {
            gpProcess(stpLoginCnt->pGpObj);
        }
        if (stpLoginCnt->connectFlag &&
            (OS_TicksToMilliSeconds(OS_GetTick() - stpLoginCnt->connectTick) > DWC_LOGIN_GPCONNECT_TIMEOUT)) {

            DWCi_StopLogin(DWC_ERROR_NETWORK, DWC_ECODE_SEQ_LOGIN + DWC_ECODE_GS_GP + DWC_ECODE_TYPE_TIMEOUT);
            stpLoginCnt->connectFlag = FALSE;
        }
        break;

    case DWC_LOGIN_STATE_INIT:
    case DWC_LOGIN_STATE_CONNECTED:
    default:
        DWC_Printf(DWC_REPORTFLAG_DEBUG, "Ignore invalid login state.\n");
        break;
    }
}