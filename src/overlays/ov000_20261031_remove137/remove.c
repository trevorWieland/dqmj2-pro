#include "context.h"
u32 native_ov000_02225bf0(u32 arg0) {
    s32 var_r4;
    s32 var_r4_2;
    s8 temp_r4;
    s32 temp_r5;

    u8 *base = (u8 *) native_data_ov000_02246c84;
    var_r4 = 0;
    if (arg0 >= 3U) {
        return 0U;
    }
    temp_r5 = (arg0 * 0x84) + (s32) base;
    if (M2C_FIELD(temp_r5, s16 *, 0x18) != 0) {
        if ((s32) native_fn_02062aa0() > 0) {
loop_4:
            if (M2C_FIELD(temp_r5, s32 *, 0x14) == M2C_FIELD((void *) native_fn_02062a50(var_r4), s32 *, 0x14)) {
                native_fn_020628b0(var_r4);
            } else {
                var_r4 += 1;
                if (var_r4 < (s32) native_fn_02062aa0()) {
                    goto loop_4;
                }
            }
        }
        var_r4_2 = 0;
        if ((s32) native_fn_02062ad0() > 0) {
loop_8:
            if (M2C_FIELD(temp_r5, s32 *, 0x14) == M2C_FIELD((void *) native_fn_02062a88(var_r4_2), s32 *, 0x14)) {
                native_fn_02062980(var_r4_2);
            } else {
                var_r4_2 += 1;
                if (var_r4_2 < (s32) native_fn_02062ad0()) {
                    goto loop_8;
                }
            }
        }
        native_fn_020627a0(M2C_FIELD(temp_r5, s32 *, 0x14));
        native_fn_02008d78(temp_r5, 0, 0x84);
        temp_r4 = (s8) arg0;
        native_fn_ov000_02223d58(0, temp_r4, 0);
        native_fn_ov000_02223e40(0, temp_r4, 1);
        native_fn_ov000_021f51d4(1);
        var_r4 = 1;
        native_data_ov000_022468b8.field_1d = (s8) (native_data_ov000_022468b8.field_1d - 1);
        native_data_ov000_022468b8.field_1e = (s8) (native_data_ov000_022468b8.field_1e + 1);
    }
    return (u32) var_r4;
}
