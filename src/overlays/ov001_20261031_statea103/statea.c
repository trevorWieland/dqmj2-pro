#include "context.h"
u32 native_ov001_021f6878(void) {
    u32 temp_r0;
    u8 temp_r2;
    s32 var_r4;

    temp_r0 = native_fn_0207afec((s32) native_data_ov001_0223989c.field_50);
    if (native_data_ov001_0223989c.field_10 != 0) {
        var_r4 = native_data_ov001_0223989c.field_80;
    } else if (((u32) (M2C_FIELD(temp_r0, u16 *, 8) << 0x10) >> 0x1C) == 0) {
        var_r4 = native_data_ov001_0223989c.field_80;
    } else {
        var_r4 = 0;
    }
    if (native_data_ov001_0223989c.field_3e == 0) {
        native_fn_ov001_021f65d8(native_data_ov001_0223989c.field_84, var_r4, native_data_ov001_0223989c.field_50);
        if (native_data_ov001_0223989c.field_10 != 0) {
            native_fn_ov001_021f2120(var_r4, 0xB0);
            native_fn_ov001_021f2120(var_r4, 0xF9);
            native_fn_ov001_021f2120(var_r4, 0x119);
            native_fn_ov001_021f2120(var_r4, 0x10D);
        }
        native_data_ov001_0223989c.field_3e = 0xAU;
        native_data_ov001_0223989c.field_3d = 0U;
    }
    if (native_data_ov001_0223989c.field_3e == 0xA) {
        if ((u32) ++native_data_ov001_0223989c.field_3d > 0x28U) {
            native_data_ov001_0223989c.field_3e = 0x64U;
        }
    }
    if (native_data_ov001_0223989c.field_3e == 0x64) {
        native_data_ov001_0223989c.field_3e = 0U;
        if (native_data_ov001_0223989c.field_10 == 0) {
            native_data_ov001_0223989c.field_1b = 0x1B;
        } else {
            native_fn_ov001_021f4210();
            native_data_ov001_0223989c.field_1b = 3;
        }
    }
    return 0U;
}
