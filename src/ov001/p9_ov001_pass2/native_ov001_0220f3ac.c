#include "context.h"

/*
 * native_ov001_0220f3ac.c: 72 bytes at 0x0220f3ac in ov001 (base 0x021d7240).
 *
 * s32 func(u8 *values, s32 value)
 *
 * Same sentinel scan; entry 0x34 selects value / 10.  The magic multiply
 * is mwcc's signed divide by 10.
 */
s32 native_ov001_0220f3ac(u8 *values, s32 value)
{
    s32 i;

    for (i = 0; i < 0x40 && values[i] != 0; i++) {
        if (values[i] == 0x34)
            return value / 10;
    }
    return 0;
}
