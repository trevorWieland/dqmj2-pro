#include "native_alarm_types.h"
void native_utility_child_arm7_arm_037fdb1c(OSAlarm *entry, u64 delay, OSAlarmHandler handler, void *argument) {
    if (entry == NULL || entry->handler != NULL) {
        native_utility_child_arm7_arm_037fe5e0();
    }
    u32 irq = native_utility_child_arm7_arm_037fe41c();
    entry->period = 0;
    entry->handler = handler;
    entry->argument = argument;
    u64 now = native_utility_child_arm7_arm_037fd724();
    native_utility_child_arm7_arm_037fdb90(entry, delay + now);
    native_utility_child_arm7_arm_037fe430(irq);
}
