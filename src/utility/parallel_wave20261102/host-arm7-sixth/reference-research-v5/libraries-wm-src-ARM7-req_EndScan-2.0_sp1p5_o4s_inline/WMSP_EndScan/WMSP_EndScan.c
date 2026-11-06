#include "context000.h"

#include "context001.h"

void WMSP_EndScan(OSMessage msg)
{
    u32 wlBuf[128];
    u16 *buf = (u16 *)wlBuf;
    WMSPWork *const work = WMSP_GetSystemWork();
    WMStatus *status = WMSP_GetStatusStructure();
    if (status->state != WM_STATE_SCAN) {
        WMCallback *callback = (WMCallback *)WMSP_GetBuffer4Callback2Wm9();
        callback->apiid = WM_APIID_END_SCAN;
        callback->errcode = WM_ERRCODE_ILLEGAL_STATE;
        WMSP_ReturnResult2Wm9(callback);
        return;
    }
    {
        WlDevIdleCfm *p_confirm = WMSP_WL_DevIdle(buf);
        if (p_confirm->resultCode != 0x00 ) {
            WmspError((0x0300 | 0x02) , p_confirm->resultCode);
            return;
        }
    }
    status->state = WM_STATE_IDLE;
    if (status->preamble == 0 ) {
        WlParamSetCfm *p_confirm;
        p_confirm = WMSP_WL_ParamSetPreambleType(buf, 1 );
        if (p_confirm->resultCode != 0x00 ) {
            WmspError((0x0200 | 0x0E) , p_confirm->resultCode);
            return;
        }
        status->preamble = 1 ;
    }
    {
        WMCallback *callback = (WMCallback *)WMSP_GetBuffer4Callback2Wm9();
        callback->apiid = WM_APIID_END_SCAN;
        callback->errcode = WM_ERRCODE_SUCCESS;
        WMSP_ReturnResult2Wm9(callback);
        return;
    }
    return;
}

#include "context002.h"
