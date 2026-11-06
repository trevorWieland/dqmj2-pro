#include "context.h"
u32 native_ov001_0221d6ec(void *arg0) {
    s32 var_r1;
    u8 *temp_r2;
    s32 temp_r6;
    s32 var_r7;
    u8 *var_r8;

    temp_r6 = ((Field491_s32_0004 *)(arg0))->value;
    if (native_fn_ov001_022187dc(temp_r6, 6, 1, 0) != 0) {
        var_r7 = 0;
loop_2:
        var_r8 = temp_r6 + (var_r7 * 0x440);
        if ((native_fn_ov001_021db8d0(var_r8) != 0) && (native_fn_ov001_02218dbc(var_r8) != 0) && (((Field491_s8_023c *)(var_r8))->value == 0) && !(native_fn_ov001_021e29e8() & 1)) {
            var_r1 = 0;
            if ((s32) ((Field491_u8_0323 *)(var_r8))->value > 0) {
                temp_r2 = var_r8;
loop_8:
                if (((Field491_u8_035e *)(var_r8))->value == 0x39) {
                    var_r7 = 3;
                } else {
                    var_r1 += 1;
                    var_r8 += 1;
                    if (var_r1 < (s32) ((Field491_u8_0323 *)(temp_r2))->value) {
                        goto loop_8;
                    }
                }
            }
        }
        if (var_r7 == 2) {
            return 1U;
        }
        var_r7 += 1;
        if (var_r7 >= 3) {
            
            goto zero;
        }
        goto loop_2;
    }
    goto zero;
zero:
    return 0U;
}
