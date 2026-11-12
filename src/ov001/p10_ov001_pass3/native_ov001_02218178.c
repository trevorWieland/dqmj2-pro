#include "context.h"

/* native_ov001_02218178.c: 72 bytes at 0x02218178 in ov001.
 * s32 func(s32 index, u32 *out0, u32 *out1): publish the two halfword columns
 * of 0x022445c8 for a table index in 0..0xff.  The shared fail return is what
 * makes both range tests branch to one 0 epilogue. */
s32 native_ov001_02218178(s32 index, u32 *out0, u32 *out1)
{
    if (index < 0)
        goto fail;
    if (index >= 0x100)
        goto fail;
    *out0 = *(u16 *)(native_data_ov001_022445c8 + index * 4);
    *out1 = *(u16 *)(native_data_ov001_022445ca + index * 4);
    return 1;
fail:
    return 0;
}
