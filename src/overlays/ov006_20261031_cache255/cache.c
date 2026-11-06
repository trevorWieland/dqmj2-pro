#include "context.h"
u32 native_ov006_021df524(u32 arg0) {
    if (native_data_ov006_0220f594.field_58 == -1U) {
        native_data_ov006_0220f594.field_58 = arg0;
        native_fn_0205e644();
        native_fn_0205e66c();
        native_fn_0205e73c(native_data_ov006_0220f594.field_58);
        return native_fn_0205e7a8(0U, native_data_ov006_0220f594.field_58);
    }
    if (native_data_ov006_0220f594.field_58 == arg0) {
        return arg0;
    }
    native_data_ov006_0220f594.field_58 = arg0;
    native_data_ov006_0220f594.field_54 = 0xF;
    return native_fn_0205e814(0U, 0U, 0xFU);
}
