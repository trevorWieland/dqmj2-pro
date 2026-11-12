#include "context.h"

/* native_ov001_02223fe8.c: 56 bytes at 0x02223fe8 in ov001.
 * void func(u32 *out, u8 *entry): clear the slot for each of three records that
 * 0x021db8d0 reports as free. */
void native_ov001_02223fe8(u32 *out, u8 *entry)
{
    s32 i = 0;

    do {
        if (native_fn_ov001_021db8d0(entry) == 0)
            out[i] = 0;
        i++;
        entry += 0x440;
    } while (i < 3);
}
