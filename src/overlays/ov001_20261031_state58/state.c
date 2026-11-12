#include "context.h"
u32 native_ov001_021f98e4(void) {
    u32 temp_r1;
    u8 temp_r2;
    u8 temp_r2_2;

    if (native_data_ov001_02239a14.field_19 == 0) {
        ov001_begin_state_transition_021f1354(1, 2, 0, 1);
        native_fn_ov001_021f989c();
        native_data_ov001_02239a14.field_19 = 0x64U;
    }
    if (native_data_ov001_02239a14.field_b == 0) {
        native_fn_ov001_021e3564(0x16, 1);
        native_fn_ov001_021f949c(0xE9, 1);
        native_data_ov001_02239a14.field_b = 0xAU;
    }
    if ((native_data_ov001_02239a14.field_b == 0xA) && (native_fn_ov001_021e3584() != 0)) {
        native_fn_ov001_021e3564(0x17, 1);
        native_data_ov001_02239a14.field_b = 0x64U;
    }
    if (native_data_ov001_02239a14.field_9 == 0) {
        native_data_ov001_02239a14.field_13 = 0U;
        native_data_ov001_02239a14.field_9 = 0xAU;
    }
    if (native_data_ov001_02239a14.field_9 == 0xA) {
        temp_r1 = 0x1F - native_data_ov001_02239a14.field_13;
        native_fn_ov001_021d8cc8((u16) (temp_r1 | (temp_r1 << 5) | (temp_r1 << 0xA)));
        if (++native_data_ov001_02239a14.field_13 > 0x18U) {
            native_data_ov001_02239a14.field_9 = 0x64U;
        }
    }
    if (native_data_ov001_02239a14.field_2 == 0) {
        native_data_ov001_02239a14.field_8 = 0U;
        native_data_ov001_02239a14.field_2 = 0xAU;
    }
    if (native_data_ov001_02239a14.field_2 == 0xA) {
        if (++native_data_ov001_02239a14.field_8 > 0x1EU) {
            native_fn_02041510(1, 3, 0xF);
            native_data_ov001_02239a14.field_2 = 0x14U;
        }
    }
    if ((native_data_ov001_02239a14.field_2 == 0x14) && (native_fn_02041800() != 1)) {
        native_data_ov001_02239a14.field_2 = 0x64U;
    }
    if ((native_data_ov001_02239a14.field_19 == 0x64) && (native_data_ov001_02239a14.field_b == 0x64) && (native_data_ov001_02239a14.field_9 == 0x64) && (native_data_ov001_02239a14.field_2 == 0x64)) {
        native_data_ov001_02239a14.field_19 = 0U;
        native_data_ov001_02239a14.field_b = 0U;
        native_data_ov001_02239a14.field_9 = 0U;
        native_data_ov001_02239a14.field_2 = 0U;
        native_data_ov001_02239a14.field_a = 3;
    }
    return 0U;
}
