#include "context_00.h"
void native_main_02007e10 (OSAlarm * alarm)
{
    OSAlarm * next;
    u32 enabled;
    ((void) 0) ;
    ((void) 0) ;
    enabled = native_fn_02007ff4();
    if (alarm->handler == ((void *)0) ) {
        (void)native_fn_02008008(enabled);
        return;
    }
    next = alarm->next;
    if (next == ((void *)0) ) {
        native_data_main_020e3704.field_0004.tail = alarm->prev;
    } else {
        next->prev = alarm->prev;
    }
    if (alarm->prev) {
        alarm->prev->next = next;
    } else {
        native_data_main_020e3704.field_0004.head = next;
        if (next) {
            native_fn_02007b4c(next);
        }
    }
    alarm->handler = ((void *)0) ;
    alarm->period = 0;
    (void)native_fn_02008008(enabled);
}
