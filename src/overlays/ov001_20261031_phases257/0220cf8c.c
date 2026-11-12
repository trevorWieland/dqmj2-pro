#include "context.h"
u32 native_ov001_0220cf8c(void) {
    u32 temp_r0;
    void *var_r0;
    u8 temp_r2;
    u32 temp_r4;
    u32 temp_r5;

    temp_r4 = native_fn_ov001_0220b770();
    temp_r5 = native_fn_ov001_0220b74c();
    temp_r0 = native_fn_ov001_0220b794();
    if (temp_r0 == 4) {
        var_r0 = NULL;
    } else {
        var_r0 = ov001_side_slot_record_021db438((s32) temp_r5, temp_r0);
    }
    if (native_data_ov001_0223e088.field_6 == 0) {
        native_fn_ov001_0220cf10(var_r0, temp_r5, temp_r4);
        native_data_ov001_0223e088.field_5 = 0U;
        native_data_ov001_0223e088.field_6 = 0xAU;
    }
    if (native_data_ov001_0223e088.field_6 == 0xA) {
        temp_r2 = ++native_data_ov001_0223e088.field_5;
        if ((u32) temp_r2 > 0x2DU) {
            native_data_ov001_0223e088.field_6 = 0x64U;
        }
    }
    if (native_data_ov001_0223e088.field_6 == 0x64) {
        native_data_ov001_0223e088.field_6 = 0U;
        native_data_ov001_0223e088.field_3 = 0xE;
    }
    return 0U;
}
