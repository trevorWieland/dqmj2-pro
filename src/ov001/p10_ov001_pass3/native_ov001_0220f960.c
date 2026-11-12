#include "context.h"

/* native_ov001_0220f960.c: 68 bytes at 0x0220f960 in ov001.
 * s32 func(s32 a, s32 b): same accumulator with the 0x3a service id. */
s32 native_ov001_0220f960(s32 a, s32 b)
{
    s32 result = 0;

    if (native_fn_0207b674(0x3a, a) > 0)
        result += (b + 5) / 10;
    return result;
}
