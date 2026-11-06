#include "native_alarm_types.h"
void native_utility_child_arm7_arm_037fdaa0(OSAlarm *entry, u64 start, u64 period, OSAlarmHandler handler, void *argument) {
    if (entry == (void *)0 || entry->handler != (void *)0) {
        native_utility_child_arm7_arm_037fe5e0();
    }
    u32 irq = native_utility_child_arm7_arm_037fe41c();
    entry->period = period;
    entry->start = start;
    entry->handler = handler;
    entry->argument = argument;
    native_utility_child_arm7_arm_037fdb90(entry, 0);
    native_utility_child_arm7_arm_037fe430(irq);
}
