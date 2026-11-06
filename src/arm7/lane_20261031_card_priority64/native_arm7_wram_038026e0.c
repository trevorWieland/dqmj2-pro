#include "native_card_priority_types.h"
u32 native_arm7_wram_038026e0(u32 priority)
{
    CardCommon *state=&CARD_COMMON;
    u32 irq=native_host_arm7_fn_037fdd00();
    u32 previous=state->priority;
    state->priority=priority;
    native_host_arm7_fn_037fc3c0(state->thread,priority);
    native_host_arm7_fn_037fdd14(irq);
    return previous;
}
