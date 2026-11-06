#include "context.h"
u32 native_ov005_021df630(void) {
    u32 (*temp_r0_3)();
    u32 (*temp_r0_5)();
    s32 temp_r0_2;
    s32 temp_r0_4;
    s32 temp_r0_6;
    void *temp_r0;
    u32 var_r5;
    s32 var_r6;
    s32 temp_r7;
    u32 temp_r8;

    temp_r0 = (void *) native_fn_ov005_021dfab0();
    temp_r7 = M2C_FIELD(temp_r0, s32 *, 0);
    temp_r8 = M2C_FIELD(temp_r0, u32 *, 4);
    temp_r0_2 = (temp_r7 * 0xC) + (s32) native_data_ov005_021e6ea4;
    var_r5 = 8;
    var_r6 = 0;
    switch (temp_r8) {
    default:
        break;
    case 0:
        temp_r0_3 = M2C_FIELD(temp_r0_2, u32 (**)(), 0);
        if (temp_r0_3 != NULL) {
            temp_r0_3();
        }
        M2C_FIELD(temp_r0, u32 *, 4) = 1U;
        break;
    case 1:
        temp_r0_4 = M2C_FIELD(temp_r0_2, s32 (**)(), 4)();
        if (temp_r0_4 != temp_r7) {
            M2C_FIELD(temp_r0, s32 *, 0xC) = (s32) M2C_FIELD(temp_r0, s32 *, 0);
            M2C_FIELD(temp_r0, u32 *, 4) = 2U;
            M2C_FIELD(temp_r0, s32 *, 8) = temp_r0_4;
            var_r6 = 1;
        }
        break;
    case 2:
        temp_r0_5 = M2C_FIELD(temp_r0_2, u32 (**)(), 8);
        if (temp_r0_5 != NULL) {
            temp_r0_5();
        }
        M2C_FIELD(temp_r0, u32 *, 4) = 3U;
        var_r6 = 1;
        break;
    case 3:
        if (native_fn_02041814() != 1) {
            M2C_FIELD(temp_r0, s32 *, 0) = (s32) M2C_FIELD(temp_r0, s32 *, 8);
            M2C_FIELD(temp_r0, u32 *, 4) = 0U;
            temp_r0_6 = M2C_FIELD(temp_r0, s32 *, 0);
            switch (temp_r0_6) {
            case 4:
                var_r5 = 0;
                break;
            case 1:
                var_r5 = 0;
                break;
            case 3:
                var_r5 = 0;
                break;
            }
        }
        break;
    }
    if ((var_r6 != 0) && (temp_r8 != M2C_FIELD(temp_r0, u32 *, 4))) {
        var_r5 = native_ov005_021df630();
    }
    if (var_r6 == 2) {
        if (temp_r8 != M2C_FIELD(temp_r0, u32 *, 4)) {
            var_r5 = native_ov005_021df630();
        }
    } else if (M2C_FIELD(temp_r0, s32 *, 0) == 1) {
        var_r5 = 0;
    } else {
        native_fn_020851d4();
        native_fn_02085200();
        native_data_02101ae8.field_c84 = 1;
    }
    native_fn_0204176c();
    return var_r5;
}
