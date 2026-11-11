#include "context.h"

extern u8 native_data_021c72a0[];

/* Replace the byte at +3 of the 0x021c72a0 block with the caller's value when it
   is in 1..15, and return the previous byte either way.
   Unknowns: what the block is, and why the accepted range starts at one. */
u32 native_main_02083e08(u32 value)
{
    u8 old = M2C_FIELD(native_data_021c72a0, u8 *, 3);

    if ((u32)(value - 1) <= 14)
        M2C_FIELD(native_data_021c72a0, u8 *, 3) = (u8)value;
    return old;
}
