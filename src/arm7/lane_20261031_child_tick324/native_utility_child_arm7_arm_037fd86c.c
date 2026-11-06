#include "native_tick_types.h"
u32 native_utility_child_arm7_arm_037fd86c(void) {
    if (native_utility_child_arm7_tick_initialized_03805b58 == 0) {
        native_utility_child_arm7_tick_initialized_03805b58 = 1;
        native_utility_child_arm7_arm_037fd708(0);
        native_utility_child_arm7_tick_counter_03805b60 = 0;
        native_utility_child_arm7_timer_control_04000102 = 0;
        native_utility_child_arm7_timer_counter_04000100 = 0;
        native_utility_child_arm7_timer_control_04000102 = 0xC1;
        native_utility_child_arm7_arm_037fbd44(8, native_utility_child_arm7_arm_037fd7d4);
        native_utility_child_arm7_arm_037fbc8c(8);
        native_utility_child_arm7_tick_reset_03805b5c = 0;
        return (u32)&native_utility_child_arm7_tick_reset_03805b5c;
    }
    return (u32)&native_utility_child_arm7_tick_initialized_03805b58;
}
