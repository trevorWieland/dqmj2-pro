#include "native_alarm_registration_types.h"
BOOL native_arm7_wram_037fe5c0(void)
{
    if (!OS_IsTickAvailable() || !OS_IsAlarmAvailable())
        return FALSE;
    if (enabled)
        return FALSE;
    OS_CreateAlarm(&alarm);
    u64 now = OS_GetTick();
    OS_SetPeriodicAlarm(&alarm, now + 0x82e, 0x82e, Callback, NULL);
    enabled = TRUE;
    return TRUE;
}
