#include "context000.h"

void native_host_arm7_main_027e5b00(OSMessage msg)
{
    u32 wlBuf[128];
    WMGetWirelessCounterCallback *cb;
    WlDevGetInfoCfm *pConfirm;
    pConfirm = (WlDevGetInfoCfm *)native_host_arm7_arm_027e290c((u16 *)wlBuf);
    if (pConfirm->resultCode != 0x00 ) {
        WmspError((0x0300 | 0x07) , pConfirm->resultCode);
        return;
    }
    cb = (WMgetWirelessCounterCallback *)native_host_arm7_arm_038073f0();
    cb->apiid = WM_APIID_GET_W_COUNTER;
    cb->errcode = WM_ERRCODE_SUCCESS;
    MI_CpuCopy16(&(pConfirm->counter), &(cb->TX_Success), 180);
    native_host_arm7_arm_038073a4((void *)cb);
    return;
}

#include "context001.h"
