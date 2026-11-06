#include "native_irq_dispatch_types.h"
void native_utility_child_arm7_arm_037fbb84(u32 index) {
    u32 mask = 1UL << native_utility_child_arm7_irq_indices_0380581c[index];
    IrqCallback callback = native_utility_child_arm7_callbacks_0380594c[index].function;
    native_utility_child_arm7_callbacks_0380594c[index].function = (void *)0;
    if (callback != (void *)0) {
        callback(native_utility_child_arm7_callbacks_0380594c[index].argument);
    }
    NATIVE_IRQ_CHECK_WORD |= mask;
    if (native_utility_child_arm7_callbacks_0380594c[index].enabled == 0) {
        native_utility_child_arm7_arm_037fbc50(mask);
    }
}
