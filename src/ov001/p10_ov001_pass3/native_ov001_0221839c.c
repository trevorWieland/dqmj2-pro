#include "context.h"

/* native_ov001_0221839c.c: 72 bytes at 0x0221839c in ov001. */
s32 native_ov001_0221839c(void)
{
    u8 *strip = native_data_ov001_0222f260;
    s32 result = 0;
    u32 size = native_fn_0202a8e0(strip);

    if (size <= 0x800)
        result = native_fn_0202a954(0, strip, native_data_ov001_02242e4c, size, 0);
    return result;
}
