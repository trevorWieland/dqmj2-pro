#include "context.h"

/*
 * native_ov001_02209490.c: 44 bytes at 0x02209490 in ov001 (base 0x021d7240).
 *
 * s32 func(s8 *object)
 *
 * Two independent signed-byte tests: +0x1d adds one, +0x16/+0x17 subtract
 * one (the second byte is only loaded when the first is zero, so the || is
 * the image's conditional-execution pair).
 */
s32 native_ov001_02209490(s8 *object)
{
    s32 value = 0;

    if (object[0x1d] != 0)
        value++;
    if (object[0x16] != 0 || object[0x17] != 0)
        value--;
    return value;
}
