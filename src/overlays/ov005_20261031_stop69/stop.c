#include "context.h"
u32 native_ov005_021d9060(void) {
    u32 (*temp_r2)(u32, u32);
    u32 temp_r0;
    u32 temp_r4;
    u32 temp_r5;

    temp_r4 = native_fn_02007ff4();
    temp_r0 = native_fn_ov005_021d90f0();
    switch (temp_r0) {
    case 0:
    case 1:
        break;
    default:
        break;
    case 2:
    case 3:
        temp_r5 = native_fn_02007ff4();
        M2C_FIELD(native_data_ov005_021e78cc, s32 *, 4) = 1;
        temp_r2 = M2C_FIELD(M2C_FIELD(native_data_ov005_021e78cc, void **, 0), u32 (**)(u32, u32), 4);
        if (temp_r2 != NULL) {
            temp_r2(1, 0);
        }
        native_fn_02008008(temp_r5);
        if (native_fn_ov005_021d9124() == 0) {
            native_fn_ov005_021d8788(M2C_FIELD(native_data_ov005_021e78cc, void **, 0) + 0x120, 0);
        }
        break;
    }
    return native_fn_02008008(temp_r4);
}
