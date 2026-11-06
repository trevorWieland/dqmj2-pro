#include "dependency000.h"
#include "dependency001.h"

WlParamSetCfm *native_host_arm7_main_027e27b8(u16 *buf, u16 gameInfoLength, u16 *gameInfo)
{
    WlParamSetGameInfoReq *req;
    WlParamSetCfm *cfm;
    WMSPWork *sys = WMSP_GetSystemWork();
    do { buf[0] = 0; buf[1] = 0; buf[2] = 0; buf[3] = 0; buf[4] = 0; buf[5] = 0; } while (0) ;
    req = (WlParamSetGameInfoReq *)buf;
    req->header.code = (0x0200 | 0x45) ;
    req->header.length = (u16)(1 + ((gameInfoLength+1)/2) );
    req->gameInfoLength = gameInfoLength;
    MI_CpuCopy16(gameInfo, req->gameInfo, gameInfoLength);
    cfm = (WlParamSetCfm *)((u32)req + ((WlCmdReq*)req)->header.length*2 + 12+4) ;
    cfm->header.code = req->header.code;
    cfm->header.length = 1;
    (void)native_host_arm7_arm_027e01cc(buf);
    return cfm;
}
