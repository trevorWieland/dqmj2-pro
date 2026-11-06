#include "context.h"
u32 native_ov000_021f6008(void) {
    s32 var_r1;
    u8 *var_r2;
    u8 spC[32];

    native_fn_02061c1c(6U, 7, 1, 0x12, 2, 0, 0);
    switch (native_data_ov000_02236ee4.field_20) {
    case 0:
        native_fn_01ffb50c(6, 0x10, 0xD, 3, 1);
        break;
    case 1:
        native_fn_01ffb50c(6, 0x10, 0xD, 0x26, 1);
        break;
    case 2:
        native_fn_01ffb50c(6, 0x10, 0xD, 0x27, 1);
        break;
    }
    var_r2 = spC;
    var_r1 = 8;
    do {
        M2C_FIELD(var_r2, s8 *, 0) = 0;
        M2C_FIELD(var_r2, s8 *, 1) = 0;
        M2C_FIELD(var_r2, s8 *, 2) = 0;
        M2C_FIELD(var_r2, s8 *, 3) = 0;
        var_r2 += 4;
        var_r1 -= 1;
    } while (var_r1 != 0);
    native_fn_0201d444(spC, native_data_ov000_0222f2f0);
    native_data_ov000_02236ee4.field_1c = native_fn_0203cc2c((u32) spC, 2U);
    M2C_FIELD((void *)0x04000008, u16 *, 0) = (u16) ((M2C_FIELD((void *)0x04000008, u16 *, 0) & ~3) | 2);
    M2C_FIELD((void *)0x04000008, u16 *, 4) = (u16) ((M2C_FIELD((void *)0x04000008, u16 *, 4) & ~3) | 1);
    M2C_FIELD((void *)0x04000008, u16 *, 6) = (u16) ((M2C_FIELD((void *)0x04000008, u16 *, 6) & ~3) | 3);
    M2C_FIELD((void *)0x04000008, u16 *, 4) = (u16) ((M2C_FIELD((void *)0x04000008, u16 *, 4) & 0x43) | 0x218);
    native_data_ov000_02236ee4.field_2 = 2;
    return 2U;
}
