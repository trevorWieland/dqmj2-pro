#include "context.h"

/* native_ov001_0221807c.c: 72 bytes at 0x0221807c in ov001.
 * s32 func(void): publish the 0x0222f1fc strip when it is at most 0x500 bytes. */
s32 native_ov001_0221807c(void)
{
    u8 *strip = native_data_ov001_0222f1fc;
    s32 result = 0;
    u32 size = native_fn_0202a8e0(strip);

    if (size <= 0x500)
        result = native_fn_0202a954(0, strip, native_data_ov001_022430c8, size, 0);
    return result;
}
