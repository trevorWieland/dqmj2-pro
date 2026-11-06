#include "context000.h"

#include "context001.h"

void native_host_arm7_main_027e2f5c(OSMessage msg)
{
    u32 *reqBuf = (u32 *)msg;
    WMStatus *status = WMSP_GetStatusStructure();
    u32 wlBuf[128];
    WMCallback *cb;
    WMParentParam *param;
    WlCmdCfm *pConfirm;
    param = (WMParentParam *)(reqBuf[1]);
    native_host_arm7_arm_037fe12c((void *)param, (void *)&(status->pparam), 64 );
    {
        u16 parentChannel;
        parentChannel = status->pparam.channel;
        if (!((0x0001 << parentChannel) & status->enableChannel)) {
            cb = native_host_arm7_arm_038073f0();
            cb->apiid = WM_APIID_SET_P_PARAM;
            cb->errcode = WM_ERRCODE_INVALID_PARAM;
            native_host_arm7_arm_038073a4(cb);
            return;
        }
    }
    pConfirm = (WlCmdCfm *)native_host_arm7_arm_027e2648((u16 *)wlBuf,
        status->pparam.maxEntry);
    if (pConfirm->resultCode != 0x00 ) {
        WmspError((0x0200 | 0x12) , pConfirm->resultCode);
        return;
    }
    cb = (WMCallback *)native_host_arm7_arm_038073f0();
    cb->apiid = WM_APIID_SET_P_PARAM;
    cb->errcode = WM_ERRCODE_SUCCESS;
    native_host_arm7_arm_038073a4((void *)cb);
    return;
}

#include "context002.h"
