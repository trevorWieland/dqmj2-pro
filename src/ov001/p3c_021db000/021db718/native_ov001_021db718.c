#include "../context.h"

/* Adds `delta` to the signed halfword counter at +0x1F0 and returns the applied
   change.  The result is clamped to [0, 0x021dbcbc(actor)]; when the platform
   reports the 0x40000000 resource as live and the actor is in mode 1, no change
   is made. */
s32 native_ov001_021db718(u8 *obj, s32 delta) {
    s32 old;
    s32 value;

    if (native_fn_02044424(0x40000000) != 0) {
        if (obj[0x31E] == 1) {
            return 0;
        }
    }
    old = *(s16 *)(obj + 0x1F0);
    value = old + delta;
    if (value < 0) {
        value = 0;
    } else if (value > native_fn_ov001_021dbcbc(obj)) {
        value = native_fn_ov001_021dbcbc(obj);
    }
    *(s16 *)(obj + 0x1F0) = (s16)value;
    return *(s16 *)(obj + 0x1F0) - old;
}
