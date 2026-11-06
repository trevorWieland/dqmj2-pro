#include "dependency000.h"
#include "dependency001.h"

void native_host_arm7_main_027e5440(OSMessage msg)
{
    u32 *buf = (u32 *)msg;
    WMStatus *status = WMSP_GetStatusStructure();
    u16 *wepkey;
    status->wepMode = (u16)buf[1];
    switch (status->wepMode) {
    case 0 :
        status->wep_flag = 0 ;
        break;
    case 1 :
    case 2 :
    case 3 :
        status->wep_flag = 1 ;
        break;
    default:
        status->wep_flag = 0 ;
    }
    if (status->wep_flag == 1 ) {
        wepkey = (u16 *)buf[2];
        native_host_arm7_arm_037fe12c(wepkey, status->wepKey, 80 );
    } else {
        MI_CpuClear8(status->wepKey, 80 );
    }
    {
        WMCallback *cb = (WMCallback *)native_host_arm7_arm_038073f0();
        cb->apiid = WM_APIID_SET_WEPKEY;
        cb->errcode = WM_ERRCODE_SUCCESS;
        native_host_arm7_arm_038073a4((void *)cb);
    }
}
