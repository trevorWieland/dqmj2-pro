#include "context.h"
u32 native_ov001_0220cbe4(void) {
    u32 temp_r0;
    u8 temp_r2;
    u32 temp_r4;
    void *var_r5;
    u32 temp_r6;

    temp_r6 = native_fn_ov001_0220b770();
    temp_r4 = native_fn_ov001_0220b74c();
    temp_r0 = native_fn_ov001_0220b794();
    if (temp_r0 == 4) {
        var_r5 = NULL;
    } else {
        var_r5 = native_fn_ov001_021db438((s32) temp_r4, temp_r0);
    }
    if (native_data_ov001_0223e088.field_a == 0) {
        native_fn_ov001_0220cab0(var_r5, temp_r4, temp_r6);
        native_data_ov001_0223e088.field_9 = 0U;
        native_data_ov001_0223e088.field_a = 0xAU;
    }
    if (native_data_ov001_0223e088.field_a == 0xA) {
        if ((u32) ++native_data_ov001_0223e088.field_9 > 0x2DU) {
            native_data_ov001_0223e088.field_a = 0x14U;
        }
    }
    if (native_data_ov001_0223e088.field_a == 0x14) {
        if (native_fn_ov001_021dbb14(var_r5, temp_r4) != 0) {
            native_data_ov001_0223e088.field_a = 0x1EU;
        } else {
            native_data_ov001_0223e088.field_a = 0x64U;
        }
    }
    if ((native_data_ov001_0223e088.field_a == 0x1E) && (native_fn_ov001_021dbb9c(var_r5, temp_r4) != 0)) {
        native_data_ov001_0223e088.field_a = 0x64U;
    }
    if (native_data_ov001_0223e088.field_a == 0x64) {
        native_data_ov001_0223e088.field_a = 0U;
        native_data_ov001_0223e088.field_3 = 0xE;
    }
    return 0U;
}
