#include "context.h"
u32 native_ov001_0222c54c(void) {
    u32 var_r7;
    s32 var_r8;
    s32 temp_r0_2;
    u8 *temp_r0;
    u32 var_r0;
    u8 temp_r2;
    u8 temp_r2_2;

    native_fn_0207afec(0xD7);
    if (native_data_ov001_022497e8.field_5 == 0) {
        native_fn_ov001_021d7f54(native_data_ov001_022497e8.field_0);
        ov001_begin_state_transition_021f1354(1, 0, 0x32, 1);
        ov001_select_mode_id_021f1438(native_fn_ov001_021f1414(native_data_ov001_022497e8.field_0));
        native_data_ov001_022497e8.field_4 = 0U;
        native_data_ov001_022497e8.field_5 = 5U;
    }
    if (native_data_ov001_022497e8.field_5 == 5) {
        temp_r2 = ++native_data_ov001_022497e8.field_4;
        if ((u32) temp_r2 > 0x1EU) {
            native_data_ov001_022497e8.field_5 = 0xAU;
        }
    }
    if (native_data_ov001_022497e8.field_5 == 0xA) {
        ov001_clear_state_flag4_021f14a4();
        var_r7 = 0;
        var_r8 = 0;
        do {
            temp_r0 = ov001_side_slot_record_021db438((s32) native_data_ov001_022497e8.field_0, var_r7);
            if (ov001_record_is_active_021db8d0(temp_r0) != 0) {
                temp_r0_2 = (s32) native_fn_ov001_0222c51c(temp_r0);
                if (temp_r0_2 > 0) {
                    native_fn_ov001_021d9494(temp_r0, 4, 1);
                    native_fn_ov001_021db718(temp_r0, 0 - temp_r0_2);
                    native_fn_ov001_022024d4(native_data_ov001_022497e8.field_0, (u8) var_r7, temp_r0_2);
                    var_r8 = 1;
                }
                native_fn_ov001_021ee78c(temp_r0, temp_r0_2, -1, 1, 0);
            }
            var_r7 += 1;
        } while ((s32) var_r7 < 3);
        if (var_r8 != 0) {
            var_r0 = 0xEE;
        } else {
            var_r0 = 0xF2;
        }
        native_fn_ov001_021f949c(var_r0, 1);
        native_data_ov001_022497e8.field_4 = 0U;
        native_data_ov001_022497e8.field_5 = 0x14U;
    } else if (native_data_ov001_022497e8.field_5 == 0x14) {
        temp_r2_2 = ++native_data_ov001_022497e8.field_4;
        if ((u32) temp_r2_2 > 0x1EU) {
            native_data_ov001_022497e8.field_5 = 0x64U;
        }
    }
    if (native_data_ov001_022497e8.field_5 == 0x64) {
        native_data_ov001_022497e8.field_5 = 0U;
        native_data_ov001_022497e8.field_1 = 7;
    }
    return 0U;
}
