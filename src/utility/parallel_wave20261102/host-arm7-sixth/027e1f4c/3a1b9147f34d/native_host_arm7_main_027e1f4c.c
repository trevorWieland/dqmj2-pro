#include "dependency000.h"

WlMlmeAuthenticateCfm *native_host_arm7_main_027e1f4c(u16 *buf, u16 *peerMacAdrs, u16 algorithm, u16 timeOut)
{
    WlMlmeAuthenticateReq *req;
    WlMlmeAuthenticateCfm *cfm;
    do { buf[0] = 0; buf[1] = 0; buf[2] = 0; buf[3] = 0; buf[4] = 0; buf[5] = 0; } while (0) ;
    req = (WlMlmeAuthenticateReq *)buf;
    req->header.code = (0x0000 | 0x04) ;
    req->header.length = 5;
    MI_CpuCopy16(peerMacAdrs, req->peerMacAdrs, sizeof(u16) * 3);
    req->algorithm = algorithm;
    req->timeOut = timeOut;
    cfm = (WlMlmeAuthenticateCfm *)((u32)req + ((WlCmdReq*)req)->header.length*2 + 12+4) ;
    cfm->header.code = req->header.code;
    cfm->header.length = 6;
    (void)native_host_arm7_arm_027e01cc(buf);
    return cfm;
}
