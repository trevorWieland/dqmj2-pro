#include "context.h"
int native_main_0209bba0(u8 aid)
{
    GT2Connection connection;

    DWC_Printf(DWC_REPORTFLAG_DEBUG, "!!DWC_CloseConnectionHard() was called!! aid = %d.\n", aid);

    if (!stpDwcCnt || DWCi_IsError() ||
        ((stpDwcCnt->state != DWC_STATE_MATCHING) && (stpDwcCnt->state != DWC_STATE_CONNECTED))) {

        DWC_Printf(DWC_REPORTFLAG_DEBUG, "But ignored.\n");
        return -1;
    }

    if (!(connection = DWCi_GetGT2Connection(aid))) {
        DWC_Printf(DWC_REPORTFLAG_DEBUG, "No connection!\n");
        return -2;
    }

    gt2CloseConnectionHard(connection);
    return 0;
}