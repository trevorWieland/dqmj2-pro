#include "context.h"
u32 native_ov005_021db400(void) {
    u32 temp_r0;
    s32 var_r6;
    u8 *var_r7;
    s32 var_r8;
    u8 *var_r9;
    u8 *var_r10;

    native_fn_02048a44(native_data_ov005_021e9eb0, 1);
    M2C_FIELD((void *)0x04000010, volatile s32 *, 0) = (s32) (native_data_ov005_021e9818.field_2c & 0x1FF);
    M2C_FIELD((void *)0x04000010, volatile s32 *, 4) = (s32) (native_data_ov005_021e9818.field_2c & 0x1FF);
    M2C_FIELD((void *)0x04000010, volatile s32 *, 0xC) = (s32) (native_data_ov005_021e9818.field_2c & 0x1FF);
    native_data_ov005_021e9818.field_2c = (s32) (native_data_ov005_021e9818.field_2c & 0x1FF);
    if (native_data_ov005_021e9818.field_68 == 1) {
        native_data_ov005_021e9b48.field_7c |= 2;
    } else {
        native_data_ov005_021e9b48.field_7c &= ~2;
    }
    if (native_data_ov005_021e9818.field_40 == 1) {
        *(volatile s32 *)0x04000000 = (*(volatile s32 *)0x04000000 & ~0x1F00) | 0x1400;
        native_data_ov005_021e9818.field_2c = 0x100;
        native_fn_02048a60(native_data_ov005_021e9ea8, 0x80, 0x80);
        native_data_ov005_021e9a28.field_7c = (s32) (native_data_ov005_021e9a28.field_7c & ~2);
    } else {
        native_fn_02048a60(native_data_ov005_021e9ea8, 0xD0 - native_data_ov005_021e9818.field_2c, 0xB8);
    }
    native_fn_02048a60(native_data_ov005_021e9cf8, 0x80 - native_data_ov005_021e9818.field_2c, 0x60);
    native_fn_02048a60(native_data_ov005_021e9bd8, 0x80 - native_data_ov005_021e9818.field_2c, 0x60);
    native_fn_02048a60(native_data_ov005_021e9ab8, 0x80 - native_data_ov005_021e9818.field_2c, 0x50);
    var_r7 = native_data_ov005_021ea298;
    var_r9 = native_data_ov005_021ea0e8;
    var_r10 = native_data_ov005_021e9f38;
    var_r6 = 0;
    var_r8 = 0x10;
    do {
        native_fn_02048a60(var_r7, var_r8 - native_data_ov005_021e9818.field_2c, 0x38);
        native_fn_02048a60(var_r9, var_r8 - native_data_ov005_021e9818.field_2c, 0x34);
        temp_r0 = native_fn_02048a60(var_r10, var_r8 - native_data_ov005_021e9818.field_2c, 0x34);
        var_r7 += 0x90;
        var_r8 += 0x30;
        var_r9 += 0x90;
        var_r10 += 0x90;
    } while (++var_r6 < 3);
    return temp_r0;
}
