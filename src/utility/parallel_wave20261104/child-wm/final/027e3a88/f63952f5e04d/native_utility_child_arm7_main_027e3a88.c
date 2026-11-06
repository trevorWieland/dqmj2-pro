#include "dependency000.h"
#include "dependency001.h"

void native_utility_child_arm7_main_027e3a88(OSMessage msg)
{
    u32 wlBuf[1024 / sizeof(u32) + (sizeof(WlMlmeScanReq) + 1) / sizeof(u32) + (sizeof(WlCmdHeader) + 1) / sizeof(u32)];
    u16 *buf = (u16 *)wlBuf;
    WMSPWork *const work = WMSP_GetSystemWork();
    WMStatus *status = WMSP_GetStatusStructure();
    u16 current_state;
    u16 scanChannelList;
    u16 scanBssid[3];
    u16 scanMaxChannelTime;
    u16 scanType;
    u16 ssidMatchLength;
    BOOL ssidMaskCustomize;
    u16 scanSsidLength;
    u8 scanSsid[32 ];
    u16 scanBufSize;
    WMStartScanExReq *args = (WMStartScanExReq *)msg;
    if (status->state != WM_STATE_IDLE && status->state != WM_STATE_CLASS1 && status->state != WM_STATE_SCAN) {
        WMStartScanExCallback *callback = (WMStartScanExCallback *)native_utility_child_arm7_arm_0380576c();
        callback->apiid = WM_APIID_START_SCAN_EX;
        callback->errcode = WM_ERRCODE_ILLEGAL_STATE;
        callback->state = WM_STATECODE_PARENT_NOT_FOUND;
        native_utility_child_arm7_arm_038057c8(callback);
        return;
    }
    status->pInfoBuf = args->scanBuf;
    status->scan_channel = scanChannelList = args->channelList;
    scanMaxChannelTime = args->maxChannelTime;
    native_utility_child_arm7_arm_037fe814(args->bssid, scanBssid, 6 );
    ssidMatchLength = args->ssidMatchLength;
    switch (args->scanType) {
    case 2 :
        ssidMaskCustomize = 1 ;
        scanType = 0 ;
        break;
    case 3 :
        ssidMaskCustomize = 1 ;
        scanType = 1 ;
        break;
    default:
        ssidMaskCustomize = 0 ;
        scanType = args->scanType;
    }
    scanSsidLength = args->ssidLength;
    native_utility_child_arm7_arm_037fe814(args->ssid, scanSsid, 32 );
    scanBufSize = args->scanBufSize;
    if ((scanBssid[0] != 0xffff) && (scanBssid[0] & 0x0001)) {
        ((void)0) ;
        scanBssid[0] &= ~(0x0001);
    }
    scanChannelList <<= 1;
    scanChannelList &= status->enableChannel;
    if (!scanChannelList) {
        WMStartScanExCallback *callback = (WMStartScanExCallback *)native_utility_child_arm7_arm_0380576c();
        callback->apiid = WM_APIID_START_SCAN_EX;
        callback->errcode = WM_ERRCODE_INVALID_PARAM;
        callback->state = WM_STATECODE_PARENT_NOT_FOUND;
        native_utility_child_arm7_arm_038057c8(callback);
        return;
    }
    if ( (args->scanBuf == ((void *)0) )
            || ((u32)(args->scanBuf) & 0x00000003)
            || (args->scanBufSize < (sizeof(WlBssDesc) - 4))) {
        WMStartScanExCallback *callback = (WMStartScanExCallback *)native_utility_child_arm7_arm_0380576c();
        callback->apiid = WM_APIID_START_SCAN_EX;
        callback->errcode = WM_ERRCODE_INVALID_PARAM;
        callback->state = WM_STATECODE_PARENT_NOT_FOUND;
        native_utility_child_arm7_arm_038057c8(callback);
        return;
    }
    status->mode = 2 ;
    {
        WlDevGetStationStateCfm *p_confirm;
        p_confirm = native_utility_child_arm7_arm_027e21c8(buf);
        if (p_confirm->resultCode != 0x00 ) {
            native_utility_child_arm7_arm_027e39cc((0x0300 | 0x08) , p_confirm->resultCode, 1 );
            return;
        }
        current_state = p_confirm->state;
    }
    if (current_state == 0x10 ) {
        if (!native_utility_child_arm7_arm_027e03b8(WM_APIID_START_SCAN_EX, buf)) {
            return;
        }
        {
            WlDevClass1Cfm *p_confirm;
            p_confirm = native_utility_child_arm7_arm_027e2238(buf);
            if (p_confirm->resultCode != 0x00 ) {
                native_utility_child_arm7_arm_027e39cc((0x0300 | 0x03) , p_confirm->resultCode, 1 );
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
            p_confirm = native_utility_child_arm7_arm_027e2d80(buf, pwrMgtMode, wakeUp, recieveDtims);
            if (p_confirm->resultCode != 0x00 ) {
                native_utility_child_arm7_arm_027e39cc((0x0000 | 0x01) , p_confirm->resultCode, 1 );
                return;
            }
            status->pwrMgtMode = pwrMgtMode;
        }
        current_state = 0x20 ;
    }
    if (scanType == 0 ) {
        if (status->preamble == 1 ) {
            WlParamSetCfm *p_confirm;
            p_confirm = native_utility_child_arm7_arm_027e2540(buf, 0 );
            if (p_confirm->resultCode != 0x00 ) {
                native_utility_child_arm7_arm_027e39cc((0x0200 | 0x0E) , p_confirm->resultCode, 1 );
                return;
            }
            status->preamble = 0 ;
        }
    } else {
        if (status->preamble == 0 ) {
            WlParamSetCfm *p_confirm;
            p_confirm = native_utility_child_arm7_arm_027e2540(buf, 1 );
            if (p_confirm->resultCode != 0x00 ) {
                native_utility_child_arm7_arm_027e39cc((0x0200 | 0x0E) , p_confirm->resultCode, 1 );
                return;
            }
            status->preamble = 1 ;
        }
    }
    if (ssidMaskCustomize == 1 ) {
        u8 mask[32];
        WlParamSetCfm *p_confirm;
        native_utility_child_arm7_arm_037fe780(mask, 0xff, 32);
        if (ssidMatchLength <= 32) {
            native_utility_child_arm7_arm_037fe780(mask, 0x00, ssidMatchLength);
        }
        p_confirm = native_utility_child_arm7_arm_027e25a0(buf, mask);
        if (p_confirm->resultCode != 0x00 ) {
            native_utility_child_arm7_arm_027e39cc((0x0200 | 0x0D) , p_confirm->resultCode, 1 );
            return;
        }
    }
    status->state = WM_STATE_SCAN;
    {
        WlMlmeScanCfm *p_confirm;
        WlMlmeScanReq *pReq = (WlMlmeScanReq *)buf;
        u32 bufSize;
        u8 channelList[SCAN_CHANNEL_MAX];
        u16 i, j;
        j = 0;
        native_utility_child_arm7_arm_037fe780(channelList, 0, sizeof(*channelList) * SCAN_CHANNEL_MAX);
        for (i = 1; i < 15; ++i)
        {
            if (scanChannelList & (0x0001 << i)) {
                MI_WriteByte(&channelList[j], (u8)i);
                ++j;
            }
        }
        bufSize = native_utility_child_arm7_arm_027e3a18(scanBufSize);
        p_confirm = native_utility_child_arm7_arm_027e2cc4(buf,
            bufSize,
            scanBssid,
            scanSsidLength,
            (u8 *)scanSsid,
            scanType,
            channelList,
            scanMaxChannelTime);
        if (p_confirm->resultCode != 0x00 ) {
            native_utility_child_arm7_arm_027e39cc((0x0000 | 0x02) , p_confirm->resultCode, 1 );
            return;
        } else {
            WMStartScanExCallback *callback = (WMStartScanExCallback *)native_utility_child_arm7_arm_0380576c();
            if (p_confirm->bssDescCount == 0) {
                callback->apiid = WM_APIID_START_SCAN_EX;
                callback->errcode = WM_ERRCODE_SUCCESS;
                callback->state = WM_STATECODE_PARENT_NOT_FOUND;
                callback->bssDescCount = 0;
                callback->channelList = (u16)(scanChannelList >> 1);
            } else {
                int i;
                WMBssDesc *src, *dest;
                src = (WMBssDesc *)&(p_confirm->bssDescList[0]);
                dest = status->pInfoBuf;
                MI_CpuClear16(dest, scanBufSize);
                for (i = 0; i < p_confirm->bssDescCount; ++i) {
                    u16 length_byte;
                    length_byte = (u16)(src->length * 2);
                    native_utility_child_arm7_arm_037fe814(src, dest, length_byte);
                    if (scanSsidLength > 0) {
                        if (!native_utility_child_arm7_arm_027e3a3c(dest)) {
                            dest->ssidLength = scanSsidLength;
                            native_utility_child_arm7_arm_037fe814(scanSsid, dest->ssid, 32 );
                        }
                    }
                    callback->bssDesc[i] = dest;
                    {
                        u8 tempRssi;
                        tempRssi = WMSP_GetRssi8((u8)(src->rssi));
                        callback->linkLevel[i] = native_utility_child_arm7_arm_027e0298(tempRssi);
                        WMSP_AddRssiToRandomPool(tempRssi);
                    }
                    src = (WMBssDesc *)((u32)src + length_byte);
                    dest = (WMBssDesc *)((u32)dest + length_byte);
                    if ((u32)dest & 0x02) {
                        dest = (WMBssDesc *)(((u32)dest + 2) & ~(0x00000003));
                    }
                }
                callback->apiid = WM_APIID_START_SCAN_EX;
                callback->errcode = WM_ERRCODE_SUCCESS;
                callback->state = WM_STATECODE_PARENT_FOUND;
                callback->bssDescCount = p_confirm->bssDescCount;
                callback->channelList = (u16)(scanChannelList >> 1);
            }
            native_utility_child_arm7_arm_038057c8(callback);
        }
    }
    return;
}
#include "dependency002.h"
