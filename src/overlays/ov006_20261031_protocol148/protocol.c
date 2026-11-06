#include "context.h"
u32 native_ov006_0220192c(void *arg0) {
    u32 var_r0;
    u16 temp_r1;
    u16 temp_r2;
    u16 temp_r4;
    u16 header_status;

    header_status = M2C_FIELD(arg0, u16 *, 2);
    if (header_status != 0) {
        native_fn_ov006_022012c0(header_status);
        return native_fn_ov006_02201270(9);
    }
    if (M2C_FIELD(native_data_ov006_0221c164, u32 (**)(u32, u8 *, u16, u16), 0) != NULL) {
        M2C_FIELD(native_data_ov006_0221c164, u32 (**)(u32, u8 *, u16, u16), 0)(0x08000000, native_data_ov006_0220e7b8, M2C_FIELD(arg0, u16 *, 8), M2C_FIELD(arg0, u16 *, 0xA));
    }
    temp_r1 = M2C_FIELD(arg0, u16 *, 8);
    temp_r4 = M2C_FIELD(arg0, u16 *, 0xA);
    temp_r2 = M2C_FIELD(M2C_FIELD(native_data_ov006_0221c164, void **, 4), u16 *, 0x5E);
    if ((u32) temp_r2 > (u32) temp_r4) {
        M2C_FIELD(M2C_FIELD(native_data_ov006_0221c164, void **, 4), u16 *, 0x5E) = temp_r4;
        M2C_FIELD(M2C_FIELD(native_data_ov006_0221c164, void **, 4), u16 *, 0x60) = (u16) (1U << (temp_r1 - 1));
    } else if (temp_r2 == temp_r4) {
        M2C_FIELD(M2C_FIELD(native_data_ov006_0221c164, void **, 4), u16 *, 0x60) = (u16) (M2C_FIELD(M2C_FIELD(native_data_ov006_0221c164, void **, 4), u16 *, 0x60) | (1U << (temp_r1 - 1)));
    }
    var_r0 = native_fn_ov006_022018bc((u16) (temp_r1 + 1));
    if (var_r0 == 0x18) {
        return native_fn_ov006_02201270(7);
    }
    if (var_r0 != 2) {
        var_r0 = native_fn_ov006_02201270(9);
    }
    return var_r0;
}
