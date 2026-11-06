#include "context.h"
u32 native_ov006_021dcb20(void) {
    u32 temp_r4;
    u16 text[32];

    temp_r4 = native_fn_020679f0();
    native_fn_ov006_021d7860();
    native_fn_ov006_021d77f8(0xD);
    native_fn_ov006_021d7e34();
    native_fn_ov006_021d7d28(native_data_ov006_0220cf44, 0xD);
    native_fn_ov006_021d79e4(0, 0xF, 2, 0x81);
    native_fn_02046af4(native_data_021c9698, native_fn_02067748() + 0x10, 0x1F, 0, text, 0xFF);
    native_fn_ov006_021d7ad0(1, text);
    native_fn_ov006_021d79f8(2, 0xF, 0xF, *(u16 *) native_fn_0206442c(), 0x10);
    native_fn_ov006_021d7e34();
    native_fn_ov006_021d7ebc(native_fn_020643fc(*(u16 *) native_fn_0206442c()), 0xC, 4);
    native_fn_02048094(M2C_FIELD(temp_r4, s32 *, 0xC) + 1, 0);
    native_fn_ov006_021d79e4(3, 0xF, 2, 0x18);
    native_fn_ov006_021d8414(M2C_FIELD(temp_r4, s32 *, 0x2C) + M2C_FIELD(temp_r4, s32 *, 0x30), text, 0x10, 4);
    native_fn_ov006_021d7ad0(4, text);
    native_fn_ov006_021d79e4(5, 0xF, 2, 0x95);
    native_fn_ov006_021d8414(M2C_FIELD(temp_r4, s32 *, 0x10), text, 0x10, 4);
    native_fn_ov006_021d7ad0(6, text);
    native_fn_ov006_021d79e4(7, 0xF, 2, 0x97);
    native_fn_ov006_021d8414(M2C_FIELD(temp_r4, s32 *, 0x18), text, 0x10, 4);
    native_fn_ov006_021d7ad0(8, text);
    native_fn_ov006_021d79e4(9, 0xF, 2, 0x96);
    native_fn_ov006_021d8414(M2C_FIELD(temp_r4, s32 *, 0x14), text, 0x10, 4);
    native_fn_ov006_021d7ad0(0xA, text);
    native_fn_ov006_021d79e4(0xB, 0xF, 2, 0xAD);
    native_fn_ov006_021d8414((((M2C_FIELD(temp_r4, s32 *, 0x2C) + M2C_FIELD(temp_r4, s32 *, 0x30)) - M2C_FIELD(temp_r4, s32 *, 0x10)) - M2C_FIELD(temp_r4, s32 *, 0x18)) - M2C_FIELD(temp_r4, s32 *, 0x14), text, 0x10, 4);
    return native_fn_ov006_021d7ad0(0xC, text);
}
