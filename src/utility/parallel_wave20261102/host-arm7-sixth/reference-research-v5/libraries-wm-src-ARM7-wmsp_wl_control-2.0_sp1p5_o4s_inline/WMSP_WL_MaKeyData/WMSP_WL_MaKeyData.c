#include "context000.h"

WlMaKeyDataCfm *WMSP_WL_MaKeyData(u16 *buf, u16 length, u16 wmHeader, u16 *keyDatap)
{
    WlMaKeyDataReq *req;
    WlMaKeyDataCfm *cfm;
    do { buf[0] = 0; buf[1] = 0; buf[2] = 0; buf[3] = 0; buf[4] = 0; buf[5] = 0; } while (0) ;
    req = (WlMaKeyDataReq *)buf;
    req->header.code = (0x0100 | 0x01) ;
    req->header.length = 4;
    req->length = length;
    req->wmHeader = wmHeader;
    req->keyDatap = keyDatap;
    cfm = (WlMaKeyDataCfm *)((u32)req + ((WlCmdReq*)req)->header.length*2 + 12+4) ;
    cfm->header.code = req->header.code;
    cfm->header.length = 1;
    (void)WMSP_WlRequest(buf);
    return cfm;
}
