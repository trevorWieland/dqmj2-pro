#include "context.h"

/* 0x0221C160 holds a pointer to the ov006 slot state; the 16-bit "active slot"
   mask is at +0x02. */
extern u32 native_data_ov006_0221c160;

/* Ask ARM-side code whether the slot may still be used. */
extern s32 native_fn_020143d0(u32 slot);

/* ov006 row 0x02200DF0: 64 bytes. Probe every set bit of the 16-bit active-slot
   mask from slot 1 upwards and fail as soon as one of those slots is refused;
   an empty mask answers 0 without probing. The call at +0x22 targets ARM code
   and is a BLX immediate in the image (13 F6 DE EA). Unknown: what a refused
   slot means and why bit 0 is never probed; the loop counter is 16-bit in the
   source, which is why the image wraps it through LSLS/LSRS after the
   increment. */
s32 native_ov006_02200df0(void)
{
    u16 slot;

    if (((u16 *)native_data_ov006_0221c160)[1] == 0)
        return 0;
    for (slot = 1; slot < 0x10; slot++) {
        if (((u16 *)native_data_ov006_0221c160)[1] & (1 << slot)) {
            if (native_fn_020143d0(slot) == 0)
                return 0;
        }
    }
    return 1;
}
