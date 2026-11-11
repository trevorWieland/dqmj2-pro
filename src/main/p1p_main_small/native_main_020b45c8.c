#include "context.h"

/* Store a big-endian halfword across two bytes. */
void native_main_020b45c8(u8 *destination, u32 offset, s32 value)
{
    destination[offset] = (u8)(value >> 8);
    destination[offset + 1] = (u8)value;
}
