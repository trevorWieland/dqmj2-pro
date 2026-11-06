#include "native_alarm_types.h"
void native_utility_child_arm7_arm_037fda10(OSAlarm *entry) {
    u32 irq = native_utility_child_arm7_arm_037fe41c();
    if (entry->handler == NULL) {
        native_utility_child_arm7_arm_037fe430(irq);
        return;
    }
    OSAlarm *next = entry->next;
    if (next == NULL) {
        native_utility_child_arm7_alarm_queue_03805b6c.tail = entry->previous;
    } else {
        next->previous = entry->previous;
    }
    OSAlarm *previous = entry->previous;
    if (previous != NULL) {
        previous->next = next;
    } else {
        native_utility_child_arm7_alarm_queue_03805b6c.head = next;
        if (next != NULL) { native_utility_child_arm7_arm_037fdd30(next); }
    }
    entry->handler = NULL;
    entry->period = 0;
    native_utility_child_arm7_arm_037fe430(irq);
}
