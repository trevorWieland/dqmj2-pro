#include "native_sdk_connected_types.h"
void native_arm7_wram_03801d50(s32 idx, OSTick tick, OSTick period, u32 id)
{
    struct SNDAlarm *alarm = &SNDi_Work.alarms[idx];

    if (alarm->enable)
    {
        OS_CancelAlarm(&alarm->alarm);
        alarm->enable = 0;
    }

    alarm->tick = tick;
    alarm->period = period;
    alarm->id = (u8)id;
}
