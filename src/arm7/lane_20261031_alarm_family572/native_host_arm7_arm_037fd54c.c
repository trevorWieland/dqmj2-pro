#include "native_alarm_registration_types.h"
void native_host_arm7_arm_037fd54c(OSAlarm *entry, u64 start, u64 period, OSAlarmHandler handler, void *argument) {
    if (entry == (void *)0 || entry->handler != (void *)0) {
        native_host_arm7_arm_037fde70();
    }
    u32 irq = native_host_arm7_arm_037fdd00();
    entry->period = period;
    entry->start = start;
    entry->handler = handler;
    entry->argument = argument;
    native_host_arm7_arm_037fd3b0(entry, 0);
    native_host_arm7_arm_037fdd14(irq);
}
