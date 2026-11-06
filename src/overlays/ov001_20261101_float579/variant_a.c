#include "variant_a.h"
void native_ov001_0221239c(void *arg0) {
    f64 temp_ret;
    f64 temp_ret_2;
    s32 temp_r6;
    u8 var_r4;
    s32 var_r5;
    u8 var_r7;
    s8 var_r8;
    u32 temp_r0;
    u32 temp_r0_2;
    u32 var_r11;
    u32 var_r9;

    var_r4 = 0;
    var_r5 = var_r4;
    var_r7 = (u8) M2C_FIELD(arg0, s16 *, 0x14);
    temp_r0 = native_fn_0205f98c(M2C_FIELD(arg0, s32 *, 0x1C), 0U);
    native_fn_ov001_021f1ba0(temp_r0, 0x1E);
    native_fn_02048a60(temp_r0, var_r7, M2C_FIELD(arg0, s16 *, 0x16));
    native_fn_02048a94(temp_r0, 8);
    var_r7 += 0x28;
    M2C_FIELD(arg0, s16 *, 0x26) = 0xA;
    var_r8 = var_r4;
    M2C_FIELD(arg0, s32 *, 0x10) = var_r8;
    var_r9 = M2C_FIELD(arg0, u32 *, 0x2C);
    var_r11 = var_r9;
loop_1:
    var_r4 += 1;
    var_r5 += native_data_ov001_0222e100[((s32) var_r11 % 10)];
    var_r11 = (s32) var_r11 / 10;
    if ((s32) var_r11 > 0) {
        var_r8 += 1;
        if ((s32) var_r8 < 7) {
            goto loop_1;
        }
    }
    var_r7 += 0x38 - var_r5;
    var_r8 = var_r4 - 1;
    if ((s32) var_r8 >= 0) {
        do {
            temp_ret = native_fn_020244c4((s32) var_r8);
            temp_ret_2 = native_fn_0202298c(10.0, temp_ret);
            temp_r6 = native_fn_02024394(temp_ret_2);
            temp_r0_2 = native_fn_0205f98c(M2C_FIELD(arg0, s32 *, 0x1C), (u8) (var_r8 + 1));
            native_fn_02048a60(temp_r0_2, var_r7, M2C_FIELD(arg0, s16 *, 0x16));
            native_fn_02048a94(temp_r0_2, 7);
            M2C_FIELD(temp_r0_2, s32 *, 0x7C) = (s32) (M2C_FIELD(temp_r0_2, s32 *, 0x7C) & ~2);
            var_r7 += native_data_ov001_0222e100[(u8) native_fn_02026144((s32) var_r9, temp_r6)];
            var_r9 = ((s32) ((s32) var_r9) % (s32) (temp_r6));
            var_r8 -= 1;
        } while ((s32) var_r8 >= 0);
    }
    native_fn_ov001_022122ac(arg0, 7, M2C_FIELD(arg0, s32 *, 0x30));
    M2C_FIELD(arg0, s8 *, 0x23) = 1;
}
