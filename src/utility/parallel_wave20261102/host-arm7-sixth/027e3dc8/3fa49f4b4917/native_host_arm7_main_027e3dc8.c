#include "dependency000.h"
#include "dependency001.h"

void native_host_arm7_main_027e3dc8(OSMessage msg)
{
    u32 wlBuf[128];
    u16 *buf = (u16 *)wlBuf;
    WMSPWork *const work = WMSP_GetSystemWork();
    WMStatus *status = WMSP_GetStatusStructure();
    if (status->state != WM_STATE_SCAN) {
        WMCallback *callback = (WMCallback *)native_host_arm7_arm_038073f0();
        callback->apiid = WM_APIID_END_SCAN;
        callback->errcode = WM_ERRCODE_ILLEGAL_STATE;
        native_host_arm7_arm_038073a4(callback);
        return;
    }
    {
        WlDevIdleCfm *p_confirm = native_host_arm7_arm_027e2898(buf);
        if (p_confirm->resultCode != 0x00 ) {
            native_host_arm7_arm_027e3e9c((0x0300 | 0x02) , p_confirm->resultCode);
            return;
        }
    }
    status->state = WM_STATE_IDLE;
    if (status->preamble == 0 ) {
        WlParamSetCfm *p_confirm;
        p_confirm = native_host_arm7_arm_027e2584(buf, 1 );
        if (p_confirm->resultCode != 0x00 ) {
            native_host_arm7_arm_027e3e9c((0x0200 | 0x0E) , p_confirm->resultCode);
            return;
        }
        status->preamble = 1 ;
    }
    {
        WMCallback *callback = (WMCallback *)native_host_arm7_arm_038073f0();
        callback->apiid = WM_APIID_END_SCAN;
        callback->errcode = WM_ERRCODE_SUCCESS;
        native_host_arm7_arm_038073a4(callback);
        return;
    }
    return;
}
#include "dependency002.h"
