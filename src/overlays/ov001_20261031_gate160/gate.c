#include "context.h"
u32 native_ov001_021f73b8(s32 arg0) {
    u32 var_r0;
    u32 var_r0_2;
    u32 var_r0_3;
    u8 *temp_r0;
    u32 var_r5;
    s32 var_r6;

    if (native_fn_020444a8() != 0) {
        if (arg0 == 0) {
            if (native_data_ov001_0223989c.field_18 == 0) {
                var_r0_3 = 1;
            } else {
                var_r0_3 = 0;
            }
            return var_r0_3;
        }
        if (native_data_ov001_0223989c.field_19 == 0) {
            var_r0_2 = 1;
        } else {
            var_r0_2 = 0;
        }
        return var_r0_2;
    }
    if (native_fn_020655d8() != 0) {
        return 0U;
    }
    if (arg0 == 0) {
        var_r6 = 1;
    } else {
        var_r6 = 0;
    }
    var_r5 = 0;
loop_16:
    temp_r0 = native_fn_ov001_021db438(var_r6, var_r5);
    if ((native_fn_ov001_021db8d0(temp_r0) != 0) && (M2C_FIELD(temp_r0, u8 *, 0x322) == 2)) {
        return 0U;
    }
    var_r5 += 1;
    if ((s32) var_r5 >= 3) {
        if (arg0 == 0) {
            if (native_data_ov001_0223989c.field_18 == 0) {
                var_r0 = 1;
            } else {
                var_r0 = 0;
            }
            return var_r0;
        }
        if (native_data_ov001_0223989c.field_19 == 0) {
            return 1U;
        }
        return 0U;
    }
    goto loop_16;
}
