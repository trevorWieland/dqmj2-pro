#include "context.h"
u32 native_ov000_022092e0(void) {
    u32 temp_r0;
    s16 var_r4;
    s16 temp_r5;
    void *var_r6;
    u16 sp8[64];

    if (native_data_ov000_02238520.field_8 == 0) {
        var_r6 = M2C_FIELD(native_data_ov000_02238514, void **, 4);
    } else {
        var_r6 = M2C_FIELD(native_data_ov000_02238514, void **, 0);
    }
    if (var_r6 == NULL) {
        return 0U;
    }
    native_fn_02008be0(0, sp8, 0x80);
    native_fn_020852b0(var_r6 + 0x3C, (s32) native_data_ov000_0223852b);
    native_fn_02046af4(native_data_021c9698, M2C_FIELD(var_r6, s32 *, 0x68), M2C_FIELD(var_r6, u8 *, 0x5E), 0, sp8, 0xFF);
    var_r4 = native_data_ov000_02238520.field_0;
    temp_r5 = native_data_ov000_02238520.field_2;
    M2C_FIELD(var_r6, s16 *, 0x6C) = (s16) native_fn_020470fc(sp8);
    temp_r0 = native_fn_02087674(native_data_021c9698, var_r6 + 0x3C, sp8);
    if (native_data_ov000_02238520.field_9 == 1) {
        var_r4 -= (s32) temp_r0 >> 1;
    } else if (native_data_ov000_02238520.field_9 == 2) {
        var_r4 -= temp_r0;
    }
    native_fn_02087a48(var_r6, 0, var_r4, temp_r5, (s32) native_data_ov000_02238520.field_a, sp8);
    return 1U;
}
