#include "native_irq_mmio_types.h"
u32 native_utility_child_arm7_arm_037fbcc4(u32 mask) {
    u16 master = native_utility_child_arm7_interrupt_master_04000208;
    native_utility_child_arm7_interrupt_master_04000208 = 0;
    u32 old = native_utility_child_arm7_interrupt_mask_04000210;
    native_utility_child_arm7_interrupt_mask_04000210 = mask;
    u16 readback = native_utility_child_arm7_interrupt_master_04000208;
    native_utility_child_arm7_interrupt_master_04000208 = master;
    return old;
}
