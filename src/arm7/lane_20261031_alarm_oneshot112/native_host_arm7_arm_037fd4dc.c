#include "native_alarm_registration_types.h"
void native_host_arm7_arm_037fd4dc(OSAlarm *entry, u64 delay, OSAlarmHandler handler, void *argument) {
    if (entry == NULL || entry->handler != NULL) {
        native_host_arm7_arm_037fde70();
    }
    u32 irq = native_host_arm7_arm_037fdd00();
    entry->period = 0;
    entry->handler = handler;
    entry->argument = argument;
    u64 now = native_host_arm7_arm_037fd21c();
    native_host_arm7_arm_037fd3b0(entry, delay + now);
    native_host_arm7_arm_037fdd14(irq);
}
