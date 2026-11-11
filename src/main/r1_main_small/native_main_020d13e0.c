#include "context.h"

extern u8 native_data_021d6bb4[];
extern u8 native_data_021d6bcc[];

/* Publish a mode byte at 0x021d6bb4 and set bit 3 of the signed flag byte at
   0x021d6bcc+0xd1. Both accesses are volatile: the image stores the mode byte
   before reading the flags, while a plain build hoists the flag read above it.
   Unknowns: the meaning of the mode byte and of flag bit 3. */
void native_main_020d13e0(u8 value)
{
    s8 temp_r0;

    M2C_FIELD(native_data_021d6bb4, volatile u8 *, 0) = value;
    temp_r0 = M2C_FIELD(native_data_021d6bcc, volatile s8 *, 0xd1);
    M2C_FIELD(native_data_021d6bcc, volatile s8 *, 0xd1) = temp_r0 | 8;
}
