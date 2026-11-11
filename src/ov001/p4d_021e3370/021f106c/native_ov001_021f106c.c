#include "../context.h"

/* 0x021f106c: classify the current mode against the 2 and 8 sentinels. */
u32 native_ov001_021f106c(void) {
    u32 value = native_fn_020443ec();
    return value == 2 || value == 8;
}
