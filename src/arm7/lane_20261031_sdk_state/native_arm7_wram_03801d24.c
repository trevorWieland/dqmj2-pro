#include "native_sdk_connected_types.h"
void native_arm7_wram_03801d24(void)
{
    for (s32 i = 0; i < SND_ALARM_COUNT; i++)
    {
        SNDi_Work.alarms[i].enable = 0;
        SNDi_Work.alarms[i].id = 0;
    }
}
