#include "context.h"
BOOL native_main_0209b898(const u16 * ingamesn,
                     const char * reserved,
                     DWCLoginCallback callback,
                     void * param)
{
#pragma unused(reserved)
    u32 len;

    SDK_ASSERT(stpDwcCnt);
    SDK_ASSERT(callback);

    DWC_Printf(DWC_REPORTFLAG_DEBUG, "!!DWC_LoginAsync() was called!!\n");

    if (ingamesn == NULL) {
        DWC_Printf(DWC_REPORTFLAG_WARNING, "ingamesn is NULL!!\n");
        return FALSE;
    }

    if (DWCi_IsError() || (stpDwcCnt->state != DWC_STATE_INIT)) {
        DWC_Printf(DWC_REPORTFLAG_DEBUG, "But ignored.\n");
        return FALSE;
    }

    stpDwcCnt->loginCallback = callback;
    stpDwcCnt->loginParam = param;

    if (!ingamesn || (ingamesn[0] == '\0')) {
        len = 0;
    } else {
        MI_CpuClear16(stpDwcCnt->playerName, DWC_MAX_PLAYER_NAME * 2);
        len = DWCi_WStrLen(ingamesn) <= DWC_MAX_PLAYER_NAME - 1 ? DWCi_WStrLen(ingamesn) : DWC_MAX_PLAYER_NAME - 1;
        MI_CpuCopy16(ingamesn, stpDwcCnt->playerName, len * 2);
    }

    stpDwcCnt->playerName[len] = 0;

    if (DWC_GetInetStatus() != DWC_CONNECTINET_STATE_CONNECTED) {
        DWCi_StopLogin(DWC_ERROR_AUTH_ANY, DWC_ECODE_SEQ_LOGIN + DWC_ECODE_TYPE_NETWORK);
        return TRUE;
    }

    DWCi_SetState(DWC_STATE_AVAILABLE_CHECK);

    GSIStartAvailableCheck(stpDwcCnt->gameName);

    return TRUE;
}