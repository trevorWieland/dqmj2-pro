#include "context.h"
s32 native_ov001_022122ac(void *arg0, s32 arg1, u32 arg2) {
    f64 temp_ret;
    f64 temp_ret_2;
    s32 temp_r3;
    s32 temp_r5;
    s32 var_r4;
    s32 var_r8;
    u32 temp_r4;
    u8 var_r5;
    u32 var_r6;
    u32 var_r9;

    var_r9 = arg2;
    temp_r3 = (s32) ((u32) arg1 - 1U);
    var_r5 = 0;
    var_r6 = var_r9;
    var_r4 = 0;
    if (temp_r3 > 0) {
loop_2:
        var_r5 += 1;
        var_r6 = (s32) var_r6 / 10;
        if ((s32) var_r6 > 0) {
            var_r4 += 1;
            if (var_r4 < temp_r3) {
                goto loop_2;
            }
        }
    }
    var_r8 = (s8) (var_r5 - 1);
    if ((s32) var_r8 >= 0) {
        do {
            temp_ret = native_fn_020244c4((s32) var_r8);
            temp_ret_2 = native_fn_0202298c(10.0, temp_ret);
            temp_r5 = native_fn_02024394(temp_ret_2);
            temp_r4 = native_fn_0205f98c(M2C_FIELD(arg0, s32 *, 0x1C), (s32) (u8) (var_r8 + 1));
            native_fn_ov001_021f1ba0(temp_r4, (u8) native_fn_02026144((s32) var_r9, temp_r5));
            M2C_FIELD(temp_r4, s32 *, 0x7C) = (s32) (M2C_FIELD(temp_r4, s32 *, 0x7C) | 2);
            var_r9 = ((s32) ((s32) var_r9) % (s32) (temp_r5));
            var_r8 -= 1;
        } while ((s32) var_r8 >= 0);
    }
    return 0;
}
