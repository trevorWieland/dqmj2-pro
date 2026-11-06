#include "context000.h"

#include "context001.h"

void native_host_arm7_main_027e7cc8(OSMessage msg)
{
    u32 *buf = (u32 *)msg;
    WMStatus *status = WMSP_GetStatusStructure();
    WlParamSetCfm *wlResult;
    u32 wlBuf[128];
    status->pparam.entryFlag = (u16)(buf[1]);
    {
        WMGameInfo GameInfo __attribute__ ((aligned(32))) ;
        u16 length;
        native_host_arm7_arm_027e030c(&GameInfo, &(status->pparam));
        length = (u16)(16 + status->pparam.userGameInfoLength);
        wlResult = native_host_arm7_arm_027e27b8((u16 *)wlBuf, length, (u16 *)(&GameInfo));
    }
    {
        WMCallback *cb = (WMCallback *)native_host_arm7_arm_038073f0();
        cb->apiid = WM_APIID_SET_ENTRY;
        if (wlResult->resultCode == 0x00 ) {
            cb->errcode = WM_ERRCODE_SUCCESS;
        } else {
            cb->errcode = WM_ERRCODE_FAILED;
            cb->wlCmdID = (0x0200 | 0x45) ;
            cb->wlResult = wlResult->resultCode;
        }
        native_host_arm7_arm_038073a4(cb);
    }
}
