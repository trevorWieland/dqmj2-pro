#include "context.h"
u32 native_ov001_0221b33c(void *arg0) {
    u8 *temp_r5;
    s32 var_r6;
    s32 var_r7;
    u8 *var_r8;
    u8 *var_r9;

    var_r8 = M2C_FIELD(arg0, u8 **, 4);
    temp_r5 = M2C_FIELD(arg0, u8 **, 8);
    if (M2C_FIELD(arg0, s32 *, 0x14) != 0) {
        var_r6 = 0;
loop_2:
        if ((native_fn_ov001_021db8d0(var_r8) != 0) && (native_fn_ov001_021e2b1c(M2C_FIELD(var_r8, u8 *, 0x31E), M2C_FIELD(var_r8, u8 *, 0x31F)) == 0) && (*(u16 *) native_fn_ov001_021e81d0(M2C_FIELD(var_r8, u8 *, 0x31E), M2C_FIELD(var_r8, u8 *, 0x31F)) == 0x77)) {
            var_r7 = 0;
            var_r9 = temp_r5;
loop_6:
            if ((native_fn_ov001_021db8d0(var_r9) != 0) && ((u32) M2C_FIELD(M2C_FIELD(var_r9, void **, 0x1E8), u8 *, 0x97) <= 3U)) {
                return 1U;
            }
            var_r7 += 1;
            var_r9 += 0x440;
            if (var_r7 >= 3) {
                goto block_10;
            }
            goto loop_6;
        }
block_10:
        var_r6 += 1;
        var_r8 += 0x440;
        if (var_r6 >= 3) {
            goto finished;
        }
        goto loop_2;
    }
finished:
    return 0U;
}
