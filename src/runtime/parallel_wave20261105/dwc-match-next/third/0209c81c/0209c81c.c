#include "context.h"
void native_main_0209c81c(DWCRemoteAuthCallback callback, void * param)
{
    DWCAuthParam auth;
    void * http;

    DWC_Printf(DWC_REPORTFLAG_LOGIN, "Start Remote Auth\n");
    MI_CpuClear8(&auth, sizeof(auth));

    stRemoteAuthCallback = callback;
    pStRemoteAuthParam = param;

    if (DWCi_Acc_IsAuthentic(stpLoginCnt->userdata)) {
        DWC_Printf(DWC_REPORTFLAG_LOGIN, "  Hmm.. you already have authentic login id.\n");

        DWCi_Acc_LoginIdToUserName(&stpLoginCnt->userdata->authentic, stpLoginCnt->userdata->gamecode, stpLoginCnt->username);
    } else {
        DWC_Printf(DWC_REPORTFLAG_LOGIN, "  Hmm.. you need to create authentic login id.\n");

        if (!DWCi_Acc_IsValidLoginId(&stpLoginCnt->tempLoginId)) {
            DWC_Printf(DWC_REPORTFLAG_LOGIN, "    Hmm.. you are the first time to get authentic login id.");

            if (DWCi_Acc_CheckConsoleUserId(&stpLoginCnt->userdata->pseudo)) {
                DWC_Printf(DWC_REPORTFLAG_LOGIN, "- copy temp loginid from pseudo login id\n");
                stpLoginCnt->tempLoginId = stpLoginCnt->userdata->pseudo;
            } else {
                DWC_Printf(DWC_REPORTFLAG_LOGIN, "- create temp loginid from console user id\n");
                DWCi_Acc_CreateTempLoginId(&stpLoginCnt->tempLoginId);
            }
        } else {
            MATHRandContext32 randcontext;

            DWC_Printf(DWC_REPORTFLAG_LOGIN, "    Hmm.. you are NOT the first times to get authentic login id.\n");

            MATH_InitRand32(&randcontext, OS_GetTick());
            DWCi_Acc_SetPlayerId(&stpLoginCnt->tempLoginId, MATH_Rand32(&randcontext, 0));
        }

        DWCi_Acc_LoginIdToUserName(&stpLoginCnt->tempLoginId, stpLoginCnt->gamecode, stpLoginCnt->username);
    }

    MI_CpuCopy8(stpLoginCnt->playerName, auth.ingamesn, DWCi_WStrLen(stpLoginCnt->playerName) * 2 + 2);

    DWC_Printf(DWC_REPORTFLAG_LOGIN, "  ingamesn : %s\n", auth.ingamesn);
    strcpy(auth.gsbrcd, &(stpLoginCnt->username[DWC_ACC_USERNAME_GSBRCD_OFFSET]));
    DWC_Printf(DWC_REPORTFLAG_LOGIN, "  gsbrcd   : %s.\n", auth.gsbrcd);

    auth.alloc = (DWCAuthAlloc)DWC_Alloc;
    auth.free = (DWCAuthFree)DWC_Free;

    http = DWC_AllocEx(DWC_ALLOCTYPE_AUTH, sizeof(DWCHttp), 4);
    SDK_ASSERTMSG(http, "DWC_LOGIN: can't alloc memory %s :%d\n", __FILE__, __LINE__);

    stpLoginCnt->http = http;
    stpLoginCnt->startTick = OS_GetTick();

    DWC_Auth_Create(&auth, http);
}