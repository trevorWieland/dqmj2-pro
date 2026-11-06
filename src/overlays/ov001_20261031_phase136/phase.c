#include "context.h"
u32 native_ov001_021f8b60(void) {
    u32 temp_r0;
    s32 var_r1;
    u8 temp_r2;
    s32 sp4;

    temp_r0 = (u32) (M2C_FIELD((void *) native_fn_0207afec((s32) native_data_ov001_0223989c.field_50), u16 *, 8) << 0x10) >> 0x1C;
    if (native_data_ov001_0223989c.field_20 == 0) {
        if (temp_r0 == 0) {
            var_r1 = native_data_ov001_0223989c.field_80;
        } else {
            var_r1 = 0;
        }
        native_fn_ov001_021f521c(native_data_ov001_0223989c.field_84, var_r1, native_data_ov001_0223989c.field_50, 0, &sp4);
        if (sp4 != 0) {
            native_fn_ov001_021e215c(native_data_ov001_0223989c.field_84);
        }
        native_data_ov001_0223989c.field_1f = 0U;
        native_data_ov001_0223989c.field_20 = 0xAU;
    }
    if (native_data_ov001_0223989c.field_20 == 0xA) {
        if (((u32) ++native_data_ov001_0223989c.field_1f > 0xFU) && (native_fn_ov001_02212290() == 0)) {
            native_data_ov001_0223989c.field_20 = 0x64U;
        }
    }
    if (native_data_ov001_0223989c.field_20 == 0x64) {
        native_data_ov001_0223989c.field_20 = 0U;
        native_data_ov001_0223989c.field_1b = 0x1B;
    }
    return 0U;
}
