#include "native_tick_types.h"
u64 native_utility_child_arm7_arm_037fd724(void) {
    volatile u16 sample;
    volatile u64 upper;
    u32 irq = native_utility_child_arm7_arm_037fe41c();
    sample = native_utility_child_arm7_timer_counter_04000100;
    upper = native_utility_child_arm7_tick_counter_03805b60 & 0xFFFFFFFFFFFFULL;
    if ((native_utility_child_arm7_interrupt_request_04000214 & 8) && !(sample & 0x8000)) { ++upper; }
    native_utility_child_arm7_arm_037fe430(irq);
    return (upper << 16) | sample;
}
