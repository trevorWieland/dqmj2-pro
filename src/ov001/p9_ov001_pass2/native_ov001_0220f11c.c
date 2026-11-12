#include "context.h"

/*
 * native_ov001_0220f11c.c: 68 bytes at 0x0220f11c in ov001 (base 0x021d7240).
 *
 * s32 func(u8 *values, s32 fallback)
 *
 * 0x40-byte scan whose loop condition is the sentinel test itself
 * (i < 0x40 && values[i] != 0): 8 yields -1, 9 yields 9999, otherwise the
 * fallback is returned.  The && form is what rotates the load into the
 * back edge.
 */
s32 native_ov001_0220f11c(u8 *values, s32 fallback)
{
    s32 i;

    for (i = 0; i < 0x40 && values[i] != 0; i++) {
        if (values[i] == 8)
            return -1;
        if (values[i] == 9)
            return 9999;
    }
    return fallback;
}
