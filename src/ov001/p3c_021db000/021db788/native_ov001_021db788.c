#include "../context.h"

/* Stores `value` into the signed halfword counter at +0x1F0, clamped to
   [0, 0x021dbcbc(actor)], and returns the value that was there before. */
s32 native_ov001_021db788(u8 *obj, s32 value) {
    s32 old;

    old = *(s16 *)(obj + 0x1F0);
    if (value < 0) {
        value = 0;
    } else if (value > native_fn_ov001_021dbcbc(obj)) {
        value = native_fn_ov001_021dbcbc(obj);
    }
    *(s16 *)(obj + 0x1F0) = (s16)value;
    return old;
}
