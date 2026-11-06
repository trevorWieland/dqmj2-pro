#include "native_itcm_01ffa988.h"
void native_itcm_01ffa988(void) {
    volatile struct {u16 x, y;} point;
    u16 x, y;
    s32 var_r5;
    u32 temp_r4;
    void *temp_r0;

    y = native_data_020dc3b0.field_a;
    x = native_data_020dc3b0.field_8;
    point.y = y;
    point.x = x;
    native_fn_01ffa968(0x10);
    native_fn_02048fcc(native_data_01fff9b4);
    M2C_FIELD(native_data_01fff9a8, s16 *, 2) = 1;
    M2C_FIELD(native_data_01fff9a8, u8 *, 0) = 0;
    M2C_FIELD(native_data_01fff9a8, s16 *, 6) = 0;
    M2C_FIELD(native_data_01fff9a8, s16 *, 4) = -1;
    native_data_01fff9a8[8] = 0;
    native_fn_02048fcc(native_fn_01ffb340());
    var_r5 = 0;
    do {
        native_fn_ov000_02223c04(var_r5, 0x20U);
        var_r5 = (s8)(var_r5 + 1);
    } while ((s32) var_r5 < 4);
    native_fn_ov000_02223c04(1, 0x20U);
    native_fn_02048f1c(3, 1);
    native_fn_02048f2c(2, 1);
    native_fn_02048f3c(0, 1);
    native_fn_01ffb398();
    native_fn_0204b4f4(native_fn_01ffb34c(), &point, 0xE0, 2, 2, 0x24);
    native_fn_020897ec(0);
    temp_r0 = (void *) native_fn_02049ae4();
    {
        const u16 *stream = M2C_FIELD(temp_r0, const u16 **, 0);
        if (stream != (void *)0) {
            native_fn_020853c8(M2C_FIELD(temp_r0, u8 **, 4), stream);
        }
    }
    native_fn_ov000_02216260(0x1F, M2C_FIELD(native_data_01fff9a8, s8 *, 0x1C), 3, 0x16, 1, 0xA, 2, 1, 1);
    native_fn_ov000_02216260(0, M2C_FIELD(native_data_01fff9a8, s8 *, 0x1C), 0x7F, 1, 1, 0x18, 2, 1, 1);
    temp_r4 = native_fn_02048f6c(1);
    native_fn_ov000_02223c04((s8) temp_r4, native_fn_ov000_02223c14((s8) native_fn_02048f6c(1)));
    native_fn_0204b85c(native_data_01fff960, &point, 8, 1, 0, 0x33, 0);
    native_fn_0205fa4c(native_data_01fff960, 0);
    native_data_01fff950 = 0;
    *native_data_01fff934 = 0;
    native_data_021cebe0.field_4 = 0;
    native_data_021cebe0.field_44 = 0;
    native_data_021cebe0.field_20 = 0;
}
