#include "context.h"
u32 native_ov006_02204e48(void) {
    s32 sp0[64];
    s32 var_r4;
    s32 var_r5;
    s32 var_r6;

    M2C_FIELD(native_data_ov006_0221c1f0, s32 *, 0) = 0;
    M2C_FIELD(native_data_ov006_0221c1f0, u32 *, 8) = 0U;
    native_fn_02008c58(0, (s32 (*)[]) &sp0[0], 0x100);
    var_r6 = 0;
    do {
        if (native_fn_020bb144(var_r6) != 0) {
            (&sp0[0])[M2C_FIELD(native_data_ov006_0221c1f0, s32 *, 0)] = var_r6 + 1;
            M2C_FIELD(native_data_ov006_0221c1f0, s32 *, 0) = (s32) (M2C_FIELD(native_data_ov006_0221c1f0, s32 *, 0) + 1);
        }
        var_r6 += 1;
    } while (var_r6 < 0x40);
    if (M2C_FIELD(native_data_ov006_0221c1f0, s32 *, 0) == 0) {
        return (u32) native_data_ov006_0221c1f0;
    }
    M2C_FIELD(native_data_ov006_0221c1f0, u32 *, 8) = native_fn_0202a44c(1, M2C_FIELD(native_data_ov006_0221c1f0, s32 *, 0) * 0xC, 4);
    var_r5 = 0;
    if ((s32) M2C_FIELD(native_data_ov006_0221c1f0, s32 *, 0) <= 0) {
        return (u32) M2C_FIELD(native_data_ov006_0221c1f0, s32 *, 0);
    }
    var_r4 = 0;
    do {
        M2C_FIELD((M2C_FIELD(native_data_ov006_0221c1f0, u32 *, 8) + var_r4), s32 *, 8) = (s32) (&sp0[0])[var_r5];
        var_r5 += 1;
        var_r4 += 0xC;
    } while (var_r5 < (s32) M2C_FIELD(native_data_ov006_0221c1f0, s32 *, 0));
    return (u32) M2C_FIELD(native_data_ov006_0221c1f0, s32 *, 0);
}
