#include "context000.h"

#include "context001.h"

void WMSP_SetWEPKey(OSMessage msg)
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
        MI_CpuCopy8(wepkey, status->wepKey, 80 );
    } else {
        MI_CpuClear8(status->wepKey, 80 );
    }
    {
        WMCallback *cb = (WMCallback *)WMSP_GetBuffer4Callback2Wm9();
        cb->apiid = WM_APIID_SET_WEPKEY;
        cb->errcode = WM_ERRCODE_SUCCESS;
        WMSP_ReturnResult2Wm9((void *)cb);
    }
}
