#include "native_timer_types.h"
void native_host_arm7_arm_037fd128(void) {
    if (native_host_arm7_timer_state_03807898.initialized == 0) {
        native_host_arm7_timer_state_03807898.initialized = 1;
        native_host_arm7_arm_037fd10c(0);
        native_host_arm7_timer_state_03807898.counter = 0;
        NATIVE_TIMER_CONTROL = 0;
        NATIVE_TIMER_COUNTER = 0;
        NATIVE_TIMER_CONTROL = 0xC1;
        native_host_arm7_arm_037fb7bc(8,native_host_arm7_arm_037fd1b4);
        native_host_arm7_arm_037fb8f0(8);
        native_host_arm7_timer_state_03807898.reset = 0;
    }
}
