#include "context.h"
u32 native_ov001_0221ebe0(void *arg0) {
    s32 var_r1;
    void *temp_r2;
    s32 temp_r6;
    s32 var_r7;
    void *var_r8;

    temp_r6 = ((Field491_s32_0004 *)(arg0))->value;
    if (native_fn_ov001_022187dc(temp_r6, 9, 1, 0) != 0) {
        var_r7 = 0;
loop_2:
        var_r8 = temp_r6 + (var_r7 * 0x440);
        if (native_fn_ov001_02218dbc(var_r8) != 0) {
            if ((((Field491_s8_0237 *)(var_r8))->value == 0) && (((Field491_s8_023c *)(var_r8))->value == 0)) {
                if (!(native_fn_ov001_021e29e8() & 1)) {
                    var_r1 = 0;
                    if ((s32) ((Field491_u8_0323 *)(var_r8))->value > 0) {
                        temp_r2 = var_r8;
loop_10:
                        if (((Field491_u8_035e *)(var_r8))->value == 0x3A) {
                            var_r7 = 3;
                        } else {
                            var_r1 += 1;
                            var_r8 += 1;
                            if (var_r1 < (s32) ((Field491_u8_0323 *)(temp_r2))->value) {
                                goto loop_10;
                            }
                        }
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
