#include "native_timer_types.h"
u64 native_host_arm7_arm_037fd21c(void) {
    volatile u16 sample;
    volatile u64 upper;
    u32 irq = native_host_arm7_arm_037fdd00();
    sample = NATIVE_TIMER_COUNTER;
    upper = *(volatile u64 *)&native_host_arm7_timer_state_03807898.counter & 0xFFFFFFFFFFFFULL;
    if ((NATIVE_IRQ_REQUEST & 8) && !(sample & 0x8000)) { ++upper; }
    native_host_arm7_arm_037fdd14(irq);
    return (upper << 16) | sample;
}
