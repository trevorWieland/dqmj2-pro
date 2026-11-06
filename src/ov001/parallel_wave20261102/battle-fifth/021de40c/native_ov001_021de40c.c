#include "context.h"
u32 native_ov001_021de40c(void) {
    s32 var_r4;
    u8 var_r1;

    var_r4 = 0;
    native_fn_0202a634();
    native_fn_ov001_021f1798();
    if (native_data_ov001_022388ec.field_5 == 0) {
        native_fn_ov001_021dcb44();
        native_data_ov001_022388ec.field_5 = 0xAU;
    }
    if (native_data_ov001_022388ec.field_5 == 0xA) {
        if ((u32) native_data_ov001_022388ec.field_6 >= 2U) {
            if (native_data_ov001_022388ec.field_9 == 0) {
                if ((native_fn_ov001_021e8748() != 0) && (native_data_ov001_022388ec.field_6 != 4)) {
                    native_fn_ov001_0220b6c4();
                    var_r4 = 1;
                    native_data_ov001_022388ec.field_9 = 1U;
                    native_data_ov001_022388ec.field_1 = 0x23U;
                } else {
                    goto block_10;
                }
            } else {
block_10:
                switch (native_data_ov001_022388ec.field_6) {
                case 2:
                    native_data_ov001_022388ec.field_1 = 3U;
                    var_r4 = 1;
                    break;
                case 3:
                    native_data_ov001_022388ec.field_1 = 0x13U;
                    var_r4 = 1;
                    break;
                case 4:
                    if (native_fn_02044424(0x40) != 0) {
                        var_r1 = 0x33;
                    } else {
                        var_r1 = 0x1D;
                    }
                    native_data_ov001_022388ec.field_1 = var_r1;
                    var_r4 = 1;
                    break;
                case 5:
                    native_data_ov001_022388ec.field_1 = 0x23U;
                    var_r4 = 1;
                    break;
                }
            }
        }
        if (var_r4 != 0) {
            native_fn_ov001_02210dd0();
            native_fn_ov001_021f165c();
            native_data_ov001_022388ec.field_5 = 0x14U;
        } else {
            native_data_ov001_022388ec.field_38 = (s32) (native_data_ov001_022388ec.field_38 + 1);
        }
    }
    if ((native_data_ov001_022388ec.field_5 == 0x14) && (native_fn_ov001_02210e08() == 0)) {
        native_data_ov001_022388ec.field_5 = 0x64U;
    }
    if (native_data_ov001_022388ec.field_5 == 0x64) {
        native_data_ov001_022388ec.field_5 = 0U;
        native_data_ov001_022388ec.field_8 = (u8) native_data_ov001_022388ec.field_1;
    }
    return 0U;
}
