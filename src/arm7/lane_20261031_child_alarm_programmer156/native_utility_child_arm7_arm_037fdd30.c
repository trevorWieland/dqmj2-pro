#include "native_alarm_types.h"
void native_utility_child_arm7_arm_037fdd30(OSAlarm *entry) {
    u64 now = native_utility_child_arm7_arm_037fd724();
    native_utility_child_arm7_timer_control_04000106 = 0;
    s64 delta = (s64)(entry->fire - now);
    native_utility_child_arm7_arm_037fbcf8(1, native_utility_child_arm7_arm_037fd900, NULL);
    unsigned short count = 0;
    if (delta < 0) {
        count = 0xFFFE;
    } else if (delta < 0x10000) {
        count = (unsigned short)~delta;
    }
    native_utility_child_arm7_timer_counter_04000104 = count;
    native_utility_child_arm7_timer_control_04000106 = 0xC1;
    native_utility_child_arm7_arm_037fbc8c(16);
}
