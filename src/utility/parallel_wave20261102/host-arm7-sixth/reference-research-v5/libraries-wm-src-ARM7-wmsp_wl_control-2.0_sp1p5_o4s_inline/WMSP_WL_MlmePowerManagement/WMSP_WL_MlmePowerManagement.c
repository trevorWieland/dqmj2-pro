#include "context000.h"

WlMlmePowerManagementCfm *WMSP_WL_MlmePowerManagement(u16 *buf, u16 pwrMgtMode, u16 wakeUp, u16 recieveDtims)
{
    WlMlmePowerManagementReq *req;
    WlMlmePowerManagementCfm *cfm;
    do { buf[0] = 0; buf[1] = 0; buf[2] = 0; buf[3] = 0; buf[4] = 0; buf[5] = 0; } while (0) ;
    req = (WlMlmePowerManagementReq *)buf;
    req->header.code = (0x0000 | 0x01) ;
    req->header.length = 3;
    req->pwrMgtMode = pwrMgtMode;
    req->wakeUp = wakeUp;
    req->recieveDtims = recieveDtims;
    cfm = (WlMlmePowerManagementCfm *)((u32)req + ((WlCmdReq*)req)->header.length*2 + 12+4) ;
    cfm->header.code = req->header.code;
    cfm->header.length = 1;
    (void)WMSP_WlRequest(buf);
    return cfm;
}
