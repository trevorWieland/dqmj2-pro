#include "context.h"
u32 native_ov001_021f9608(void) {
    s32 value;
    void *temp_r0;

    native_fn_ov001_021f1294(0x10, 2);
    native_fn_0202ac08(native_data_ov001_02239a8c);
    temp_r0 = ov001_side_slot_record_021db438(1, (u32) native_data_ov001_0222ed28.field_1);
    M2C_FIELD(native_data_ov001_02239a14, void **, 0x40) = temp_r0;
    value = 0;
    M2C_FIELD(native_data_ov001_02239a14, s16 *, 0x26) = (s16)value;
    value += M2C_FIELD(M2C_FIELD(temp_r0, void **, 0x1E8), s8 *, 0xB0) * 0xA;
    M2C_FIELD(native_data_ov001_02239a14, s16 *, 0x26) = (s16)value;
    if (native_fn_02044424(0x40000) != 0) {
        M2C_FIELD(native_data_ov001_02239a14, s16 *, 0x26) = (s16) (M2C_FIELD(native_data_ov001_02239a14, s16 *, 0x26) + 0x190);
    }
    native_fn_02008d78(native_data_ov001_02239abc, 0, 0x84);
    native_fn_02063c00(0xD, 1);
    M2C_FIELD(native_data_ov001_02239a14, s8 *, 0xA) = 1;
    return 0U;
}
