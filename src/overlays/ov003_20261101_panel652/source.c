#include "context.h"
u32 native_ov003_021df6ac(void *arg0) {
    s8 temp_r1_2;
    s8 var_r9;
    u32 var_r0;
    u8 *var_r4;
    u8 *var_r5;
    u8 *var_r6;
    void *temp_r9;
    void *temp_r0;
    void *temp_r9_2;
    s32 var_r4_2;

    if (M2C_FIELD(arg0, s8 *, 0x10) == 3) {
        native_fn_0206b324(0);
    } else {
        var_r4 = native_data_ov003_021e0a68;
        var_r5 = native_data_ov003_021e0a70;
        var_r6 = native_data_ov003_021e0a6c;
        var_r9 = 0;
        do {
            native_fn_02049008(arg0, (s8)*var_r6++, (s8)*var_r5++, (s8)*var_r4++, 2);
            var_r9 += 1;
        } while ((s32) var_r9 < 2);
    }
    var_r4_2 = 0;
    do {
        temp_r0 = (void *) native_fn_02049ad0(var_r4_2);
        temp_r9 = M2C_FIELD(temp_r0, void **, 0);
        if ((temp_r9 != NULL) && ((M2C_FIELD(M2C_FIELD(temp_r9, void **, 4), s32 *, 0x18) & 2) == 2)) {
            var_r0 = native_fn_ov003_021de71c(M2C_FIELD(temp_r0, s8 *, 5));
            if (var_r0 != 0x7F) {
                temp_r1_2 = M2C_FIELD(temp_r0, s8 *, 5);
                temp_r9_2 = M2C_FIELD(temp_r9, void **, 4);
                if (temp_r1_2 == 0x7F) {
                    native_fn_02045dc4(1, native_fn_02048f5c(1), M2C_FIELD(temp_r9_2, u8 *, 0x5C), M2C_FIELD(temp_r9_2, u8 *, 0x5D), (s32) M2C_FIELD(temp_r9_2, u8 *, 0x5E), (s32) M2C_FIELD(temp_r9_2, u8 *, 0x5F));
                } else {
                    if (temp_r1_2 == 0xF) {
                        if ((var_r4_2 >= 8) && (var_r4_2 <= 0xE)) {
                            M2C_FIELD(temp_r0, s8 *, 5) = 0xD;
                        }
                        if ((var_r4_2 >= 0xF) && (var_r4_2 <= 0x15)) {
                            M2C_FIELD(temp_r0, s8 *, 5) = (s8) native_fn_ov003_021de71c(0xE);
                        }
                        var_r0 = native_fn_ov003_021de71c(M2C_FIELD(temp_r0, s8 *, 5));
                    }
                    native_fn_0206006c((0xC * var_r0) + (s32) native_data_ov003_021e0a9c, (s8) M2C_FIELD(temp_r9_2, u8 *, 0x5C), (s8) M2C_FIELD(temp_r9_2, u8 *, 0x5D), (s8) M2C_FIELD(temp_r9_2, u8 *, 0x5E), (s32) (s8) M2C_FIELD(temp_r9_2, u8 *, 0x5F));
                }
            }
        }
        var_r4_2 = (s32) (s8) (var_r4_2 + 1);
    } while (var_r4_2 < 0x24);
    native_fn_020851d4();
    return native_fn_02085200();
}
