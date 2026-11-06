#include "context000.h"

#include "context001.h"

void native_host_arm7_main_027e87d8(OSMessage msg)
{
    WMStatus *status = WMSP_GetStatusStructure();
    u32 wlBuf[128];
    u16 *buf = (u16 *)wlBuf;
    BOOL powerSave;
    u16 pwrMgtMode;
    WMCallback *callback = (WMCallback *)native_host_arm7_arm_038073f0();
    callback->apiid = WM_APIID_SET_PS_MODE;
    if (status->state != WM_STATE_DCF_CHILD) {
        callback->errcode = WM_ERRCODE_ILLEGAL_STATE;
        native_host_arm7_arm_038073a4(callback);
        return;
    }
    powerSave = (BOOL)(((u32 *)msg)[1]);
    if (powerSave == 1 ) {
        pwrMgtMode = 1 ;
    } else {
        pwrMgtMode = 0 ;
    }
    {
        WlMlmePowerManagementCfm *p_confirm;
        u16 wakeUp;
        u16 recieveDtims;
        wakeUp = 0 ;
        recieveDtims = 1 ;
        p_confirm = native_host_arm7_arm_027e1dbc(buf, pwrMgtMode, wakeUp, recieveDtims);
        if (p_confirm->resultCode != 0x00 ) {
            callback->errcode = WM_ERRCODE_FAILED;
            callback->wlCmdID = (0x0000 | 0x01) ;
            callback->wlResult = p_confirm->resultCode;
            native_host_arm7_arm_038073a4(callback);
            return;
        }
    }
    {
        WlMaDataCfm *p_confirm;
        WlTxFrame wlTxFrame;
        WMSPWork *sys = WMSP_GetSystemWork();
        WMStatus *status = WMSP_GetStatusStructure();
        native_host_arm7_arm_037fe12c(status->parentMacAddress, status->dcf_destAdr, 6 );
        status->dcf_sendData = (u16 *)wlBuf;
        status->dcf_sendSize = 0;
        status->dcf_sendFlag = 1 ;
        MI_CpuClear16(&wlTxFrame, sizeof(wlTxFrame));
        wlTxFrame.frameId = (u16)0;
        wlTxFrame.length = 0;
        MI_WriteByte(&wlTxFrame.rate,
            (u8)((status->rate == 2 ) ? 0x14 : 0xa ));
        native_host_arm7_arm_037fe12c(status->parentMacAddress, wlTxFrame.destAdrs, 6 );
        native_host_arm7_arm_037fe12c(status->MacAddress, wlTxFrame.srcAdrs, 6 );
        wlTxFrame.datap = (u16 *)wlBuf;
        p_confirm = native_host_arm7_arm_027e2200((u16 *)wlBuf, &wlTxFrame);
        if (p_confirm->resultCode != 0x00 ) {
            callback->errcode = WM_ERRCODE_FAILED;
            callback->wlCmdID = (0x0100 | 0x00) ;
            callback->wlResult = p_confirm->resultCode;
            native_host_arm7_arm_038073a4(callback);
            return;
        }
    }
    callback->errcode = WM_ERRCODE_SUCCESS;
    native_host_arm7_arm_038073a4(callback);
    return;
}
