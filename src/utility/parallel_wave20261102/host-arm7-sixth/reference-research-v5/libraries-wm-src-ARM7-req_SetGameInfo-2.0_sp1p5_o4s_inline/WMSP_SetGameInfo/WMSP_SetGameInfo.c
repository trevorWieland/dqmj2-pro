#include "context000.h"

#include "context001.h"

void WMSP_SetGameInfo(OSMessage msg)
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
        WMSP_CopyParentParam(&GameInfo, &(status->pparam));
        length = (u16)(16 + status->pparam.userGameInfoLength);
        wlResult = WMSP_WL_ParamSetGameInfo((u16 *)wlBuf, length, (u16 *)(&GameInfo));
    }
    {
        WMCallback *cb = (WMCallback *)WMSP_GetBuffer4Callback2Wm9();
        cb->apiid = WM_APIID_SET_GAMEINFO;
        cb->errcode = (wlResult->resultCode == 0x00 ) ? WM_ERRCODE_SUCCESS : WM_ERRCODE_FAILED;
        if (wlResult->resultCode != 0x00 ) {
            cb->wlCmdID = (0x0200 | 0x45) ;
            cb->wlResult = wlResult->resultCode;
        }
        WMSP_ReturnResult2Wm9((void *)cb);
    }
}
