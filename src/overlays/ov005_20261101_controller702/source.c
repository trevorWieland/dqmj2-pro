#include "context.h"
void native_ov005_021e1600(void) {
    u32 *auxiliary = native_data_ov005_021ed494;
    u32 temp_r0;
    u32 temp_r0_2;

    native_fn_0200f3e0(native_data_ov005_021ed484);
    M2C_FIELD(native_data_ov005_021ed438, s32 *, 0x4C) = (s32) ((u32) M2C_FIELD(native_data_ov005_021ed438, s32 *, 0x4C) + 0x7D0U);
    native_fn_02089804();
    M2C_FIELD(native_data_ov005_021ed438, s32 *, 0x18) = 0;
    native_fn_02008c58(0, native_data_ov005_021edfe0, 0x2300);
    native_fn_02089aa4(native_data_ov005_021edfe0, 0x2300);
    if (*(u8 *) native_fn_ov005_021decb0() == 0) {
        native_fn_02041538(0, 2, 0xA);
    }
    M2C_FIELD(native_data_ov005_021ed438, u32 *, 0x40) = native_fn_02063f6c();
    M2C_FIELD(native_data_ov005_021ed438, s32 *, 0x38) = (s32) *auxiliary;
    native_fn_ov005_021dfacc();
    temp_r0 = native_fn_020642dc() - 0x2A;
    switch (temp_r0) {
    case 0:
        native_fn_ov005_021e026c(3, 1U, 0, 0x1A, 0, 3);
        native_fn_ov005_021e155c(1);
        native_fn_01ff8580(1);
        break;
    case 1:
        native_fn_ov005_021e026c(3, 2U, 0, 0x1A, 0, 3);
        native_fn_ov005_021e155c(1);
        native_fn_01ff8580(1);
        break;
    case 6:
        native_fn_ov005_021e1048(0x57);
        native_fn_ov005_021e0de0(0);
        if (*(s32 *) native_fn_02064340() == 1) {
            native_fn_ov005_021e155c(0x21);
            native_fn_ov005_021e00b4(0x13, 0, 8, 1);
            M2C_FIELD(native_data_ov005_021ed438, u8 *, 4) = (u8) native_fn_020bf4d4();
            native_fn_ov005_021e026c(8, M2C_FIELD(native_data_ov005_021ed438, u8 *, 4), 0, 0, 0, 2);
            M2C_FIELD(native_data_ov005_021ed438, s32 *, 0x48) = 1;
            *(s32 *) native_fn_02064340() = 0;
        } else {
            temp_r0_2 = native_fn_ov005_021e0fb0(M2C_FIELD(M2C_FIELD(native_data_ov005_021ed438, u32 *, 0x40), s32 *, 0x44));
            if (temp_r0_2 != 0) {
                native_fn_02048094(temp_r0_2, 0);
                native_fn_ov005_021e0730(0x13, 2, 0xC);
            } else {
                native_fn_ov005_021e0730(0x13, 2, 0xD);
            }
            native_fn_ov005_021e155c(0x20);
            native_fn_ov005_021e0de0(0);
        }
        break;
    case 10:
        native_fn_ov005_021e0de0(1);
        native_fn_ov005_021e026c(4, 0U, 0, 1, 0, 0);
        native_fn_ov005_021e155c(0);
        break;
    case 7:
        if (M2C_FIELD((void *) native_fn_020bf218(), u8 *, 0xAF) == 3) {
            native_fn_02048034(native_fn_020bf218() + 0xB0, 0);
            native_fn_ov005_021e0708(0x13, 2, 0xE);
            native_fn_ov005_021e155c(0x35);
            M2C_FIELD(native_data_ov005_021ed438, s32 *, 0x64) = 0x3C;
        } else {
            native_fn_ov005_021e155c(0x1C);
            native_fn_01ff8580(1);
        }
        break;
    case 8:
        *native_data_ov005_021e7764 = -1;
        native_fn_ov005_021e155c(0x1D);
        M2C_FIELD(native_data_ov005_021ed438, s32 *, 0x64) = 0x2C;
        native_fn_01ff8580(1);
        break;
    default:
    case 2:
    case 3:
    case 4:
    case 5:
    case 9:
        *(s32 *) native_fn_02064340() = 0;
        if (native_fn_020bef58() == 1) {
            if (native_fn_020bf084() != 0) {
                M2C_FIELD(native_data_ov005_021ed438, s32 *, 0x18) = 1;
            }
            native_fn_ov005_021e155c(0x1A);
            native_fn_ov005_021e0de0(0);
        } else {
            native_fn_ov005_021e155c(0);
            native_fn_ov005_021e0de0(1);
            native_fn_ov005_021e026c(4, 0U, 0, 1, 0, 0);
            native_fn_ov005_021e155c(0);
            native_fn_ov005_021e0df8(0x32);
            native_fn_01ff8580(0);
            native_fn_01ff8580(1);
        }
        break;
    }
    native_fn_ov005_021e0e28();
    native_fn_020bef48(0);
    native_fn_020642cc(0);
    M2C_FIELD(native_data_ov005_021ed438, u32 *, 0x28) = native_fn_0202a37c(1, 0xA000, 0x20);
    M2C_FIELD(native_data_ov005_021ed438, s32 *, 0x14) = 0;
    M2C_FIELD(native_data_ov005_021ed438, s32 *, 0x34) = 0;
    M2C_FIELD(native_data_ov005_021ed438, s8 *, 9) = 3;
    M2C_FIELD(native_data_ov005_021ed438, s8 *, 5) = 0;
    M2C_FIELD(native_data_ov005_021ed438, s32 *, 0x2C) = 0;
    M2C_FIELD(native_data_ov005_021ed438, s32 *, 0x30) = 0;
    M2C_FIELD(native_data_ov005_021ed438, s8 *, 7) = 0;
    M2C_FIELD(native_data_ov005_021ed438, s8 *, 0) = -1;
}
