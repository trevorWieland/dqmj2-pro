#include "native_irq_callback_types.h"
void native_utility_child_arm7_arm_037fbcf8(u32 index, TimerCallback callback, void *argument) {
    u32 mask = 1UL << (index + 3);
    native_utility_child_arm7_timer_callbacks_0380597c[index].function = callback;
    native_utility_child_arm7_timer_callbacks_0380597c[index].argument = argument;
    native_utility_child_arm7_arm_037fbc8c(mask);
    native_utility_child_arm7_timer_callbacks_0380597c[index].enabled = 1;
}
