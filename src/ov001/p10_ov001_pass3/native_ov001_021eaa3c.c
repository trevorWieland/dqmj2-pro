#include "context.h"

/* native_ov001_021eaa3c.c: 76 bytes at 0x021eaa3c in ov001.
 * s32 func(void): publish the session bytes through 0x021f1354 and mark the
 * 0x02238d7c +0x27 byte 0x1e. */
s32 native_ov001_021eaa3c(void)
{
    s32 result = 0;

    if (native_data_ov001_0222ec84[0] != 0) {
        native_fn_ov001_021f1354(native_data_ov001_02238d7c[0x1a],
                                 native_data_ov001_02238d7c[0x17],
                                 *(u16 *)(native_data_ov001_02238d7c + 0x38), 1);
        native_data_ov001_02238d7c[0x27] = 0x1e;
        result = 1;
    }
    return result;
}
