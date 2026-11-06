#include "context.h"
u32 native_ov001_0220c554(void) {
    u32 temp_r0;
    u8 *temp_r0_2;
    u8 temp_r2;
    u8 temp_r2_2;
    u32 temp_r4;
    u32 temp_r5;
    u32 var_r6_2;
    u8 *var_r6;

    temp_r4 = native_fn_ov001_0220b770();
    temp_r5 = native_fn_ov001_0220b74c();
    temp_r0 = native_fn_ov001_0220b794();
    if (temp_r0 == 4) {
        var_r6 = NULL;
    } else {
        var_r6 = native_fn_ov001_021db438((s32) temp_r5, temp_r0);
    }
    if (native_data_ov001_0223e088.field_10 == 0) {
        native_fn_ov001_0220c3f4(var_r6, temp_r5, temp_r4);
        native_data_ov001_0223e088.field_f = 0U;
        native_data_ov001_0223e088.field_10 = 0xAU;
    }
    if (native_data_ov001_0223e088.field_10 == 0xA) {
        if ((u32) ++native_data_ov001_0223e088.field_f > 0x1EU) {
            native_data_ov001_0223e088.field_10 = 0x14U;
        }
    }
    if (native_data_ov001_0223e088.field_10 == 0x14) {
        if (M2C_FIELD((void *) native_fn_02065d88(temp_r4), u8 *, 0x28) == 0x22) {
            if (var_r6 != NULL) {
                native_fn_ov001_021ee91c(var_r6, M2C_FIELD(var_r6, s8 *, 0x234));
            } else {
                var_r6_2 = 0;
                do {
                    temp_r0_2 = native_fn_ov001_021db438((s32) temp_r5, var_r6_2);
                    if (native_fn_ov001_021db8d0(temp_r0_2) != 0) {
                        native_fn_ov001_021ee91c(temp_r0_2, M2C_FIELD(temp_r0_2, s8 *, 0x234));
                    }
                    var_r6_2 += 1;
                } while ((s32) var_r6_2 < 3);
            }
            native_data_ov001_0223e088.field_f = 0U;
            native_data_ov001_0223e088.field_10 = 0x1EU;
        } else {
            native_data_ov001_0223e088.field_10 = 0x64U;
        }
    }
    if (native_data_ov001_0223e088.field_10 == 0x1E) {
        if ((u32) ++native_data_ov001_0223e088.field_f > 0x1EU) {
            native_data_ov001_0223e088.field_10 = 0x64U;
        }
    }
    if (native_data_ov001_0223e088.field_10 == 0x64) {
        native_data_ov001_0223e088.field_10 = 0U;
        native_data_ov001_0223e088.field_3 = 0xE;
    }
    return 0U;
}
