#include "context.h"

/* native_ov001_0220f91c.c: 68 bytes at 0x0220f91c in ov001.
 * s32 func(s32 a, s32 b): when the 0x0f/2 probe is positive, add a tenth of
 * b+5 to the zeroed accumulator. */
s32 native_ov001_0220f91c(s32 a, s32 b)
{
    s32 result = 0;

    if (native_fn_0207b674(0x0f, a) > 0)
        result += (b + 5) / 10;
    return result;
}
