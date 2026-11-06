#include "context.h"
u32 native_ov006_021e3064(void) {
    u32 var_r0;
    s32 temp_r1;
    s8 var_r1;
    u32 var_r4;
    u32 temp_r5;
    u32 temp_r5_2;
    u32 temp_r5_3;
    u32 var_r5;

    var_r4 = 5;
    switch (native_data_ov006_02217be0.field_c) {
    default:
        break;
    case 0:
        if (native_fn_ov006_021dfd34() == 2) {
            native_fn_02067a60(7);
            native_fn_ov006_021df974(1, 0xB, native_fn_02063ef8(), 0x100);
            native_fn_ov006_021e2f58(1);
        }
        break;
    case 1:
        if (native_fn_ov006_021dfd34() == 2) {
            native_fn_ov006_021df590(0x57);
            native_fn_ov006_021dee68();
            native_fn_ov006_021ded5c(0xF, 4, 0x68U);
            native_fn_ov006_021e2f58(4);
        }
        break;
    case 4:
        if (M2C_FIELD((void *) native_fn_ov006_021df150(), u16 *, 2) & 0xFF7) {
            native_fn_ov006_021df590(0x52);
            native_fn_ov006_021dee68();
            native_fn_ov006_021ded5c(0xF, 4, 0x69U);
            native_fn_ov006_021e2f58(5);
        }
        break;
    case 5:
        if (M2C_FIELD((void *) native_fn_ov006_021df150(), u16 *, 2) & 0xFF7) {
            native_fn_ov006_021df590(0x52);
            native_fn_ov006_021dee68();
            native_fn_02048034(native_fn_0205dc70(0xF, 2, (u16) (M2C_FIELD((void *) native_fn_02067748(), s32 *, 4) + 0x3B)), 0);
            native_fn_02048034(native_fn_0205dc70(0xF, 2, (u16) (native_fn_02067d54(*(u32 *)(native_data_ov006_02217bf0 + (M2C_FIELD((void *) native_fn_02067748(), s32 *, 4) * 4))) + 0xA4)), 0x20);
            native_fn_ov006_021ded5c(0xF, 4, 0x23U);
            native_fn_ov006_021e2f58(6);
            native_fn_ov006_021db59c(1, 0, 0);
            native_fn_ov006_021d77e8(4);
        }
        break;
    case 6:
        if (M2C_FIELD((void *) native_fn_ov006_021df150(), u16 *, 2) & 0xFF7) {
            native_fn_ov006_021df590(0x52);
            native_fn_ov006_021dee68();
            native_fn_ov006_021ded5c(0xF, 4, (u16) (native_fn_ov006_021e3b10() + 0x4E));
            native_fn_ov006_021e2f58(8);
            if (native_fn_ov006_021e3b10() == 0) {
                native_data_ov006_02217be0.field_0 = 0x3E;
                native_fn_ov006_021e2f58(7);
                native_fn_ov006_021def28(1);
            }
            if (native_fn_ov006_021e3b10() == 1) {
                native_fn_ov006_021e2f58(7);
                native_data_ov006_02217be0.field_0 = 0x3B;
                native_fn_ov006_021def28(1);
            }
        }
        break;
    case 7:
        if (native_fn_0205e844(native_data_ov006_02217be0.field_0) != 0) {
            native_fn_ov006_021e2f58(8);
            native_fn_ov006_021def28(0);
        }
        break;
    case 8:
        if (M2C_FIELD((void *) native_fn_ov006_021df150(), u16 *, 2) & 0xFF7) {
            native_fn_ov006_021df590(0x52);
            native_fn_ov006_021dee68();
            temp_r5 = native_fn_02063ef8();
            native_fn_02048094(native_fn_ov006_021de358(M2C_FIELD(temp_r5, s32 *, 0xC) - M2C_FIELD((void *) native_fn_02063ef8(), u8 *, 3)), 0);
            native_fn_02048094(native_fn_ov006_021de358(M2C_FIELD((void *) native_fn_02067904(), s32 *, 0xC)), 0x20);
            native_fn_ov006_021ded5c(0xF, 4, 0x51U);
            native_fn_ov006_021e2f58(9);
        }
        break;
    case 9:
        if (M2C_FIELD((void *) native_fn_ov006_021df150(), u16 *, 2) & 0xFF7) {
            native_fn_ov006_021df590(0x52);
            native_fn_ov006_021dee68();
            if (M2C_FIELD((void *) native_fn_02063ef8(), u8 *, 2) != 0) {
                var_r5 = 0;
                if (M2C_FIELD((void *) native_fn_02063ef8(), u8 *, 2) & 1) {
                    var_r5 += 1;
                }
                if (M2C_FIELD((void *) native_fn_02063ef8(), u8 *, 2) & 2) {
                    var_r5 += 1;
                }
                if (M2C_FIELD((void *) native_fn_02063ef8(), u8 *, 2) & 4) {
                    var_r5 += 1;
                }
                native_fn_02048094(var_r5, 0);
                native_fn_02048094(native_fn_ov006_021de358((s32) M2C_FIELD((void *) native_fn_02063ef8(), u8 *, 3)), 0x20);
                native_fn_ov006_021ded5c(0xF, 4, 0x8FU);
                native_fn_ov006_021e2f58(0xB);
            } else {
                temp_r5_2 = native_fn_020679f0();
                native_fn_02048094(native_fn_ov006_021de358(M2C_FIELD(temp_r5_2, s32 *, 0x2C) + M2C_FIELD((void *) native_fn_020679f0(), s32 *, 0x30)), 0);
                native_fn_ov006_021ded5c(0xF, 4, 0x52U);
                native_fn_ov006_021e2f58(0xB);
            }
        }
        break;
    case 10:
        if (M2C_FIELD((void *) native_fn_ov006_021df150(), u16 *, 2) & 0xFF7) {
            native_fn_ov006_021df590(0x52);
            native_fn_ov006_021dee68();
            temp_r5_3 = native_fn_020679f0();
            native_fn_02048094(native_fn_ov006_021de358(M2C_FIELD(temp_r5_3, s32 *, 0x2C) + M2C_FIELD((void *) native_fn_020679f0(), s32 *, 0x30)), 0);
            native_fn_ov006_021ded5c(0xF, 4, 0x52U);
            native_fn_ov006_021e2f58(0xB);
        }
        break;
    case 11:
        if (M2C_FIELD((void *) native_fn_ov006_021df150(), u16 *, 2) & 0xFF7) {
            native_fn_ov006_021df590(0x52);
            native_fn_ov006_021dee68();
            native_fn_ov006_021ded5c(0xF, 4, *(u16 *)(native_data_ov006_0220d0f0 + (native_fn_ov006_021e3b7c(M2C_FIELD((void *) native_fn_020679f0(), s32 *, 4)) * 2)));
            native_fn_ov006_021e2f58(0xC);
        }
        break;
    case 12:
        if (M2C_FIELD((void *) native_fn_ov006_021df150(), u16 *, 2) & 0xFF7) {
            native_fn_ov006_021df590(0x52);
            native_fn_ov006_021dee68();
            native_fn_01ff8604(0);
            native_fn_02064488(2);
            native_fn_ov006_021e2f58(2);
            native_fn_ov006_021dee68();
            native_fn_ov006_021ded5c(0xF, 3, 3U);
            native_fn_ov006_021def28(1);
        }
        break;
    case 2:
        if (native_fn_020644c0() != 0) {
            native_fn_01ff8604(1);
            native_fn_ov006_021df590(0x57);
            native_fn_ov006_021dee68();
            native_fn_ov006_021ded5c(0xF, 3, 4U);
            native_fn_ov006_021e2f58(3);
        }
        break;
    case 3:
        if (M2C_FIELD((void *) native_fn_ov006_021df150(), u16 *, 2) & 0xFF7) {
            native_fn_ov006_021dee68();
            native_fn_ov006_021df590(0x52);
            native_fn_ov006_021df4c8(-1);
            native_fn_0205e814(0, 0, 0x1E);
            native_data_ov006_02217be0.field_8 = 0x20;
            native_fn_ov006_021e2f58(0x18);
        }
        break;
    case 24:
        temp_r1 = native_data_ov006_02217be0.field_8 - 1;
        native_data_ov006_02217be0.field_8 = temp_r1;
        if (temp_r1 == 0) {
            native_fn_020642cc(0x2D);
            var_r4 = 0;
        }
        break;
    case 13:
        if (native_fn_ov006_021dfd34() == 2) {
            native_fn_ov006_021df974(1, 9, (u32) native_data_ov006_02217c00, 0x18);
            native_fn_ov006_021e2f58(0xF);
        }
        break;
    case 15:
        if (native_fn_ov006_021dfd34() == 2) {
            native_fn_ov006_021df974(1, 0xB, native_fn_02063ef8(), 0x100);
            native_fn_ov006_021e2f58(0xE);
        }
        break;
    case 14:
        if (native_fn_ov006_021dfd34() == 2) {
            native_fn_ov006_021dee68();
            native_fn_02048094(M2C_FIELD((void *) native_fn_02067b58(), u32 *, 0x24), 0);
            native_fn_02048034(native_fn_0205dc70(0xF, 2, (u16) (M2C_FIELD((void *) native_fn_02067748(), s32 *, 4) + 0x3B)), 0x20);
            native_fn_ov006_021ded5c(0xF, 4, 0x78U);
            native_fn_ov006_021e2f58(0x10);
            native_fn_02063f24(native_data_ov006_02217be0.field_28, native_data_ov006_02217be0.field_20);
            native_fn_ov006_021d8288(0);
            native_fn_0205e814(0, 0, 0x1E);
            native_fn_020414b0(0x2F);
            native_fn_02041510(1, 2, 0x1E);
        }
        break;
    case 16:
        if (M2C_FIELD((void *) native_fn_ov006_021df150(), u16 *, 2) & 0xFF7) {
            native_fn_ov006_021df590(0x52);
            native_fn_ov006_021dee68();
            native_fn_ov006_021ded5c(0xF, 4, 0x79U);
            native_fn_ov006_021e2f58(0x12);
        }
        break;
    case 18:
        if ((native_fn_02041800() != 1) && (M2C_FIELD((void *) native_fn_ov006_021df150(), u16 *, 2) & 0xFF7)) {
            native_fn_ov006_021df590(0x52);
            native_fn_ov006_021dee68();
            native_fn_ov006_021e2f58(0x11);
            native_fn_ov006_021d83b4();
            native_fn_ov006_021db59c(2, M2C_FIELD((void *) native_fn_02067748(), s32 *, 4), 0);
            native_fn_ov006_021d77e8(4);
            native_fn_ov006_021e9444(0xDC);
        }
        break;
    case 17:
        if (native_fn_ov006_021e9484() != 0) {
            native_fn_ov006_021df524(0x50);
            native_fn_ov006_021ded5c(0xF, 4, 0x7AU);
            native_fn_ov006_021e2f58(0x13);
        }
        break;
    case 19:
        if (M2C_FIELD((void *) native_fn_ov006_021df150(), u16 *, 2) & 0xFF7) {
            native_fn_ov006_021df590(0x52);
            native_fn_ov006_021dee68();
            if ((*(s32 *) native_fn_ov006_021e2f38() == 0) || ((u32) *(u32 *) native_fn_ov006_021e2f38() > 0xAU)) {
                native_fn_ov006_021ded5c(0xF, 4, 0x7BU);
            } else {
                native_fn_ov006_021ded5c(0xF, 4, 0x7CU);
            }
            native_fn_ov006_021e2f58(0x14);
        }
        break;
    case 20:
        if (M2C_FIELD((void *) native_fn_ov006_021df150(), u16 *, 2) & 0xFF7) {
            native_fn_ov006_021df590(0x52);
            native_fn_ov006_021dee68();
            native_fn_02048034(native_fn_0205dc70(0xF, 2, (u16) (M2C_FIELD((void *) native_fn_02067748(), s32 *, 4) + 0x3B)), 0x20);
            native_fn_02048094(*(u32 *) native_fn_ov006_021e2f38(), 0x40);
            native_data_ov006_02217be0.field_4 = 3U;
            if (M2C_FIELD((void *) native_fn_ov006_021e2f38(), u16 *, 0xC) != 0) {
                native_data_ov006_02217be0.field_4 = 2U;
            }
            if (*(s32 *) native_fn_ov006_021e2f38() == 1) {
                native_data_ov006_02217be0.field_4 = 0U;
            }
            if (((u32) *(u32 *) native_fn_ov006_021e2f38() >= 2U) && ((u32) *(u32 *) native_fn_ov006_021e2f38() <= 0xAU)) {
                native_data_ov006_02217be0.field_4 = 1U;
            }
            switch (native_data_ov006_02217be0.field_4) {
            default:
                break;
            case 0:
                native_fn_ov006_021da3e8(5);
                native_fn_ov006_021ded5c(0xF, 4, 0x2EU);
                native_fn_ov006_021def28(1);
                native_data_ov006_02217be0.field_0 = 0x3F;
                native_fn_ov006_021e2f58(0x15);
                break;
            case 1:
                native_fn_ov006_021da3e8(6);
                native_fn_ov006_021ded5c(0xF, 4, 0x2DU);
                native_fn_ov006_021def28(1);
                native_data_ov006_02217be0.field_0 = 0x3E;
                native_fn_ov006_021e2f58(0x15);
                break;
            case 2:
                native_fn_ov006_021da3e8(7);
                native_fn_ov006_021ded5c(0xF, 4, 0x2DU);
                native_fn_ov006_021def28(1);
                native_data_ov006_02217be0.field_0 = 0x3E;
                native_fn_ov006_021e2f58(0x15);
                break;
            case 3:
                native_fn_ov006_021da3e8(8);
                native_fn_ov006_021ded5c(0xF, 4, 0x2DU);
                native_fn_ov006_021e2f58(0x16);
                break;
            }
            native_fn_ov006_021d77e8(1);
        }
        break;
    case 21:
        if (native_fn_0205e844(native_data_ov006_02217be0.field_0) != 0) {
            native_fn_ov006_021e2f58(0x16);
            native_fn_ov006_021def28(0);
        }
        break;
    case 22:
        if (M2C_FIELD((void *) native_fn_ov006_021df150(), u16 *, 2) & 0xFF7) {
            native_fn_ov006_021df590(0x52);
            native_fn_ov006_021dee68();
            if (native_data_ov006_02217be0.field_4 != 3) {
                native_fn_02064304(native_fn_ov006_021e2f38() + 0xC);
                if (native_data_ov006_02217be0.field_4 == 0) {
                    var_r0 = native_fn_020642f8();
                    var_r1 = 5;
                } else {
                    var_r0 = native_fn_020642f8();
                    var_r1 = 6;
                }
                M2C_FIELD(var_r0, s8 *, 4) = var_r1;
                var_r4 = 4;
            } else {
                native_fn_ov006_021ded5c(0xF, 4, 0x59U);
                native_fn_ov006_021e2f58(0x17);
            }
        }
        break;
    case 23:
        if (M2C_FIELD((void *) native_fn_ov006_021df150(), u16 *, 2) & 0xFF7) {
            native_fn_ov006_021df590(0x52);
            native_fn_ov006_021dee68();
            native_fn_01ff8604(0);
            native_fn_02064488(2);
            native_fn_ov006_021e2f58(2);
            native_fn_ov006_021dee68();
            native_fn_ov006_021ded5c(0xF, 3, 3U);
            native_fn_ov006_021def28(1);
        }
        break;
    }
    return var_r4;
}
