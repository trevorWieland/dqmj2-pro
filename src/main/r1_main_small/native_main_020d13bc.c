#include "context.h"

extern u8 native_data_021d6bc0[];
extern u8 native_data_021d6bcc[];

/* Store a word in the 0x021d6bc0 array at `index` and set bit 3 of the signed
   flag byte at 0x021d6bcc+0xd1. Volatile for the same ordering reason as
   0x020d13e0: the image writes the word before reading the flags.
   Unknowns: the array's element type beyond four-byte stride, and flag bit 3. */
void native_main_020d13bc(u32 index, u32 value)
{
    s8 temp_r0;

    M2C_FIELD(native_data_021d6bc0, volatile u32 *, index * 4) = value;
    temp_r0 = M2C_FIELD(native_data_021d6bcc, volatile s8 *, 0xd1);
    M2C_FIELD(native_data_021d6bcc, volatile s8 *, 0xd1) = temp_r0 | 8;
}
