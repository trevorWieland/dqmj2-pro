#include "context.h"
BOOL native_main_0209b940(const char * playerName,
                             DWCUpdateServersCallback updateCallback,
                             void * updateParam,
                             DWCFriendStatusCallback statusCallback,
                             void * statusParam,
                             DWCDeleteFriendListCallback deleteCallback,
                             void * deleteParam)
{
#pragma unused(playerName)

    SDK_ASSERT(stpDwcCnt);
    SDK_ASSERT(updateCallback);

    DWC_Printf(DWC_REPORTFLAG_DEBUG, "!!DWC_UpdateServersAsync() was called!!\n");

    if (DWCi_IsError() ||
        (stpDwcCnt->state < DWC_STATE_ONLINE) || (stpDwcCnt->state == DWC_STATE_UPDATE_SERVERS)) {

        DWC_Printf(DWC_REPORTFLAG_DEBUG, "But ignored.\n");
        return FALSE;
    }

    stpDwcCnt->updateServersCallback = updateCallback;
    stpDwcCnt->updateServersParam = updateParam;

    DWCi_SetState(DWC_STATE_UPDATE_SERVERS);
    DWCi_UpdateServersAsync(stpDwcCnt->logcnt.authToken,
                            stpDwcCnt->logcnt.partnerChallenge,
                            DWCi_UpdateServersCallback, NULL,
                            statusCallback, statusParam,
                            deleteCallback, deleteParam);

    return TRUE;
}