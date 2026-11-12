#include "context.h"

/* native_ov001_02202540.c: 40 bytes at 0x02202540 in ov001.
 * void func(s32 flag, s32 value): when the flag is clear, sign-extend the low
 * byte for 0x022028c8 and forward the value unchanged to 0x02202598. */
void native_ov001_02202540(s32 flag, s32 value)
{
    if (flag != 0)
        return;
    native_fn_ov001_022028c8((s8)value);
    native_fn_ov001_02202598(value);
}
