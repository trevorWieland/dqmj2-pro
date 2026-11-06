#include "context.h"
u32 native_ov001_0222bf54(s32 arg0, s32 arg1) {
    u32 var_r0;
    s16 temp_r4;
    s32 var_r5;
    s32 temp_r0;
    s8 var_r7;
    u8 *var_r8;
    s32 values[3];

    var_r7 = -1;
    temp_r4 = M2C_FIELD((void *) native_fn_0207afec(arg0), s16 *, 0xC);
    temp_r0 = (s32) native_fn_0205d790(temp_r4);
    if (temp_r0 >= 0) {
        var_r8 = native_fn_ov001_021db438(arg1, 0U);
        var_r5 = 0;
        do {
            if (native_fn_ov001_021db8d0(var_r8) != 0) {
                var_r7 = (s8) native_fn_ov001_021eec7c(temp_r4, var_r8, temp_r0);
            }
            var_r5 += 1;
            var_r8 += 0x440;
        } while (var_r5 < 3);
    } else {
        if (arg1 == 0) {
            var_r0 = 3;
        } else {
            var_r0 = 0xB;
        }
        native_fn_ov001_021d8b4c(var_r0, values);
        var_r7 = (s8) native_fn_ov001_021eedbc(temp_r4, values[0], values[1], (s32)((u32)values[2] << 3) / 10, arg1);
    }
    return (u32) var_r7;
}
