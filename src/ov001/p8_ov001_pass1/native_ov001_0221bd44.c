#include "context.h"

/* Report whether the object's flag byte at +0x31E is clear to the overlay
 * control helper at 0x021db578, and convert its answer to a boolean. */
s32 native_ov001_0221bd44(u32 *object)
{
    u8 *record = (u8 *)*object;

    return native_fn_ov001_021db578(record[0x31E] == 0) == 1;
}
