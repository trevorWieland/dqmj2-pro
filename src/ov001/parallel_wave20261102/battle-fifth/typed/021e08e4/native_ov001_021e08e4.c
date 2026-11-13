#include "context.h"
u32 native_ov001_021e08e4(void) {
    s8 temp_r0;
    u32 temp_r0_2;
    u32 temp_r0_3;
    u32 temp_r4;
    u32 temp_r5;
    u32 var_r4;
    u32 var_r8;
    u8 var_r0;

    var_r4 = 0;
    if (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x23) == 0x0) {
        if ((native_fn_020444ec() == 0) || (temp_r4 = native_fn_01ffa824(), ((u32) (u8) temp_r4 < native_fn_01ffa84c()))) {
            M2C_FIELD(native_data_ov001_022389b8, u8 *, 0) = 0;
            M2C_FIELD(native_data_ov001_022389b8, s8 *, 1) = 1;
        } else {
            M2C_FIELD(native_data_ov001_022389b8, u8 *, 0) = 1;
            M2C_FIELD(native_data_ov001_022389b8, s8 *, 1) = 0;
        }
        M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x22) = 0;
        M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x23) = 0xA;
        var_r4 = 1;
    }
    else if (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x23) == 0xA) {
        if ((s8) native_data_ov001_022389b8[M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x22)] == 0) {
            var_r0 = M2C_FIELD(native_data_ov001_022388ec, u8 *, 0x18);
        } else {
            var_r0 = M2C_FIELD(native_data_ov001_022388ec, u8 *, 0x19);
        }
        M2C_FIELD(native_data_ov001_022388ec, u8 *, 0x1F) = var_r0;
        if ((s8) M2C_FIELD(native_data_ov001_022388ec, u8 *, 0x1F) == 0) {
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x22) = (s8) (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x22) + 1);
            if ((s32) M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x22) >= 2) {
                M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x23) = 0x64;
            }
        } else {
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x20) = 0;
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x23) = 0x14;
        }
    }
    else if (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x23) == 0x14) {
        temp_r0 = (s8) native_data_ov001_022389b8[M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x22)];
        temp_r0_2 = ov001_side_slot_record_021db438((u32) temp_r0, (u32) *(temp_r0 + (native_data_ov001_0223893c + (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x20) * 2))));
        native_fn_ov001_021d7e80(temp_r0_2);
        temp_r5 = native_fn_0205d790(0x101U);
        if (ov001_record_is_active_021db8d0(temp_r0_2) != 0) {
            ov001_effect_resource_create_021eec7c(0x101U, temp_r0_2, temp_r5);
            native_fn_ov001_021dbf98(temp_r0_2, 8, 1, -1, 0);
        }
        native_fn_02048034(M2C_FIELD(temp_r0_2, void **, 0x1E8) + 0xB2, 0);
        ov001_begin_state_transition_021f1354(1, 0, (u8) ((u32) (M2C_FIELD((void *) native_fn_020449d4((u32) M2C_FIELD(M2C_FIELD(temp_r0_2, void **, 0x1E8), s16 *, 0x2A)), u16 *, 4) << 0x18) >> 0x1C) + 0x2F, 1);
        ov001_select_mode_id_021f1438(native_fn_ov001_021f1414((u32) native_data_ov001_022389b8[M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x22)]));
        M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x23) = 0x1E;
        M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x21) = 0;
    }
    else if (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x23) == 0x1E) {
        M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x21) = (s8) (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x21) + 1);
        if ((s32) M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x21) > 0x1E) {
            ov001_clear_state_flag4_021f14a4();
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x23) = 0x23;
        }
    }
    else if (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x23) == 0x23) {
        if (native_fn_ov001_021f14e4() == 0) {
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x23) = 0x28;
        }
    }
    else if (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x23) == 0x28) {
        var_r8 = 0;
        do {
            temp_r0_3 = ov001_side_slot_record_021db438((u32) (s8) native_data_ov001_022389b8[M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x22)], var_r8);
            if (ov001_record_is_active_021db8d0(temp_r0_3) != 0) {
                native_fn_ov001_021ee91c(temp_r0_3, M2C_FIELD(temp_r0_3, s8 *, 0x234));
            }
            var_r8 += 1;
        } while ((s32) var_r8 < 3);
        native_fn_02048034(native_data_ov001_0222ebd4, 0);
        ov001_begin_state_transition_021f1354(5, 3, 8, 1);
        M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x23) = 0x32;
        M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x21) = 0;
    }
    else if (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x23) == 0x32) {
        M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x21) = (s8) (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x21) + 1);
        if ((s32) M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x21) > 0x32) {
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x23) = 0x3C;
            ov001_clear_state_flag4_021f14a4();
        }
    }
    else if (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x23) == 0x3C) {
        if (native_fn_ov001_021f14e4() == 0) {
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x20) = (s8) (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x20) + 1);
            if ((s32) M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x20) >= (s32) (s8) M2C_FIELD(native_data_ov001_022388ec, u8 *, 0x1F)) {
                M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x22) = (s8) (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x22) + 1);
                if ((s32) M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x22) >= 2) {
                    M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x23) = 0x64;
                } else {
                    M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x23) = 0xA;
                }
            } else {
                M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x23) = 0x14;
            }
        }
    }
    else if (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x23) == 0x64) {
        M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x23) = 0;
        M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x22) = 0;
        native_fn_ov001_021f1324();
        M2C_FIELD(native_data_ov001_022388ec, u8 *, 8) = (u8) M2C_FIELD(native_data_ov001_022388ec, u8 *, 4);
    }
    return var_r4;
}
