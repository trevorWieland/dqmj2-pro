#include "context.h"
u32 native_ov001_021dee18(void) {
    s8 var_r0;
    void *temp_r0;
    u8 temp_r1;
    u8 temp_r1_2;
    u16 temp_r2;
    u32 temp_r2_2;
    u32 temp_r4;
    u32 var_r5;
    u32 temp_r6;
    s8 sp1;
    s8 sp0;

    native_fn_ov001_021dcb90();
    native_data_ov001_022388ec.field_18 = 0;
    native_data_ov001_022388ec.field_19 = 0;
    native_fn_ov001_021e8178(native_data_ov001_022388ec.field_12, &sp1, &sp0);
    if (native_data_ov001_022388ec.field_1a == 0) {
        native_data_ov001_022388ec.field_a = (s8) native_fn_ov001_021e85f4(sp1, sp0);
        if ((M2C_FIELD((void *) ov001_side_slot_record_021db438(sp1, sp0), s8 *, 0x237) != 0) && (native_data_ov001_022388ec.field_7 == 0)) {
            native_fn_ov001_021e8510(sp1, sp0);
        }
        if ((*(u16 *) native_fn_ov001_021e81d0(sp1, sp0) == 6) && (native_data_ov001_022388ec.field_a == 0)) {
            native_data_ov001_022388ec.field_a = 1;
        }
        if (native_data_ov001_022388ec.field_a == 0) {
            native_fn_ov001_021e865c(sp1, sp0);
        }
    } else if (native_data_ov001_022388ec.field_7 == 0) {
        native_fn_ov001_021e8510(sp1, sp0);
    }
    temp_r4 = ov001_side_slot_record_021db438(sp1, sp0);
    if ((native_fn_ov001_021e29d8() == 0) && (native_fn_ov001_0220b770() == 0)) {
        native_fn_ov001_021e8424(sp1, sp0);
    } else {
        native_data_ov001_022388ec.field_11 = 0;
    }
    temp_r0 = (void *) native_fn_ov001_021e81d0(sp1, sp0);
    var_r5 = ov001_side_slot_record_021db438(M2C_FIELD(temp_r0, u8 *, 2), M2C_FIELD(temp_r0, s8 *, 3));
    temp_r2 = M2C_FIELD(temp_r0, u16 *, 0);
    native_data_ov001_022388ec.field_36 = temp_r2;
    temp_r6 = native_fn_0207afec(temp_r2);
    if ((var_r5 != 0) && (ov001_record_is_active_021db8d0(var_r5) == 0) && ((M2C_FIELD(var_r5, u8 *, 0x31C) == 0) || (((u32) (M2C_FIELD(temp_r6, u16 *, 8) << 0x14) >> 0x1C) != 3))) {
        var_r5 = native_fn_ov001_021db918(M2C_FIELD(temp_r0, u8 *, 2));
    }
    native_data_ov001_022388ec.field_17 = (u8) M2C_FIELD(temp_r0, u8 *, 2);
    native_data_ov001_022388ec.field_48 = temp_r4;
    if (native_fn_ov001_0220b770() != 0) {
        native_data_ov001_022388ec.field_8 = 0x16;
    } else if (ov001_record_is_active_021db8d0(temp_r4) == 0) {
        native_data_ov001_022388ec.field_8 = 0x18;
    } else if ((native_fn_ov001_021dc138(temp_r4) != 0) && ((s32) native_fn_0207b674(0x41, M2C_FIELD(temp_r4, s32 *, 0x1E8) + 0x46) > 0) && (((M2C_FIELD(temp_r4, u8 *, 0x31E) == 0) && (native_data_ov001_022388ec.field_1b == 0)) || ((M2C_FIELD(temp_r4, u8 *, 0x31E) == 1) && (native_data_ov001_022388ec.field_7 == 0)))) {
        native_fn_ov001_021dd108(temp_r4);
        native_fn_ov001_022142d0(2);
        native_fn_ov001_022148a0(0xB, 0, 0x41, 2);
        M2C_FIELD(native_data_ov001_022388ec.field_48, u16 *, 0x344) = 6U;
        native_fn_ov001_02214308(1);
        native_data_ov001_022388ec.field_8 = 0xB;
    } else {
        if ((M2C_FIELD(temp_r4, s8 *, 0x236) != 0) && ((s32) native_fn_0207b674(0x3E, M2C_FIELD(temp_r4, s32 *, 0x1E8) + 0x46) > 0)) {
            native_fn_ov001_021e95d8(0);
            if (M2C_FIELD(native_data_ov001_022388ec.field_48, u8 *, 0x31E) == 0) {
                var_r0 = 1;
            } else {
                var_r0 = 0;
            }
            native_data_ov001_022388ec.field_40 = ov001_side_slot_record_021db438(var_r0, 0);
            M2C_FIELD(native_data_ov001_022388ec.field_48, u16 *, 0x344) = 6U;
            native_fn_ov001_021e97a4(0xB, 0, 0x3E, 2);
            native_data_ov001_022388ec.field_8 = 5;
        } else if (native_fn_ov001_021dc108(temp_r4) == 0) {
            native_data_ov001_022388ec.field_8 = 0xF;
            if (native_fn_0207b02c(native_data_ov001_022388ec.field_36, 0x80000800) != 0) {
                native_fn_ov001_021e865c(M2C_FIELD(temp_r4, u8 *, 0x31E), M2C_FIELD(temp_r4, u8 *, 0x31F));
            }
        } else if ((native_data_ov001_022388ec.field_a == 0) && (((M2C_FIELD(native_data_ov001_022388ec.field_48, u8 *, 0x31E) == 0) && (native_data_ov001_022388ec.field_1d == 0)) || ((M2C_FIELD(native_data_ov001_022388ec.field_48, u8 *, 0x31E) == 1) && (native_data_ov001_022388ec.field_c == 0)))) {
            native_data_ov001_022388ec.field_8 = 0x2D;
        } else {
            if (native_data_ov001_022388ec.field_36 == 6) {
                native_data_ov001_022388ec.field_8 = 0x2C;
            } else {
                temp_r2_2 = (u32) (M2C_FIELD(temp_r6, u16 *, 8) << 0x1C) >> 0x1C;
                if (temp_r2_2 == 1) {
                    native_data_ov001_022388ec.field_40 = var_r5;
                    native_fn_ov001_021e95d8(native_data_ov001_022388ec.field_36);
                    M2C_FIELD(native_data_ov001_022388ec.field_48, u16 *, 0x344) = (u16) native_data_ov001_022388ec.field_36;
                    native_data_ov001_022388ec.field_8 = 5;
                }
                else if (temp_r2_2 == 2) {
                    native_data_ov001_022388ec.field_40 = temp_r4;
                    native_fn_ov001_02217a7c(native_data_ov001_022388ec.field_36);
                    M2C_FIELD(native_data_ov001_022388ec.field_48, u16 *, 0x344) = (u16) native_data_ov001_022388ec.field_36;
                    native_data_ov001_022388ec.field_8 = 9;
                }
                else if (temp_r2_2 == 3) {
                    native_data_ov001_022388ec.field_40 = temp_r4;
                    native_fn_ov001_022142d0(native_data_ov001_022388ec.field_36);
                    M2C_FIELD(native_data_ov001_022388ec.field_48, u16 *, 0x344) = (u16) native_data_ov001_022388ec.field_36;
                    native_fn_ov001_02214308(0);
                    native_data_ov001_022388ec.field_8 = 0xB;
                }
                else if (temp_r2_2 == 7) {
                    native_data_ov001_022388ec.field_40 = var_r5;
                    native_fn_ov001_02215274(native_data_ov001_022388ec.field_36);
                    native_data_ov001_022388ec.field_8 = 0xD;
                }
                else if (temp_r2_2 == 4) {
                    native_fn_ov001_0221689c(native_data_ov001_022388ec.field_36);
                    native_data_ov001_022388ec.field_8 = 0x11;
                }
                else {
                    native_data_ov001_022388ec.field_40 = var_r5;
                    if (temp_r2_2 >= 5U) {
                        native_fn_ov001_021f1bf0(native_data_ov001_022388ec.field_36);
                        M2C_FIELD(native_data_ov001_022388ec.field_48, u16 *, 0x344) = (u16) native_data_ov001_022388ec.field_36;
                        native_data_ov001_022388ec.field_8 = 7;
                    } else {
                        native_fn_ov001_021f1bf0(native_data_ov001_022388ec.field_36);
                        native_data_ov001_022388ec.field_8 = 7;
                    }
                }

            }
        }
    }
    return 1U;
}
