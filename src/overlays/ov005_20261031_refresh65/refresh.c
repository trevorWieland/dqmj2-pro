#include "context.h"
u32 native_ov005_021e24bc(void) {
    u16 temp_r0;
    u8 temp_r0_2;

    native_data_ov005_021ed438.field_20 = (s32)((u32)native_data_ov005_021ed438.field_20 + 1U);
    native_fn_ov005_021e6004(0);
    native_fn_02049604(native_fn_ov005_021e0a68(), 1);
    native_fn_ov005_021e653c();
    if (native_data_ov005_021ed438.field_1 != native_fn_020bf084()) {
        native_fn_02048094(native_data_ov005_021ed438.field_1 = native_fn_020bf084(), 0);
        native_fn_ov005_021e0818();
        native_fn_ov005_021e0730(0x13, 2, 3);
    }
    temp_r0 = M2C_FIELD((void *) native_fn_ov005_021e0a84(), u16 *, 2);
    if (!(temp_r0 & 2)) {
        return (u32) temp_r0;
    }
    native_fn_ov005_021e0818();
    native_fn_ov005_021e1144(0);
    native_data_ov005_021ed438.field_c = 0;
    native_data_ov005_021ed438.field_34 = 0;
    native_data_ov005_021ed438.field_2 = 0x1E;
    native_fn_ov005_021e1048(0x53);
    native_fn_ov005_021e0730(0x13, 2, 0x1F);
    native_fn_ov005_021e085c(1);
    return native_fn_ov005_021e155c(0x16);
}
