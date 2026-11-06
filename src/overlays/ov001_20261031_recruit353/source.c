#include "context.h"
u32 native_ov001_022095f4(s32 arg0, s8 arg1) {
    u32 temp_r0_2;
    u32 temp_r0_3;
    void *temp_r0;
    void *temp_r0_4;
    s32 var_r5;
    s32 var_r6;
    u8 sp0[64];

    native_fn_0207a9ec(2);
    M2C_FIELD(native_data_ov001_0223def8, s32 *, 0x10) = arg0;
    M2C_FIELD(native_data_ov001_0223def8, s8 *, 5) = arg1;
    M2C_FIELD(native_data_ov001_0223def8, s8 *, 6) = 0;
    M2C_FIELD(native_data_ov001_0223def8, s32 *, 0x20) = 0;
    native_fn_02061238(1, 2, 3);
    temp_r0 = (void *) native_fn_ov001_021fbe70();
    temp_r0_2 = native_fn_0206271c(M2C_FIELD(temp_r0, s16 *, 0x64), M2C_FIELD(temp_r0, u8 *, 0x66));
    M2C_FIELD(native_data_ov001_0223def8, u32 *, 0x1C) = temp_r0_2;
    native_fn_02062d24(temp_r0_2, temp_r0);
    var_r5 = 0;
    if ((s32) M2C_FIELD((void *) native_fn_ov001_021fbe70(), u8 *, 0x68) > 0) {
        var_r6 = 0;
        do {
            native_fn_02062e44(M2C_FIELD(native_data_ov001_0223def8, u32 *, 0x1C), (s8)var_r5, native_fn_ov001_021fbe70() + 0x20 + var_r6);
            var_r6 += 2;
            var_r5 += 1;
        } while ((s32) var_r5 < (s32) M2C_FIELD((void *) native_fn_ov001_021fbe70(), u8 *, 0x68));
    }
    native_fn_02063038(M2C_FIELD(native_data_ov001_0223def8, u32 *, 0x1C), M2C_FIELD((void *) native_fn_ov001_021fbe70(), u8 *, 0x6A));
    temp_r0_3 = native_fn_020443ec();
    if ((temp_r0_3 != 3) && (temp_r0_3 != 7)) {

    } else {
        native_fn_02062fd4(M2C_FIELD(native_data_ov001_0223def8, u32 *, 0x1C), native_fn_ov001_021fbe70() + 0x2A);
        native_fn_02063068(M2C_FIELD(native_data_ov001_0223def8, u32 *, 0x1C), M2C_FIELD((void *) native_fn_ov001_021fbe70(), u8 *, 0x6C));
    }
    if (native_fn_02044424(0x20) != 0) {
        native_fn_02063080(M2C_FIELD(native_data_ov001_0223def8, u32 *, 0x1C), 1);
    }
    native_fn_02063050(M2C_FIELD(native_data_ov001_0223def8, u32 *, 0x1C), M2C_FIELD((void *) native_fn_ov001_021fbe70(), u8 *, 0x6B));
    temp_r0_4 = (void *) native_fn_02062a10(M2C_FIELD(native_data_ov001_0223def8, u32 *, 0x1C));
    native_fn_0207b460(M2C_FIELD(temp_r0_4, s16 *, 0x18), M2C_FIELD(temp_r0_4, u8 *, 0x1A), temp_r0_4 + 0x7A, &sp0);
    M2C_FIELD(temp_r0_4, s16 *, 0x24) = (s16) native_fn_0207c2b8(temp_r0_4 + 0x20, &sp0);
    M2C_FIELD(temp_r0_4, s16 *, 0x26) = (s16) native_fn_0207c3d8(temp_r0_4 + 0x20, &sp0);
    M2C_FIELD(native_data_ov001_0223def8, s32 *, 0x14) = 0;
    return (u32) native_data_ov001_0223def8;
}
