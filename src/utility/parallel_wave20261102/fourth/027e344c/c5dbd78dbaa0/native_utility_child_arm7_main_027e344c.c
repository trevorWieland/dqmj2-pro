#include "dependency000.h"
#include "dependency001.h"

void native_utility_child_arm7_main_027e344c(OSMessage msg)
{
    u32 *reqBuf = (u32 *)msg;
    WMStatus *status = WMSP_GetStatusStructure();
    u32 wlBuf[128];
    WMCallback *cb;
    WMParentParam *param;
    WlCmdCfm *pConfirm;
    param = (WMParentParam *)(reqBuf[1]);
    native_utility_child_arm7_arm_037fe814((void *)param, (void *)&(status->pparam), 64 );
    {
        u16 parentChannel;
        parentChannel = status->pparam.channel;
        if (!((0x0001 << parentChannel) & status->enableChannel)) {
            cb = native_utility_child_arm7_arm_0380576c();
            cb->apiid = WM_APIID_SET_P_PARAM;
            cb->errcode = WM_ERRCODE_INVALID_PARAM;
            native_utility_child_arm7_arm_038057c8(cb);
            return;
        }
    }
    pConfirm = (WlCmdCfm *)native_utility_child_arm7_arm_027e2474((u16 *)wlBuf,
        status->pparam.maxEntry);
    if (pConfirm->resultCode != 0x00 ) {
        native_utility_child_arm7_arm_027e3410((0x0200 | 0x12) , pConfirm->resultCode);
        return;
    }
    cb = (WMCallback *)native_utility_child_arm7_arm_0380576c();
    cb->apiid = WM_APIID_SET_P_PARAM;
    cb->errcode = WM_ERRCODE_SUCCESS;
    native_utility_child_arm7_arm_038057c8((void *)cb);
    return;
}
#include "dependency002.h"
