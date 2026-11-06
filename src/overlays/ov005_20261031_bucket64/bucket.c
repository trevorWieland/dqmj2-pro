#include "context.h"
u32 native_ov005_021e6b30(void) {
    s8 *temp_r0;
    u32 temp_r0_2;
    u8 var_r1;
    u32 temp_r4;
    s8 var_r5;
    u8 *var_r6;
    u8 var_r7;

    temp_r4 = native_fn_0203d294(0xA);
    var_r7 = 0;
    var_r6 = native_data_ov005_021e7768;
    var_r5 = 0x17;
    if (native_fn_02063b18(0) >= 0xBU) {
        var_r6 = native_data_ov005_021e776c;
    }
    if (native_fn_02063b18(0) >= 0xDU) {
        var_r6 = native_data_ov005_021e7770;
    }
    if (native_fn_02063b18(0x14) >= 0x1DU) {
        var_r6 = native_data_ov005_021e7774;
    }
    var_r1 = 0;
loop_7:
    if ((s32) temp_r4 < (s32) (s8) *var_r6) {
        var_r7 = var_r1;
    } else {
        var_r1 += 1;
        var_r6 += 1;
        if ((u32) var_r1 < 4U) {
            goto loop_7;
        }
    }
    temp_r0_2 = native_fn_0203d294(0xA);
    switch (var_r7) {
    case 1:
        if ((s32) temp_r0_2 < 5) {
            var_r5 = 0x18;
        }
        break;
    case 2:
        var_r5 = 0x18;
        if ((s32) temp_r0_2 < 5) {
            var_r5 = 0x19;
        }
        break;
    case 3:
        var_r5 = 0x19;
        if ((s32) temp_r0_2 < 3) {
            var_r5 = 0x1A;
        }
        break;
    }
    native_fn_ov005_021e63e8((u8) (var_r7 + 1));
    temp_r0 = (s8 *) native_fn_020642ec();
    *temp_r0 = var_r5;
    return (u32) temp_r0;
}
