#include "context.h"
u32 native_ov005_021d9ae0(void *arg0, u32 arg1, void *arg2, void *arg3) {
    void *var_r0;
    s32 temp_r1;
    void *temp_r2;
    u32 temp_r5;
    u32 temp_r6;
    u16 temp_r7;

    var_r0 = M2C_FIELD(M2C_FIELD(arg0, void **, 0x20), void **, 0xC);
    temp_r2 = M2C_FIELD(var_r0, void **, 0x24);
    M2C_FIELD(arg2, s16 *, 2) = arg1;
    if (arg1 != 0xFFFF) {
        var_r0 = (void *)0xFFFE;
        if (arg1 != 0xFFFE) {
            var_r0 = (void *)0xFFFD;
            if (arg1 != 0xFFFD) {
                temp_r7 = M2C_FIELD(temp_r2, u16 *, 0x584);
                temp_r6 = M2C_FIELD(arg3, u32 *, 8);
                temp_r5 = arg1 * temp_r7;
                if (arg1 == (M2C_FIELD(temp_r2, u32 *, 0x424) - 1U)) {
                    temp_r1 = ((s32) (M2C_FIELD(temp_r2, s32 *, 0x420)) % (s32) (temp_r7));
                    if (temp_r1 != 0) {
                        return native_fn_02008e0c(temp_r6 + temp_r5, arg2 + 4, temp_r1);
                    }
                    return native_fn_02008e0c(temp_r6 + temp_r5, arg2 + 4, (s32) temp_r7);
                }
                return native_fn_02008e0c(temp_r6 + temp_r5, arg2 + 4, (s32) temp_r7);
            }
        }
    }
    return (u32) var_r0;
}
