#include "context000.h"

WlParamSetCfm *WMSP_WL_ParamSetLifeTime(u16 *buf, u16 tableNumber, u16 camLifeTime, u16 frameLifeTime)
{
    WlParamSetLifeTimeReq *req;
    WlParamSetCfm *cfm;
    do { buf[0] = 0; buf[1] = 0; buf[2] = 0; buf[3] = 0; buf[4] = 0; buf[5] = 0; } while (0) ;
    req = (WlParamSetLifeTimeReq *)buf;
    req->header.code = (0x0200 | 0x11) ;
    req->header.length = 3;
    req->tableNumber = tableNumber;
    req->camLifeTime = camLifeTime;
    req->frameLifeTime = frameLifeTime;
    cfm = (WlParamSetCfm *)((u32)req + ((WlCmdReq*)req)->header.length*2 + 12+4) ;
    cfm->header.code = req->header.code;
    cfm->header.length = 1;
    (void)WMSP_WlRequest(buf);
    return cfm;
}
