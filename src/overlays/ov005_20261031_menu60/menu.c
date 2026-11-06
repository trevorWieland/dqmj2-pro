#include "context.h"
u32 native_ov005_021e3560(void) {
    u16 temp_r0;
    u32 temp_r0_2;
    u8 temp_r0_3;
    u32 temp_r4;

    temp_r0_2 = native_fn_ov005_021dd788();
    if (temp_r0_2 != 1) {
        return temp_r0_2;
    }
    native_fn_ov005_021e0040();
    temp_r4 = native_fn_ov005_021e0a90();
    native_fn_ov005_021e0d88();
    if (native_data_ov005_021ed438.field_48 == 1) {
        native_fn_ov005_021de19c((s8) native_fn_ov005_021e0a90());
        native_data_ov005_021ed438.field_48 = 0;
    }
    if (temp_r4 != native_fn_ov005_021e0a90()) {
        native_fn_ov005_021de19c((s8) native_fn_ov005_021e0a90());
    }
    if (M2C_FIELD((void *) native_fn_ov005_021e0a84(), u16 *, 2) & 1) {
        native_fn_020bf4c4(native_data_ov005_021ed438.field_4 = native_fn_ov005_021e0a90());
        if (M2C_FIELD(((native_data_ov005_021ed438.field_4 * 0x268) + native_data_ov005_021ed438.field_40), u8 *, 0xFF) == 0) {
            return native_fn_ov005_021e1048(0x54);
        }
        native_fn_ov005_021e155c(0x22);
        return native_fn_ov005_021e1048(0x52);
    }
    temp_r0 = M2C_FIELD((void *) native_fn_ov005_021e0a84(), u16 *, 2);
    if (!(temp_r0 & 2)) {
        return (u32) temp_r0;
    }
    native_fn_ov005_021ddf24();
    native_fn_ov005_021e026c(4, 1, 0, 1, 0, 0);
    native_fn_ov005_021e1048(0x53);
    return native_fn_ov005_021e155c(0);
}
