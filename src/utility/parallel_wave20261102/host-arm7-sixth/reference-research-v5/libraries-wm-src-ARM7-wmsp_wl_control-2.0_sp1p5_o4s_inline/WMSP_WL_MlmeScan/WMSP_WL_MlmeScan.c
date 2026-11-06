#include "context000.h"

WlMlmeScanCfm *WMSP_WL_MlmeScan(u16 *buf, u32 bufSize, u16 *bssid, u16 ssidLength, u8 *ssid, u16 scanType, u8 *channelList, u16 maxChannelTime)
{
    WlMlmeScanReq *req;
    WlMlmeScanCfm *cfm;
    do { buf[0] = 0; buf[1] = 0; buf[2] = 0; buf[3] = 0; buf[4] = 0; buf[5] = 0; } while (0) ;
    req = (WlMlmeScanReq *)buf;
    req->header.code = (0x0000 | 0x02) ;
    req->header.length = 31;
    MI_CpuCopy16(bssid, req->bssid, sizeof(u16) * 3);
    req->ssidLength = ssidLength;
    MI_CpuCopy16(ssid, req->ssid, sizeof(u8) * 32);
    req->scanType = scanType;
    MI_CpuCopy16(channelList, req->channelList, sizeof(u8) * 16);
    req->maxChannelTime = maxChannelTime;
    req->bssidMaskCount = 0;
    cfm = (WlMlmeScanCfm *)((u32)req + ((WlCmdReq*)req)->header.length*2 + 12+4) ;
    cfm->header.code = req->header.code;
    cfm->header.length = (u16)(bufSize / 2 - (sizeof(WlMlmeScanReq) + 1) / 2 - (sizeof(WlCmdHeader) + 1) / 2);
    (void)WMSP_WlRequest(buf);
    return cfm;
}
