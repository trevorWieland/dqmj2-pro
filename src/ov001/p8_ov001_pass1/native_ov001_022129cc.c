#include "context.h"

/* Fixed-point scale: pick a signed 16-bit factor from the 4-byte-entry table at
 * 0x020d3fe0 with the selector scaled by 182/16, then multiply by the second
 * argument and shift the Q12 product down. */
s32 native_ov001_022129cc(s32 selector, s32 value)
{
    s32 index = (selector * 0xB6) >> 4;
    s16 factor = *(s16 *)(native_data_020d3fe0 + index * 4);

    return (value * factor) >> 12;
}
