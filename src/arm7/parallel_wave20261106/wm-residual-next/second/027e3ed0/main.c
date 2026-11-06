#include "context000.h"

#include "context001.h"

void native_host_arm7_main_027e3ed0(OSMessage msg)
{
    u32 wlBuf[128];
    u16 *buf = (u16 *)wlBuf;
    WMSPWork *const work = WMSP_GetSystemWork();
    WMArm7Buf *const p = work->wm7buf;
    WMStatus *status = WMSP_GetStatusStructure();
    WMStartConnectReq *args = (WMStartConnectReq *)msg;
    WlMlmeAssociateCfm *assConfirm;
    if (status->state != WM_STATE_IDLE || (status->miscFlags & 0x0001 )) {
        WMStartConnectCallback *callback = (WMStartConnectCallback *)native_host_arm7_arm_038073f0();
        callback->apiid = WM_APIID_START_CONNECT;
        callback->errcode = WM_ERRCODE_ILLEGAL_STATE;
        callback->state = WM_STATECODE_CONNECT_START;
        native_host_arm7_arm_038073a4(callback);
        return;
    }
    native_host_arm7_arm_037fe12c((void *)(args->pInfo), &(p->connectPInfo), 192 );
    {
        if (p->connectPInfo.gameInfoLength >= 16) {
            if (!(p->connectPInfo.gameInfo.attribute & (1 << 0) )) {
                WMStartConnectCallback *cb = (WMStartConnectCallback *)native_host_arm7_arm_038073f0();
                cb->apiid = WM_APIID_START_CONNECT;
                cb->errcode = WM_ERRCODE_NO_ENTRY;
                cb->state = WM_STATECODE_CONNECT_START;
                native_host_arm7_arm_038073a4(cb);
                return;
            }
        }
    }
    {
        u16 connectChannel;
        connectChannel = p->connectPInfo.channel;
        if ((!((0x0001 << connectChannel) & status->enableChannel)) || (!(((0x0001 << connectChannel) >> 1) & 0x1fff ))) {
            WMStartConnectCallback *cb = (WMStartConnectCallback *)native_host_arm7_arm_038073f0();
            cb->apiid = WM_APIID_START_CONNECT;
            cb->errcode = WM_ERRCODE_INVALID_PARAM;
            cb->state = WM_STATECODE_CONNECT_START;
            native_host_arm7_arm_038073a4(cb);
            return;
        }
    }
    {
        WMStartConnectCallback *callback = (WMStartConnectCallback *)native_host_arm7_arm_038073f0();
        callback->apiid = WM_APIID_START_CONNECT;
        callback->errcode = WM_ERRCODE_SUCCESS;
        callback->state = WM_STATECODE_CONNECT_START;
        (void)native_host_arm7_arm_038073a4((void *)callback);
    }
    {
        if (status->rate == 1 ) {
            if (p->connectPInfo.rateSet.basic & 0x0001) {
                status->rate = 1 ;
            } else {
                status->rate = 2 ;
            }
        } else {
            if (p->connectPInfo.rateSet.basic & 0x0002) {
                status->rate = 2 ;
            } else {
                status->rate = 1 ;
            }
        }
        if (p->connectPInfo.capaInfo & 0x0020) {
            status->preamble = 1 ;
        } else {
            status->preamble = 0 ;
        }
        if (p->connectPInfo.gameInfoLength == 0) {
            status->mode = 3 ;
        } else {
            status->mode = 2 ;
        }
        if (!native_host_arm7_arm_027e03d0(WM_APIID_START_CONNECT, buf)) {
            return;
        }
    }
    {
        WlCmdCfm *p_confirm;
        p_confirm = (WlCmdCfm *)native_host_arm7_arm_027e2700(buf, 0);
        if (p_confirm->resultCode != 0x00 ) {
            native_host_arm7_arm_027e4474((0x0200 | 0x16) , p_confirm->resultCode, 0 );
            return;
        }
    }
    {
        if (p->connectPInfo.gameInfoLength < 16) {
            u16 beaconLostTh;
            WlParamSetCfm *p_confirm;
            beaconLostTh = (u16)(p->connectPInfo.beaconPeriod > 0 ? (10 * 1000 / p->connectPInfo.beaconPeriod) + 1 : 1);
            beaconLostTh = (beaconLostTh > (u16)255 ) ? (u16)255 : beaconLostTh;
            p_confirm = native_host_arm7_arm_027e24b4(buf, beaconLostTh);
            if (p_confirm->resultCode != 0x00 ) {
                native_host_arm7_arm_027e4474((0x0200 | 0x0B) , p_confirm->resultCode, 0 );
                return;
            }
        }
    }
    {
        WlDevClass1Cfm *p_confirm;
        p_confirm = native_host_arm7_arm_027e28b0(buf);
        if (p_confirm->resultCode != 0x00 ) {
            native_host_arm7_arm_027e4474((0x0300 | 0x03) , p_confirm->resultCode, 0 );
            return;
        }
    }
    status->state = WM_STATE_CLASS1;
    {
        WlMlmePowerManagementCfm *p_confirm;
        u16 pwrMgtMode;
        u16 wakeUp;
        u16 recieveDtims;
        pwrMgtMode = (u16)(args->powerSave ? 1 : 0 );
        wakeUp = 0 ;
        recieveDtims = 1 ;
        p_confirm = native_host_arm7_arm_027e1dbc(buf, pwrMgtMode, wakeUp, recieveDtims);
        if (p_confirm->resultCode != 0x00 ) {
            native_host_arm7_arm_027e4474((0x0000 | 0x01) , p_confirm->resultCode, 0 );
            return;
        }
        status->pwrMgtMode = pwrMgtMode;
    }
    {
        WlMlmeJoinCfm *p_confirm;
        u16 timeOut;
        WlBssDesc bss_desc;
        enum {
            BSS_DESC_BLIT_SIZE = 64
        };
        extern void sdk_compiler_assert__LINE__ (char is[(BSS_DESC_BLIT_SIZE == sizeof(bss_desc) - sizeof(bss_desc.gameInfo)) ? +1 : -1]) ;
        timeOut = 2000 ;
        native_host_arm7_arm_037fe12c(&p->connectPInfo, &bss_desc, BSS_DESC_BLIT_SIZE);
        if (status->mode == 2 ) {
            bss_desc.ssidLength = 32;
            *(u16 *)&(bss_desc.ssid[0]) = (u16)(p->connectPInfo.gameInfo.ggid & 0x0ffff);
            *(u16 *)&(bss_desc.ssid[2]) = (u16)(p->connectPInfo.gameInfo.ggid >> 16);
            *(u16 *)&(bss_desc.ssid[4]) = p->connectPInfo.gameInfo.tgid;
            *(u16 *)&(bss_desc.ssid[6]) = 0;
            native_host_arm7_arm_037fe12c(args->ssid, &(bss_desc.ssid[8]), 24 );
        }
        p_confirm = native_host_arm7_arm_027e1ed4(buf, timeOut, &bss_desc);
        if ((p_confirm->resultCode != 0x00 ) || (p_confirm->statusCode != 0 )) {
            native_host_arm7_arm_027e4474((0x0000 | 0x03) , p_confirm->resultCode, p_confirm->statusCode);
            return;
        }
        native_host_arm7_arm_037fe12c(p_confirm->peerMacAdrs, status->parentMacAddress, 6 );
    }
    {
        WlMlmeAuthenticateCfm *p_confirm;
        u16 algorithm;
        u16 timeOut;
        u16 mac[3];
        native_host_arm7_arm_037fe12c(status->parentMacAddress, mac, 6 );
        algorithm = args->authMode;
        timeOut = 2000 ;
        p_confirm = native_host_arm7_arm_027e1f4c(buf, mac, algorithm, timeOut);
        if ((p_confirm->resultCode == 0x0C ) && ((p_confirm->statusCode == 19 ))) {
            WMStartConnectCallback *callback = (WMStartConnectCallback *)native_host_arm7_arm_038073f0();
            callback->apiid = WM_APIID_START_CONNECT;
            callback->errcode = WM_ERRCODE_OVER_MAX_ENTRY;
            callback->state = WM_STATECODE_CONNECT_START;
            native_host_arm7_arm_038073a4((void *)callback);
            return;
        }
        if ((p_confirm->resultCode != 0x00 ) || (p_confirm->statusCode != 0 )) {
            native_host_arm7_arm_027e4474((0x0000 | 0x04) , p_confirm->resultCode, p_confirm->statusCode);
            return;
        }
    }
    {
        u16 mac[3];
        u16 listenInterval;
        u16 timeOut;
        native_host_arm7_arm_037fe12c(status->parentMacAddress, mac, 6 );
        listenInterval = 1;
        timeOut = 2000 ;
        assConfirm = native_host_arm7_arm_027e2044(buf, mac, listenInterval, timeOut);
    }
    {
        OSIntrMode e = native_host_arm7_arm_037fdd00();
        if ((assConfirm->resultCode == 0x0C ) && ((assConfirm->statusCode == 19 ))) {
            WMStartConnectCallback *callback;
            (void)native_host_arm7_arm_037fdd14(e);
            callback = (WMStartConnectCallback *)native_host_arm7_arm_038073f0();
            callback->apiid = WM_APIID_START_CONNECT;
            callback->errcode = WM_ERRCODE_OVER_MAX_ENTRY;
            callback->state = WM_STATECODE_CONNECT_START;
            native_host_arm7_arm_038073a4((void *)callback);
            return;
        }
        if ((assConfirm->resultCode != 0x00 ) || (assConfirm->statusCode != 0 )) {
            (void)native_host_arm7_arm_037fdd14(e);
            native_host_arm7_arm_027e4474((0x0000 | 0x06) , assConfirm->resultCode, assConfirm->statusCode);
            return;
        }
        status->aid = assConfirm->aid;
        status->curr_tgid = p->connectPInfo.gameInfo.tgid;
        MI_CpuFill16(status->portSeqNo[0], 0x0001, sizeof(status->portSeqNo[0]));
        {
            u8 tempRssi8;
            u16 linkLevel;
            tempRssi8 = WMSP_GetRssi8((u8)p->connectPInfo.rssi);
            linkLevel = native_host_arm7_arm_027e05d8(tempRssi8);
            status->linkLevel = linkLevel;
            native_host_arm7_arm_027e0564(tempRssi8);
        }
        {
            OSIntrMode e = native_host_arm7_arm_037fdd00();
            status->child_bitmap = 0x0001;
            status->mp_readyBitmap = 0x0001;
            if (status->mp_lifeTimeTick != 0ULL) {
                status->mp_lastRecvTick[0] = native_host_arm7_arm_037fd21c() | 1;
            }
            status->state = WM_STATE_CHILD;
            native_host_arm7_arm_027e07a0((u16)(p->connectPInfo.gameInfo.parentMaxSize
                + ((p->connectPInfo.gameInfo.attribute & (1 << 2) ) ? (2 * 16 + 4) + (2 + 4) : 0)));
            native_host_arm7_arm_027e07f0((u16)(p->connectPInfo.gameInfo.childMaxSize
                + ((p->connectPInfo.gameInfo.attribute & (1 << 2) ) ? 2 + (2 + 2) : 0)));
            (void)native_host_arm7_arm_037fdd14(e);
        }
        status->beaconIndicateFlag = 1;
        {
            WMStartConnectCallback *callback = (WMStartConnectCallback *)native_host_arm7_arm_038073f0();
            callback->apiid = WM_APIID_START_CONNECT;
            callback->errcode = WM_ERRCODE_SUCCESS;
            callback->state = WM_STATECODE_CONNECTED;
            callback->aid = status->aid;
            native_host_arm7_arm_037fe12c(status->parentMacAddress, callback->macAddress, 6 );
            callback->parentSize = status->mp_parentSize;
            callback->childSize = status->mp_childSize;
            native_host_arm7_arm_038073a4((void *)callback);
        }
        (void)native_host_arm7_arm_037fdd14(e);
    }
    return;
}

#include "context002.h"
