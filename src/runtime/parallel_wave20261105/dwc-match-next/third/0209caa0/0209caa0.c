#include "context.h"
void native_main_0209caa0(GPConnection * pconnection, GPGetInfoResponseArg * arg, void * param)
{
#pragma unused(param)

    if (arg->result == GP_NO_ERROR) {
        if (stpLoginCnt->state == DWC_LOGIN_STATE_GPGETINFO) {
            if (arg->lastname[0] == 0) {
                GPResult gpResult;
                char pseudo_name[DWC_ACC_USERNAME_STRING_BUFSIZE];

                DWC_Printf(DWC_REPORTFLAG_LOGIN, "    login id is authenticated. set lastname field.\n");
                DWCi_Acc_LoginIdToUserName(&stpLoginCnt->userdata->pseudo, stpLoginCnt->gamecode, pseudo_name);
                gpResult = gpSetInfos(pconnection, GP_LASTNAME, pseudo_name);
                if (DWCi_HandleGPError(gpResult)) return;

                stpLoginCnt->state = DWC_LOGIN_STATE_GPSETINFO;
                gpResult = gpGetInfo(pconnection, arg->profile, GP_DONT_CHECK_CACHE, GP_NON_BLOCKING, (GPCallback)DWCi_GPGetInfoCallback, NULL);
                if (DWCi_HandleGPError(gpResult)) return;

                DWC_Printf(DWC_REPORTFLAG_LOGIN, "    call gpSetInfos\n");
            } else {
                DWC_Printf(DWC_REPORTFLAG_LOGIN, "    this login id is used by anybody.... retry.\n");
                gpDisconnect(pconnection);
                DWCi_RemoteLogin(DWCi_RemoteAuthCallback, NULL);
                stpLoginCnt->state = DWC_LOGIN_STATE_REMOTE_AUTH;
            }
        } else if (stpLoginCnt->state == DWC_LOGIN_STATE_GPSETINFO)   {
            char pseudo_name[DWC_ACC_USERNAME_STRING_BUFSIZE];
            DWCi_Acc_LoginIdToUserName(&stpLoginCnt->userdata->pseudo, stpLoginCnt->gamecode, pseudo_name);

            if (strcmp(arg->lastname, pseudo_name) == 0) {
                char username[DWC_ACC_USERNAME_STRING_BUFSIZE];
                DWCi_Acc_LoginIdToUserName(&stpLoginCnt->tempLoginId, stpLoginCnt->gamecode, username);
                DWC_Printf(DWC_REPORTFLAG_LOGIN, "    Account is created : %s(%s) - %d.\n", username, pseudo_name, arg->profile);
                DWCi_Acc_SetLoginIdToUserData(stpLoginCnt->userdata, &stpLoginCnt->tempLoginId, arg->profile);
                stpLoginCnt->state = DWC_LOGIN_STATE_CONNECTING;
                native_fn_0209c6e4(pconnection, &stpLoginCnt->gpconnectresponsearg, NULL);
            } else {
                GPResult gpResult;
                DWC_Printf(DWC_REPORTFLAG_LOGIN, "    Login but gpSetInfo failed... %s : %d retry gpGetInfo.\n", arg->lastname, arg->profile);

                gpResult = gpGetInfo(pconnection, arg->profile, GP_DONT_CHECK_CACHE, GP_NON_BLOCKING, (GPCallback)DWCi_GPGetInfoCallback, NULL);
                if (DWCi_HandleGPError(gpResult)) return;
            }
        }
    } else {
        DWC_Printf(DWC_REPORTFLAG_LOGIN, " ERROR: gpGetInfo. why? : %d\n", arg->result);
    }
}