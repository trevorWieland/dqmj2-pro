#include "context000.h"

#include "context001.h"

void native_host_arm7_main_027e5f98(void *arg)
{
#pragma unused(arg)
    WMSPWork *p = WMSP_GetSystemWork();
    WMStatus *status = WMSP_GetStatusStructure();
    s32 vcount;
    if (status->valarm_counter >= 60) {
        vcount = GX_GetVCount();
        if (203 <= vcount && vcount < 210 ) {
            GX_SetVCount(vcount);
            status->valarm_counter = 0;
        }
    } else {
        ++status->valarm_counter;
    }
    WmspSetVTSF();
    WmspSetVAlarm((s16)status->mp_parentVCount, native_host_arm7_arm_027e6050, (void *)5 );
}

#include "context002.h"
