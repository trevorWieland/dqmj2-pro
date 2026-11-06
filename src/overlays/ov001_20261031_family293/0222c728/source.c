#include "context.h"
u32 native_ov001_0222c728(void) {
    u32 var_r7;
    u32 var_r8;
    u8 *temp_r0;
    u8 temp_r2;

    if ((native_data_ov001_022497e8.field_3 == 0) && (native_fn_ov001_0222c024(0xF7, native_data_ov001_022497e8.field_0, 0x33) != 0)) {
        native_data_ov001_022497e8.field_3 = 0xAU;
    }
    if (native_data_ov001_022497e8.field_3 == 0xA) {
        var_r7 = 0;
        do {
            temp_r0 = native_fn_ov001_021db438((s32) native_data_ov001_022497e8.field_0, var_r7);
            if (native_fn_ov001_021db8d0(temp_r0) != 0) {
                var_r8 = native_fn_ov001_0222c700(temp_r0);
                if ((s32) var_r8 > 0) {
                    native_fn_ov001_021d9494(temp_r0, 0, 0);
                    var_r8 = native_fn_ov001_021db7cc(temp_r0, (s32) var_r8);
                    native_fn_ov001_022024d4(native_data_ov001_022497e8.field_0, (u8) var_r7, 0 - var_r8);
                }
                native_fn_ov001_021ee7d4(temp_r0, var_r8, 2);
            }
            var_r7 += 1;
        } while ((s32) var_r7 < 3);
        native_data_ov001_022497e8.field_2 = 0U;
        native_data_ov001_022497e8.field_3 = 0x32U;
    }
    if (native_data_ov001_022497e8.field_3 == 0x32) {
        temp_r2 = ++native_data_ov001_022497e8.field_2;
        if ((u32) temp_r2 > 0x2DU) {
            native_data_ov001_022497e8.field_3 = 0x64U;
        }
    }
    if (native_data_ov001_022497e8.field_3 == 0x64) {
        native_data_ov001_022497e8.field_3 = 0U;
        native_data_ov001_022497e8.field_1 = 7;
    }
    return 0U;
}
