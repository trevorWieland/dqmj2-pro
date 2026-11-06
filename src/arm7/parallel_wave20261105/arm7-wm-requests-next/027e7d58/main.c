#include "context000.h"

void native_host_arm7_main_027e7d58(OSMessage msg)
{
    u32 wlBuf[128];
    u32 *arg = (u32 *)msg;
    u16 wMac[3];
    WlCmdCfm *pConfirm;
    native_host_arm7_arm_037fe12c(&arg[1], wMac, 6);
    {
        s32 auth_retry;
        for (auth_retry = 0; auth_retry < 2 ;) {
            pConfirm = (WlCmdCfm *)native_host_arm7_arm_027e1fcc((u16 *)wlBuf, wMac, 19 );
            switch (pConfirm->resultCode) {
            case 0x00 :
                break;
            case 0x07 :
            case 0x0C :
                auth_retry++;
                continue;
            default:
                break;
            }
            break;
        }
    }
    {
        WMCallback *cb = (WMCallback *)native_host_arm7_arm_038073f0();
        cb->apiid = WM_APIID_AUTO_DEAUTH;
        if (pConfirm->resultCode == 0x00 ) {
            cb->errcode = WM_ERRCODE_SUCCESS;
        } else {
            cb->errcode = WM_ERRCODE_FAILED;
            cb->wlCmdID = (0x0000 | 0x05) ;
            cb->wlResult = pConfirm->resultCode;
        }
        native_host_arm7_arm_038073a4(cb);
    }
}
