#include "native_irq_types.h"
u32 native_host_arm7_arm_037fb928(u32 mask) {
    u32 master = native_host_arm7_arm_037fb8d8();
    u32 old = NATIVE_IE;
    NATIVE_IE = old & ~mask;
    u16 readback = NATIVE_IME;
    NATIVE_IME = master;
    return old;
}
