#include "context.h"

/*
 * native_ov001_022141f0.c: 68 bytes at 0x022141f0 in ov001 (base 0x021d7240).
 *
 * s32 func(void)
 *
 * Advances the signed byte cursor at 0x02242aac, reloads it, indexes the
 * 12-byte-record table at 0x02242ab4 with it, and publishes 3 when the
 * record word is zero, 1 otherwise.  Returns 0.
 */
extern u8 native_data_ov001_02242aac[];
extern u8 native_data_ov001_02242ab4[];

s32 native_ov001_022141f0(void)
{
    s8 index;

    native_data_ov001_02242aac[0] = (u8)((s8)native_data_ov001_02242aac[0] + 1);
    index = (s8)native_data_ov001_02242aac[0];
    if (*(u32 *)(native_data_ov001_02242ab4 + index * 12) == 0)
        native_data_ov001_02242aac[1] = 3;
    else
        native_data_ov001_02242aac[1] = 1;
    return 0;
}
