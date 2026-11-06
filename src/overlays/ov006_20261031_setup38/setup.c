#include "context.h"
u32 native_ov006_021d7860(void) {
    u32 temp_r0;
    u32 temp_r0_2;
    u32 temp_r0_3;
    u32 temp_r0_4;
    char path[32];
    s16 sp0;

    sp0 = 0;
    native_fn_02002c98(1, 0, 0);
    M2C_FIELD((void *)0x04000008, u16 *, 0) = (u16) ((M2C_FIELD((void *)0x04000008, u16 *, 0) & 0x43) | 0x4004);
    M2C_FIELD((void *)0x04000008, u16 *, 2) = (u16) ((M2C_FIELD((void *)0x04000008, u16 *, 2) & 0x43) | 0x210);
    M2C_FIELD((void *)0x04000008, u16 *, 6) = (u16) ((M2C_FIELD((void *)0x04000008, u16 *, 6) & 0x43) | 0x518);
    *(s32 *)0x04000000 = (*(s32 *)0x04000000 & ~0x1F00) | 0x1B00;
    M2C_FIELD((void *)0x04000008, u16 *, 0) = (u16) ((M2C_FIELD((void *)0x04000008, u16 *, 0) & ~3) | 3);
    M2C_FIELD((void *)0x04000008, u16 *, 2) = (u16) ((M2C_FIELD((void *)0x04000008, u16 *, 2) & ~3) | 2);
    M2C_FIELD((void *)0x04000008, u16 *, 6) = (u16) (M2C_FIELD((void *)0x04000008, u16 *, 6) & ~3);
    native_fn_02008c58(0, (u8 *)0x06000000, 0x80000);
    native_fn_0201d444(path, native_data_ov006_0220cb04);
    temp_r0 = native_fn_0202a8e0(path);
    if (temp_r0 != 0) {
        temp_r0_2 = native_fn_0203cc2c(path, 2);
        native_fn_020481b8(temp_r0_2, 0, temp_r0);
        native_fn_020481b8((u32) &sp0, 0, 2U);
        native_fn_0202a498(2, temp_r0_2);
    }
    native_fn_0201d444(path, native_data_ov006_0220cb1c);
    temp_r0_3 = native_fn_0202a8e0(path);
    if (temp_r0_3 != 0) {
        temp_r0_4 = native_fn_0203cc2c(path, 2);
        native_fn_0204540c(0, temp_r0_4, 0, temp_r0_3);
        native_fn_0202a498(2, temp_r0_4);
    }
    native_fn_02008c58(0, native_data_ov006_0220eb04, 0xA0);
    return native_fn_02048308();
}
