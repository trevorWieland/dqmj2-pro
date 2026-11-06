#include "context000.h"

#include "context001.h"

void native_host_arm7_main_027e614c(OSMessage msg)
{
    WMSPWork *sys = WMSP_GetSystemWork();
    WMStatus *status = WMSP_GetStatusStructure();
    OSIntrMode enabled;
    status->valarm_queuedFlag = 0 ;
    status->mp_newFrameFlag = 1 ;
    --status->rssiCounter;
    if (status->rssiCounter == 0) {
        if (status->minRssi == 0xffff) {
            status->minRssi = 4 ;
        }
        native_host_arm7_arm_027e0520((u8)status->minRssi);
        status->linkLevel = native_host_arm7_arm_027e059c();
        status->minRssi = 0xffff;
        status->rssiCounter = 1 ;
    }
    if (status->state == WM_STATE_MP_PARENT) {
        BOOL sleeping;
        BOOL kick;
        enabled = native_host_arm7_arm_037fdd00();
        if (status->child_bitmap == 0) {
            status->mp_count = 0;
            (void)native_host_arm7_arm_037fdd14(enabled);
            return;
        }
        sleeping = (status->mp_count <= 0 || status->mp_limitCount <= 0);
        if (status->mp_count < 0) {
            status->mp_count = 0;
        }
        status->mp_count += (s16)status->mp_current_freq;
        if (status->mp_count > 256 ) {
            status->mp_count = 256 ;
        }
        status->mp_limitCount = (s16)status->mp_current_maxFreq;
        kick = (sleeping && status->mp_count > 0 && status->mp_limitCount > 0);
        (void)native_host_arm7_arm_037fdd14(enabled);
        if (kick) {
            native_host_arm7_arm_027e692c(0xffff);
        }
        if (status->mp_current_minPollBmpMode == 1 ) {
            status->mp_pingCounter--;
            if (status->mp_pingCounter == 0) {
                status->mp_pingFlag = 1 ;
                status->mp_pingCounter = 60 ;
            }
        }
    }
    else if (status->state == WM_STATE_MP_CHILD) {
        BOOL kick = 0 ;
        enabled = native_host_arm7_arm_037fdd00();
        {
            if (status->sendQueueInUse == 1 ) {
                ((void) 0) ;
            } else {
                kick = 1 ;
                status->mp_vsyncFlag = 0 ;
            }
        }
        (void)native_host_arm7_arm_037fdd14(enabled);
        if (kick == 1 ) {
            native_host_arm7_arm_027e6434();
        }
    }
}
