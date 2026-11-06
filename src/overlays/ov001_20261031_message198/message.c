#include "context.h"
u32 native_ov001_021d7e80(void *arg0) {
    u8 temp_r0;
    u8 var_r1;
    u8 var_r2;
    u32 temp_r4;

    temp_r4 = native_fn_ov001_021db9e0(arg0);
    if (native_fn_ov001_021dbaac(arg0) != 0) {
        if (M2C_FIELD(arg0, u8 *, 0x31E) == 0) {
            native_fn_ov001_021d75d4(0x12);
        } else {
            native_fn_ov001_021d75d4(0x11);
        }
    } else {
        switch (temp_r4) {
        default:
        case 0:
            native_fn_ov001_021d75d4(0xE);
            break;
        case 1:
            native_fn_ov001_021d75d4(0xF);
            break;
        case 2:
            native_fn_ov001_021d75d4(0x10);
            break;
        }
    }
    native_fn_ov001_021d77b0(-1, native_fn_02042c2c(arg0));
    native_fn_ov001_021d7814(-1, native_fn_02041f74(arg0, 0));
    temp_r0 = M2C_FIELD(arg0, u8 *, 0x31E);
    var_r1 = (temp_r0 == 0);
    var_r2 = (temp_r0 == 1);
    return native_fn_ov001_021d94cc(var_r1, var_r2);
}
