#include "context000.h"

WlParamSetCfm *WMSP_WL_ParamSetAll(WlParamSetAllReq *req)
{
    WlParamSetCfm *cfm;
    do { ((u16 *)req)[0] = 0; ((u16 *)req)[1] = 0; ((u16 *)req)[2] = 0; ((u16 *)req)[3] = 0; ((u16 *)req)[4] = 0; ((u16 *)req)[5] = 0; } while (0) ;
    req->header.code = (0x0200 | 0x00) ;
    req->header.length = 72;
    cfm = (WlParamSetCfm *)((u32)req + ((WlCmdReq*)req)->header.length*2 + 12+4) ;
    cfm->header.code = req->header.code;
    cfm->header.length = 1;
    (void)WMSP_WlRequest((u16 *)req);
    return cfm;
}
