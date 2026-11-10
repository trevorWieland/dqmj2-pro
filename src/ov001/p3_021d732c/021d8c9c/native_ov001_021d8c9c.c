#include "../context.h"

/* Returns the live asset handle stored in the 0x60 cell of the 0x022316bc state
   block when it is positive, and 0 when no asset is bound.  0x021eeb70 releases
   or resolves the handle; the negative/zero case short-circuits. */
u32 native_ov001_021d8c9c(void) {
    s32 handle;
    u32 result;

    handle = *(s16 *)(native_data_ov001_022316bc + 0x60);
    result = 0;
    if (handle > 0) {
        result = native_fn_ov001_021eeb70(handle);
    }
    return result;
}
