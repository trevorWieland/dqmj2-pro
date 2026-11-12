#include "context.h"

/* native_ov001_0220409c.c: 92 bytes at 0x0220409c in ov001.
 * void func(void): allocate the 0x1200-byte 4-slot pool, clear it and seed the
 * 0x40 cursor words with 0x7f. */
void native_ov001_0220409c(void)
{
    u8 *buffer;
    s8 i;

    buffer = (u8 *)native_fn_0202a37c(2, 0x1200, 4);
    *(u32 *)native_data_ov001_0223d900 = (u32)buffer;
    native_fn_02008c14(0, buffer, 0x1200);
    i = 0;
    do {
        *(s32 *)native_fn_ov001_02204250(i) = 0x7f;
        i++;
    } while (i < 0x40);
}
