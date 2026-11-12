#include "context.h"

/*
 * native_ov001_0220f3f4.c: 72 bytes at 0x0220f3f4 in ov001 (base 0x021d7240).
 *
 * s32 func(u8 *values, s32 value)
 *
 * Same sentinel scan; entry 0x35 selects value / 5.
 */
s32 native_ov001_0220f3f4(u8 *values, s32 value)
{
    s32 i;

    for (i = 0; i < 0x40 && values[i] != 0; i++) {
        if (values[i] == 0x35)
            return value / 5;
    }
    return 0;
}
