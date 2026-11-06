#include "context.h"
u32 native_ov001_0220c9ec(void) {
    u32 temp_r0;
    u8 temp_r2;
    u32 temp_r4;
    void *var_r4;
    u32 temp_r5;

    if (native_data_ov001_0223e088.field_c == 0) {
        temp_r5 = native_fn_ov001_0220b770();
        temp_r4 = native_fn_ov001_0220b74c();
        temp_r0 = native_fn_ov001_0220b794();
        if (temp_r0 == 4) {
            var_r4 = NULL;
        } else {
            var_r4 = native_fn_ov001_021db438((s32) temp_r4, temp_r0);
        }
        M2C_FIELD(M2C_FIELD(var_r4, void **, 0x1E8), u8 *, 0xB0) = (u8) M2C_FIELD((void *) native_fn_02065d88(temp_r5), u8 *, 0x2A);
        native_data_ov001_0223e088.field_b = 0U;
        native_data_ov001_0223e088.field_c = 0xAU;
    }
    if (native_data_ov001_0223e088.field_c == 0xA) {
        temp_r2 = ++native_data_ov001_0223e088.field_b;
        if ((u32) temp_r2 > 0x1EU) {
            native_data_ov001_0223e088.field_c = 0x64U;
        }
    }
    if (native_data_ov001_0223e088.field_c == 0x64) {
        native_data_ov001_0223e088.field_c = 0U;
        native_data_ov001_0223e088.field_3 = 0xE;
    }
    return 0U;
}
