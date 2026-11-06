#include "context.h"
u32 native_ov006_021eb240(s32 arg0) {
    u32 temp_r4;
    u32 temp_r5;
    u32 var_r1;
    u32 var_r1_2;
    u32 var_r1_3;
    u32 var_r1_4;
    u32 var_r1_5;

    temp_r4 = native_fn_020685f0(M2C_FIELD(native_data_ov006_0220d3b8, s32 *, 8));
    temp_r5 = native_fn_0206877c(M2C_FIELD(native_data_ov006_0220d3b8, s32 *, 8));
    if (arg0 != 0) {
        native_fn_ov006_021e75ec(0x29);
        native_fn_ov006_021e749c(0x2A, 3, 0, 0xF, 2);
        native_fn_ov006_021e75ec(0x2B);
        native_fn_ov006_021e75ec(0x2C);
        native_fn_ov006_021e75ec(0x2D);
        native_fn_ov006_021e75ec(0x2E);
    }
    native_fn_ov006_021e7b64(0x29);
    native_fn_ov006_021e7b64(0x2A);
    native_fn_ov006_021e7b64(0x2B);
    native_fn_ov006_021e7b64(0x2C);
    native_fn_ov006_021e7b64(0x2D);
    native_fn_ov006_021e7b64(0x2E);
    if (M2C_FIELD(temp_r4, u8 *, 0x14) != 0) {
        native_fn_ov006_021e7824(0x29U, temp_r4 + 0x14, 0, 0, 0x13U, 1U, 0U);
    } else {
        native_fn_ov006_021e791c(0x29U, native_data_ov006_022084f8, 0, 0, 0x13U, 1U, 0U);
    }
    native_fn_ov006_021e796c(0x2A, M2C_FIELD(temp_r4, u16 *, 0x2C), 1, 0);
    native_fn_ov006_021e791c(0x2AU, (void *) native_fn_ov006_0220769c(M2C_FIELD(temp_r4, u16 *, 0x2C)), 3, 0, 0xFU, 1U, 0U);
    native_fn_ov006_021e791c(0x2BU, (void *) native_fn_ov006_021e92bc(M2C_FIELD(temp_r4, s32 *, 0x30)), 0, 0, 0xDU, 1U, 1U);
    var_r1 = M2C_FIELD(temp_r4, u32 *, 0x34);
    if (var_r1 != 0) {
        if (var_r1 >= 0xF423FU) {
            var_r1 = 0xF423F;
        }
        native_fn_ov006_021e78ac(0x2CU, var_r1, 6, 0, 0U, 9U, 1U, 1U);
    } else {
        native_fn_ov006_021e775c(0x2C, native_data_ov006_0220d3d0, 0, 0, 9U, 1U, 1U);
    }
    native_fn_ov006_021e791c(0x2CU, native_data_ov006_02208504, 9, 0, 2U, 1U, 1U);
    var_r1_2 = M2C_FIELD(temp_r4, u32 *, 0x38);
    if (var_r1_2 != 0) {
        if (var_r1_2 >= 0xF423FU) {
            var_r1_2 = 0xF423F;
        }
        native_fn_ov006_021e78ac(0x2DU, var_r1_2, 6, 0, 0U, 9U, 1U, 1U);
    } else {
        native_fn_ov006_021e775c(0x2D, native_data_ov006_0220d3d4, 0, 0, 9U, 1U, 1U);
    }
    native_fn_ov006_021e791c(0x2DU, native_data_ov006_02208504, 9, 0, 2U, 1U, 1U);
    var_r1_3 = M2C_FIELD(temp_r5, u32 *, 0);
    if (var_r1_3 >= 0x270FU) {
        var_r1_3 = 0x270F;
    }
    native_fn_ov006_021e78ac(0x2EU, var_r1_3, 4, 4, 0U, 5U, 1U, 1U);
    native_fn_ov006_021e791c(0x2EU, native_data_ov006_02208518, 9, 0, 2U, 1U, 0U);
    var_r1_4 = M2C_FIELD(temp_r5, u32 *, 4);
    if (var_r1_4 >= 0x270FU) {
        var_r1_4 = 0x270F;
    }
    native_fn_ov006_021e78ac(0x2EU, var_r1_4, 4, 0xB, 0U, 5U, 1U, 1U);
    native_fn_ov006_021e791c(0x2EU, native_data_ov006_02208514, 0x10, 0, 2U, 1U, 0U);
    var_r1_5 = M2C_FIELD(temp_r5, u32 *, 8);
    if (var_r1_5 >= 0x270FU) {
        var_r1_5 = 0x270F;
    }
    native_fn_ov006_021e78ac(0x2EU, var_r1_5, 4, 0x12, 0U, 5U, 1U, 1U);
    return native_fn_ov006_021e791c(0x2EU, native_data_ov006_02208510, 0x17, 0, 5U, 1U, 0U);
}
