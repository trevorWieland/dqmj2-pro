#include "context000.h"

#include "context001.h"

void WMSP_SetDCFData(OSMessage msg)
{
    u32 *buf = (u32 *)msg;
    WMStatus *status = WMSP_GetStatusStructure();
    u32 wlBuf[128];
    WlTxFrame wlTxFrame;
    WlMaDataCfm *wlResult;
    MI_CpuCopy8(&buf[1], status->dcf_destAdr, 6);
    status->dcf_sendData = (u16 *)buf[3];
    status->dcf_sendSize = (u16)buf[4];
    status->dcf_sendFlag = 1 ;
    MI_CpuClear16(&wlTxFrame, sizeof(wlTxFrame));
    wlTxFrame.frameId = (u16)0;
    wlTxFrame.length = (u16)buf[4];
    MI_WriteByte(&wlTxFrame.rate,
        (u8)((status->rate == 2 ) ? 0x14 : 0xa ));
    MI_CpuCopy8(&buf[1], wlTxFrame.destAdrs, 6 );
    MI_CpuCopy8(status->MacAddress, wlTxFrame.srcAdrs, 6 );
    wlTxFrame.datap = (u16 *)buf[3];
    wlResult = WMSP_WL_MaData((u16 *)wlBuf, &wlTxFrame);
    {
        WMCallback *cb = (WMCallback *)WMSP_GetBuffer4Callback2Wm9();
        cb->apiid = WM_APIID_SET_DCF_DATA;
        cb->errcode = (wlResult->resultCode == 0x00 ) ? WM_ERRCODE_SUCCESS : WM_ERRCODE_FAILED;
        if (wlResult->resultCode != 0x00 ) {
            cb->wlCmdID = (0x0100 | 0x00) ;
            cb->wlResult = wlResult->resultCode;
        }
        WMSP_ReturnResult2Wm9((void *)cb);
    }
}
