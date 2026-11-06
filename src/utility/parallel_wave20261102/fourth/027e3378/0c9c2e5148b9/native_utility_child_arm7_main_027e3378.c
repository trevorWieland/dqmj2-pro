#include "dependency000.h"
#include "dependency001.h"

void native_utility_child_arm7_main_027e3378(OSMessage msg)
{
    WMStatus *status = WMSP_GetStatusStructure();
    u32 wlBuf[128];
    WMCallback *cb;
    WlCmdCfm *pConfirm;
    if (status->state != WM_STATE_IDLE) {
        cb = (WMCallback *)native_utility_child_arm7_arm_0380576c();
        cb->apiid = WM_APIID_END;
        cb->errcode = WM_ERRCODE_ILLEGAL_STATE;
        native_utility_child_arm7_arm_038057c8((void *)cb);
        return;
    }
    pConfirm = (WlCmdCfm *)native_utility_child_arm7_arm_027e2268((u16 *)wlBuf);
    if (pConfirm->resultCode != 0x00 ) {
        native_utility_child_arm7_arm_027e333c((0x0300 | 0x01) , pConfirm->resultCode);
        return;
    }
    status->state = WM_STATE_STOP;
    native_utility_child_arm7_arm_027e2eec(PM_LED_PATTERN_ON );
    status->state = WM_STATE_READY;
    cb = (WMCallback *)native_utility_child_arm7_arm_0380576c();
    cb->apiid = WM_APIID_END;
    cb->errcode = WM_ERRCODE_SUCCESS;
    native_utility_child_arm7_arm_038057c8((void *)cb);
    return;
}
#include "dependency002.h"
