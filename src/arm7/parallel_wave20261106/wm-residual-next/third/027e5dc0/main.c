#include "context000.h"

#include "context001.h"

void native_host_arm7_main_027e5dc0(void *arg)
{
#pragma unused(arg)
    WMSPWork *p = WMSP_GetSystemWork();
    WMStatus *status = WMSP_GetStatusStructure();
    WmspExpendVRemain();
    if (status->v_remain >= ((u32)(1000000ULL * (2) * (256 + 99) * 6 / 33513982)) ) {
        status->VSyncFlag = 0 ;
    }
    WmspSetVAlarm((s16)status->mp_childVCount, native_host_arm7_main_027e5e80, (void *)4 );
}

#include "context002.h"
