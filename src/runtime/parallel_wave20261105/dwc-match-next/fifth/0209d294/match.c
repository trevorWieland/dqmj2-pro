#include "context.h"
GPResult native_main_0209d294(void)
{
    GPResult result = GP_NO_ERROR;

    if (OS_TicksToMilliSeconds(OS_GetTick() - stpFriendCnt->lastGpProcess) >= DWC_GP_PROCESS_INTERVAL) {
        stpFriendCnt->gpProcessCount++;

#if defined(DWC_ENABLE_KEEPALIVE_TO_GPSERVER)
        if ((stpFriendCnt->gpProcessCount % DWC_GP_KEEP_ALIVE_COUNT) == 0) {
            DWC_Printf(DWC_REPORTFLAG_DEBUG, "GP:keep alive\n");
            (void)gpSetInfoi(stpFriendCnt->pGpObj, GP_INTERESTS1, 0);
        }
#endif
        result = gpProcess(stpFriendCnt->pGpObj);
        stpFriendCnt->lastGpProcess = OS_GetTick();
    }

    return result;
}