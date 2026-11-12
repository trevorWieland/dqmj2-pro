#include "context.h"

/* native_ov001_0220b780.c: 20 bytes at 0x0220b780 in ov001.
 * u32 func(u32 value): publish the low byte at 0x0223e088[0x1c] and return it
 * zero-extended. */
u32 native_ov001_0220b780(u32 value)
{
    native_data_ov001_0223e088[0x1c] = (u8)value;
    return value & 0xff;
}
