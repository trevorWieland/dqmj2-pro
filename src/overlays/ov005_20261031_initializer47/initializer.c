#include "context.h"
u32 native_ov005_021d8edc(s32 arg0, u32 (*arg1)(u32, u32), s32 arg2) {
    u32 (*temp_r2)(u32, u32);
    u32 temp_r4;
    u32 temp_r5;

    temp_r4 = native_fn_02007ff4();
    if (native_fn_ov005_021d90f0() == 0) {
        if (arg0 & 0x1F) {
            native_fn_02008430();
        }
        native_data_ov005_021e78cc.field_0 = arg0;
        native_fn_02008c14(0, arg0, 0x5A88);
        M2C_FIELD(native_data_ov005_021e78cc.field_0, s32 *, 0) = arg2;
        M2C_FIELD(native_data_ov005_021e78cc.field_0, u32 (**)(u32, u32), 4) = arg1;
        native_fn_ov005_021d87b4(native_data_ov005_021e78cc.field_0 + 8);
        native_fn_ov005_021d731c(native_data_ov005_021e78cc.field_0 + 0x5760);
        M2C_FIELD(native_data_ov005_021e78cc.field_0, s16 *, 0xF0) = 1;
        M2C_FIELD(native_data_ov005_021e78cc.field_0, s16 *, 0x114) = 0x200;
        M2C_FIELD(native_data_ov005_021e78cc.field_0, s16 *, 0x116) = 0x200;
        M2C_FIELD(native_data_ov005_021e78cc.field_0, s16 *, 0xF6) = 1;
        native_fn_ov005_021d86f0(native_data_ov005_021e78cc.field_0 + 0x120, native_data_ov005_021e78cc.field_0 + 0xE0, native_fn_ov005_021d8900, M2C_FIELD(native_data_ov005_021e78cc.field_0, s32 *, 0));
        temp_r5 = native_fn_02007ff4();
        native_data_ov005_021e78cc.field_4 = 2;
        temp_r2 = M2C_FIELD(native_data_ov005_021e78cc.field_0, u32 (**)(u32, u32), 4);
        if (temp_r2 != NULL) {
            temp_r2(2, 0);
        }
        native_fn_02008008(temp_r5);
    }
    return native_fn_02008008(temp_r4);
}
