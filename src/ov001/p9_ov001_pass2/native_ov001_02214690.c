#include "context.h"

/*
 * native_ov001_02214690.c: 68 bytes at 0x02214690 in ov001 (base 0x021d7240).
 *
 * s32 func(void)
 *
 * Publishes the 5 state when the overlay service accepts the state block
 * word at 0x02242b50+0x10, the byte at +6 and the "mode is 1" flag.
 */
extern u8 native_data_ov001_02242b50[];
extern s32 native_fn_ov001_02216ac4(u32 value, u8 arg1, s32 arg2);

s32 native_ov001_02214690(void)
{
    s32 mode = native_data_ov001_02242b50[7] == 1;

    if (native_fn_ov001_02216ac4(*(u32 *)(native_data_ov001_02242b50 + 0x10),
                                 native_data_ov001_02242b50[6], mode) != 0)
        native_data_ov001_02242b50[2] = 5;
    return 0;
}
