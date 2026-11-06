#include "context000.h"

WlMaMpCfm *WMSP_WL_MaMp(u16 *buf, u16 resume, u16 retryLimit, u16 txop, u16 pollBitmap, u16 tmptt, u16 currTsf, u16 dataLength, u16 wmHeader, u16 *datap)
{
    WlMaMpReq *req;
    WlMaMpCfm *cfm;
    do { buf[0] = 0; buf[1] = 0; buf[2] = 0; buf[3] = 0; buf[4] = 0; buf[5] = 0; } while (0) ;
    req = (WlMaMpReq *)buf;
    req->header.code = (0x0100 | 0x02) ;
    req->header.length = 10;
    req->resume = resume;
    req->retryLimit = retryLimit;
    req->txop = txop;
    req->pollBitmap = pollBitmap;
    req->tmptt = tmptt;
    req->currTsf = currTsf;
    req->dataLength = dataLength;
    req->wmHeader = wmHeader;
    req->datap = datap;
    cfm = (WlMaMpCfm *)((u32)req + ((WlCmdReq*)req)->header.length*2 + 12+4) ;
    cfm->header.code = req->header.code;
    cfm->header.length = 1;
    (void)WMSP_WlRequest(buf);
    return cfm;
}
