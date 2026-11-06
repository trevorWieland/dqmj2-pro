#include "context.h"
u32 native_ov000_02212d54(u8 arg0, s32 arg1, s32 arg2, s32 arg3, s32 arg4, u8 arg5, u8 arg6, s16 arg7) {
    s32 var_r4;
    s32 temp_r5;
    s32 var_ip;
    u8 *var_lr;

    var_lr = native_data_ov000_02243e3c;
    var_r4 = -1;
    var_ip = 0;
loop_1:
    if (M2C_FIELD(var_lr, u8 *, 0x105) == 0) {
        var_r4 = var_ip;
    } else {
        var_ip += 1;
        var_lr += 0x10C;
        if (var_ip < 0x10) {
            goto loop_1;
        }
    }
    if (var_r4 >= 0) {
        temp_r5 = (var_r4 * 0x10C) + (s32) native_data_ov000_02243e3c;
        M2C_FIELD(temp_r5, s32 *, 0x70) = arg1;
        M2C_FIELD(temp_r5, s32 *, 0x74) = arg2;
        M2C_FIELD(temp_r5, s32 *, 0x78) = arg3;
        M2C_FIELD(temp_r5, s32 *, 0x88) = 0;
        M2C_FIELD(temp_r5, s32 *, 0x8C) = arg4;
        M2C_FIELD(temp_r5, s32 *, 0x90) = 0;
        M2C_FIELD(temp_r5, s32 *, 0x7C) = 0x1000;
        M2C_FIELD(temp_r5, s32 *, 0x80) = 0x1000;
        M2C_FIELD(temp_r5, s32 *, 0x84) = 0x1000;
        M2C_FIELD(temp_r5, u8 *, 0x106) = arg0;
        M2C_FIELD(temp_r5, u8 *, 0x107) = arg5;
        M2C_FIELD(temp_r5, s16 *, 0x100) = arg7;
        M2C_FIELD(temp_r5, u8 *, 0x108) = arg6;
        M2C_FIELD(temp_r5, s8 *, 0x105) = 1;
        native_fn_ov000_021df950((s16) native_data_ov000_0222baf4[M2C_FIELD(temp_r5, u8 *, 0x106)]);
        native_fn_ov000_02212f80(temp_r5);
    }
    return (u32) var_r4;
}
