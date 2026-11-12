#include "context.h"

/* native_ov001_022181c0.c: 72 bytes at 0x022181c0 in ov001. */
s32 native_ov001_022181c0(void)
{
    u8 *strip = native_data_ov001_0222f21c;
    s32 result = 0;
    u32 size = native_fn_0202a8e0(strip);

    if (size <= 0x200)
        result = native_fn_0202a954(0, strip, native_data_ov001_02242ec8, size, 0);
    return result;
}
