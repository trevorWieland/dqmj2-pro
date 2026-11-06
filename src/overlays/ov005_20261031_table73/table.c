#include "context.h"
u32 native_ov005_021e6c18(void) {
    u16 temp_r0;
    u16 temp_r1;
    s32 var_r2;
    u16 *var_r3;
    s32 var_r4;
    u16 sp0[72];
    u8 *var_ip;

    var_ip = native_data_ov005_021e6f2c;
    var_r3 = sp0;
    var_r4 = 0;
    var_r2 = 0x24;
    do {
        temp_r1 = M2C_FIELD(var_ip, u16 *, 0);
        temp_r0 = M2C_FIELD(var_ip, u16 *, 2);
        var_ip += 4;
        M2C_FIELD(var_r3, u16 *, 0) = temp_r1;
        M2C_FIELD(var_r3, u16 *, 2) = temp_r0;
        var_r3 += 2;
        var_r2 -= 1;
    } while (var_r2 != 0);
    if (native_fn_02063b18(0) >= 0xBU) {
        var_r4 = 3;
    }
    if (native_fn_02063b18(0) >= 0xDU) {
        var_r4 = 6;
    }
    if (native_fn_02063b18(0x14) >= 0x1DU) {
        var_r4 = 9;
    }
    if ((u32) native_data_ov005_021ed438.field_20 >= 0x69780U) {
        var_r4 += 1;
    }
    if ((u32) native_data_ov005_021ed438.field_20 >= 0x13C680U) {
        var_r4 += 1;
    }
    return native_fn_02064304((var_r4 * 0xC) + (s32) sp0);
}
