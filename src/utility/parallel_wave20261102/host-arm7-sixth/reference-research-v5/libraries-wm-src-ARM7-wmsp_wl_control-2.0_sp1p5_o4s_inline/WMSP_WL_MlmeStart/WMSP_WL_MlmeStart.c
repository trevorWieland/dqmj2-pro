#include "context000.h"

WlMlmeStartCfm *WMSP_WL_MlmeStart(u16 *buf, u16 ssidLength, u8 *ssid, u16 beaconPeriod, u16 dtimPeriod, u16 channel, u16 basicRateSet, u16 supportRateSet, u16 gameInfoLength, WMGameInfo *gameInfo)
{
    WlMlmeStartReq *req;
    WlMlmeStartCfm *cfm;
    do { buf[0] = 0; buf[1] = 0; buf[2] = 0; buf[3] = 0; buf[4] = 0; buf[5] = 0; } while (0) ;
    req = (WlMlmeStartReq *)buf;
    req->header.code = (0x0000 | 0x09) ;
    req->header.length = (u16)(23 + ((gameInfoLength+1)/2) );
    req->ssidLength = ssidLength;
    MI_CpuCopy16(ssid, req->ssid, sizeof(u8) * 32);
    req->beaconPeriod = beaconPeriod;
    req->dtimPeriod = dtimPeriod;
    req->channel = channel;
    req->basicRateSet = basicRateSet;
    req->supportRateSet = supportRateSet;
    req->gameInfoLength = gameInfoLength;
    MI_CpuCopy16(gameInfo, req->gameInfo, gameInfoLength);
    cfm = (WlMlmeStartCfm *)((u32)req + ((WlCmdReq*)req)->header.length*2 + 12+4) ;
    cfm->header.code = req->header.code;
    cfm->header.length = 1;
    (void)WMSP_WlRequest(buf);
    return cfm;
}
