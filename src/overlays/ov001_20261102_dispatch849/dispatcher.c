#include "context.h"
u32 native_ov001_021eae04(void) {
    u32 var_r0;
    u8 temp_r0;
    u8 var_r1;
    u8 var_r2;

    if (M2C_FIELD(native_data_ov001_02238d7c, u8 *, 0xE) == 0x0) {
        if (M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, void **, 0x60), s8 *, 0x1E4) == 0) {
            if (M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, void **, 0x60), u8 *, 0x31E) == 0) {
                var_r0 = 0xDD;
            } else {
                var_r0 = 0xE0;
            }
            native_fn_ov001_021f949c(var_r0, 1U);
            native_fn_ov001_021eaa3c(M2C_FIELD(native_data_ov001_02238d7c, u16 *, 0x36));
            native_fn_ov001_021f1438((u32) M2C_FIELD(native_data_ov001_02238d7c, u8 *, 0x29));
            M2C_FIELD(native_data_ov001_02238d7c, s8 *, 0xA) = 2;
            if (native_fn_ov001_021dbaac((u32) M2C_FIELD(native_data_ov001_02238d7c, void **, 0x60)) != 0) {
                if (M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, void **, 0x60), u8 *, 0x31E) == 0) {
                    native_fn_ov001_021d75d4(0x29);
                } else {
                    native_fn_ov001_021d75d4(0x25);
                }
                native_fn_ov001_021d77b0(-1, native_fn_02042c2c((u32) M2C_FIELD(native_data_ov001_02238d7c, void **, 0x60)));
                native_fn_ov001_021d7814(-1U, native_fn_02041f74(M2C_FIELD(native_data_ov001_02238d7c, void **, 0x60), 0));
                temp_r0 = M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, void **, 0x60), u8 *, 0x31E);
                var_r1 = temp_r0 == 0;
                var_r2 = temp_r0 == 1;
                native_fn_ov001_021d94cc((u32) var_r1, (u32) var_r2);
            } else {
                native_fn_ov001_021d7e80((u32) M2C_FIELD(native_data_ov001_02238d7c, void **, 0x60));
            }
            native_fn_ov001_021d9494((u32) M2C_FIELD(native_data_ov001_02238d7c, void **, 0x60), 2U, 1U);
            M2C_FIELD(native_data_ov001_02238d7c, u8 *, 0xE) = 0xAU;
        }
    }
    else if (M2C_FIELD(native_data_ov001_02238d7c, u8 *, 0xE) == 0xA) {
        if ((native_fn_ov001_021d9534((u32) M2C_FIELD(native_data_ov001_02238d7c, void **, 0x60), -1U, 6U, 0U) - 5) == ((s32) *M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, void **, 0x60), s32 **, 0x60) >> 0xC)) {
            M2C_FIELD(native_data_ov001_02238d7c, u8 *, 0xE) = 0x64U;
        }
    }
    else if (M2C_FIELD(native_data_ov001_02238d7c, u8 *, 0xE) == 0x64) {
        M2C_FIELD(native_data_ov001_02238d7c, u8 *, 0xE) = 0U;
        if (((((u32) M2C_FIELD((void *) native_fn_0207afec((u32) M2C_FIELD(native_data_ov001_02238d7c, u16 *, 0x36)), u16 *, 8) << 0x10) >> 0x1C) == 1) || ((M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, void **, 0x60), u8 *, 0x1FD) != 0) && (native_fn_0207b058((u32) M2C_FIELD(native_data_ov001_02238d7c, u16 *, 0x36), 1U) != 0) && (M2C_FIELD((void *) native_fn_02065d88((u32) M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, void **, 0x60), u8 *, 0x1FD)), u8 *, 0x2D) == 4)) || (M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, void **, 0x60), s8 *, 0x236) != 0)) {
            M2C_FIELD(native_data_ov001_02238d7c, s8 *, 0x13) = 6;
        } else {
            M2C_FIELD(native_data_ov001_02238d7c, s8 *, 0x13) = 5;
        }
    }
    return 0U;
}
