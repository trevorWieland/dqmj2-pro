#include "native_timer_types.h"
void native_host_arm7_arm_037fb858(u32 index, TimerCallback callback, void *argument) {
    u32 mask = 1UL << (index + 3);
    native_host_arm7_timer_callbacks_038076b0[index].function = callback;
    native_host_arm7_timer_callbacks_038076b0[index].argument = argument;
    native_host_arm7_arm_037fb8f0(mask);
    native_host_arm7_timer_callbacks_038076b0[index].enabled = 1;
}
