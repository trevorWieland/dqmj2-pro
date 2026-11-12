#include "context.h"

/* native_ov001_0220b75c.c: 20 bytes at 0x0220b75c in ov001.
 * u32 func(u32 value): publish the low byte at 0x0223e088[0x1b] and return it
 * zero-extended. */
u32 native_ov001_0220b75c(u32 value)
{
    native_data_ov001_0223e088[0x1b] = (u8)value;
    return value & 0xff;
}
