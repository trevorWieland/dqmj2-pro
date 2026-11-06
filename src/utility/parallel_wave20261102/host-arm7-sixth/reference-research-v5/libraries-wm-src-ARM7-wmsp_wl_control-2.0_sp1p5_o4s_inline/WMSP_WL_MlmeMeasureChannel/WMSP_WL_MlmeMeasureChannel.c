#include "context000.h"

WlMlmeMeasureChannelCfm *WMSP_WL_MlmeMeasureChannel(u16 *buf, u16 ccaMode, u16 edThreshold, u16 measureTime, u8 *channelList)
{
    WlMlmeMeasureChannelReq *req;
    WlMlmeMeasureChannelCfm *cfm;
    do { buf[0] = 0; buf[1] = 0; buf[2] = 0; buf[3] = 0; buf[4] = 0; buf[5] = 0; } while (0) ;
    req = (WlMlmeMeasureChannelReq *)buf;
    req->header.code = (0x0000 | 0x0A) ;
    req->header.length = 12;
    req->rsv = 0;
    req->ccaMode = ccaMode;
    req->edThreshold = edThreshold;
    req->measureTime = measureTime;
    MI_CpuCopy16(channelList, req->channelList, sizeof(u8) * 16);
    cfm = (WlMlmeMeasureChannelCfm *)((u32)req + ((WlCmdReq*)req)->header.length*2 + 12+4) ;
    cfm->header.code = req->header.code;
    cfm->header.length = 18;
    (void)WMSP_WlRequest(buf);
    return cfm;
}
