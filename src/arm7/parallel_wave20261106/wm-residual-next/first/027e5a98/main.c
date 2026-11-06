#include "context000.h"

void native_host_arm7_main_027e5a98(OSMessage msg)
{
    u32 wlBuf[128];
    WMCallback *cb;
    WlCmdCfm *pConfirm;
    pConfirm = (WlCmdCfm *)native_host_arm7_arm_027e28dc((u16 *)wlBuf);
    if (pConfirm->resultCode != 0x00 ) {
        WmspError((0x0300 | 0x05) , pConfirm->resultCode);
        return;
    }
    cb = (WMCallback *)native_host_arm7_arm_038073f0();
    cb->apiid = WM_APIID_INIT_W_COUNTER;
    cb->errcode = WM_ERRCODE_SUCCESS;
    native_host_arm7_arm_038073a4((void *)cb);
    return;
}

#include "context001.h"
