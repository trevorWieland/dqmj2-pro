#include "../context.h"

/* Per-frame actor update.  Bit 0 of the 0x35D status byte stops the update
   outright and bit 1 stops it for actors still in phase 0; both are extracted
   with the shift pairs the original uses, and every early exit shares the single
   `return 0`.  The optional 0x02042b3c hook supplies a 12-byte vector that
   replaces the actor's +0x70 staging vector, 0x021d95b0 then commits the
   transform, and phases 1 and 4 advance the actor through 0x021d9494 once its
   12-bit sub-counter reaches the value encoded in its resource block.  Phase 1
   also re-seeds the actor through 0x021db438/0x021da480.  Finally the 0x354
   countdown is decremented and, at zero, the actor is released with the 0x355
   mode. */
u32 native_ov001_021da6e8(u8 *obj) {
    Vector3 staged;
    u8 status;
    s8 phase;
    s8 count;

    status = obj[0x35D];
    if (((u32)(status << 31) >> 31) == 0) {
        phase = *(s8 *)(obj + 0x1E4);
        if (phase != 0 || ((u32)(status << 30) >> 31) == 0) {
            if (native_fn_02042b3c(obj, &staged) != 0) {
                *(Vector3 *)(obj + 0x70) = staged;
            }
            native_fn_ov001_021d95b0(obj);
            if (phase == 4) {
                if (*(s32 *)(*(u32 *)(obj + 0x60)) >=
                    (s32)((*(u16 *)(*(u32 *)(*(u32 *)(obj + 0x60) + 8) + 4) << 12) - 1)) {
                    native_fn_ov001_021d9494(obj, 0, 1);
                }
            } else if (phase == 1) {
                if (*(s32 *)(*(u32 *)(obj + 0x60)) >=
                    (s32)((*(u16 *)(*(u32 *)(*(u32 *)(obj + 0x60) + 8) + 4) << 12) - 1)) {
                    native_fn_ov001_021d9494(obj, 0, 1);
                    native_fn_ov001_021da480(
                        native_fn_ov001_021db438(obj[0x31E], obj[0x31F]), 0);
                }
            }
            count = *(s8 *)(obj + 0x354);
            if (count > 0) {
                *(u8 *)(obj + 0x354) = count - 1;
                if (*(s8 *)(obj + 0x354) == 0) {
                    native_fn_ov001_021d9494(obj, obj[0x355], 0);
                }
            }
        }
    }
    return 0;
}

