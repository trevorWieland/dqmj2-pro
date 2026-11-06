#include "context_00.h"
void native_main_02007ea8 (void)
{
    OSTick tick;
    OSAlarm * alarm;
    OSAlarm * next;
    OSAlarmHandler handler;
    OS_SetTimerControl(OS_TIMER_1 , 0);
    (void)native_fn_02005d50((1UL << 4) );
    OS_SetIrqCheckFlag((1UL << 4) );
    tick = native_fn_02007a9c();
    alarm = native_data_main_020e3704.field_0004.head;
    if (alarm == ((void *)0) ) {
        return;
    }
    if (tick < alarm->fire) {
        native_fn_02007b4c(alarm);
        return;
    }
    next = alarm->next;
    native_data_main_020e3704.field_0004.head = next;
    if (next == ((void *)0) ) {
        native_data_main_020e3704.field_0004.tail = ((void *)0) ;
    } else {
        next->prev = ((void *)0) ;
    }
    handler = alarm->handler;
    if (alarm->period == 0) {
        alarm->handler = ((void *)0) ;
    }
    if (handler) {
        (handler) (alarm->arg);
    }
    if (alarm->period > 0) {
        alarm->handler = handler;
        native_fn_02007c78(alarm, 0);
    }
    if (native_data_main_020e3704.field_0004.head) {
        native_fn_02007b4c(native_data_main_020e3704.field_0004.head);
    }
}
