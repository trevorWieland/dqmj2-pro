#include "context000.h"

#include "context001.h"

void native_host_arm7_main_027e5e80(void *arg)
{
#pragma unused(arg)
    WMSPWork *p = WMSP_GetSystemWork();
    WMStatus *status = WMSP_GetStatusStructure();
    if (status->mp_flag == 1 ) {
        WmspSetVAlarm(200 ,
            native_host_arm7_main_027e5c5c,
            (void *)1 );
        if (status->mp_lifeTimeTick != 0ULL) {
            OSTick now;
            OSTick last;
            BOOL result;
            now = native_host_arm7_arm_037fd21c() | 1;
            last = status->mp_lastRecvTick[0];
            if ((last != 0ULL) && ((now - last) > status->mp_lifeTimeTick)) {
                u32 *buf;
                ((void) 0) ;
                status->mp_lastRecvTick[0] = 0ULL;
                buf = native_host_arm7_arm_027e0700();
                if (buf == ((void *)0) ) {
                    result = 0 ;
                } else {
                    buf[0] = WM_APIID_AUTO_DISCONNECT;
                    buf[1] = 0;
                    buf[2] = WM_DISCONNECT_REASON_MP_LIFETIME;
                    ((void)0) ;
                    result = native_host_arm7_arm_037fc6d4(&(WMSP_GetSystemWork()->requestQ),
                        (OSMessage)buf,
                        0 );
                }
                if (!result) {
                    WMIndCallback *cb = (WMIndCallback *)native_host_arm7_arm_038073f0();
                    cb->apiid = WM_APIID_INDICATION;
                    cb->errcode = WM_ERRCODE_FIFO_ERROR;
                    cb->state = WM_STATECODE_FIFO_ERROR;
                    cb->reason = WM_APIID_AUTO_DISCONNECT;
                    native_host_arm7_arm_038073a4(cb);
                }
                return;
            }
        }
        native_host_arm7_arm_027e609c();
    }
}

#include "context002.h"
