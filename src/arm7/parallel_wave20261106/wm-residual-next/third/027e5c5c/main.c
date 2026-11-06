#include "context000.h"

#include "context001.h"

void native_host_arm7_main_027e5c5c(void *arg)
{
#pragma unused(arg)
    WMSPWork *p = WMSP_GetSystemWork();
    WMStatus *status = WMSP_GetStatusStructure();
    status->v_tsf = *(u16 *)(((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x30)) ;
    if (status->v_tsf_bak != status->v_tsf) {
        status->v_tsf_bak = status->v_tsf;
        WmspCalcVRemain();
    }
    if (status->v_remain > ((u32)(1000000ULL * (2) * (256 + 99) * 6 / 33513982)) ) {
        WmspSetVAlarm(208 ,
            native_host_arm7_main_027e5dc0,
            (void *)2 );
        ((void)0) ;
    } else {
        status->VSyncFlag = 1 ;
        WmspSetVAlarm((s16)status->mp_childVCount, native_host_arm7_main_027e5e80, (void *)4 );
        ((void)0) ;
    }
}

#include "context002.h"
