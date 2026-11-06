#include "context_00.h"
void native_main_02007c78 (OSAlarm * alarm, OSTick fire)
{
    OSAlarm * prev;
    OSAlarm * next;
    if (alarm->period > 0) {
        OSTick tick = native_fn_02007a9c();
        fire = alarm->start;
        if (alarm->start < tick) {
            fire += alarm->period * ((tick - alarm->start) / alarm->period + 1);
        }
    }
    alarm->fire = fire;
    for (next = native_data_main_020e3704.field_0004.head; next; next = next->next) {
        if ((s64)(fire - next->fire) >= 0) {
            continue;
        }
        alarm->prev = next->prev;
        next->prev = alarm;
        alarm->next = next;
        prev = alarm->prev;
        if (prev) {
            prev->next = alarm;
        } else {
            native_data_main_020e3704.field_0004.head = alarm;
            native_fn_02007b4c(alarm);
        }
        return;
    }
    alarm->next = 0;
    prev = native_data_main_020e3704.field_0004.tail;
    native_data_main_020e3704.field_0004.tail = alarm;
    alarm->prev = prev;
    if (prev) {
        prev->next = alarm;
    } else {
        native_data_main_020e3704.field_0004.head = native_data_main_020e3704.field_0004.tail = alarm;
        native_fn_02007b4c(alarm);
    }
}
