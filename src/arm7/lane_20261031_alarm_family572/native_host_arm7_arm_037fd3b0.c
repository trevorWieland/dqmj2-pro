#include "native_alarm_registration_types.h"
void native_host_arm7_arm_037fd3b0(OSAlarm *entry, u64 fire) {
    if (entry->period != 0) {
        u64 now = native_host_arm7_arm_037fd21c();
        fire = entry->start;
        if (fire < now) {
            fire += entry->period * (((now - fire) / entry->period) + 1);
        }
    }
    entry->fire = fire;
    OSAlarm *next = native_host_arm7_alarm_queue_038078a8.head;
    while (next != (void *)0) {
        if ((signed long long)(fire - next->fire) < 0) {
            entry->previous = next->previous;
            next->previous = entry;
            entry->next = next;
            if (entry->previous != (void *)0) {
                entry->previous->next = entry;
            } else {
                native_host_arm7_alarm_queue_038078a8.head = entry;
                native_host_arm7_arm_037fd2c0(entry);
            }
            return;
        }
        next = next->next;
    }
    entry->next = (void *)0;
    OSAlarm *previous = native_host_arm7_alarm_queue_038078a8.tail;
    native_host_arm7_alarm_queue_038078a8.tail = entry;
    entry->previous = previous;
    if (previous != (void *)0) {
        previous->next = entry;
    } else {
        native_host_arm7_alarm_queue_038078a8.tail = entry;
        native_host_arm7_alarm_queue_038078a8.head = entry;
        native_host_arm7_arm_037fd2c0(entry);
    }
}
