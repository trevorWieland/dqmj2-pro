#include "../context.h"

/* Applies one mode-coded step to the signed halfword counter at +0x1F2.  Step
   10000 resets the counter and returns the negated previous value; step 10001
   halves it (rounded toward zero) and returns the change; any other step is
   applied as a delta through 0x021db7cc.  While the overlay's step clock is at
   or above 10000 the step is simply negated. */
s32 native_ov001_021db834(u8 *obj, s32 step) {
    s32 old;

    if (native_fn_ov001_021dbd30() >= 10000) {
        return -step;
    }
    if (step == 10000) {
        old = *(s16 *)(obj + 0x1F2);
        *(s16 *)(obj + 0x1F2) = 0;
        return -old;
    }
    if (step == 10001) {
        old = *(s16 *)(obj + 0x1F2);
        *(s16 *)(obj + 0x1F2) = (s16)((old + 1) / 2);
        return *(s16 *)(obj + 0x1F2) - old;
    }
    return native_fn_ov001_021db7cc(obj, -step);
}
