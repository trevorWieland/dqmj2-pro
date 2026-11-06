#include "dependency000.h"
#include "dependency001.h"

void native_utility_child_arm7_main_027e5840(OSMessage msg)
{
    u32 *buf = (u32 *)msg;
    WMStatus *status = WMSP_GetStatusStructure();
    u32 wlBuf[128];
    WlTxFrame wlTxFrame;
    WlMaDataCfm *wlResult;
    native_utility_child_arm7_arm_037fe814(&buf[1], status->dcf_destAdr, 6);
    status->dcf_sendData = (u16 *)buf[3];
    status->dcf_sendSize = (u16)buf[4];
    status->dcf_sendFlag = 1 ;
    MI_CpuClear16(&wlTxFrame, sizeof(wlTxFrame));
    wlTxFrame.frameId = (u16)0;
    wlTxFrame.length = (u16)buf[4];
    MI_WriteByte(&wlTxFrame.rate,
        (u8)((status->rate == 2 ) ? 0x14 : 0xa ));
    native_utility_child_arm7_arm_037fe814(&buf[1], wlTxFrame.destAdrs, 6 );
    native_utility_child_arm7_arm_037fe814(status->MacAddress, wlTxFrame.srcAdrs, 6 );
    wlTxFrame.datap = (u16 *)buf[3];
    wlResult = native_utility_child_arm7_arm_027e28a0((u16 *)wlBuf, &wlTxFrame);
    {
        WMCallback *cb = (WMCallback *)native_utility_child_arm7_arm_0380576c();
        cb->apiid = WM_APIID_SET_DCF_DATA;
        cb->errcode = (wlResult->resultCode == 0x00 ) ? WM_ERRCODE_SUCCESS : WM_ERRCODE_FAILED;
        if (wlResult->resultCode != 0x00 ) {
            cb->wlCmdID = (0x0100 | 0x00) ;
            cb->wlResult = wlResult->resultCode;
        }
        native_utility_child_arm7_arm_038057c8((void *)cb);
    }
}
