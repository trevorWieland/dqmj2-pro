#include "context.h"
u32 native_ov001_0222c27c(void) {
    u8 temp_r2;

    if ((native_data_ov001_022497e8.field_b == 0) && (native_fn_ov001_0222c024(0xD7, native_data_ov001_022497e8.field_0, 0x30) != 0)) {
        native_data_ov001_022497e8.field_b = 0x14U;
    }
    if (native_data_ov001_022497e8.field_b == 0x14) {
        native_fn_ov001_0222c1c0(0xD7, native_data_ov001_022497e8.field_0);
        native_data_ov001_022497e8.field_a = 0U;
        native_data_ov001_022497e8.field_b = 0x1EU;
    }
    if (native_data_ov001_022497e8.field_b == 0x1E) {
        temp_r2 = ++native_data_ov001_022497e8.field_a;
        if ((u32) temp_r2 > 0x2DU) {
            native_data_ov001_022497e8.field_b = 0x64U;
        }
    }
    if (native_data_ov001_022497e8.field_b == 0x64) {
        native_data_ov001_022497e8.field_b = 0U;
        native_data_ov001_022497e8.field_1 = 7;
    }
    return 0U;
}
