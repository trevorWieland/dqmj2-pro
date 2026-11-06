#include "context000.h"

#include "context001.h"

void WMSP_EndMP(OSMessage msg)
{
    WMStatus *status = WMSP_GetStatusStructure();
    u32 wlBuf[128];
    WlCmdCfm *pConfirm;
    BOOL fCleanQueue = 0 ;
    if (status->state != WM_STATE_MP_PARENT && status->state != WM_STATE_MP_CHILD) {
        WMCallback *callback = (WMCallback *)WMSP_GetBuffer4Callback2Wm9();
        callback->apiid = WM_APIID_END_MP;
        callback->errcode = WM_ERRCODE_ILLEGAL_STATE;
        WMSP_ReturnResult2Wm9(callback);
        return;
    }
    {
        OSIntrMode e = OS_DisableInterrupts();
        if (status->mp_flag == 1 ) {
            fCleanQueue = 1 ;
        }
        status->mp_flag = 0 ;
        WMSP_CancelVAlarm();
        WMSP_SetThreadPriorityLow();
        if (status->state == WM_STATE_MP_CHILD) {
            status->state = WM_STATE_CHILD;
        } else if (status->state == WM_STATE_MP_PARENT) {
            status->state = WM_STATE_PARENT;
        }
        (void)OS_RestoreInterrupts(e);
    }
    pConfirm = (WlCmdCfm *)WMSP_WL_ParamSetNullKeyResponseMode((u16 *)wlBuf, 0);
    if (pConfirm->resultCode != 0x00 ) {
        WmspError((0x0200 | 0x16) , pConfirm->resultCode);
        return;
    }
    pConfirm = (WlCmdCfm *)WMSP_WL_MaClearData((u16 *)wlBuf, 0x0007);
    if (pConfirm->resultCode != 0x00 ) {
        WmspError((0x0100 | 0x04) , pConfirm->resultCode);
        return;
    }
    status->mp_setDataFlag = 0 ;
    if (fCleanQueue) {
        WMSP_CleanSendQueue(0xffff);
    }
    {
        WMCallback *cb = (WMCallback *)WMSP_GetBuffer4Callback2Wm9();
        cb->apiid = WM_APIID_END_MP;
        cb->errcode = WM_ERRCODE_SUCCESS;
        WMSP_ReturnResult2Wm9((void *)cb);
    }
}

#include "context002.h"
