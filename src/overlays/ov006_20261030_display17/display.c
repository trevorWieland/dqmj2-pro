#include "context.h"
u32 native_ov006_021db050(void) {
    s32 temp_r4_3;
    s32 var_r4;
    u32 temp_r4;
    u32 temp_r4_2;
    s32 temp_r5;
    s32 var_r5;
    s32 var_r6;
    u16 text[32];

    native_fn_ov006_021d7860();
    native_fn_ov006_021d77f8(9);
    native_fn_ov006_021d7d28(native_data_ov006_0220cbd8, 0x13);
    native_fn_ov006_021d79e4(0, 0xF, 2, 0x81U);
    native_fn_02046af4(native_data_021c9698, native_fn_02067748() + 0x10, 0x1F, 0, text, 0xFF);
    native_fn_ov006_021d7ad0(1, text);
    if (*(u16 *) native_fn_0206442c() != 0) {
        native_fn_ov006_021d79f8(2, 0xF, 0xF, *(u16 *) native_fn_0206442c(), 0x10);
        native_fn_ov006_021d7e34();
        native_fn_ov006_021d7ebc(native_fn_020643fc(*(u16 *) native_fn_0206442c()), 0xC, 5);
    } else {
        native_fn_ov006_021d79e4(2, 0xF, 0xF, 0U);
    }
    native_fn_ov006_021d79e4(3, 0xF, 2, 0x99U);
    native_fn_ov006_021d79e4(4, 0xF, 2, (u16) (*(s32 *) native_fn_020679f0() + 0x3B));
    native_fn_ov006_021d79e4(5, 0xF, 2, 0x34U);
    if (M2C_FIELD((void *) native_fn_020679f0(), s32 *, 4) == 0) {
        native_fn_ov006_021d79f8(6, 0xF, 2, 0x7AU, 0x30);
    } else {
        native_fn_ov006_021d8414(M2C_FIELD((void *) native_fn_020679f0(), s32 *, 4), text, 0x10, 6);
        native_fn_ov006_021d7ad0(6, text);
    }
    native_fn_ov006_021d79e4(7, 0xF, 2, 0x9DU);
    native_fn_ov006_021d79e4(8, 0xF, 2, 0x35U);
    if (M2C_FIELD((void *) native_fn_020679f0(), s32 *, 0x38) == 0) {
        native_fn_ov006_021d79f8(9, 0xF, 2, 0x7AU, 0x30);
    } else {
        native_fn_ov006_021d8414(M2C_FIELD((void *) native_fn_020679f0(), s32 *, 0x38), text, 0x10, 6);
        native_fn_ov006_021d7ad0(9, text);
    }
    native_fn_ov006_021d79e4(0xA, 0xF, 2, 0x9DU);
    native_fn_ov006_021d79e4(0xB, 0xF, 2, 0x87U);
    native_fn_ov006_021d79e4(0xC, 0xF, 7, 3U);
    native_fn_ov006_021d79e4(0xD, 0xF, 7, 4U);
    temp_r4 = native_fn_020679f0();
    temp_r5 = M2C_FIELD(temp_r4, s32 *, 0x24) + M2C_FIELD((void *) native_fn_020679f0(), s32 *, 0x28);
    temp_r4_2 = native_fn_020679f0();
    temp_r4_3 = M2C_FIELD(temp_r4_2, s32 *, 0x1C) + M2C_FIELD((void *) native_fn_020679f0(), s32 *, 0x20);
    native_fn_ov006_021d8414(temp_r5, text, 0x10, 2);
    native_fn_ov006_021d7ad0(0xE, text);
    native_fn_ov006_021d8414(temp_r4_3 - temp_r5, text, 0x10, 2);
    native_fn_ov006_021d7ad0(0xF, text);
    native_fn_ov006_021d79e4(0x10, 0xF, 2, 0x8AU);
    native_fn_ov006_021d79e4(0x11, 0xF, 2, 0x78U);
    var_r5 = 0;
    var_r4 = 0;
    var_r6 = 0;
    do {
        var_r5 += M2C_FIELD((native_fn_02067a30() + var_r6), s32 *, 0x10);
        var_r6 += 0x14;
    } while (++var_r4 < 4);
    native_fn_ov006_021d8414(var_r5, text, 0x10, 2);
    return native_fn_ov006_021d7ad0(0x12, text);
}
