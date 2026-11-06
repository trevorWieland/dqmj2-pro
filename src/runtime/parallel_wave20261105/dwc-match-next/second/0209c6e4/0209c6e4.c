#include "context.h"
void native_main_0209c6e4(GPConnection * pconnection, GPConnectResponseArg * arg, void * param)
{
#pragma unused(param)
    GPResult gpResult;

    DWC_Printf(DWC_REPORTFLAG_LOGIN, "Finished connecting to GP server, result = %d\n", arg->result);

    stpLoginCnt->connectFlag = FALSE;

    if (arg->result == GP_NO_ERROR) {
        stpLoginCnt->gpconnectresponsearg = *arg;
        if (stpLoginCnt->state == DWC_LOGIN_STATE_CONNECTING) {
            if (stpLoginCnt->userdata->gs_profile_id == arg->profile) {
                DWC_Printf(DWC_REPORTFLAG_LOGIN, "  gs profile id is valid.\n");

                stpLoginCnt->state = DWC_LOGIN_STATE_CONNECTED;
                gpResult = DWCi_SetGPStatus(DWC_STATUS_ONLINE, native_data_020e017c, NULL);

                if (DWCi_HandleGPError(gpResult)) return;

                stpLoginCnt->callback(DWC_ERROR_NONE, arg->profile, stpLoginCnt->param);

                if (!DWCi_GT2Startup()) {
                    if (DWCi_QR2Startup(arg->profile)) return;
                } else return;

            } else {
                DWC_Printf(DWC_REPORTFLAG_LOGIN, "  gs profile id is invalid.\n");
                DWCi_StopLogin(DWC_ERROR_NETWORK, DWC_ECODE_SEQ_LOGIN);
            }
        } else if (stpLoginCnt->state == DWC_LOGIN_STATE_GPGETINFO)   {
            gpResult = gpGetInfo(pconnection, arg->profile, GP_DONT_CHECK_CACHE, GP_NON_BLOCKING, (GPCallback)DWCi_GPGetInfoCallback, NULL);
            if (DWCi_HandleGPError(gpResult)) return;
        }
    } else {
        (void)DWCi_HandleGPError(arg->result);
    }
}