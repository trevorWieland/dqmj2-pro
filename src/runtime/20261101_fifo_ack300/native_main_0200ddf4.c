#include "state.h"
u32 native_main_0200ddf4(void) {
    s32 var_r0;
    u32 temp_r4;

    temp_r4 = native_fn_02007ff4();
    if ((s32) native_fn_0200a440(6, 0x03000000, 0) >= 0) {
        var_r0 = 1;
    } else {
        var_r0 = 0;
    }
    if (var_r0 == 0) {
        native_fn_02008008(temp_r4);
        M2C_FIELD(native_data_020e53d0, u16 *, 0x38) = (u16) (M2C_FIELD(native_data_020e53d0, u16 *, 0x38) | 1);
        if (M2C_FIELD(native_data_020e53d0, u32 (**)(u32, u32, u32), 4) == NULL) {
            return (u32) native_data_020e53d0;
        }
        return M2C_FIELD(native_data_020e53d0, u32 (**)(u32, u32, u32), 4)(0, 4, 0);
    }
    M2C_FIELD(native_data_020e53d0, u16 *, 0x3A) = (u16) (M2C_FIELD(native_data_020e53d0, u16 *, 0x3A) | 1);
    M2C_FIELD(native_data_020e53d0, u16 *, 0x38) = (u16) (M2C_FIELD(native_data_020e53d0, u16 *, 0x38) & ~1);
    return native_fn_02008008(temp_r4);
}
