#include "context.h"
void native_ov001_021dfd74(void) {
    s8 temp_r0;
    void *temp_r0_2;
    void *temp_r0_3;
    void *temp_r0_4;
    u8 temp_r2;
    u8 temp_r2_2;
    u8 temp_r2_3;
    s32 var_r4;
    u16 temp_r5;
    s8 var_r6;
    s8 var_r7;
    s8 sp1;
    s8 sp0;

    if (native_data_ov001_022388ec.field_b == 0) {
        temp_r0 = native_data_ov001_022388ec.field_12;
        var_r4 = 0;
        if ((s32) temp_r0 > 0) {
            do {
                native_fn_ov001_021e8178(var_r4, &sp1, &sp0);
                temp_r5 = *(u16 *) native_fn_ov001_021e81d0(sp1, sp0);
                if (native_fn_0207b02c(temp_r5, 0x80000800) != 0) {
                    if (((u32) (M2C_FIELD((void *) native_fn_0207afec(temp_r5), u16 *, 8) << 0x10) >> 0x1C) == 0) {
                        temp_r0_2 = (void *) native_fn_ov001_021db438(sp1, sp0);
                        temp_r2 = M2C_FIELD(temp_r0_2, u8 *, 0x43C);
                        M2C_FIELD(temp_r0_2, u8 *, 0x43C) = (u8) (temp_r2 + 1);
                        M2C_FIELD((temp_r0_2 + temp_r2), s8 *, 0x432) = (s8) temp_r5;
                    } else {
                        var_r7 = 0;
                        do {
                            temp_r0_3 = (void *) native_fn_ov001_021db438(sp1, var_r7);
                            temp_r2_2 = M2C_FIELD(temp_r0_3, u8 *, 0x43C);
                            var_r7 += 1;
                            M2C_FIELD(temp_r0_3, s8 *, 0x43C) = (s8) (temp_r2_2 + 1);
                            M2C_FIELD((temp_r0_3 + temp_r2_2), u8 *, 0x432) = (u8) temp_r5;
                        } while ((s32) var_r7 < 3);
                        var_r6 = 0;
                        do {
                            temp_r0_4 = (void *) native_fn_ov001_021db438(sp1 + 2, var_r6);
                            temp_r2_3 = M2C_FIELD(temp_r0_4, u8 *, 0x43C);
                            var_r6 += 1;
                            M2C_FIELD(temp_r0_4, s8 *, 0x43C) = (s8) (temp_r2_3 + 1);
                            M2C_FIELD((temp_r0_4 + temp_r2_3), u8 *, 0x432) = (u8) temp_r5;
                        } while ((s32) var_r6 < 3);
                    }
                }
                var_r4 += 1;
            } while (var_r4 < (s32) native_data_ov001_022388ec.field_12);
        }
        if ((s32) temp_r0 < (s32) native_data_ov001_022388ec.field_1e) {
            do {
                native_fn_ov001_021e8178((s32) temp_r0, &sp1, &sp0);
                native_fn_ov001_021db0d8(native_fn_ov001_021db438(sp1, sp0), 1);
                native_data_ov001_022388ec.field_12 = (s8) (native_data_ov001_022388ec.field_12 + 1);
            } while ((s32) native_data_ov001_022388ec.field_12 < (s32) native_data_ov001_022388ec.field_1e);
        }
        native_fn_ov001_021db2ec();
    }
    native_data_ov001_022388ec.field_8 = 0x1A;
}
