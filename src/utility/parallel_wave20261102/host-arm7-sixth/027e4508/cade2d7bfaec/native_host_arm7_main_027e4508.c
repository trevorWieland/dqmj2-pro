#include "dependency000.h"
#include "dependency001.h"

BOOL native_host_arm7_main_027e4508(u32 *args, BOOL indicateFlag, u16 *disconnected)
{
    u32 wlBuf[128];
    u16 *buf = (u16 *)wlBuf;
    WlCmdCfm *pConfirm;
    WMStatus *status = WMSP_GetStatusStructure();
    u16 aidBitmap = (u16)args[1];
    u16 reason = (u16)(indicateFlag ? args[2] : 0);
    u16 resBitmap = 0x0000;
    BOOL fCleanQueue = 0 ;
    if (WMSPi_IsParent(status->state)) {
        if (status->mp_flag == 1 ) {
            fCleanQueue = 1 ;
        }
    } else if (WMSPi_IsChild(status->state)) {
        OSIntrMode e = native_host_arm7_arm_037fdd00();
        if (status->child_bitmap == 0) {
            (void)native_host_arm7_arm_037fdd14(e);
            if (!indicateFlag) {
                WMDisconnectCallback *callback = (WMDisconnectCallback *)native_host_arm7_arm_038073f0();
                callback->apiid = WM_APIID_DISCONNECT;
                callback->errcode = WM_ERRCODE_ILLEGAL_STATE;
                callback->wlCmdID = 0;
                callback->wlResult = 0;
                callback->tryBitmap = aidBitmap;
                callback->disconnectedBitmap = resBitmap;
                native_host_arm7_arm_038073a4(callback);
            }
            return 0 ;
        }
        if (status->mp_flag == 1 ) {
            status->mp_flag = 0 ;
            fCleanQueue = 1 ;
            native_host_arm7_arm_027e5b98();
            native_host_arm7_arm_027e0640();
            if (status->state == WM_STATE_MP_CHILD) {
                status->state = WM_STATE_CHILD;
            }
        }
        status->child_bitmap = 0;
        status->mp_readyBitmap = 0;
        status->ks_flag = 0 ;
        status->dcf_flag = 0 ;
        status->VSyncFlag = 0 ;
        (void)native_host_arm7_arm_037fdd14(e);
    } else {
        if (!indicateFlag) {
            WMDisconnectCallback *callback = (WMDisconnectCallback *)native_host_arm7_arm_038073f0();
            callback->apiid = WM_APIID_DISCONNECT;
            callback->errcode = WM_ERRCODE_ILLEGAL_STATE;
            callback->wlCmdID = 0;
            callback->wlResult = 0;
            callback->tryBitmap = aidBitmap;
            callback->disconnectedBitmap = resBitmap;
            native_host_arm7_arm_038073a4(callback);
        } else {
        }
        return 0 ;
    }
    if (WMSPi_IsChild(status->state)) {
        u16 wMac[3];
        native_host_arm7_arm_037fe12c(status->parentMacAddress, wMac, 6 );
        {
            s32 auth_retry;
            for (auth_retry = 0; auth_retry < 2 ;) {
                pConfirm = (WlCmdCfm *)native_host_arm7_arm_027e1fcc(buf, wMac, 3 );
                switch (pConfirm->resultCode) {
                case 0x00 :
                    break;
                case 0x01 :
                    break;
                case 0x07 :
                case 0x0C :
                    auth_retry++;
                    continue;
                default:
                    if (indicateFlag) {
                        native_host_arm7_arm_027e4b9c((0x0000 | 0x05) , pConfirm->resultCode, aidBitmap, resBitmap);
                    } else {
                        native_host_arm7_arm_027e4b58((0x0000 | 0x05) , pConfirm->resultCode, aidBitmap, resBitmap);
                    }
                    if (fCleanQueue) {
                        native_host_arm7_arm_027e7828(0x0001);
                    }
                    return 0 ;
                }
                break;
            }
        }
        resBitmap = 0x0001;
        status->beaconIndicateFlag = 0;
        status->state = WM_STATE_CLASS1;
        pConfirm = (WlCmdCfm *)native_host_arm7_arm_027e1d68(buf, 1 );
        if (pConfirm->resultCode != 0x00 ) {
            if (indicateFlag) {
                native_host_arm7_arm_027e4b9c((0x0000 | 0x00) , pConfirm->resultCode, aidBitmap, resBitmap);
            } else {
                native_host_arm7_arm_027e4b58((0x0000 | 0x00) , pConfirm->resultCode, aidBitmap, resBitmap);
            }
            if (fCleanQueue) {
                native_host_arm7_arm_027e7828(0x0001);
            }
            return 0 ;
        }
        pConfirm = (WlCmdCfm *)native_host_arm7_arm_027e2898(buf);
        if (pConfirm->resultCode != 0x00 ) {
            if (indicateFlag) {
                native_host_arm7_arm_027e4b9c((0x0300 | 0x02) , pConfirm->resultCode, aidBitmap, resBitmap);
            } else {
                native_host_arm7_arm_027e4b58((0x0300 | 0x02) , pConfirm->resultCode, aidBitmap, resBitmap);
            }
            if (fCleanQueue) {
                native_host_arm7_arm_027e7828(0x0001);
            }
            return 0 ;
        }
        status->state = WM_STATE_IDLE;
        status->wep_flag = 0 ;
        status->wepMode = 0 ;
        MI_CpuClear8(status->wepKey, 80 );
        native_host_arm7_arm_027e076c();
        if (indicateFlag == 1 ) {
            WMStartConnectCallback *cb = (WMStartConnectCallback *)native_host_arm7_arm_038073f0();
            cb->apiid = WM_APIID_START_CONNECT;
            cb->errcode = WM_ERRCODE_SUCCESS;
            cb->state = WM_STATECODE_DISCONNECTED;
            cb->reason = reason;
            cb->aid = status->aid;
            native_host_arm7_arm_037fe12c(wMac, cb->macAddress, 6 );
            cb->parentSize = status->mp_parentSize;
            cb->childSize = status->mp_childSize;
            native_host_arm7_arm_038073a4(cb);
        } else {
            native_host_arm7_arm_027e4a94(0 , 0, wMac);
        }
        if (fCleanQueue) {
            native_host_arm7_arm_027e7828(0x0001);
        }
    } else {
        u16 wMac[3];
        s32 i;
        u16 aid;
        for (i = 1; i < (15 + 1); i++) {
            if (status->child_bitmap & aidBitmap & (0x0001 << i)) {
                aid = (u16)i;
                native_host_arm7_arm_037fe12c(status->childMacAddress[i - 1], wMac, 6 );
                {
                    s32 auth_retry;
                    for (auth_retry = 0; auth_retry < 2 ;) {
                        pConfirm = (WlCmdCfm *)native_host_arm7_arm_027e1fcc(buf, wMac, 3 );
                        switch (pConfirm->resultCode) {
                        case 0x00 :
                            break;
                        case 0x07 :
                        case 0x0C :
                            auth_retry++;
                            continue;
                        default:
                            if (indicateFlag) {
                                native_host_arm7_arm_027e4b9c((0x0000 | 0x05) , pConfirm->resultCode, aidBitmap, resBitmap);
                            } else {
                                native_host_arm7_arm_027e4b58((0x0000 | 0x05) , pConfirm->resultCode, aidBitmap, resBitmap);
                            }
                            if (fCleanQueue) {
                                native_host_arm7_arm_027e7828(0x0001);
                            }
                            return 0 ;
                        }
                        break;
                    }
                }
                {
                    OSIntrMode e = native_host_arm7_arm_037fdd00();
                    if (status->child_bitmap & (0x0001 << i)) {
                        resBitmap |= (0x0001 << aid);
                        status->child_bitmap &= ~(0x0001 << i);
                        status->mp_readyBitmap &= ~(0x0001 << i);
                        status->mp_lastRecvTick[aid] = 0ULL;
                        MI_CpuClear8(status->childMacAddress[i - 1], 6 );
                        (void)native_host_arm7_arm_037fdd14(e);
                        if (indicateFlag == 1 ) {
                            WMStartParentCallback *cb = (WMStartParentCallback *)native_host_arm7_arm_038073f0();
                            cb->apiid = WM_APIID_START_PARENT;
                            cb->errcode = WM_ERRCODE_SUCCESS;
                            cb->state = WM_STATECODE_DISCONNECTED;
                            cb->reason = reason;
                            cb->aid = aid;
                            native_host_arm7_arm_037fe12c(wMac, cb->macAddress, 6 );
                            cb->parentSize = status->mp_parentSize;
                            cb->childSize = status->mp_childSize;
                            native_host_arm7_arm_038073a4(cb);
                        } else {
                            native_host_arm7_arm_027e4a94(1 , (u16)i, wMac);
                        }
                        if (fCleanQueue) {
                            native_host_arm7_arm_027e7828((u16)(0x0001 << i));
                        }
                    } else {
                        (void)native_host_arm7_arm_037fdd14(e);
                    }
                }
            }
        }
    }
    if (disconnected != ((void *)0) ) {
        *disconnected = resBitmap;
    }
    return 1 ;
}
#include "dependency002.h"
