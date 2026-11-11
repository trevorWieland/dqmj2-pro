#include "../context.h"

/* 0x021e3438: copy the three-word selection block when both gate bytes are set. */
u32 native_ov001_021e3438(void) {
    Params local;
    u32 result = 0;

    if (native_data_ov001_02238ad4[0x1e8] != 0 && native_data_ov001_02238ad4[0x1e9] != 0) {
        if (native_fn_02042b3c(native_data_ov001_02238ad4, &local) != 0) {
            *(Params *)native_data_ov001_02238b44 = local;
            native_fn_ov001_021d95b0(native_data_ov001_02238ad4);
            result = 1;
        }
    }
    return result;
}
