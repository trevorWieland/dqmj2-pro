#include "context.h"

/* native_ov001_021f927c.c: 60 bytes at 0x021f927c in ov001.
 * s32 func(s32 value): latch the 0x0205f5dc result into 0x02239a08+4 when the
 * 0x0205e73c query accepts the value. */
s32 native_ov001_021f927c(s32 value)
{
    s32 result = 0;

    native_fn_0205e684();
    if (native_fn_0205e73c(value) != 0) {
        *(s32 *)(native_data_ov001_02239a08 + 4) = native_fn_0205f5dc();
        result = 1;
    }
    return result;
}
