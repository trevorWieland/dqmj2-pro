#include "context.h"

/* native_ov001_02218304.c: 72 bytes at 0x02218304 in ov001. */
s32 native_ov001_02218304(void)
{
    u8 *strip = native_data_ov001_0222f248;
    s32 result = 0;
    u32 size = native_fn_0202a8e0(strip);

    if (size <= 0x800)
        result = native_fn_0202a954(0, strip, native_data_ov001_022435c8, size, 0);
    return result;
}
