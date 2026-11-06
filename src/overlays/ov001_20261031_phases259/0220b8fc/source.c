#include "context.h"
u32 native_ov001_0220b8fc(void) {
    u8 temp_r2;

    if (native_data_ov001_0223e088.field_0 == 0) {
        native_fn_ov001_021f1354(4, 0, native_fn_ov001_0220b770(), 1);
        native_fn_ov001_0220b8b4();
        native_fn_ov001_021e3564(0x18, 1);
        native_data_ov001_0223e088.field_0 = 0xA;
    }
    if ((native_data_ov001_0223e088.field_0 == 0xA) && (native_fn_ov001_021e3584() != 0)) {
        native_fn_ov001_021e3564(0x19, 1);
        native_data_ov001_0223e088.field_16 = 0U;
        native_data_ov001_0223e088.field_0 = 0x14;
    }
    if (native_data_ov001_0223e088.field_0 == 0x14) {
        temp_r2 = ++native_data_ov001_0223e088.field_16;
        if ((u32) temp_r2 > 0x1EU) {
            native_data_ov001_0223e088.field_0 = 0x64;
        }
    }
    if (native_data_ov001_0223e088.field_0 == 0x64) {
        native_fn_ov001_021f14a4();
        native_data_ov001_0223e088.field_0 = 0;
        native_data_ov001_0223e088.field_3 = 3;
    }
    return 0U;
}
