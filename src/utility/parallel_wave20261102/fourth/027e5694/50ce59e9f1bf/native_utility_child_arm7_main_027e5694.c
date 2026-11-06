#include "dependency000.h"
#include "dependency001.h"

void native_utility_child_arm7_main_027e5694(OSMessage msg)
{
    WMStatus *status = WMSP_GetStatusStructure();
    u32 wlBuf[128];
    WlCmdCfm *pConfirm;
    BOOL fCleanQueue = 0 ;
    if (status->state != WM_STATE_MP_PARENT && status->state != WM_STATE_MP_CHILD) {
        WMCallback *callback = (WMCallback *)native_utility_child_arm7_arm_0380576c();
        callback->apiid = WM_APIID_END_MP;
        callback->errcode = WM_ERRCODE_ILLEGAL_STATE;
        native_utility_child_arm7_arm_038057c8(callback);
        return;
    }
    {
        OSIntrMode e = native_utility_child_arm7_arm_037fe41c();
        if (status->mp_flag == 1 ) {
            fCleanQueue = 1 ;
        }
        status->mp_flag = 0 ;
        native_utility_child_arm7_arm_027e6834();
        native_utility_child_arm7_arm_027e0238();
        if (status->state == WM_STATE_MP_CHILD) {
            status->state = WM_STATE_CHILD;
        } else if (status->state == WM_STATE_MP_PARENT) {
            status->state = WM_STATE_PARENT;
        }
        (void)native_utility_child_arm7_arm_037fe430(e);
    }
    pConfirm = (WlCmdCfm *)native_utility_child_arm7_arm_027e23b4((u16 *)wlBuf, 0);
    if (pConfirm->resultCode != 0x00 ) {
        native_utility_child_arm7_arm_027e5658((0x0200 | 0x16) , pConfirm->resultCode);
        return;
    }
    pConfirm = (WlCmdCfm *)native_utility_child_arm7_arm_027e273c((u16 *)wlBuf, 0x0007);
    if (pConfirm->resultCode != 0x00 ) {
        native_utility_child_arm7_arm_027e5658((0x0100 | 0x04) , pConfirm->resultCode);
        return;
    }
    status->mp_setDataFlag = 0 ;
    if (fCleanQueue) {
        native_utility_child_arm7_arm_027e6e08(0xffff);
    }
    {
        WMCallback *cb = (WMCallback *)native_utility_child_arm7_arm_0380576c();
        cb->apiid = WM_APIID_END_MP;
        cb->errcode = WM_ERRCODE_SUCCESS;
        native_utility_child_arm7_arm_038057c8((void *)cb);
    }
}
#include "dependency002.h"
