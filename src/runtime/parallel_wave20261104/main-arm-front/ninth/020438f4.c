#include "context.h"
u32 native_main_020438f4(void) {
    u32 temp_r0;
    u32 var_r0;
    u32 var_r0_3;
    u8 var_r0_2;
    u32 temp_r4;
    u32 temp_r4_2;
    u32 temp_r4_3;
    u32 temp_r4_4;

    temp_r0 = native_fn_0206533c();
    switch (temp_r0) {
    case 0:
        temp_r4 = native_fn_ov001_0220fed4(0, 1);
        if ((s32) temp_r4 > (s32) native_fn_0203d294(0x20)) {
            return 1U;
        }
        temp_r4_2 = native_fn_ov001_0220fed4(1, 1);
        if ((s32) temp_r4_2 > (s32) native_fn_0203d294(0x20)) {
            var_r0 = 2;
        } else {
            var_r0 = 0;
        }
        return var_r0;
    case 1:
        temp_r4_3 = native_fn_ov001_0220fed4(0, 0xC);
        if ((s32) temp_r4_3 > (s32) native_fn_0203d294(0x20)) {
            var_r0_2 = 1;
        } else {
            var_r0_2 = 0;
        }
        return (u32) var_r0_2;
    case 2:
        temp_r4_4 = native_fn_ov001_0220fed4(1, 0x1B);
        if ((s32) temp_r4_4 > (s32) native_fn_0203d294(0x20)) {
            var_r0_3 = 2;
        } else {
            var_r0_3 = 0;
        }
        return var_r0_3;
    case 3:
        return 0U;
    default:
        return 0U;
    }
}
