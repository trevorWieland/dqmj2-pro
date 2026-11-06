#include "context.h"
u32 native_ov000_0221da64(void) {
    u32 temp_r0;
    void *temp_r0_2;
    s32 var_r8;
    s32 var_r9;

    var_r8 = 0;
    do {
        temp_r0_2 = native_data_ov000_02246348[var_r8];
        if (temp_r0_2 != NULL) {
            native_fn_0204861c(1, M2C_FIELD(temp_r0_2, u8 *, 0x81));
            native_fn_0202a498(2, native_data_ov000_02246348[var_r8]);
            native_data_ov000_02246348[var_r8] = 0;
        }
        var_r8 += 1;
    } while (var_r8 < 0x16);
    if (M2C_FIELD(native_data_ov000_02246318, void **, 4) != NULL) {
        native_fn_020485b4(M2C_FIELD(native_data_ov000_02246318, void **, 4));
    }
    native_fn_020484dc(1U, (u32) M2C_FIELD(native_data_ov000_02246318, u8 *, 1));
    var_r9 = 0;
    do {
        native_fn_0205f920(native_data_ov000_0224632c[var_r9], 1, 2);
        temp_r0 = native_fn_0202a498(2, native_data_ov000_0224632c[var_r9]);
        native_data_ov000_0224632c[var_r9] = 0;
        var_r9 += 1;
    } while (var_r9 < 5);
    return temp_r0;
}
