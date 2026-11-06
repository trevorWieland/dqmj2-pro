#include "context.h"
u32 native_ov006_021dbe64(void) {
    u8 sp8[64];
    s32 temp_r0;
    s32 temp_r1;
    u32 temp_r4;
    u32 var_r1_2;

    temp_r4 = native_fn_02063eec();
    native_fn_ov006_021d7e34();
    native_fn_02067bd4(M2C_FIELD(native_data_ov006_0220f3b8, u32 *, 0x14));
    native_fn_02048094(M2C_FIELD(native_data_ov006_0220f3b8, u32 *, 0x14) + 1, 0);
    native_fn_ov006_021d79e4(0, 0xF, 2, 0x8DU);
    native_fn_02046af4(native_data_021c9698, (M2C_FIELD(native_data_ov006_0220f3b8, u32 *, 0x14) * 0x30) + (temp_r4 + 0x10), 0x1F, 0, sp8, 0xFF);
    native_fn_ov006_021d7ad0(2U, (u32) sp8);
    temp_r0 = M2C_FIELD(((M2C_FIELD(native_data_ov006_0220f3b8, u32 *, 0x14) * 0x30) + temp_r4), s32 *, 0x30);
    if (temp_r0 == 0) {
        native_fn_ov006_021d79e4(6, 0xF, 2, 0x7AU);
    } else {
        native_fn_02048094(temp_r0, 0);
        native_fn_ov006_021d79e4(6, 0xF, 2, 0x8BU);
    }
    native_fn_ov006_021d7ebc(native_fn_020643fc((u32) (u16) M2C_FIELD(((M2C_FIELD(native_data_ov006_0220f3b8, u32 *, 0x14) * 0x30) + temp_r4), s32 *, 0x2C)), 0xEU, 7U);
    native_fn_ov006_021d79e4(4, 0xF, 0xF, (u16) M2C_FIELD(((M2C_FIELD(native_data_ov006_0220f3b8, u32 *, 0x14) * 0x30) + temp_r4), s32 *, 0x2C));
    native_fn_ov006_021d79e4(8, 0xF, 2, (u16) (native_fn_02067d54(native_fn_ov006_021de1a8(M2C_FIELD(native_data_ov006_0220f3b8, u32 *, 0x14))) + 0xA4));
    if (M2C_FIELD(((M2C_FIELD(native_data_ov006_0220f3b8, u32 *, 0x14) * 0x30) + temp_r4), s32 *, 0x34) == 0) {
        native_fn_ov006_021d79e4(0xA, 0xF, 2, 0x9FU);
    } else {
        native_fn_ov006_021d79e4(0xA, 0xF, 2, 0x9EU);
        native_fn_ov006_021de228(M2C_FIELD(native_data_ov006_0220f3b8, u32 *, 0x14));
    }
    if (M2C_FIELD(((M2C_FIELD(native_data_ov006_0220f3b8, u32 *, 0x14) * 0x30) + temp_r4), s32 *, 0x34) != 1) {
        var_r1_2 = 0;
    } else {
        var_r1_2 = native_fn_02067b48();
    }
    native_fn_ov006_021dc08c(0xC, var_r1_2, 4);
    temp_r1 = (M2C_FIELD(native_data_ov006_0220f3b8, u32 *, 0x14) * 0x30) + temp_r4;
    return native_fn_ov006_021dc08c(0xEU,
        M2C_FIELD(((M2C_FIELD(native_data_ov006_0220f3b8, u32 *, 0x14) * 0x30) + temp_r4), s32 *, 0x34) == 1
            ? M2C_FIELD(((M2C_FIELD(native_data_ov006_0220f3b8, u32 *, 0x14) * 0x30) + temp_r4), u16 *, 0x3E) : 0U,
        4U);
}
