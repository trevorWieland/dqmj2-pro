#include "context.h"
u32 native_ov000_02209554(void) {
    u32 var_r4;

    var_r4 = 0;
    if (((Field491_voidptr_0004 *)(native_data_ov000_02238514))->value != NULL) {
        native_fn_0202a498(1, ((Field491_s32_0040 *)(((Field491_voidptr_0004 *)(native_data_ov000_02238514))->value))->value);
        native_fn_0202a498(1, ((Field491_s32_0044 *)(((Field491_voidptr_0004 *)(native_data_ov000_02238514))->value))->value);
        native_fn_0202a498(1, ((Field491_s32_0048 *)(((Field491_voidptr_0004 *)(native_data_ov000_02238514))->value))->value);
        ((Field491_s32_0040 *)(((Field491_voidptr_0004 *)(native_data_ov000_02238514))->value))->value = 0;
        ((Field491_s32_0044 *)(((Field491_voidptr_0004 *)(native_data_ov000_02238514))->value))->value = 0;
        ((Field491_s32_0048 *)(((Field491_voidptr_0004 *)(native_data_ov000_02238514))->value))->value = 0;
        ((Field491_s32_0060 *)(((Field491_voidptr_0004 *)(native_data_ov000_02238514))->value))->value = 0;
        native_fn_02084f4c((u32) ((Field491_voidptr_0004 *)(native_data_ov000_02238514))->value);
        var_r4 |= 1;
    }
    if (((Field491_voidptr_0000 *)(native_data_ov000_02238514))->value != NULL) {
        native_fn_0202a498(1, ((Field491_s32_0040 *)(((Field491_voidptr_0000 *)(native_data_ov000_02238514))->value))->value);
        native_fn_0202a498(1, ((Field491_s32_0044 *)(((Field491_voidptr_0000 *)(native_data_ov000_02238514))->value))->value);
        native_fn_0202a498(1, ((Field491_s32_0048 *)(((Field491_voidptr_0000 *)(native_data_ov000_02238514))->value))->value);
        ((Field491_s32_0040 *)(((Field491_voidptr_0000 *)(native_data_ov000_02238514))->value))->value = 0;
        ((Field491_s32_0044 *)(((Field491_voidptr_0000 *)(native_data_ov000_02238514))->value))->value = 0;
        ((Field491_s32_0048 *)(((Field491_voidptr_0000 *)(native_data_ov000_02238514))->value))->value = 0;
        ((Field491_s32_0060 *)(((Field491_voidptr_0000 *)(native_data_ov000_02238514))->value))->value = 0;
        native_fn_02084f60((u32) ((Field491_voidptr_0000 *)(native_data_ov000_02238514))->value);
        var_r4 |= 2;
    }
    if (native_data_ov000_0223852b != NULL) {
        var_r4 |= 4;
    }
    native_fn_02088578(0U);
    return var_r4;
}
