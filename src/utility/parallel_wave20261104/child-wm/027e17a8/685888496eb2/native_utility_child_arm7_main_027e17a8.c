#include "dependency000.h"
#include "dependency001.h"

void native_utility_child_arm7_main_027e17a8(u16 pollbmp)
{
    u32 *buf = native_utility_child_arm7_arm_027e0134();
    WMSPWork *sys = WMSP_GetSystemWork();
    int result;
    if (buf == ((void *)0) ) {
        result = 0 ;
    } else {
        buf[0] = WM_APIID_KICK_MP_PARENT;
        buf[1] = (u32)pollbmp;
        ((void)0) ;
        result = native_utility_child_arm7_arm_037fcccc(&(sys->requestQ), (OSMessage)buf, 0 );
    }
    if (!result) {
        if (sys->wm7buf != ((void *)0) ) {
            WMIndCallback *cb = (WMIndCallback *)native_utility_child_arm7_arm_0380576c();
            cb->apiid = WM_APIID_INDICATION;
            cb->errcode = WM_ERRCODE_FIFO_ERROR;
            cb->state = WM_STATECODE_FIFO_ERROR;
            cb->reason = WM_APIID_KICK_MP_PARENT;
            native_utility_child_arm7_arm_038057c8(cb);
        }
    }
}
