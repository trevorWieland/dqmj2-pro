#include "../context.h"

/* 0x021e3370: load the parameter block for a slot and hand it to the setup pair. */
void native_ov001_021e3370(void) {
    u32 flag = native_fn_ov001_021dba58(0, 2) != 0;
    u32 *params = (u32 *)native_fn_ov001_021d8b4c(flag, 0);
    u8 *slot = native_fn_ov001_021d8b78(flag);

    native_fn_ov001_021e33c8(params[0], params[1], params[2]);
    native_fn_ov001_021e3408(slot);
    native_fn_ov001_021d95b0(native_data_ov001_02238ad4);
}
