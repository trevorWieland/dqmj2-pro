#include "context.h"

/* Same flag test as its sibling, but the helper's answer is compared against 2:
 * the state counts as reached when it is at least 2. */
s32 native_ov001_0221be4c(u32 *object)
{
    u8 *record = (u8 *)*object;

    return native_fn_ov001_021db578(record[0x31E] == 0) >= 2;
}
