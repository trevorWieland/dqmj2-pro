#include "context.h"
u32 native_ov001_02203e7c(void) {
    if (native_fn_02041814() == 1) {
        return 0U;
    }
    native_fn_02068d54();
    native_fn_ov001_02204090();
    native_fn_ov001_02203e60();
    native_fn_ov001_021fe54c(0, 0x7F);
    native_fn_ov001_021fe54c(8, 0x1D);
    native_fn_ov001_021fe54c(8, 0x1C);
    native_fn_ov001_021fe54c(8, 0x18);
    native_fn_ov001_021fe54c(8, 0x7F);
    native_fn_ov001_021fe54c(8, 0x1E);
    if (native_data_ov001_0223d8ec.field_4 != 0) {
        native_fn_0202a498(2, (u32)native_data_ov001_0223d8ec.field_4);
        native_data_ov001_0223d8ec.field_4 = 0;
    }
    native_fn_ov001_021fd354(0);
    native_data_ov001_0223d8ec.field_1 = 0;
    return 1U;
}
