#include "dependency000.h"
#include "dependency001.h"

void native_host_arm7_main_027e50b0(OSMessage msg)
{
    WMStatus *status = WMSP_GetStatusStructure();
    u32 wlBuf[128];
    WlCmdCfm *pConfirm;
    BOOL fCleanQueue = 0 ;
    if (status->state != WM_STATE_MP_PARENT && status->state != WM_STATE_MP_CHILD) {
        WMCallback *callback = (WMCallback *)native_host_arm7_arm_038073f0();
        callback->apiid = WM_APIID_END_MP;
        callback->errcode = WM_ERRCODE_ILLEGAL_STATE;
        native_host_arm7_arm_038073a4(callback);
        return;
    }
    {
        OSIntrMode e = native_host_arm7_arm_037fdd00();
        if (status->mp_flag == 1 ) {
            fCleanQueue = 1 ;
        }
        status->mp_flag = 0 ;
        native_host_arm7_arm_027e5b98();
        native_host_arm7_arm_027e0640();
        if (status->state == WM_STATE_MP_CHILD) {
            status->state = WM_STATE_CHILD;
        } else if (status->state == WM_STATE_MP_PARENT) {
            status->state = WM_STATE_PARENT;
        }
        (void)native_host_arm7_arm_037fdd14(e);
    }
    pConfirm = (WlCmdCfm *)native_host_arm7_arm_027e2700((u16 *)wlBuf, 0);
    if (pConfirm->resultCode != 0x00 ) {
        native_host_arm7_arm_027e51cc((0x0200 | 0x16) , pConfirm->resultCode);
        return;
    }
    pConfirm = (WlCmdCfm *)native_host_arm7_arm_027e23ac((u16 *)wlBuf, 0x0007);
    if (pConfirm->resultCode != 0x00 ) {
        native_host_arm7_arm_027e51cc((0x0100 | 0x04) , pConfirm->resultCode);
        return;
    }
    status->mp_setDataFlag = 0 ;
    if (fCleanQueue) {
        native_host_arm7_arm_027e7828(0xffff);
    }
    {
        WMCallback *cb = (WMCallback *)native_host_arm7_arm_038073f0();
        cb->apiid = WM_APIID_END_MP;
        cb->errcode = WM_ERRCODE_SUCCESS;
        native_host_arm7_arm_038073a4((void *)cb);
    }
}
#include "dependency002.h"
