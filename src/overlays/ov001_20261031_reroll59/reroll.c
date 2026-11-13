#include "context.h"
u32 native_ov001_0220c888(void) {
    u32 temp_r0;
    u8 var_r1;
    u8 temp_r2;
    u8 temp_r2_2;
    u32 temp_r4;
    u32 temp_r5;
    void *var_r6;
    u32 temp_r7;

    temp_r4 = native_fn_ov001_0220b770();
    temp_r5 = native_fn_ov001_0220b74c();
    temp_r0 = native_fn_ov001_0220b794();
    if (temp_r0 == 4) {
        var_r6 = NULL;
    } else {
        var_r6 = ov001_side_slot_record_021db438((s32) temp_r5, temp_r0);
    }
    if (native_data_ov001_0223e088.field_e == 0) {
        temp_r7 = native_fn_02066a7c(temp_r4);
        if ((s32) native_fn_0203d294(0x64) < (s32) temp_r7) {
            var_r1 = 0xA;
        } else {
            var_r1 = 0x64;
        }
        native_data_ov001_0223e088.field_e = var_r1;
    }
    if (native_data_ov001_0223e088.field_e == 0xA) {
        native_fn_ov001_0220c6e0(var_r6, temp_r4, temp_r5);
        native_data_ov001_0223e088.field_d = 0U;
        native_data_ov001_0223e088.field_e = 0x14U;
    }
    if (native_data_ov001_0223e088.field_e == 0x14) {
        if (native_fn_ov001_0220c7ec(var_r6, temp_r4, temp_r5) != 0) {
            native_data_ov001_0223e088.field_d = 0U;
            native_data_ov001_0223e088.field_e = 0x1EU;
        } else {
            if (++native_data_ov001_0223e088.field_d > 0x1EU) {
                native_data_ov001_0223e088.field_d = 0U;
                native_data_ov001_0223e088.field_e = 0x1EU;
            }
        }
    }
    if (native_data_ov001_0223e088.field_e == 0x1E) {
        if (++native_data_ov001_0223e088.field_d > 0x1EU) {
            native_data_ov001_0223e088.field_e = 0x64U;
        }
    }
    if (native_data_ov001_0223e088.field_e == 0x64) {
        native_data_ov001_0223e088.field_e = 0U;
        native_data_ov001_0223e088.field_3 = 0xE;
    }
    return 0U;
}
