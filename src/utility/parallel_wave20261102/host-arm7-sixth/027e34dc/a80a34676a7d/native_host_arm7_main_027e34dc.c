#include "dependency000.h"
#include "dependency001.h"

void native_host_arm7_main_027e34dc(OSMessage msg)
{
    u32 wlBuf[128];
    u16 *buf = (u16 *)wlBuf;
    WMSPWork *const work = WMSP_GetSystemWork();
    WMStatus *status = WMSP_GetStatusStructure();
    u16 current_state;
    u16 scanChannel;
    u16 scanBssid[3];
    u16 scanMaxChannelTime;
    WMStartScanReq *args = (WMStartScanReq *)msg;
    if (status->state != WM_STATE_IDLE && status->state != WM_STATE_CLASS1 && status->state != WM_STATE_SCAN) {
        WMStartScanCallback *callback = (WMStartScanCallback *)native_host_arm7_arm_038073f0();
        callback->apiid = WM_APIID_START_SCAN;
        callback->errcode = WM_ERRCODE_ILLEGAL_STATE;
        callback->state = WM_STATECODE_PARENT_NOT_FOUND;
        native_host_arm7_arm_038073a4(callback);
        return;
    }
    status->pInfoBuf = args->scanBuf;
    status->scan_channel = scanChannel = args->channel;
    scanMaxChannelTime = args->maxChannelTime;
    native_host_arm7_arm_037fe12c(args->bssid, scanBssid, 6 );
    if ((scanBssid[0] != 0xffff) && (scanBssid[0] & 0x0001)) {
        ((void)0) ;
        scanBssid[0] &= ~(0x0001);
    }
    if (!scanChannel) {
        WMStartScanCallback *callback = (WMStartScanCallback *)native_host_arm7_arm_038073f0();
        callback->apiid = WM_APIID_START_SCAN;
        callback->errcode = WM_ERRCODE_INVALID_PARAM;
        callback->state = WM_STATECODE_PARENT_NOT_FOUND;
        native_host_arm7_arm_038073a4(callback);
        return;
    }
    if (!((0x0001 << scanChannel) & status->enableChannel)) {
        WMStartScanCallback *cb = (WMStartScanCallback *)native_host_arm7_arm_038073f0();
        cb->apiid = WM_APIID_START_SCAN;
        cb->errcode = WM_ERRCODE_INVALID_PARAM;
        cb->state = WM_STATECODE_PARENT_NOT_FOUND;
        native_host_arm7_arm_038073a4(cb);
        return;
    }
    status->mode = 2 ;
    {
        WlDevGetStationStateCfm *p_confirm;
        p_confirm = native_host_arm7_arm_027e2924(buf);
        if (p_confirm->resultCode != 0x00 ) {
            native_host_arm7_arm_027e3d80((0x0300 | 0x08) , p_confirm->resultCode, 0 );
            return;
        }
        current_state = p_confirm->state;
    }
    if (current_state == 0x10 ) {
        if (!native_host_arm7_arm_027e03d0(WM_APIID_START_SCAN, buf)) {
            return;
        }
        {
            WlDevClass1Cfm *p_confirm;
            p_confirm = native_host_arm7_arm_027e28b0(buf);
            if (p_confirm->resultCode != 0x00 ) {
                native_host_arm7_arm_027e3d80((0x0300 | 0x03) , p_confirm->resultCode, 0 );
                return;
            }
        }
        status->state = WM_STATE_CLASS1;
        {
            WlMlmePowerManagementCfm *p_confirm;
            u16 pwrMgtMode;
            u16 wakeUp;
            u16 recieveDtims;
            pwrMgtMode = 1 ;
            wakeUp = 0 ;
            recieveDtims = 1 ;
            p_confirm = native_host_arm7_arm_027e1dbc(buf, pwrMgtMode, wakeUp, recieveDtims);
            if (p_confirm->resultCode != 0x00 ) {
                native_host_arm7_arm_027e3d80((0x0000 | 0x01) , p_confirm->resultCode, 0 );
                return;
            }
            status->pwrMgtMode = pwrMgtMode;
        }
        current_state = 0x20 ;
    }
    status->state = WM_STATE_SCAN;
    {
        WlMlmeScanCfm *p_confirm;
        WlMlmeScanReq *pReq = (WlMlmeScanReq *)buf;
        u32 bufSize;
        u16 ssidLength;
        u16 ssid[32 / sizeof(u16)];
        u16 scanType;
        u8 channelList[SCAN_CHANNEL_MAX];
        ssidLength = 0;
        MI_CpuFill16(ssid, 0xffff, 32 );
        scanType = 1 ;
        MI_WriteByte(&channelList[0], (u8)scanChannel);
        native_host_arm7_arm_037fe070(&channelList[1], 0, sizeof(*channelList) * (SCAN_CHANNEL_MAX - 1));
        bufSize = (((sizeof(WlMlmeScanReq) + 1) / 2 * 2) + ((sizeof(WlCmdHeader) + 1) / 2 * 2) + 6 +
            ((64 + (128 + 1) / 2 * 2) * 1));
        p_confirm = native_host_arm7_arm_027e1e1c(buf,
            bufSize,
            scanBssid,
            ssidLength,
            (u8 *)ssid,
            scanType,
            channelList,
            scanMaxChannelTime);
        if (p_confirm->resultCode != 0x00 ) {
            native_host_arm7_arm_027e3d80((0x0000 | 0x02) , p_confirm->resultCode, 0 );
            return;
        } else {
            WMStartScanCallback *callback = (WMStartScanCallback *)native_host_arm7_arm_038073f0();
            if (p_confirm->bssDescCount == 0) {
                callback->apiid = WM_APIID_START_SCAN;
                callback->errcode = WM_ERRCODE_SUCCESS;
                callback->state = WM_STATECODE_PARENT_NOT_FOUND;
                callback->channel = scanChannel;
                callback->linkLevel = WM_LINK_LEVEL_0;
            } else {
                MI_CpuClear16(&(status->pInfoBuf->gameInfo), sizeof(WMGameInfo));
                native_host_arm7_arm_037fe12c(&(p_confirm->bssDescList[0]),
                    status->pInfoBuf,
                    p_confirm->bssDescList[0].length * 2U);
                callback->apiid = WM_APIID_START_SCAN;
                callback->errcode = WM_ERRCODE_SUCCESS;
                callback->state = WM_STATECODE_PARENT_FOUND;
                callback->channel = p_confirm->bssDescList[0].channel;
                {
                    u8 tempRssi;
                    tempRssi = native_host_arm7_arm_027e383c((u8)p_confirm->bssDescList[0].rssi);
                    callback->linkLevel = native_host_arm7_arm_027e05d8(tempRssi);
                    native_host_arm7_arm_027e3850(tempRssi);
                }
                callback->ssidLength = p_confirm->bssDescList[0].ssidLength;
                native_host_arm7_arm_037fe12c(p_confirm->bssDescList[0].bssid, callback->macAddress, 6 );
                MI_CpuCopy16(&(p_confirm->bssDescList[0].ssid), &(callback->ssid), 32);
                callback->gameInfoLength = p_confirm->bssDescList[0].gameInfoLength;
                if (callback->gameInfoLength > 128) {
                    callback->apiid = WM_APIID_START_SCAN;
                    callback->errcode = WM_ERRCODE_SUCCESS;
                    callback->state = WM_STATECODE_PARENT_NOT_FOUND;
                    callback->channel = scanChannel;
                    callback->linkLevel = WM_LINK_LEVEL_0;
                } else {
                    MI_CpuClear16(&(callback->gameInfo), sizeof(WMGameInfo));
                    MI_CpuCopy16(&(p_confirm->bssDescList[0].gameInfo),
                        &(callback->gameInfo),
                        ((callback->gameInfoLength + 1U) & ~1U));
                }
            }
            native_host_arm7_arm_038073a4(callback);
        }
    }
    return;
}
#include "dependency002.h"
