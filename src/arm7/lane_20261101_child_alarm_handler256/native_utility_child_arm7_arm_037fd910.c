#include "native_alarm_types.h"
void native_utility_child_arm7_arm_037fd910(void) {
    *(volatile unsigned short *)0x04000106 = 0;
    native_utility_child_arm7_arm_037fbc50(16);
    NATIVE_IRQ_CHECK_WORD |= 16;
    u64 now = native_utility_child_arm7_arm_037fd724();
    OSAlarm *entry = native_utility_child_arm7_alarm_queue_03805b6c.head;
    if (entry == (void *)0) {
        return;
    }
    if (now < entry->fire) {
        native_utility_child_arm7_arm_037fdd30(entry);
        return;
    }
    OSAlarm *next = entry->next;
    native_utility_child_arm7_alarm_queue_03805b6c.head = next;
    if (next == (void *)0) {
        native_utility_child_arm7_alarm_queue_03805b6c.tail = (void *)0;
    } else {
        next->previous = (void *)0;
    }
    OSAlarmHandler callback = entry->handler;
    if (entry->period == 0) {
        entry->handler = (void *)0;
    }
    if (callback != (void *)0) {
        callback(entry->argument);
    }
    if (entry->period != 0) {
        entry->handler = callback;
        native_utility_child_arm7_arm_037fdb90(entry, 0);
    }
    entry = native_utility_child_arm7_alarm_queue_03805b6c.head;
    if (entry != (void *)0) {
        native_utility_child_arm7_arm_037fdd30(entry);
    }
}
