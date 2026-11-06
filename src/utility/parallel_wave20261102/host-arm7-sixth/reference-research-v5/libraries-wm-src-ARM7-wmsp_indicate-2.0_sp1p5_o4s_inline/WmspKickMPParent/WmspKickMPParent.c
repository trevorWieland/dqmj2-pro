#include "context000.h"

#include "context001.h"

static void WmspKickMPParent(u16 pollbmp)
{
    u32 *buf = WMSP_GetInternalRequestBuf();
    WMSPWork *sys = WMSP_GetSystemWork();
    int result;
    if (buf == ((void *)0) ) {
        result = 0 ;
    } else {
        buf[0] = WM_APIID_KICK_MP_PARENT;
        buf[1] = (u32)pollbmp;
        ((void)0) ;
        result = OS_SendMessage(&(sys->requestQ), (OSMessage)buf, 0 );
    }
    if (!result) {
        if (sys->wm7buf != ((void *)0) ) {
            WMIndCallback *cb = (WMIndCallback *)WMSP_GetBuffer4Callback2Wm9();
            cb->apiid = WM_APIID_INDICATION;
            cb->errcode = WM_ERRCODE_FIFO_ERROR;
            cb->state = WM_STATECODE_FIFO_ERROR;
            cb->reason = WM_APIID_KICK_MP_PARENT;
            WMSP_ReturnResult2Wm9(cb);
        }
    }
}
