#include "context000.h"

#include "context001.h"

void native_host_arm7_main_027e609c(void)
{
    BOOL result;
    u32 *buf;
    WMSPWork *native_host_arm7_data_027f7884 = WMSP_GetSystemWork();
    WMStatus *status = WMSP_GetStatusStructure();
    OSIntrMode enabled;
    enabled = native_host_arm7_arm_037fdd00();
    if (status->valarm_queuedFlag == 1 ) {
        (void)native_host_arm7_arm_037fdd14(enabled);
        return;
    }
    status->valarm_queuedFlag = 1 ;
    (void)native_host_arm7_arm_037fdd14(enabled);
    buf = native_host_arm7_arm_027e0700();
    if (buf == ((void *)0) ) {
        result = 0 ;
    } else {
        buf[0] = WM_APIID_VALARM_MP;
        ((void)0) ;
        result = native_host_arm7_arm_037fc6d4(&(native_host_arm7_data_027f7884->requestQ), (OSMessage)buf, 0 );
    }
    if (!result) {
        status->valarm_queuedFlag = 0 ;
        if (native_host_arm7_data_027f7884->wm7buf != ((void *)0) ) {
            WMIndCallback *cb = (WMIndCallback *)native_host_arm7_arm_038073f0();
            cb->apiid = WM_APIID_INDICATION;
            cb->errcode = WM_ERRCODE_FIFO_ERROR;
            cb->state = WM_STATECODE_FIFO_ERROR;
            cb->reason = WM_APIID_VALARM_MP;
            native_host_arm7_arm_038073a4((void *)cb);
        }
    }
}
