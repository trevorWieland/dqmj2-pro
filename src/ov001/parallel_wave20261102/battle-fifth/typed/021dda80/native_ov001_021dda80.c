#include "context.h"
u32 native_ov001_021dda80(void) {
    u32 temp_r0;
    u32 temp_r11;
    u32 temp_r4;
    u32 temp_r5;
    u32 temp_r6;
    u32 temp_r7;
    u32 temp_r8;
    u32 temp_r9;
    u32 var_r10;

    var_r10 = 1;
    temp_r9 = native_fn_020444ec();
    temp_r8 = native_fn_0204453c();
    temp_r11 = native_fn_ov001_021db8b8(0);
    temp_r7 = native_fn_ov001_021db8b8(1);
    temp_r6 = native_fn_ov001_021dda00(0);
    temp_r5 = native_fn_ov001_021dda00(1);
    temp_r4 = native_fn_ov001_021f1c28();
    temp_r0 = native_fn_ov001_02215284();
    if ((temp_r4 == 0) && (temp_r0 == 0)) {
        if (temp_r11 != 0) {
            if (temp_r7 != 0) {
                if (temp_r6 != 0) {
                    if (temp_r5 != 0) {
                        native_fn_ov001_021dc3c4(0);
                        native_fn_ov001_021dc3c4(1);
                        native_fn_ov001_021e66f8(7);
                    } else {
                        native_fn_ov001_021dc3c4(0);
                        native_fn_ov001_021e66f8(7);
                    }
                } else if (temp_r5 != 0) {
                    native_fn_ov001_021dc3c4(1);
                    native_fn_ov001_021e66f8(7);
                } else if ((temp_r9 == 0) && (temp_r8 == 0)) {
                    native_fn_ov001_021e66f8(1);
                } else if (M2C_FIELD(M2C_FIELD(native_data_ov001_022388ec, void **, 0x48), u8 *, 0x31E) == 0) {
                    native_fn_ov001_021e66f8(0);
                } else {
                    native_fn_ov001_021e66f8(1);
                }
            } else if (temp_r6 != 0) {
                native_fn_ov001_021dc3c4(0);
                native_fn_ov001_021e66f8(7);
            } else {
                native_fn_ov001_021e66f8(1);
            }
        } else if (temp_r7 != 0) {
            if (temp_r5 != 0) {
                native_fn_ov001_021dc3c4(1);
                native_fn_ov001_021e66f8(7);
            } else {
                native_fn_ov001_021e66f8(0);
            }
        } else {
            var_r10 = 0;
        }
    } else {
        native_fn_ov001_021e66f8(4);
    }
    return var_r10;
}
