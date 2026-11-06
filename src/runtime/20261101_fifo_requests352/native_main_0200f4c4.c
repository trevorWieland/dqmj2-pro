#include "state.h"
u32 native_main_0200f4c4(u32 arg0, u32 arg1, u32 arg2, u32 arg3) {
    u32 temp_r0;

    temp_r0 = native_fn_02007ff4();
    if (native_data_020e5438.field_c != 0) {
        native_fn_02008008(temp_r0);
        return 1U;
    }
    native_data_020e5438.field_c = 1;
    native_fn_02008008(temp_r0);
    native_data_020e5438.field_20 = 2;
    native_data_020e5438.field_24 = 0;
    native_data_020e5438.field_14 = arg0;
    native_data_020e5438.field_18 = arg1;
    native_data_020e5438.field_10 = arg2;
    native_data_020e5438.field_1c = arg3;
    if (native_fn_0200fb60() != 0) {
        return 0U;
    }
    return 3U;
}
