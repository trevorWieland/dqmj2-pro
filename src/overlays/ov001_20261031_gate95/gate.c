#include "context.h"
u32 native_ov001_021e9b84(void *arg0, s32 arg1) {
    u32 temp_r0;
    u32 var_r4_2;
    u32 var_r4;

    var_r4 = 0;
    if ((M2C_FIELD(arg0, s8 *, 0x244) != 0) && (arg1 != 0xD9)) {

    } else if (arg1 == 0x77) {
        var_r4 = native_fn_ov001_02210ad0(arg0, 2, 1U);
    } else if (native_fn_ov001_0220f098(arg0, arg1) != 0) {
        var_r4 = native_fn_ov001_0220f0cc(arg0, arg1);
    } else if ((M2C_FIELD(arg0, s8 *, 0x22D) != 0) && (arg1 != 0xD9)) {
        var_r4 = 0;
    } else if (arg1 == 0xD9) {
        var_r4 = 1;
    } else if ((native_fn_0207b004(arg1, 0x20) != 0) && (native_data_ov001_02238d7c.field_16 == 0)) {
        if ((M2C_FIELD(arg0, u8 *, 0x31E) == 0) || (native_fn_020444a8() != 0)) {
            var_r4_2 = 4;
        } else {
            var_r4_2 = 2;
        }
        temp_r0 = native_fn_0207d5a0(M2C_FIELD(arg0, u8 *, 0x1FD), var_r4_2, (u32) (M2C_FIELD((void *) native_fn_0207afec(arg1), u16 *, 8) << 0x1C) >> 0x1C);
        var_r4 = native_fn_ov001_0220efd0(arg0, arg1, temp_r0, native_fn_ov001_02210ad0(arg0, 0x100, temp_r0));
        if (var_r4 != 0) {
            native_data_ov001_02238d7c.field_16 = 1U;
        }
    }
    return var_r4;
}
