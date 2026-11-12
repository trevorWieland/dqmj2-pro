#include "context.h"

/* native_ov001_0220b738.c: 20 bytes at 0x0220b738 in ov001.
 * u32 func(u32 value): publish the low byte at 0x0223e088[0x1a] and return it
 * zero-extended; the explicit mask is the image's trailing and #0xff. */
u32 native_ov001_0220b738(u32 value)
{
    native_data_ov001_0223e088[0x1a] = (u8)value;
    return value & 0xff;
}
