#include "context000.h"

#include "context001.h"

static void WmspPxiCallback(PXIFifoTag tag, u32 data, BOOL err)
{
    BOOL result;
    if (err) {
        return;
    }
    ((void)0) ;
    result = OS_SendMessage(&(wmspW.requestQ), (OSMessage)data, 0 );
    if (!result) {
        if (wmspW.wm7buf != ((void *)0) ) {
            WMCallback *cb = (WMCallback *)WMSP_GetBuffer4Callback2Wm9();
            cb->apiid = *((u16 *)data);
            cb->errcode = WM_ERRCODE_FIFO_ERROR;
            cb->wlCmdID = 0;
            cb->wlResult = 0;
            WMSP_ReturnResult2Wm9((void *)cb);
        }
    }
}
