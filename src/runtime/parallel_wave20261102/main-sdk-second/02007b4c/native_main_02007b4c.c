#include "context_00.h"
void native_main_02007b4c (OSAlarm * alarm)
{
    s64 delta;
    OSTick tick = native_fn_02007a9c();
    u16 timerCount;
    OS_SetTimerControl(OS_TIMER_1 , 0);
    delta = (s64)(alarm->fire - tick);
    native_fn_02005cac(OS_TIMER_1 , native_fn_02007e98, ((void *)0) );
    if (delta < 0) {
        timerCount = (u16) ~1;
    } else if (delta < 0x10000)   {
        timerCount = (u16)(~delta);
    } else {
        timerCount = 0;
    }
    OS_SetTimerCount((OSTimer)OS_TIMER_1 , timerCount);
    OS_SetTimerControl(OS_TIMER_1 , (u16)(0x0080 | 0x0040 | OS_TIMER_PRESCALER_64) );
    (void)native_fn_02005d20((1UL << 4) );
}
