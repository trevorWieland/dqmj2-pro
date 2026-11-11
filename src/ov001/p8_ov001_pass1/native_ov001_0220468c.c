#include "context.h"

/* Build the event mask (bit 0 for "always", 2 shifted by the caller's bit index,
 * bit 5 for the trailing flag) and hand it to the overlay event dispatcher with
 * the caller's payload. */
void native_ov001_0220468c(s32 always, s32 payload, s32 bit, s32 flag)
{
    s32 mask = 0;

    if (always == 0)
        mask |= 1;
    mask |= 2 << bit;
    if (flag != 0)
        mask |= 0x20;
    native_fn_ov001_0220459c(payload, mask);
}
