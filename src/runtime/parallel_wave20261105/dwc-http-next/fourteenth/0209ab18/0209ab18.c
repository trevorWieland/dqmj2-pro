#include "context.h"
void native_main_0209ab18 (DWCInetControl * inetCntl, u16 dmaNo, u16 powerMode, u16 ssl_priority)
{
#ifdef SDK_FINALROM
#pragma unused(powerMode)
#endif
    SDK_ASSERT(powerMode == DWC_CONNECTINET_POWERMODE_ACTIVE);
    if (stpInetCntl == NULL) {
        DWC_Printf(DWC_REPORTFLAG_CONNECTINET, "InitInet dma : %d, powerMode: %d\n", dmaNo, powerMode);
        SDK_ASSERT(inetCntl);
        MI_CpuClear8(inetCntl, sizeof(DWCInetControl));
        inetCntl->dmaNo = dmaNo;
        inetCntl->powerMode = DWC_CONNECTINET_POWERMODE_ACTIVE;
        inetCntl->state = DWC_CONNECTINET_STATE_IDLE;
        inetCntl->online = FALSE;
        inetCntl->wontExecuteWDS = FALSE;
        inetCntl->processWDSstate = DWC_WDS_STATE_IDLE;
#ifndef SDK_FINALROM
        inetCntl->connectType = 0;
#endif
        stpInetCntl = inetCntl;
#if SDK_WIFI_VERSION_DATE >= 20051005
        native_fn_02090b60(ssl_priority);
#else
        (void)ssl_priority;
#endif
    }
}
