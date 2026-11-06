#include "native_alarm_types.h"
void native_utility_child_arm7_arm_037fdb90(OSAlarm *entry, u64 fire) {
    if (entry->period != 0) {
        u64 now = native_utility_child_arm7_arm_037fd724();
        fire = entry->start;
        if (fire < now) {
            fire += entry->period * (((now - fire) / entry->period) + 1);
        }
    }
    entry->fire = fire;
    OSAlarm *next = native_utility_child_arm7_alarm_queue_03805b6c.head;
    while (next != (void *)0) {
        if ((signed long long)(fire - next->fire) < 0) {
            entry->previous = next->previous;
            next->previous = entry;
            entry->next = next;
            if (entry->previous != (void *)0) {
                entry->previous->next = entry;
            } else {
                native_utility_child_arm7_alarm_queue_03805b6c.head = entry;
                native_utility_child_arm7_arm_037fdd30(entry);
            }
            return;
        }
        next = next->next;
    }
    entry->next = (void *)0;
    OSAlarm *previous = native_utility_child_arm7_alarm_queue_03805b6c.tail;
    native_utility_child_arm7_alarm_queue_03805b6c.tail = entry;
    entry->previous = previous;
    if (previous != (void *)0) {
        previous->next = entry;
    } else {
        native_utility_child_arm7_alarm_queue_03805b6c.tail = entry;
        native_utility_child_arm7_alarm_queue_03805b6c.head = entry;
        native_utility_child_arm7_arm_037fdd30(entry);
    }
}
