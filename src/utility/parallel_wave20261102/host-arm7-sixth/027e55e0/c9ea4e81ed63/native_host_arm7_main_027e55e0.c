#include "dependency000.h"
#include "dependency001.h"

void native_host_arm7_main_027e55e0(OSMessage msg)
{
    u32 *buf = (u32 *)msg;
    WMSPWork *sys = WMSP_GetSystemWork();
    WMStatus *status = WMSP_GetStatusStructure();
    u8 attribute;
    u16 length;
    u32 wlBuf[128];
    WlParamSetCfm *wlResult;
    status->pparam.userGameInfo = (u16 *)(buf[1]);
    status->pparam.userGameInfoLength = (u16)(buf[2]);
    status->pparam.ggid = buf[3];
    status->pparam.tgid = (u16)(buf[4]);
    attribute = (u8)(buf[5]);
    status->pparam.entryFlag = (u16)((attribute & (1 << 0) ) ? 1 : 0);
    status->pparam.multiBootFlag = (u16)((attribute & (1 << 1) ) ? 1 : 0);
    status->pparam.KS_Flag = (u16)((attribute & (1 << 2) ) ? 1 : 0);
    status->pparam.CS_Flag = (u16)((attribute & (1 << 3) ) ? 1 : 0);
    {
        WMGameInfo GameInfo __attribute__ ((aligned(32))) ;
        native_host_arm7_arm_027e030c(&GameInfo, &(status->pparam));
        length = (u16)(16 + status->pparam.userGameInfoLength);
        wlResult = native_host_arm7_arm_027e27b8((u16 *)wlBuf, length, (u16 *)(&GameInfo));
    }
    {
        WMCallback *cb = (WMCallback *)native_host_arm7_arm_038073f0();
        cb->apiid = WM_APIID_SET_GAMEINFO;
        cb->errcode = (wlResult->resultCode == 0x00 ) ? WM_ERRCODE_SUCCESS : WM_ERRCODE_FAILED;
        if (wlResult->resultCode != 0x00 ) {
            cb->wlCmdID = (0x0200 | 0x45) ;
            cb->wlResult = wlResult->resultCode;
        }
        native_host_arm7_arm_038073a4((void *)cb);
    }
}
