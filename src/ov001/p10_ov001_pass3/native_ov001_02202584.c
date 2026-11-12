#include "context.h"

/* native_ov001_02202584.c: 20 bytes at 0x02202584 in ov001.
 * s32 func(s32 value): sign-extend the low byte and tail-call 0x022028c8
 * through the address in the pool (indirect call, hence bx ip). */
s32 native_ov001_02202584(s32 value)
{
    return native_fn_ov001_022028c8((s8)value);
}
