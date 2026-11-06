#include "context.h"
void native_main_0209c940(void)
{
    if (DWC_Auth_GetError() == DWCAUTH_E_FINISH) {
        DWCAuthResult result;
        DWC_Printf(DWC_REPORTFLAG_LOGIN, " *** Auth Done\n");
        DWC_Auth_GetResult(&result);

        strcpy(stpLoginCnt->authToken, result.token);
        strcpy(stpLoginCnt->partnerChallenge, result.challenge);

        DWC_Auth_Destroy();

        DWC_Free(DWC_ALLOCTYPE_AUTH, stpLoginCnt->http, 0);
        stpLoginCnt->http = NULL;

        if (DWCi_Acc_IsAuthentic(stpLoginCnt->userdata)) {
            stRemoteAuthCallback(stpLoginCnt->authToken, stpLoginCnt->partnerChallenge, pStRemoteAuthParam);
        } else {

            DWCi_GPConnect(stpLoginCnt->authToken, stpLoginCnt->partnerChallenge, (GPCallback)DWCi_GPConnectCallback, DWC_LOGIN_STATE_GPGETINFO);
        }
    } else if (DWC_Auth_GetError() != DWCAUTH_E_NOERR)   {
        OSTick nowTick;

        DWC_Printf(DWC_REPORTFLAG_LOGIN, " *** Auth Error\n");
        nowTick = OS_GetTick();
        if (OS_TicksToMilliSeconds(nowTick - stpLoginCnt->startTick) > DWC_LOGIN_AUTH_TIMEOUT) {
            DWCAuthResult result;
            DWC_Auth_GetResult(&result);

            DWC_Auth_Destroy();
            DWC_Free(DWC_ALLOCTYPE_AUTH, stpLoginCnt->http, 0);
            stpLoginCnt->http = NULL;

            DWCi_StopLogin(DWC_ERROR_AUTH_ANY, result.returncode);

            return;

        } else {
            DWCAuthParam auth;

            DWC_Printf(DWC_REPORTFLAG_LOGIN, "  **** AUTH FAILED ... retry AUTH_ERROR:%d.\n", DWC_Auth_GetError());
            DWC_Auth_Destroy();

            MI_CpuClear8(&auth, sizeof(auth));
            MI_CpuCopy8(stpLoginCnt->playerName, auth.ingamesn, DWCi_WStrLen(stpLoginCnt->playerName) * 2 + 2);

            DWC_Printf(DWC_REPORTFLAG_LOGIN, "  ingamesn : %s\n", auth.ingamesn);
            strcpy(auth.gsbrcd, &(stpLoginCnt->username[DWC_ACC_USERNAME_GSBRCD_OFFSET]));

            auth.alloc = (DWCAuthAlloc)DWC_Alloc;
            auth.free = (DWCAuthFree)native_fn_0209aa65;

            DWC_Printf(DWC_REPORTFLAG_LOGIN, "  gsbrcd   : %s.\n", auth.gsbrcd);
            DWC_Auth_Create(&auth, stpLoginCnt->http);
        }
    }
}