#include "context000.h"

#include "context001.h"

void native_host_arm7_main_027e8320(OSMessage msg)
{
    WMStatus *status = WMSP_GetStatusStructure();
    u32 wlBuf[128];
    WMCallback *cb;
    WlCmdCfm *pConfirm;
    if (status->state != WM_STATE_IDLE) {
        cb = (WMCallback *)native_host_arm7_arm_038073f0();
        cb->apiid = WM_APIID_POWER_OFF;
        cb->errcode = WM_ERRCODE_ILLEGAL_STATE;
        native_host_arm7_arm_038073a4((void *)cb);
        return;
    }
    pConfirm = (WlCmdCfm *)native_host_arm7_arm_027e2880((u16 *)wlBuf);
    if (pConfirm->resultCode != 0x00 ) {
        cb = (WMCallback *)native_host_arm7_arm_038073f0();
        cb->apiid = WM_APIID_POWER_OFF;
        cb->errcode = WM_ERRCODE_FAILED;
        cb->wlCmdID = (0x0300 | 0x01) ;
        cb->wlResult = pConfirm->resultCode;
        native_host_arm7_arm_038073a4((void *)cb);
        return;
    }
    status->state = WM_STATE_STOP;
    cb = (WMCallback *)native_host_arm7_arm_038073f0();
    cb->apiid = WM_APIID_POWER_OFF;
    cb->errcode = WM_ERRCODE_SUCCESS;
    native_host_arm7_arm_038073a4((void *)cb);
    return;
}
