#include "allocation_header_20261030.h"
u32 native_main_020780b0(s32 arg0) {
    u32 var_r0;
    void **temp_r4;
    void *temp_r5;
    u32 var_r6;
    s16 coordinates[2];

    temp_r5 = M2C_FIELD(native_data_021c6234, void **, 0x1EC);
    temp_r4 = native_fn_02049ad0(1);
    var_r6 = 0;
    native_fn_02062aa0();
    native_fn_02049ffc(M2C_FIELD(*temp_r4, s32 *, 4));
    native_fn_02049f4c(temp_r4);
    coordinates[1] = 0;
    coordinates[0] = 0x18;
    native_fn_020602ec(*temp_r4, M2C_FIELD(temp_r5, s16 *, 0x18), temp_r5, coordinates[0], 0, 1);
    coordinates[0] = 0;
    native_fn_0204a724(1, coordinates, 0x38, 5, 2, 0x13, 1, 0);
    coordinates[0] = 0xB8;
    native_fn_0204a808(1, coordinates, 1, native_data_020de410, 0);
    coordinates[0] = 0xC0;
    native_fn_0204a154(1, coordinates, 1, arg0, 3, 0);
    if (native_fn_02063fa0(M2C_FIELD(temp_r5, s32 *, 0x14)) != 0) {
        var_r0 = native_fn_ov000_0221742c(7);
        var_r6 = var_r0;
    } else {
        var_r0 = native_fn_02063fac(M2C_FIELD(temp_r5, s32 *, 0x14));
        if (var_r0 != 0) {
            var_r0 = native_fn_ov000_0221742c(8);
            var_r6 = var_r0;
        }
    }
    if (var_r6 == 0) {
        return var_r0;
    }
    return native_fn_02065818(var_r6, 3, 3);
}
