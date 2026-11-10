#include "../context.h"

/* Runs the record's staged action under the overlay's serialised action lock:
   the 0x4C cell of the record is non-zero while another action owns the record,
   so the call is skipped in that case.  0x0202a260/0x0202a1e0/0x0202a280 bracket
   the call as the platform's GX/interrupt guard pair.  The return value is
   whatever the callee produced when the lock was free and is indeterminate when
   the action was skipped, which is how the original falls through. */
u32 native_ov001_021d7508(u32 slotId, s32 arg1, s32 arg2, s32 arg3) {
    u32 result;
    u8 *record;

    record = native_data_ov001_0222fda0 + slotId * 0x78;
    if (*(s32 *)(record + 0x4C) == 0) {
        native_fn_0202a260();
        native_fn_0202a1e0(1);
        result = native_fn_020445e4(arg1, arg2, record + 0x1C, arg3);
        native_fn_0202a280();
    }
    return result;
}
