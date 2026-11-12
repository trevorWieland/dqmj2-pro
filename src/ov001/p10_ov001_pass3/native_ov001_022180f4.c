#include "context.h"

/* native_ov001_022180f4.c: 80 bytes at 0x022180f4 in ov001.
 * s32 func(void): publish the 0x0222f20c strip when it is at most 0x5220 bytes. */
s32 native_ov001_022180f4(void)
{
    u8 *strip = native_data_ov001_0222f20c;
    s32 result = 0;
    u32 size = native_fn_0202a8e0(strip);

    if (size <= 0x5220)
        result = native_fn_0202a954(0, strip, native_data_ov001_022445c8, size, 0);
    return result;
}
