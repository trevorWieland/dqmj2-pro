#include "../context.h"

/* Queues one action event for the actor.  When the 0x80000 resource is live the
   event kind's directory record (0x021d8dec) must carry the 0x20 flag and the
   actor must be in a non-zero mode, otherwise nothing is queued.  The event is
   submitted through 0x022092c0 with the extra descriptor from the caller; kind 11
   additionally clears the +4 byte of the 0x021e81d0 record (or re-seeds through
   0x021e865c when the count is not positive).  Returns the submission result,
   or 0 when the event was rejected. */
u32 native_ov001_021dbf98(u8 *obj, s32 kind, s32 count, s32 mode, s32 extra) {
    u32 result;
    u8 *entry;

    result = 1;
    if (native_fn_02044424(0x80000) != 0) {
        entry = (u8 *)native_fn_ov001_021d8dec(kind);
        if ((entry[3] & 0x20) != 0) {
            if (obj[0x31E] == 0) {
                result = 0;
            }
        }
    }
    if (result != 0) {
        result = native_fn_022092c0(obj + 0x22C, kind, count, mode, extra);
        if (result != 0) {
            if (kind == 11) {
                if (count > 0) {
                    (native_fn_021e81d0(obj[0x31E], obj[0x31F]))[4] = 0;
                } else {
                    native_fn_021e865c(obj[0x31E], obj[0x31F]);
                }
            }
        }
    }
    return result;
}
