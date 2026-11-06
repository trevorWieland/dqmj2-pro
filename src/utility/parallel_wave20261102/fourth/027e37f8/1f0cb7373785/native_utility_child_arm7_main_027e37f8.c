#include "dependency000.h"
#include "dependency001.h"

void native_utility_child_arm7_main_027e37f8(OSMessage msg)
{
    WMStatus *status = WMSP_GetStatusStructure();
    u32 wlBuf[128];
    WMCallback *cb;
    WlCmdCfm *pConfirm;
    if (status->state != WM_STATE_PARENT) {
        WMCallback *callback = (WMCallback *)native_utility_child_arm7_arm_0380576c();
        callback->apiid = WM_APIID_END_PARENT;
        callback->errcode = WM_ERRCODE_ILLEGAL_STATE;
        native_utility_child_arm7_arm_038057c8(callback);
        return;
    }
    status->pparam.entryFlag = 0 ;
    {
        u16 wMac[3];
        s32 i;
        OSIntrMode e;
        for (i = 1; i < (15 + 1); i++) {
            if (status->child_bitmap & (0x0001 << i)) {
                native_utility_child_arm7_arm_037fe814(status->childMacAddress[i - 1], wMac, 6 );
                {
                    s32 auth_retry;
                    for (auth_retry = 0; auth_retry < 2 ;) {
                        pConfirm = (WlCmdCfm *)native_utility_child_arm7_arm_027e2b38((u16 *)wlBuf, wMac, 3 );
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
                e = native_utility_child_arm7_arm_037fe41c();
                if (status->child_bitmap & (0x0001 << i)) {
                    status->child_bitmap &= ~(0x0001 << i);
                    status->mp_readyBitmap &= ~(0x0001 << i);
                    status->mp_lastRecvTick[i] = 0ULL;
                    (void)native_utility_child_arm7_arm_037fe430(e);
                    native_utility_child_arm7_arm_027e4b28(1 , (u16)i, wMac);
                } else {
                    (void)native_utility_child_arm7_arm_037fe430(e);
                }
            }
        }
    }
    pConfirm = (WlCmdCfm *)native_utility_child_arm7_arm_027e2de4((u16 *)wlBuf, 1 );
    if (pConfirm->resultCode != 0x00 ) {
        native_utility_child_arm7_arm_027e37bc((0x0000 | 0x00) , pConfirm->resultCode);
        return;
    }
    status->beaconIndicateFlag = 0;
    status->state = WM_STATE_CLASS1;
    pConfirm = (WlCmdCfm *)native_utility_child_arm7_arm_027e2250((u16 *)wlBuf);
    if (pConfirm->resultCode != 0x00 ) {
        native_utility_child_arm7_arm_027e37bc((0x0300 | 0x02) , pConfirm->resultCode);
        return;
    }
    status->state = WM_STATE_IDLE;
    status->wep_flag = 0 ;
    status->wepMode = 0 ;
    MI_CpuClear8(status->wepKey, 80 );
    native_utility_child_arm7_arm_027e0100();
    cb = (WMCallback *)native_utility_child_arm7_arm_0380576c();
    cb->apiid = WM_APIID_END_PARENT;
    cb->errcode = WM_ERRCODE_SUCCESS;
    native_utility_child_arm7_arm_038057c8((void *)cb);
    return;
}
#include "dependency002.h"
