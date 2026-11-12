#include "context.h"
u32 native_ov001_0220bfc0(void) {
    u16 temp_r0_2;
    u16 temp_r7;
    u32 temp_r4;
    u32 temp_r5;
    u32 temp_r0;
    u8 temp_r0_3;
    u8 temp_r4_2;

    temp_r4 = native_fn_ov001_0220b770();
    temp_r5 = native_fn_ov001_0220b74c();
    temp_r0 = native_fn_ov001_0220b794();
    ov001_side_slot_record_021db438(temp_r5, temp_r0);
    if (M2C_FIELD(native_data_ov001_0223e088, s8 *, 0x15) == 0) {
        native_fn_ov001_0220b9e0();
        native_fn_ov001_021e3544(0U, 1U);
        M2C_FIELD(native_data_ov001_0223e088, s8 *, 0x15) = 0xA;
    }
    if (M2C_FIELD(native_data_ov001_0223e088, s8 *, 0x15) == 0xA) {
        native_fn_0202ac08(native_data_ov001_0223e0a8);
        temp_r0_2 = M2C_FIELD((void *) native_fn_02065d88(temp_r4), u16 *, 0x1A);
        if ((s32) temp_r0_2 > 0) {
            native_fn_ov001_021eea10(temp_r0_2, 0);
            M2C_FIELD(native_data_ov001_0223e088, s8 *, 0x15) = 0xF;
        } else {
            M2C_FIELD(native_data_ov001_0223e088, s8 *, 0x15) = 0x64;
        }
    } else if (M2C_FIELD(native_data_ov001_0223e088, s8 *, 0x15) == 0xF) {
        temp_r7 = M2C_FIELD((void *) native_fn_02065d88(temp_r4), u16 *, 0x1A);
        native_fn_0205c904((u32) temp_r7);
        M2C_FIELD(native_data_ov001_0223e088, s8 *, 0x14) = (s8) native_fn_ov001_0220bbb8(temp_r7);
        native_fn_ov001_0220bd30(temp_r5, temp_r0, temp_r4, 1);
        M2C_FIELD(native_data_ov001_0223e088, u16 *, 0x18) = (u16) native_fn_ov001_0220bf30(temp_r4, temp_r5);
        M2C_FIELD(native_data_ov001_0223e088, s8 *, 0x15) = 0x14;
    }
    if (M2C_FIELD(native_data_ov001_0223e088, s8 *, 0x15) == 0x14) {
        if (native_fn_0205d6f4((u32) M2C_FIELD(native_data_ov001_0223e088, s8 *, 0x14)) == 0) {
            native_fn_ov001_0220bd30(temp_r5, temp_r0, temp_r4, 0);
            M2C_FIELD(native_data_ov001_0223e088, s8 *, 0x15) = 0x19;
        } else {
            native_fn_ov001_0220bde8(temp_r5, temp_r0, temp_r4);
        }
    } else if (M2C_FIELD(native_data_ov001_0223e088, s8 *, 0x15) == 0x19) {
        native_fn_ov001_021eeb70((u32) M2C_FIELD((void *) native_fn_02065d88(temp_r4), u16 *, 0x1A));
        native_fn_0202ac4c(native_data_ov001_0223e0a8);
        if (M2C_FIELD(native_data_ov001_0223e088, u16 *, 0x18) != 0) {
            ov001_clear_state_flag4_021f14a4();
        }
        M2C_FIELD(native_data_ov001_0223e088, s8 *, 0x15) = 0x64;
    }
    if (M2C_FIELD(native_data_ov001_0223e088, s8 *, 0x15) == 0x64) {
        temp_r4_2 = M2C_FIELD((void *) native_fn_02065d88(native_fn_ov001_0220b770()), u8 *, 0x2C);
        temp_r0_3 = M2C_FIELD((void *) native_fn_02065d88(native_fn_ov001_0220b770()), u8 *, 0x29);
        if (temp_r4_2 == 1) {
            M2C_FIELD(native_data_ov001_0223e088, s8 *, 3) = 6;
        }
        else if (temp_r4_2 == 2) {
            M2C_FIELD(native_data_ov001_0223e088, s8 *, 3) = 7;
        }
        else if (temp_r4_2 == 8) {
            M2C_FIELD(native_data_ov001_0223e088, s8 *, 3) = 8;
        }
        else if (temp_r4_2 == 11) {
            M2C_FIELD(native_data_ov001_0223e088, s8 *, 3) = 9;
        }
        else if (temp_r4_2 == 10) {
            M2C_FIELD(native_data_ov001_0223e088, s8 *, 3) = 0xA;
        }
        else if (temp_r4_2 == 12) {
            M2C_FIELD(native_data_ov001_0223e088, s8 *, 3) = 0xB;
        }
        else if (temp_r4_2 == 9) {
            M2C_FIELD(native_data_ov001_0223e088, s8 *, 3) = 0xC;
        }
        else if (temp_r4_2 == 13) {
            M2C_FIELD(native_data_ov001_0223e088, s8 *, 3) = 0xD;
        }
        else {
            if (temp_r0_3 == 0x2F) {
                M2C_FIELD(native_data_ov001_0223e088, s8 *, 3) = 0xD;
            } else {
                M2C_FIELD(native_data_ov001_0223e088, s8 *, 3) = 6;
            }
        }
        M2C_FIELD(native_data_ov001_0223e088, s8 *, 0x15) = 0;
    }
    return 0U;
}
