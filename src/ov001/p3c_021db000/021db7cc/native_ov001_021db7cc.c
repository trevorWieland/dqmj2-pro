#include "../context.h"

/* Adds `delta` to the signed halfword counter at +0x1F2, clamped to
   [0, 0x021dbcf0(actor)], and returns the applied change.  While the overlay's
   step clock (0x021dbd30) is at or above 10000 the delta is returned unchanged
   and the counter is left alone. */
s32 native_ov001_021db7cc(u8 *obj, s32 delta) {
    s32 old;
    s32 value;

    if (ov001_record_field_1f2_021dbd30() >= 10000) {
        return delta;
    }
    old = *(s16 *)(obj + 0x1F2);
    value = old + delta;
    if (value < 0) {
        value = 0;
    } else if (value > native_fn_ov001_021dbcf0(obj)) {
        value = native_fn_ov001_021dbcf0(obj);
    }
    *(s16 *)(obj + 0x1F2) = (s16)value;
    return *(s16 *)(obj + 0x1F2) - old;
}
