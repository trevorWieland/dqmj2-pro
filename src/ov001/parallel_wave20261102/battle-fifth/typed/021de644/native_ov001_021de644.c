#include "context.h"
u32 native_ov001_021de644(void) {
    s32 sp8;
    s32 sp4;
    u8 sp0;
    s32 temp_r8;
    s32 temp_r8_2;
    s32 temp_r8_3;
    s32 temp_r8_4;
    s32 var_r1;
    s32 var_r2_2;
    s32 var_r2_3;
    s32 var_r2_4;
    s8 var_r1_5;
    u32 temp_r0;
    u32 temp_r0_2;
    u32 temp_r0_3;
    u32 temp_r0_4;
    u32 temp_r0_5;
    u32 temp_r0_6;
    u32 temp_r0_7;
    u32 temp_r0_8;
    u32 temp_r4;
    u32 var_r9;
    u32 var_r9_2;
    u32 var_r9_3;
    u32 var_r9_4;
    u8 *var_r1_2;
    u8 *var_r1_3;
    u8 *var_r1_4;
    u8 *var_r2;
    u8 temp_r3;
    u8 temp_r3_2;
    u8 temp_r3_3;
    u8 temp_r3_4;
    u8 var_r10;
    void *temp_ip;
    void *temp_ip_2;
    void *temp_ip_3;
    void *temp_ip_4;

    var_r10 = 0;
    sp8 = 0;
    sp4 = 0;
    M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x18) = 0;
    M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x19) = 0;
    native_fn_02008d78(native_data_ov001_022389bc, 0, 0x4B);
    if ((native_fn_020444ec() == 0) || (temp_r4 = native_fn_01ffa824(), ((u32) (u8) temp_r4 < native_fn_01ffa84c()))) {
        var_r9 = 0;
        do {
            temp_r0 = ov001_side_slot_record_021db438(0U, var_r9);
            if (ov001_record_is_active_021db8d0(temp_r0) != 0) {
                if ((M2C_FIELD(native_data_ov001_022388ec, u8 *, 0x1D) == 0) && (M2C_FIELD(native_data_ov001_022388ec, u8 *, 0x1B) == 0)) {
                    temp_r0_2 = native_fn_ov001_0221003c(temp_r0, &sp8, &sp0, 4);
                    if (temp_r0_2 != 0) {
                        var_r1 = 0;
                        if ((s32) temp_r0_2 > 0) {
                            var_r2 = &sp0;
                            do {
                                temp_r3 = *var_r2;
                                var_r2 += 1;
                                temp_r8 = var_r10 * 3;
                                temp_ip = native_data_ov001_022389bc + temp_r8;
                                *(native_data_ov001_022389bc + temp_r8) = temp_r3;
                                M2C_FIELD(temp_ip, s8 *, 1) = 0;
                                M2C_FIELD(temp_ip, s8 *, 2) = (s8) var_r9;
                                var_r10 += 1;
                                var_r1 += 1;
                            } while (var_r1 < (s32) temp_r0_2);
                        }
                    }
                }
            }
            var_r9 = (u32) (u8) (var_r9 + 1);
        } while (var_r9 < 3U);
        var_r9_2 = 0;
        do {
            temp_r0_3 = ov001_side_slot_record_021db438(1U, var_r9_2);
            if (ov001_record_is_active_021db8d0(temp_r0_3) != 0) {
                if ((M2C_FIELD(native_data_ov001_022388ec, u8 *, 0xC) == 0) && (M2C_FIELD(native_data_ov001_022388ec, u8 *, 7) == 0)) {
                    temp_r0_4 = native_fn_ov001_0221003c(temp_r0_3, &sp4, &sp0, 4);
                    if (temp_r0_4 != 0) {
                        var_r2_2 = 0;
                        if ((s32) temp_r0_4 > 0) {
                            var_r1_2 = &sp0;
                            do {
                                temp_r3_2 = *var_r1_2;
                                var_r1_2 += 1;
                                temp_r8_2 = var_r10 * 3;
                                temp_ip_2 = native_data_ov001_022389bc + temp_r8_2;
                                *(native_data_ov001_022389bc + temp_r8_2) = temp_r3_2;
                                M2C_FIELD(temp_ip_2, s8 *, 1) = 1;
                                M2C_FIELD(temp_ip_2, s8 *, 2) = (s8) var_r9_2;
                                var_r10 += 1;
                                var_r2_2 += 1;
                            } while (var_r2_2 < (s32) temp_r0_4);
                        }
                    }
                }
            }
            var_r9_2 = (u32) (u8) (var_r9_2 + 1);
        } while (var_r9_2 < 3U);
    } else {
        var_r9_3 = 0;
        do {
            temp_r0_5 = ov001_side_slot_record_021db438(1U, var_r9_3);
            if (ov001_record_is_active_021db8d0(temp_r0_5) != 0) {
                if ((M2C_FIELD(native_data_ov001_022388ec, u8 *, 0xC) == 0) && (M2C_FIELD(native_data_ov001_022388ec, u8 *, 7) == 0)) {
                    temp_r0_6 = native_fn_ov001_0221003c(temp_r0_5, &sp4, &sp0, 4);
                    if (temp_r0_6 != 0) {
                        var_r2_3 = 0;
                        if ((s32) temp_r0_6 > 0) {
                            var_r1_3 = &sp0;
                            do {
                                temp_r3_3 = *var_r1_3;
                                var_r1_3 += 1;
                                temp_r8_3 = var_r10 * 3;
                                temp_ip_3 = native_data_ov001_022389bc + temp_r8_3;
                                *(native_data_ov001_022389bc + temp_r8_3) = temp_r3_3;
                                M2C_FIELD(temp_ip_3, s8 *, 1) = 1;
                                M2C_FIELD(temp_ip_3, s8 *, 2) = (s8) var_r9_3;
                                var_r10 += 1;
                                var_r2_3 += 1;
                            } while (var_r2_3 < (s32) temp_r0_6);
                        }
                    }
                }
            }
            var_r9_3 = (u32) (u8) (var_r9_3 + 1);
        } while (var_r9_3 < 3U);
        var_r9_4 = 0;
        do {
            temp_r0_7 = ov001_side_slot_record_021db438(0U, var_r9_4);
            if (ov001_record_is_active_021db8d0(temp_r0_7) != 0) {
                if ((M2C_FIELD(native_data_ov001_022388ec, u8 *, 0x1D) == 0) && (M2C_FIELD(native_data_ov001_022388ec, u8 *, 0x1B) == 0)) {
                    temp_r0_8 = native_fn_ov001_0221003c(temp_r0_7, &sp8, &sp0, 4);
                    if (temp_r0_8 != 0) {
                        var_r2_4 = 0;
                        if ((s32) temp_r0_8 > 0) {
                            var_r1_4 = &sp0;
                            do {
                                temp_r3_4 = *var_r1_4;
                                var_r1_4 += 1;
                                temp_r8_4 = var_r10 * 3;
                                temp_ip_4 = native_data_ov001_022389bc + temp_r8_4;
                                *(native_data_ov001_022389bc + temp_r8_4) = temp_r3_4;
                                M2C_FIELD(temp_ip_4, s8 *, 1) = 0;
                                M2C_FIELD(temp_ip_4, s8 *, 2) = (s8) var_r9_4;
                                var_r10 += 1;
                                var_r2_4 += 1;
                            } while (var_r2_4 < (s32) temp_r0_8);
                        }
                    }
                }
            }
            var_r9_4 = (u32) (u8) (var_r9_4 + 1);
        } while (var_r9_4 < 3U);
    }
    if (var_r10 == 0) {
        var_r1_5 = 4;
    } else {
        var_r1_5 = 0x22;
    }
    M2C_FIELD(native_data_ov001_022388ec, s8 *, 8) = var_r1_5;
    M2C_FIELD(native_data_ov001_022388ec, s8 *, 0xF) = 0;
    return 1U;
}
