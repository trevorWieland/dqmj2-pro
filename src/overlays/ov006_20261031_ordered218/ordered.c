#include "context.h"
u32 native_ov006_021fabe4(void) {
    s32 var_r4;
    s32 var_r4_2;
    u32 var_r5;
    u32 var_r6;

    var_r5 = native_fn_02002480(M2C_FIELD(native_data_ov006_0221c0ec, u16 *, 4), 0x1D);
    native_fn_ov006_0220383c(M2C_FIELD(M2C_FIELD(native_data_ov006_0221c0ec, void **, 8), s32 *, 0x14), 0);
    var_r4 = 0;
    var_r6 = var_r5;
    do {
        native_fn_ov006_021fac5c(var_r6, var_r4);
        var_r4 += 1;
        var_r6 += 1;
    } while (var_r4 < 5);
    native_fn_ov006_021fe510(M2C_FIELD(M2C_FIELD(native_data_ov006_0221c0ec, void **, 8), s32 *, 8) + (native_data_ov006_0220b73e[var_r5] * 2), 0, 0x1E, 0x13);
    var_r4_2 = 0;
    do {
        native_fn_ov006_021fad68(var_r5, var_r4_2);
        var_r4_2 += 1;
        var_r5 += 1;
    } while (var_r4_2 < 5);
    native_fn_ov006_021fe4fc();
    native_fn_ov006_022038ac(M2C_FIELD(M2C_FIELD(native_data_ov006_0221c0ec, void **, 8), s32 *, 0x14));
    return native_fn_ov006_021fb080();
}
