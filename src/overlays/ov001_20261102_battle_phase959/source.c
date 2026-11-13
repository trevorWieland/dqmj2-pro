#include "context.h"
u32 native_ov001_021f9b54(void) {
    u32 temp_r0;
    u32 temp_r0_2;
    u8 temp_r2;
    u8 temp_r2_2;

    if (M2C_FIELD(native_data_ov001_02239a14, u8 *, 3) == 0) {
        native_fn_02041510(0U, 3U, 0x14U);
        native_fn_ov001_021f9ac8();
        native_fn_0202ac08(native_data_ov001_02239a5c);
        native_fn_ov001_021eea10(7, 0);
        M2C_FIELD(native_data_ov001_02239a14, u8 *, 3) = 0xAU;
    }
    if ((M2C_FIELD(native_data_ov001_02239a14, u8 *, 3) == 0xA) && (native_fn_02041800() != 1)) {
        native_fn_0205c904(7U);
        M2C_FIELD(native_data_ov001_02239a14, u8 *, 3) = 0x14U;
    }
    if (M2C_FIELD(native_data_ov001_02239a14, u8 *, 3) == 0x14) {
        M2C_FIELD(native_data_ov001_02239a14, u8 *, 0) = 0;
        M2C_FIELD(native_data_ov001_02239a14, u8 *, 3) = 0x1EU;
    }
    if (M2C_FIELD(native_data_ov001_02239a14, u8 *, 3) == 30) {
        if (ov001_record_is_active_021db8d0((void *) ov001_side_slot_record_021db438(0U, (u32) M2C_FIELD(native_data_ov001_02239a14, u8 *, 0))) != 0) {
            M2C_FIELD(native_data_ov001_02239a14, u8 *, 3) = 0x23U;
        } else {
            M2C_FIELD(native_data_ov001_02239a14, u8 *, 3) = 0x28U;
        }
    }
    else if (M2C_FIELD(native_data_ov001_02239a14, u8 *, 3) == 35) {
        temp_r0 = ov001_side_slot_record_021db438(0U, (u32) M2C_FIELD(native_data_ov001_02239a14, u8 *, 0));
        ov001_effect_resource_create_021eec7c(7U, (u8 *) temp_r0, 0);
        native_fn_ov001_021f94d8(0x4AU, 1U);
        M2C_FIELD(temp_r0, s8 *, 0x324) = 0;
        M2C_FIELD(native_data_ov001_02239a14, u8 *, 3) = (u8) (M2C_FIELD(native_data_ov001_02239a14, u8 *, 3) + 1);
    }
    else if (M2C_FIELD(native_data_ov001_02239a14, u8 *, 3) == 36) {
        temp_r0_2 = ov001_side_slot_record_021db438(0U, (u32) M2C_FIELD(native_data_ov001_02239a14, u8 *, 0));
        M2C_FIELD(temp_r0_2, s8 *, 0x358) = (s8) ov001_effect_resource_create_021eec7c(8U, (u8 *) temp_r0_2, 2);
        if (M2C_FIELD(native_data_ov001_02239a14, u8 *, 4) == 0) {
            M2C_FIELD(temp_r0_2, s8 *, 0x324) = (s8) native_fn_ov001_021f949c(0xEAU, 1U);
            M2C_FIELD(native_data_ov001_02239a14, u8 *, 4) = (u8) (M2C_FIELD(native_data_ov001_02239a14, u8 *, 4) + 1);
        }
        M2C_FIELD(native_data_ov001_02239a14, u8 *, 3) = 0x28U;
    }
    else if (M2C_FIELD(native_data_ov001_02239a14, u8 *, 3) == 40) {
        if ((u32) (M2C_FIELD(native_data_ov001_02239a14, u8 *, 0) = (u8) (M2C_FIELD(native_data_ov001_02239a14, u8 *, 0) + 1)) >= 3U) {
            M2C_FIELD(native_data_ov001_02239a14, u8 *, 3) = 0x32U;
        } else {
            M2C_FIELD(native_data_ov001_02239a14, u8 *, 3) = 0x1EU;
        }
    }
    else if (M2C_FIELD(native_data_ov001_02239a14, u8 *, 3) < 50) {
        M2C_FIELD(native_data_ov001_02239a14, u8 *, 3) = (u8) (M2C_FIELD(native_data_ov001_02239a14, u8 *, 3) + 1);
    }
    if (M2C_FIELD(native_data_ov001_02239a14, u8 *, 3) == 0x32) {
        M2C_FIELD(native_data_ov001_02239a14, u8 *, 0) = 0;
        M2C_FIELD(native_data_ov001_02239a14, u8 *, 3) = 0x37U;
    }
    if (M2C_FIELD(native_data_ov001_02239a14, u8 *, 3) == 0x37) {
        if ((u32) (M2C_FIELD(native_data_ov001_02239a14, u8 *, 0) = (u8) (M2C_FIELD(native_data_ov001_02239a14, u8 *, 0) + 1)) > 0xFU) {
            M2C_FIELD(native_data_ov001_02239a14, u8 *, 3) = 0x64U;
        }
    }
    if (M2C_FIELD(native_data_ov001_02239a14, u8 *, 3) == 0x64) {
        ov001_clear_state_flag4_021f14a4();
        native_fn_ov001_021eeb70(7U);
        native_fn_0202ac4c(native_data_ov001_02239a5c);
        M2C_FIELD(native_data_ov001_02239a14, u8 *, 3) = 0U;
        M2C_FIELD(native_data_ov001_02239a14, u8 *, 4) = 0U;
        M2C_FIELD(native_data_ov001_02239a14, s8 *, 0xA) = 4;
    }
    return 0U;
}
