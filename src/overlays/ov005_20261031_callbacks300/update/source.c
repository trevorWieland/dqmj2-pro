#include "context.h"
u32 native_ov005_021e19b8(void) {
    u32 var_r4;

    var_r4 = native_data_ov005_021ed438.field_5c;
    if (*(u8 *) native_fn_ov005_021decb0() == 1) {
        if (native_fn_0205e844(0x3E) != 0) {
            *(s8 *) native_fn_ov005_021decb0() = 0;
        }
        return var_r4;
    }
    if (native_fn_ov005_021e09dc() == 1) {
        return var_r4;
    }
    if (native_data_ov005_021ed438.field_60 == 0x3D) {
        var_r4 = native_fn_ov005_021e4e48();
    } else {
        native_data_ov005_021e7778[native_data_ov005_021ed438.field_60]();
    }
    native_fn_ov005_021dfd70();
    native_fn_ov005_021e5dcc();
    if (M2C_FIELD((void *) native_fn_ov005_021e0a68(), u8 *, 0x11) != 0) {
        native_fn_ov005_021e4e80();
    }
    native_data_ov005_021ed438.field_14 += 1U;
    return var_r4;
}
