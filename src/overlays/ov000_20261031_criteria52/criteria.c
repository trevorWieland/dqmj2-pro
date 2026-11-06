#include "context.h"
u32 native_ov000_022189e4(s32 arg0, s32 arg1) {
    u32 temp_r0;
    s32 temp_r1;
    u32 var_r5;
    u32 temp_r6;
    u32 temp_r7;
    u16 var_r8;
    s32 var_r11;

    var_r5 = 0;
    temp_r6 = (u32) (*(u16 *) native_fn_ov000_021df3bc(arg1) << 0x10) >> 0x1B;
    if ((temp_r6 == 0) || (temp_r6 == 0x10)) {
        var_r11 = 1;
    } else {
        var_r11 = 0;
    }
    temp_r0 = native_fn_0205bf3c();
    if ((temp_r0 != 1) && (temp_r0 != 2) && (temp_r0 != 5)) {
        return 0U;
    }
    var_r8 = 0;
    do {
        temp_r7 = native_fn_ov000_02215048(var_r8);
        if (native_fn_0205fb90(var_r8) == 0) {
            if (var_r11 == 0) {
                if (M2C_FIELD(temp_r7, u8 *, 0) == (s8) native_data_ov000_0222fa10[temp_r6]) {
                    goto block_14;
                }
            } else if (M2C_FIELD(temp_r7, u8 *, 0) == 1) {
block_14:
                if (M2C_FIELD(temp_r7, s8 *, 2) == 1) {
                    temp_r1 = M2C_FIELD(temp_r7, s32 *, 4);
                    if ((temp_r1 == arg0) && (M2C_FIELD(temp_r7, s32 *, 8) == arg1)) {
                        goto block_22;
                    }
                    if ((M2C_FIELD(temp_r7, s32 *, 8) == arg0) && (temp_r1 == arg1)) {
block_22:
                        native_fn_0205fbb4(var_r8, 1);
                        var_r5 = 1;
                    }
                }
                if ((M2C_FIELD(temp_r7, s8 *, 2) == 0) && (arg1 == M2C_FIELD(temp_r7, s32 *, 4))) {
                    native_fn_0205fbb4(var_r8, 1);
                    var_r5 = 1;
                }
                if ((M2C_FIELD(temp_r7, s8 *, 2) == 3) && ((M2C_FIELD(temp_r7, s32 *, 4) == -1) || (native_fn_02063b40(M2C_FIELD(temp_r7, s32 *, 4)) != 0)) && ((M2C_FIELD(temp_r7, s32 *, 8) == -1) || (native_fn_02063b40(M2C_FIELD(temp_r7, s32 *, 8)) != 0))) {
                    native_fn_0205fbb4(var_r8, 1);
                    var_r5 = 1;
                }
            }
        }
        var_r8 += 1;
    } while ((u32) var_r8 < 0x300U);
    return var_r5;
}
