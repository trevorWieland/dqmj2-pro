#include "context.h"
u32 native_itcm_01ff97e0(void) {
    u32 temp_r0_2;
    u8 *temp_r0;
    s8 temp_r1_2;
    u16 temp_r1;
    s32 var_r2;
    u16 temp_r2;
    u16 temp_r2_2;
    u8 *temp_r4;
    s8 temp_r5;
    u32 var_r5;
    u32 *temp_r6;
    u32 var_r6;
    s32 var_r7;
    u32 temp_r10;

    temp_r6 = native_fn_ov000_02223c60();
    temp_r4 = native_fn_ov000_02223c54();
    temp_r5 = M2C_FIELD(native_fn_ov000_02223c54(), s8 *, 0x5A);
    var_r6 = *temp_r6;
    if (M2C_FIELD(native_data_021ceb54, s32 *, 4) == 1) {
        native_fn_020885d0();
        return var_r6;
    }
    if (native_fn_01ffb230() == 1) {
        if (M2C_FIELD(native_data_021ceb54, u32 *, 0xC) == 0x18) {
            native_fn_01ffa440();
        }
        return var_r6;
    }
    switch (M2C_FIELD(native_data_021ceb54, u32 *, 0xC)) {
    default:
        break;
    case 1:
        var_r6 = native_fn_01ff97a0();
        break;
    case 0:
        native_fn_01ffb4c4();
        native_fn_01ff86cc();
        break;
    case 19:
        native_fn_020889cc(1);
        native_fn_01ff8eec();
        native_fn_01ffa5ac(native_data_021ceb94, 0x34, 1);
        temp_r1 = M2C_FIELD(native_data_021ceb54, u16 *, 0);
        M2C_FIELD(native_data_021ceb54, u16 *, 0) = (u16) (temp_r1 - 1);
        if (temp_r1 == 0) {
            M2C_FIELD(native_data_021ceb54, u32 *, 0xC) = 0x14U;
            M2C_FIELD(native_data_021ceb54, s32 *, 0x54) = 1;
            native_fn_01ffa5ac(native_data_021ceb94, 0x34, 2);
            native_fn_01ffafb8();
        }
        break;
    case 2:
        native_fn_01ffb4c4();
        native_fn_01ff883c();
        break;
    case 3:
        native_fn_01ffb4c4();
        native_fn_01ff8964();
        break;
    case 4:
        native_fn_01ffb4c4();
        native_fn_01ff8a4c();
        break;
    case 6:
        native_fn_01ff96bc();
        break;
    case 5:
        native_fn_01ffb03c();
        native_fn_01ff8c50();
        break;
    case 15:
        if (native_fn_01ffa2fc() == 1) {
            temp_r0 = native_fn_ov000_02223c54();
            M2C_FIELD(native_data_021ceb54, u32 *, 0xC) = 0x10U;
            if (M2C_FIELD(temp_r0, s8 *, 0x58) == 1) {
                native_fn_020620e8(0x15, 1);
            }
        }
        break;
    case 16:
        native_fn_01ff8f5c();
        break;
    case 17:
        temp_r2 = M2C_FIELD(native_data_021ceb54, u16 *, 0);
        M2C_FIELD(native_data_021ceb54, u16 *, 0) = (u16) (temp_r2 + 1);
        if ((u32) temp_r2 > 0x5AU) {
            M2C_FIELD(native_data_021ceb54, u32 *, 0xC) = 4U;
            native_fn_01ffafb8();
            temp_r1_2 = M2C_FIELD(temp_r4, s8 *, 0x58);
            if (temp_r1_2 == 1) {
                native_fn_02061260(0);
                native_fn_01ffac9c(2, 0, 0xD, 1, 2, 2);
            } else if (M2C_FIELD(native_data_021ceb54, s32 *, 8) == 1) {
                native_fn_01ffac9c(2, 0, 2, 3, 2, (s32) (s16) (temp_r1_2 + 1));
            } else {
                native_fn_01ffac9c(2, 0, 7, 0, 0, 2);
            }
        }
        break;
    case 18:
        native_fn_01ffb03c();
        native_fn_01ff9204();
        break;
    case 20:
        native_fn_020889cc(2);
        if (native_fn_01ffa5fc(0U, 2) != 0) {
            M2C_FIELD(native_data_021ceb54, u32 *, 0xC) = 7U;
        }
        break;
    case 21:
        if (native_fn_01ffa5fc(0U, 2) != 0) {
            M2C_FIELD(native_data_021ceb54, u32 *, 0xC) = 0x16U;
            M2C_FIELD(native_data_021ceb54, u16 *, 0) = 0xAU;
        }
        break;
    case 22:
        temp_r2_2 = M2C_FIELD(native_data_021ceb54, u16 *, 0);
        M2C_FIELD(native_data_021ceb54, u16 *, 0) = (u16) (temp_r2_2 - 1);
        if (temp_r2_2 == 0) {
            M2C_FIELD(native_data_021ceb54, u32 *, 0xC) = 6U;
            native_fn_01ffa804();
        }
        break;
    case 23:
        native_fn_01ff8f5c();
        if (M2C_FIELD((void *) native_fn_01ffb35c(), u16 *, 2) & 0xFF7) {
            native_fn_01ffafb8();
            native_fn_01ffae5c(0x10, 0xF, 1, -1, 1);
            M2C_FIELD(native_data_021ceb54, u32 *, 0xC) = 0x10U;
            native_fn_0205e7a8(-1, 0x52);
        }
        break;
    case 24:
        native_fn_01ffb4c4();
        native_fn_01ff92cc();
        break;
    case 25:
        if (M2C_FIELD(temp_r4, s8 *, 0x58) == 1) {
            if ((native_fn_01ffa6c0(0, 2) != 0) || (native_fn_01ffa6c0(0, 1) != 0)) {
                M2C_FIELD(native_data_021ceb54, u32 *, 0xC) = 0x1AU;
                native_fn_020620e8(0x15, 1);
            }
        } else if (native_fn_01ffa5fc(0U, 1) != 0) {
            M2C_FIELD(native_data_021ceb54, u32 *, 0xC) = 0x1AU;
        }
        break;
    case 26:
        native_fn_01ff951c();
        break;
    case 27:
        native_fn_020889cc(2);
        if (native_fn_01ffa5fc(0U, 2) != 0) {
            M2C_FIELD(native_data_021ceb54, u32 *, 0xC) = 7U;
        }
        break;
    case 28:
        if (M2C_FIELD(temp_r4, s8 *, 0x58) == 1) {
            M2C_FIELD(native_data_021ceb54, u32 *, 0xC) = 6U;
            native_fn_01ffa804();
            native_fn_020620e8(0x1B, 1);
        } else if (native_fn_01ffa5fc(0U, 2) != 0) {
            M2C_FIELD(native_data_021ceb54, u32 *, 0xC) = 6U;
            native_fn_01ffa804();
        }
        break;
    case 7:
        if ((M2C_FIELD(temp_r4, s8 *, 0x58) == 1) && (temp_r5 == 0)) {
            native_fn_0205e7a8(-1, 0x57);
        }
        native_fn_01ffae9c(0x10, 6, 3, -1);
        M2C_FIELD(native_data_021ceb54, u32 *, 0xC) = 8U;
        M2C_FIELD(native_data_021ceb54, u16 *, 0) = 0U;
        native_fn_01ffb060(1);
        native_fn_02061260(1);
        break;
    case 8:
        M2C_FIELD(native_data_021ceb54, u16 *, 0) = (u16) (M2C_FIELD(native_data_021ceb54, u16 *, 0) + 1);
        if ((u32) M2C_FIELD(native_data_021ceb54, u16 *, 0) > 0x2DU) {
            M2C_FIELD(native_data_021ceb54, u32 *, 0xC) = 9U;
            if (M2C_FIELD(temp_r4, s8 *, 0x58) != 1) {
                native_fn_01ffa348(3);
            }
            native_fn_01ffafb8();
        }
        break;
    case 9:
        if ((M2C_FIELD(native_fn_ov000_02223c54(), s8 *, 0x59) == 1) && (M2C_FIELD(native_data_021ceb54, s32 *, 8) == 2)) {
            var_r2 = 0;
            do {
                ((u32 *)native_data_021ceb64)[var_r2] = 0;
                var_r2 += 1;
            } while (var_r2 < 0xC);
        }
        native_fn_01ffa5ac(native_data_021ceb64, 0x30, 3);
        if (native_fn_01ffa5fc(native_fn_01ffa84c(), 3) != 0) {
            var_r7 = 0;
            if ((M2C_FIELD(native_fn_ov000_02223c54(), s8 *, 0x59) == 1) && (M2C_FIELD(native_data_021ceb54, s32 *, 8) == 2)) {

            } else {
                var_r5 = 0;
                do {
                    if ((native_fn_01ffa394(var_r5) == 1) && (var_r5 != (u8) native_fn_01ffa824())) {
                        temp_r10 = native_fn_01ffa5fc(var_r5, 3);
                        temp_r0_2 = native_fn_020687dc(temp_r10, native_fn_01ffb4ec(var_r5));
                        if (temp_r0_2 == -1U) {
                            var_r7 = 1;
                        }
                        M2C_FIELD((void *) native_fn_01ffb4ec((u32) (u8) native_fn_01ffa824()), u32 *, 0x168) = temp_r0_2;
                    }
                    var_r5 = (u32) (u8) (var_r5 + 1);
                } while (var_r5 < 8U);
            }
            if (var_r7 == 1) {
                native_fn_01ffae9c(0x10, 6, 4, 0x57);
                M2C_FIELD(native_data_021ceb54, u32 *, 0xC) = 0xAU;
            } else {
                M2C_FIELD(native_data_021ceb54, u32 *, 0xC) = 0xBU;
            }
        }
        break;
    case 10:
        if (M2C_FIELD((void *) native_fn_01ffb35c(), u16 *, 2) & 0xFF7) {
            M2C_FIELD(native_data_021ceb54, u32 *, 0xC) = 0xBU;
            M2C_FIELD((void *) native_fn_01ffb4ec((u32) (u8) native_fn_01ffa824()), s32 *, 0x168) = -1;
        }
        break;
    case 11:
        native_fn_01ffafb8();
        native_fn_01ffae9c(0x10, 6, 6, 0x57);
        native_fn_01ffb060(1);
        M2C_FIELD(native_data_021ceb54, u32 *, 0xC) = 0xCU;
        break;
    case 12:
        native_fn_02089644();
        native_fn_02089454();
        native_fn_02064488(2);
        M2C_FIELD(native_data_021ceb54, u32 *, 0xC) = 0xDU;
        break;
    case 13:
        if (native_fn_020644c0() != 0) {
            native_fn_02089680();
            native_fn_01ffafb8();
            native_fn_01ffae9c(0x10, 6, 8, 0x57);
            M2C_FIELD(native_data_021ceb54, u32 *, 0xC) = 0xEU;
            M2C_FIELD(native_data_021ceb54, u16 *, 0) = 0U;
            native_fn_01ffb060(1);
            if (M2C_FIELD(native_data_021ceb54, s32 *, 8) == 1) {
                native_fn_0205e814(0, 0, 0x14);
            }
        }
        break;
    case 14:
        if ((u32) M2C_FIELD(native_data_021ceb54, u16 *, 0) < 0x1EU) {
            M2C_FIELD(native_data_021ceb54, u16 *, 0) = (u16) (M2C_FIELD(native_data_021ceb54, u16 *, 0) + 1);
        } else {
            native_fn_01ffa5ac(native_data_021ceb64, 0x30, 4);
            if (native_fn_01ffa5fc(0U, 4) != 0) {
                native_fn_01ffafb8();
                M2C_FIELD(native_data_021ceb54, u32 *, 0xC) = 1U;
                *(s8 *) native_fn_01ffa010() = 0;
                native_fn_02041538(1, 2, 0xA);
            }
        }
        break;
    }
    native_fn_01ffab90();
    if (M2C_FIELD(native_fn_01ffb340(), u8 *, 0x11) != 0) {
        native_fn_0208870c();
    }
    native_fn_01ffa4b4();
    return var_r6;
}
