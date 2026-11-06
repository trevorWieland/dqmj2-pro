#include "native_tick_types.h"
void native_utility_child_arm7_arm_037fd7d4(void *argument) {
    ++native_utility_child_arm7_tick_counter_03805b60;
    if (native_utility_child_arm7_tick_reset_03805b5c != 0) {
        native_utility_child_arm7_timer_control_04000102 = 0;
        native_utility_child_arm7_timer_counter_04000100 = 0;
        native_utility_child_arm7_timer_control_04000102 = 0xC1;
        native_utility_child_arm7_tick_reset_03805b5c = 0;
    }
    native_utility_child_arm7_arm_037fbcf8(0, native_utility_child_arm7_arm_037fd7d4, (void *)0);
}
