#include "context.h"
int native_main_0209bb30(void)
{
    DWC_Printf(DWC_REPORTFLAG_DEBUG, "!!DWC_CloseAllConnectionsHard() was called!!\n");

    if (!stpDwcCnt || DWCi_IsError() ||
        ((stpDwcCnt->state != DWC_STATE_MATCHING) && (stpDwcCnt->state != DWC_STATE_CONNECTED))) {

        DWC_Printf(DWC_REPORTFLAG_DEBUG, "But ignored.\n");
        return -1;
    }

    if (!stpDwcCnt->matchcnt.gt2NumConnection) {
        DWC_Printf(DWC_REPORTFLAG_TRANSPORT, "Closed 0 connection.\n");
        (void)DWCi_SetGPStatus(DWC_STATUS_ONLINE, native_data_020e016c, NULL);
        DWCi_NNFreeNegotiateList();
        DWCi_SetState(DWC_STATE_ONLINE);
        return 1;
    }

    stpDwcCnt->ownCloseFlag = TRUE;
    gt2CloseAllConnectionsHard(stpDwcCnt->gt2Socket);
    stpDwcCnt->ownCloseFlag = FALSE;

    return 0;
}