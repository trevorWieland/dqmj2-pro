#include "native_irq_types.h"
u32 native_host_arm7_arm_037fb8d8(void) {
    u32 old = NATIVE_IME;
    NATIVE_IME = 0;
    return old;
}
