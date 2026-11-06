#include "dependency000.h"
#include "dependency001.h"

void native_utility_child_arm7_main_027e5a50(OSMessage msg)
{
    u32 *msgbuf = (u32 *)msg;
    WMStatus *status = WMSP_GetStatusStructure();
    u8 *wepkey;
    status->wepMode = (u16)msgbuf[1];
    switch (status->wepMode) {
    case 0 :
        status->wep_flag = 0 ;
        break;
    case 1 :
    case 2 :
    case 3 :
        status->wep_flag = 1 ;
        break;
    default:
        status->wep_flag = 0 ;
    }
    if (status->wep_flag == 1 ) {
        wepkey = (u8 *)msgbuf[2];
        native_utility_child_arm7_arm_037fe814(wepkey, status->wepKey, 80 );
    } else {
        MI_CpuClear8(status->wepKey, 80 );
    }
    status->wepKeyId = (u16)msgbuf[3];
    {
        WlCmdCfm *pConfirm;
        u32 wlBuf[128];
        u16 *buf = (u16 *)wlBuf;
        pConfirm = (WlCmdCfm *)native_utility_child_arm7_arm_027e2680(buf, status->wepKeyId);
        if (pConfirm->resultCode != 0x00 ) {
            native_utility_child_arm7_arm_027e5a14((0x0200 | 0x07) , pConfirm->resultCode);
        }
    }
    {
        WMCallback *cb = (WMCallback *)native_utility_child_arm7_arm_0380576c();
        cb->apiid = WM_APIID_SET_WEPKEY_EX;
        cb->errcode = WM_ERRCODE_SUCCESS;
        native_utility_child_arm7_arm_038057c8((void *)cb);
    }
}
#include "dependency002.h"
