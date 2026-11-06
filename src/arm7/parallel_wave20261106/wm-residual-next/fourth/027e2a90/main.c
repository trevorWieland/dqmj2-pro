#include "context000.h"

#include "context001.h"

void native_host_arm7_main_027e2a90(OSMessage msg)
{
    WMStatus *status = WMSP_GetStatusStructure();
    u32 wlBuf[128];
    u16 *buf = (u16 *)wlBuf;
    WMCallback *cb;
    WlCmdCfm *pConfirm;
    u16 station;
    u16 mode;
    u16 child_bitmap;
    BOOL fparent;
    {
        BOOL fCleanQueue = 0 ;
        OSIntrMode e = native_host_arm7_arm_037fdd00();
        if (status->mp_flag == 1 ) {
            status->mp_flag = 0 ;
            fCleanQueue = 1 ;
            native_host_arm7_arm_027e5b98();
            native_host_arm7_arm_027e0640();
            if (status->state == WM_STATE_MP_CHILD) {
                status->state = WM_STATE_CHILD;
            } else if (status->state == WM_STATE_MP_PARENT) {
                status->state = WM_STATE_PARENT;
            }
        }
        if (status->state == WM_STATE_PARENT || status->state == WM_STATE_CHILD) {
            child_bitmap = status->child_bitmap;
            fparent = (status->state == WM_STATE_PARENT);
        } else {
            child_bitmap = 0;
        }
        status->child_bitmap = 0;
        status->mp_readyBitmap = 0;
        status->ks_flag = 0 ;
        status->dcf_flag = 0 ;
        status->VSyncFlag = 0 ;
        status->beaconIndicateFlag = 0;
        (void)native_host_arm7_arm_037fdd14(e);
        if (fCleanQueue) {
            native_host_arm7_arm_027e7828(0xffff);
        }
    }
    if (fparent) {
        status->pparam.entryFlag = 0 ;
    }
    if (child_bitmap != 0) {
        int i;
        for (i = 0; i < (15 + 1); i++) {
            if (child_bitmap & (0x0001 << i)) {
                u8 *mac;
                if (i == 0) {
                    mac = status->parentMacAddress;
                } else {
                    mac = status->childMacAddress[i - 1];
                }
                native_host_arm7_arm_027e4a94(fparent, (u16)i, mac);
            }
        }
    }
    MI_CpuClear8(status->childMacAddress, sizeof(status->childMacAddress));
    pConfirm = (WlCmdCfm *)native_host_arm7_arm_027e2924(buf);
    if (pConfirm->resultCode != 0x00 ) {
        native_host_arm7_arm_027e2e7c((0x0300 | 0x08) , pConfirm->resultCode);
        return;
    }
    station = pConfirm->buf[0];
    pConfirm = (WlCmdCfm *)native_host_arm7_arm_027e286c(buf);
    if (pConfirm->resultCode != 0x00 ) {
        native_host_arm7_arm_027e2e7c((0x0200 | 0x84) , pConfirm->resultCode);
        return;
    }
    mode = pConfirm->buf[0];
    switch (station) {
    case 0x40 :
    case 0x30 :
        if ((mode == 2 ) || (mode == 3 )) {
            {
                u16 wMac[6 / sizeof(u16)];
                native_host_arm7_arm_037fe12c(status->parentMacAddress, wMac, 6 );
                {
                    s32 auth_retry;
                    for (auth_retry = 0; auth_retry < 2 ;) {
                        if (status->state != WM_STATE_CHILD) {
                            break;
                        }
                        pConfirm = (WlCmdCfm *)native_host_arm7_arm_027e1fcc(buf, wMac, 3 );
                        switch (pConfirm->resultCode) {
                        case 0x00 :
                            status->state = WM_STATE_CLASS1;
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
            }
        } else if (mode == 1 ) {
            {
                u16 wMac[6 / sizeof(u16)];
                native_host_arm7_arm_037fe070(wMac, 0xff, 6 );
                pConfirm = (WlCmdCfm *)native_host_arm7_arm_027e1fcc(buf, wMac, 3 );
                if (pConfirm->resultCode == 0x00 ) {
                    status->state = WM_STATE_CLASS1;
                }
            }
        } else {
        }
    case 0x20 :
        pConfirm = (WlCmdCfm *)native_host_arm7_arm_027e1d68(buf, 1 );
        if (pConfirm->resultCode != 0x00 ) {
            native_host_arm7_arm_027e2e7c((0x0000 | 0x00) , pConfirm->resultCode);
            return;
        }
    case 0x00 :
        pConfirm = (WlCmdCfm *)native_host_arm7_arm_027e2898(buf);
        if (pConfirm->resultCode != 0x00 ) {
            native_host_arm7_arm_027e2e7c((0x0300 | 0x02) , pConfirm->resultCode);
            return;
        }
    case 0x10 :
        if (status->preamble == 0 ) {
            WlParamSetCfm *p_confirm;
            p_confirm = native_host_arm7_arm_027e2584(buf, 1 );
            if (p_confirm->resultCode != 0x00 ) {
                native_host_arm7_arm_027e2e7c((0x0200 | 0x0E) , p_confirm->resultCode);
                return;
            }
            status->preamble = 1 ;
        }
        status->state = WM_STATE_IDLE;
        status->wep_flag = 0 ;
        native_host_arm7_arm_027e076c();
        break;
    case 0x11:
    case 0x12:
        if (mode == 0 ) {
            pConfirm = (WlCmdCfm *)native_host_arm7_arm_027e2938(buf, 0 ,
                0,
                0x14 ,
                1
            );
            if (pConfirm->resultCode != 0x00 ) {
                native_host_arm7_arm_027e2e7c((0x0300 | 0x09) , pConfirm->resultCode);
                return;
            }
        }
        pConfirm = (WlCmdCfm *)native_host_arm7_arm_027e2898(buf);
        if (pConfirm->resultCode != 0x00 ) {
            native_host_arm7_arm_027e2e7c((0x0300 | 0x02) , pConfirm->resultCode);
            return;
        }
        status->state = WM_STATE_IDLE;
        break;
    default:
        native_host_arm7_arm_027e2e7c((0x0300 | 0x08) , 0x00 );
        return;
    }
    cb = (WMCallback *)native_host_arm7_arm_038073f0();
    cb->apiid = WM_APIID_RESET;
    cb->errcode = WM_ERRCODE_SUCCESS;
    native_host_arm7_arm_038073a4((void *)cb);
    return;
}

#include "context002.h"
