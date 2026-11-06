#include "context.h"
u32 native_ov006_021e7d98(u32 arg0) {
    u32 var_r0;
    u32 var_r2;

    if (M2C_FIELD(native_data_ov006_02218d90, s32 *, 0x28) == 0) {
        if (arg0 != 0) {
            var_r0 = 0x3E;
        } else {
            var_r0 = 0x2E;
        }
        native_fn_020414c8(var_r0);
        if (native_fn_02041814() == 1) {
            var_r2 = 1;
        } else {
            var_r2 = 4;
        }
        native_fn_02041538(1U, 2U, var_r2);
        native_fn_0204157c(0xA);
        M2C_FIELD(native_data_ov006_02218d90, s32 *, 0x28) = 1;
        M2C_FIELD(native_data_ov006_02218d90, u32 *, 0x4C) = arg0;
        return (u32) native_data_ov006_02218d90;
    }
    if (M2C_FIELD(native_data_ov006_02218d90, u32 *, 0x4C) == arg0) {
        return M2C_FIELD(native_data_ov006_02218d90, u32 *, 0x4C);
    }
    native_fn_020418b0(0U);
    M2C_FIELD(native_data_ov006_02218d90, s32 *, 0x28) = 0;
    return native_ov006_021e7d98(arg0);
}
