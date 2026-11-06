#include "context.h"
u32 native_ov006_021ea660(void) {
    u32 temp_r0;
    u32 layoutOffset;
    s32 temp_r1;
    u32 var_r5;
    s32 var_r6;
    s32 temp_r7_2;
    u32 temp_r7;
    s32 var_r8;
    s32 var_r9;
    s32 var_r10;
    u32 sp4;
    s32 sp0;

    temp_r0 = native_fn_02067b08();
    var_r6 = 0;
    sp4 = temp_r0;
    sp0 = 0;
    if ((s32) temp_r0 > 0) {
        var_r9 = 0;
        var_r10 = 8;
        do {
            temp_r7 = native_fn_02067af4(sp0);
            layoutOffset = native_fn_ov006_021ea2ac((void *)temp_r7);
            layoutOffset += var_r9;
            native_fn_ov006_021e7f08(7, 9, layoutOffset + 0xA);
            temp_r7_2 = native_fn_02044cdc(M2C_FIELD(temp_r7, s16 *, 0x18)) + 1;
            var_r8 = 0;
            if ((temp_r7_2 > 0) && (temp_r7_2 > 0)) {
                do {
                    native_fn_ov006_021e7f08(0, 3, var_r10);
                    native_fn_ov006_021e7f08(var_r6 + 1, 3, var_r10);
                    var_r8 += 1;
                    var_r9 += 5;
                    var_r10 += 5;
                    var_r6 += 1;
                } while (var_r8 < temp_r7_2);
            }
            temp_r1 = sp0 + 1;
            sp0 = temp_r1;
        } while (temp_r1 < (s32) sp4);
    }
    var_r5 = 0;
    do {
        native_fn_ov006_021e7608(M2C_FIELD(native_data_ov006_0220860c, u32 *, var_r5 * 8));
        var_r5 += 1;
    } while (var_r5 < 0xBU);
    return 1U;
}
