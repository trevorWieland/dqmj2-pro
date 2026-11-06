#include "context.h"
u32 native_ov001_0222c024(u32 arg0, u32 arg1, u32 arg2) {
    u8 temp_r2;
    u32 var_r4;
    u8 *temp_r5;

    var_r4 = 0;
    temp_r5 = native_fn_0207afec(arg0);
    if (native_data_ov001_022497e8.field_d == 0) {
        native_fn_ov001_021d7f54(arg1);
        native_fn_ov001_021f1354(1, 0, arg2, 1);
        native_fn_ov001_021f1414((u8)arg1);
        native_fn_ov001_021f1438();
        native_data_ov001_022497e8.field_c = 0U;
        native_data_ov001_022497e8.field_d = 5U;
    }
    if (native_data_ov001_022497e8.field_d == 5) {
        temp_r2 = ++native_data_ov001_022497e8.field_c;
        if ((u32) temp_r2 > 0x1EU) {
            native_data_ov001_022497e8.field_d = 0xAU;
        }
    }
    if (native_data_ov001_022497e8.field_d == 0xA) {
        if (M2C_FIELD(temp_r5, s16 *, 0xC) != 0) {
            native_fn_0202ac08(native_data_ov001_022497f8);
            native_fn_ov001_021eea10(M2C_FIELD(temp_r5, s16 *, 0xC), 0);
        }
        native_data_ov001_022497e8.field_d = 0x14U;
    } else if (native_data_ov001_022497e8.field_d == 0x14) {
        if (M2C_FIELD(temp_r5, s16 *, 0xC) != 0) {
            native_fn_0205c904();
            native_data_ov001_022497e8.field_e = (s8) native_fn_ov001_0222bf54(arg0, arg1);
        }
        native_data_ov001_022497e8.field_d = 0x1EU;
    }
    if (native_data_ov001_022497e8.field_d == 30) {
        if ((M2C_FIELD(temp_r5, s16 *, 0xC) == 0) || (native_fn_0205d6f4(native_data_ov001_022497e8.field_e) == 0)) {
            native_data_ov001_022497e8.field_d = 0x23U;
        }
    }
    else if (native_data_ov001_022497e8.field_d == 35) {
        if (M2C_FIELD(temp_r5, s16 *, 0xC) != 0) {
            native_fn_ov001_021eeb70();
            native_fn_0202ac4c(native_data_ov001_022497f8);
        }
        native_fn_ov001_021f14a4();
        native_data_ov001_022497e8.field_d = 0x28U;
    }
    else if (native_data_ov001_022497e8.field_d == 40) {
        native_data_ov001_022497e8.field_d = 0U;
        var_r4 = 1;
    }

    return var_r4;
}
