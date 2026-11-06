#include "native_timer_types.h"
void native_host_arm7_arm_037fd1b4(void *argument) {
    ++native_host_arm7_timer_state_03807898.counter;
    if (native_host_arm7_timer_state_03807898.reset != 0) {
        NATIVE_TIMER_CONTROL = 0;
        NATIVE_TIMER_COUNTER = 0;
        NATIVE_TIMER_CONTROL = 0xC1;
        native_host_arm7_timer_state_03807898.reset = 0;
    }
    native_host_arm7_arm_037fb858(0, native_host_arm7_arm_037fd1b4, (void *)0);
}
