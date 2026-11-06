#include "context.h"
u32 native_ov000_021e3c0c(s32 arg0) {
    s32 temp_r0;
    u32 temp_r0_2;
    u32 var_r4;
    s32 temp_r5;
    float rounded;

    var_r4 = 0;
    temp_r0 = (s32) native_fn_ov000_021e3444();
    if (temp_r0 >= 0) {
        temp_r5 = (temp_r0 * 0x34) + (s32) native_data_ov000_02234388;
        native_fn_ov000_021e3478(temp_r5, arg0, 3);
        if (native_fn_0201d914(arg0 + 2, native_data_ov000_0222ec40, 7) == 0) {
            M2C_FIELD(temp_r5, s8 *, 0x1E) = (s8) native_fn_0201f274(arg0 + 9);
            M2C_FIELD(temp_r5, s8 *, 0x20) = 2;
        } else if (native_fn_0201d914(arg0 + 2, native_data_ov000_0222ec48, 7) == 0) {
            temp_r0_2 = arg0 + 9;
            if ((s32) native_fn_0201f274(arg0 + 9) > 0) {
                rounded = native_fn_02024e0c(0.5f, native_fn_02025a28((s32)(native_fn_0201f274(temp_r0_2) << 0xC)));
            } else {
                rounded = native_fn_02025ca4(native_fn_02025a28((s32)(native_fn_0201f274(temp_r0_2) << 0xC)), 0.5f);
            }
            native_fn_020282a8(0, native_fn_020259b4(rounded));
            M2C_FIELD(temp_r5, s8 *, 0x1E) = 0;
            M2C_FIELD(temp_r5, s8 *, 0x20) = 1;
            native_fn_ov000_021d8b24(temp_r5, temp_r5 + 0xC);
            native_fn_ov000_021d8a08(1);
        }
        var_r4 = 1;
        M2C_FIELD(temp_r5, s8 *, 0x1C) = 1;
    }
    return var_r4;
}
