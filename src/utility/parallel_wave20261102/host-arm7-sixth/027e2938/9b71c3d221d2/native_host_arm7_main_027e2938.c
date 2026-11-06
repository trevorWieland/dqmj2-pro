#include "dependency000.h"

WlDevTestSignalCfm *native_host_arm7_main_027e2938(u16 *buf, u16 control, u16 signal, u16 rate, u16 channel)
{
    WlDevTestSignalReq *req;
    WlDevTestSignalCfm *cfm;
    do { buf[0] = 0; buf[1] = 0; buf[2] = 0; buf[3] = 0; buf[4] = 0; buf[5] = 0; } while (0) ;
    req = (WlDevTestSignalReq *)buf;
    req->header.code = (0x0300 | 0x09) ;
    req->header.length = 4;
    req->control = control;
    req->signal = signal;
    req->rate = rate;
    req->channel = channel;
    cfm = (WlDevTestSignalCfm *)((u32)req + ((WlCmdReq*)req)->header.length*2 + 12+4) ;
    cfm->header.code = req->header.code;
    cfm->header.length = 1;
    (void)native_host_arm7_arm_027e01cc(buf);
    return cfm;
}
