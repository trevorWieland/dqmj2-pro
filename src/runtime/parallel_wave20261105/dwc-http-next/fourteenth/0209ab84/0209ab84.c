#include "context.h"
void native_main_0209ab84 (void)
{
    DWCACConfig inp;
    if (stpInetCntl != NULL) {
        if (stpInetCntl->state != DWC_CONNECTINET_STATE_IDLE) {
            return;
        }
        MI_CpuClear8(&inp, sizeof(DWCACConfig));
        inp.dmaNo = (u8)stpInetCntl->dmaNo;
        inp.powerMode = (u8)stpInetCntl->powerMode;
        inp.alloc = (DWCACAlloc)native_fn_0209aa38;
        inp.free = (DWCACFree) native_fn_0209aa64;
#ifndef SDK_FINALROM
        inp.option.connectType = (u8)stpInetCntl->connectType;
#endif
        DWC_Printf(DWC_REPORTFLAG_CONNECTINET, "ConnectInet Async\n");
        stpInetCntl->state = DWC_CONNECTINET_STATE_OPERATING;
        if (!native_fn_02094284(&inp)) {
            native_fn_0209a9f8(DWC_ERROR_FATAL, -50199);
        }
    } else {
        native_fn_0209a9f8(DWC_ERROR_FATAL, -50199);
    }
}
