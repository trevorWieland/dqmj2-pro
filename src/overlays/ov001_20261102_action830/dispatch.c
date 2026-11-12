#include "context.h"
u32 native_ov001_021f35f0(void) {
    s16 temp_r0;
    s16 temp_r0_3;
    s32 temp_r0_2;
    u16 temp_r2;
    u32 temp_r0_4;
    u32 temp_r4;

    temp_r4 = native_fn_0207afec((u32) M2C_FIELD(native_data_ov001_0223989c, u16 *, 0x50));
    if (M2C_FIELD(native_data_ov001_0223989c, u8 *, 9) == 0) {
        if ((M2C_FIELD(native_data_ov001_0223989c, u8 *, 0x10) == 0) || (M2C_FIELD(native_data_ov001_0223989c, u8 *, 0x13) != 0)) {
            if (((u32) ((u32)M2C_FIELD((void *) native_fn_0207afec((u32) M2C_FIELD(native_data_ov001_0223989c, u16 *, 0x50)), u16 *, 8) << 0x14) >> 0x1C) != 7) {
                if ((((u32) ((u32)M2C_FIELD((void *) native_fn_0207afec((u32) M2C_FIELD(native_data_ov001_0223989c, u16 *, 0x50)), u16 *, 8) << 0x14) >> 0x1C) != 9) && (M2C_FIELD(native_data_ov001_0223989c, u16 *, 0x50) != 0xB6)) {
                    native_fn_ov001_021f1f1c(temp_r4);
                } else {
                    goto block_9;
                }
            } else {
block_9:
                native_fn_ov001_021d7f54(M2C_FIELD(M2C_FIELD(native_data_ov001_0223989c, u32 *, 0x80), u8 *, 0x31E));
            }
        } else {
            native_fn_ov001_021d7e80(M2C_FIELD(native_data_ov001_0223989c, u32 *, 0x80));
        }
        M2C_FIELD(native_data_ov001_0223989c, s32 *, 0x6C) = 0;
        M2C_FIELD(native_data_ov001_0223989c, u8 *, 9) = 5U;
    }
    if (M2C_FIELD(native_data_ov001_0223989c, u8 *, 9) == 5) {
        native_fn_ov001_021f34c8((u32) ((u32)M2C_FIELD(temp_r4, u16 *, 8) << 0x14) >> 0x1C);
        M2C_FIELD(native_data_ov001_0223989c, u8 *, 9) = 0xAU;
    }
    if (M2C_FIELD(native_data_ov001_0223989c, u8 *, 9) == 0xA) {
        if (M2C_FIELD(temp_r4, s16 *, 0xC) != 0) {
            native_fn_0202ac08(native_data_ov001_0223992c);
            native_fn_ov001_021eea10(M2C_FIELD(temp_r4, s16 *, 0xC), 0);
        }
        M2C_FIELD(native_data_ov001_0223989c, u8 *, 9) = 0xFU;
    } else if (M2C_FIELD(native_data_ov001_0223989c, u8 *, 9) == 0xF) {
        temp_r0 = M2C_FIELD(temp_r4, s16 *, 0xC);
        if (temp_r0 != 0) {
            native_fn_0205c904((u32) temp_r0);
            M2C_FIELD(native_data_ov001_0223989c, u8 *, 0) = (u8) native_fn_ov001_021f32b4(M2C_FIELD(native_data_ov001_0223989c, u16 *, 0x50), M2C_FIELD(native_data_ov001_0223989c, u32 *, 0x80));
        }
        native_fn_ov001_021f30cc(M2C_FIELD(native_data_ov001_0223989c, u32 *, 0x80), M2C_FIELD(native_data_ov001_0223989c, u16 *, 0x50), 1);
        temp_r0_2 = (s32) native_fn_0207b20c((u32) M2C_FIELD(native_data_ov001_0223989c, u16 *, 0x50));
        if (temp_r0_2 > 0) {
            temp_r2 = M2C_FIELD((void *) native_fn_ov001_021d8dec((u32) temp_r0_2), u16 *, 0xC);
            if (temp_r2 != 0) {
                ov001_begin_state_transition_021f1354(1, 0, temp_r2, 1);
            }
        }
        M2C_FIELD(native_data_ov001_0223989c, u8 *, 9) = 0x14U;
    }
    if (M2C_FIELD(native_data_ov001_0223989c, u8 *, 9) == 0x14) {
        if ((M2C_FIELD(temp_r4, s16 *, 0xC) == 0) || (native_fn_0205d6f4((u32) (s8) M2C_FIELD(native_data_ov001_0223989c, u8 *, 0)) == 0)) {
            native_fn_ov001_021f30cc(M2C_FIELD(native_data_ov001_0223989c, u32 *, 0x80), M2C_FIELD(native_data_ov001_0223989c, u16 *, 0x50), 0);
            M2C_FIELD(native_data_ov001_0223989c, u8 *, 9) = 0x19U;
        } else {
            native_fn_ov001_021f3178(M2C_FIELD(native_data_ov001_0223989c, u32 *, 0x80), M2C_FIELD(native_data_ov001_0223989c, u16 *, 0x50));
        }
    } else if (M2C_FIELD(native_data_ov001_0223989c, u8 *, 9) == 0x19) {
        temp_r0_3 = M2C_FIELD(temp_r4, s16 *, 0xC);
        if (temp_r0_3 != 0) {
            native_fn_ov001_021eeb70((u32) temp_r0_3);
            native_fn_0202ac4c(native_data_ov001_0223992c);
        }
        M2C_FIELD(native_data_ov001_0223989c, u8 *, 9) = 0x1EU;
    }
    if (M2C_FIELD(native_data_ov001_0223989c, u8 *, 9) == 0x1E) {
        if (native_fn_ov001_021f14e4() != 0) {
            ov001_clear_state_flag4_021f14a4();
        }
        M2C_FIELD(native_data_ov001_0223989c, u8 *, 9) = 0x64U;
    }
    if (M2C_FIELD(native_data_ov001_0223989c, u8 *, 9) == 0x64) {
        if ((native_fn_ov001_021f358c() != 0) && (native_fn_0207b02c(M2C_FIELD(native_data_ov001_0223989c, u16 *, 0x50), 0x80008000) != 0)) {
            M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x1B) = 0x19;
        } else {
            temp_r0_4 = (u32) ((u32)M2C_FIELD(temp_r4, u16 *, 8) << 0x14) >> 0x1C;
            if ((u8) temp_r0_4 == 1) {
                M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x1B) = 4;
            } else if ((u8) temp_r0_4 == 2) {
                M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x1B) = 5;
            } else if ((u8) temp_r0_4 == 3) {
                M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x1B) = 7;
            } else if ((u8) temp_r0_4 == 4) {
                M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x1B) = 6;
            } else if ((u8) temp_r0_4 == 5) {
                M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x1B) = 8;
            } else if ((u8) temp_r0_4 == 6) {
                M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x1B) = 9;
            } else if ((u8) temp_r0_4 == 7) {
                M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x1B) = 0xA;
            } else if ((u8) temp_r0_4 == 8) {
                M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x1B) = 0xB;
            } else if ((u8) temp_r0_4 == 9) {
                M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x1B) = 0xC;
            } else if ((u8) temp_r0_4 == 10) {
                M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x1B) = 0xD;
            } else {
                M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x1B) = 4;
            }
        }
        M2C_FIELD(native_data_ov001_0223989c, u8 *, 9) = 0U;
    }
    return 0U;
}
