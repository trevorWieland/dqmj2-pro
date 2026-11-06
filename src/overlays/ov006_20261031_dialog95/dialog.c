#include "context.h"
u32 native_ov006_021e979c(u32 arg0) {
    u32 var_r1;
    u32 temp_r4;

    temp_r4 = native_fn_ov006_021e5750();
    native_fn_ov006_021e6488(arg0);
    if ((temp_r4 != 0) && (native_fn_ov006_021e801c() == 3)) {
        native_fn_ov006_021e9dc8(native_data_ov006_022083de, temp_r4);
        native_fn_ov006_021eb9a4(4, 1, 0);
    } else {
        if (native_fn_ov006_021e9cc0() != 5) {
            var_r1 = 1;
        } else {
            var_r1 = 0;
        }
        native_fn_ov006_021eb9a4(5, var_r1, 0);
    }
    native_fn_ov006_021e81e8(1, native_data_ov006_022083e6, 5, native_data_ov006_02208440, 0x17, 0, 1, 0, 0);
    if (native_fn_ov006_021e571c() != 0) {
        return native_fn_ov006_021e92f4(4);
    }
    return native_fn_ov006_021e92f4(M2C_FIELD((void *) native_fn_ov006_021e5738(), s32 *, 4) & ~0x80000000);
}
