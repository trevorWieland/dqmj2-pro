#include "native_sdk_connected_types.h"
void native_arm7_wram_03801dac(s32 idx)
{
    OSTick tick;
    OSTick period;

    struct SNDAlarm *alarm = &SNDi_Work.alarms[idx];

    if (alarm->enable != 0)
    {
        OS_CancelAlarm(&alarm->alarm);
        alarm->enable = 0;
    }

    tick = alarm->tick;
    period = alarm->period;
    s32 arg = idx | (alarm->id << 8);

    OS_CreateAlarm(&alarm->alarm);

    if (period == 0)
    {
        OS_SetAlarm(&alarm->alarm, tick, AlarmHandler, (void *)arg);
    }
    else
    {
        OS_SetPeriodicAlarm(&alarm->alarm, tick + OS_GetTick(), period, AlarmHandler, (void *)arg);
    }

    alarm->enable = 1;
}
