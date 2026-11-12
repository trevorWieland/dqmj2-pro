#include "context.h"
u32 native_ov001_021df680(void)
{
    u32 handle;
    if (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x31) == 0) {
        handle = native_fn_ov001_021dcfa0(M2C_FIELD(native_data_ov001_022388ec, void **, 0x48));
        M2C_FIELD(native_data_ov001_022388ec, u32 *, 0x3C) = handle;
        if (handle != 0xFFFFFFFFU) {
            native_fn_ov001_021d7e80(M2C_FIELD(native_data_ov001_022388ec, void **, 0x48));
            native_fn_ov001_021f1294(0x10, 2);
            ov001_begin_state_transition_021f1354(1, 5, (u16)M2C_FIELD(native_data_ov001_022388ec, u32 *, 0x3C), 1);
            ov001_select_mode_id_021f1438(M2C_FIELD(M2C_FIELD(native_data_ov001_022388ec, void **, 0x48), u8 *, 0x31E));
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x30) = 0;
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x31) = 0xA;
        } else {
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x31) = 0x64;
            return 1U;
        }
    } else if (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x31) == 0xA) {
        M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x30) = (s8)(M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x30) + 1);
        if (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x30) >= 0x1E) {
            ov001_clear_state_flag4_021f14a4();
            handle = native_fn_ov001_021dcfa0(M2C_FIELD(native_data_ov001_022388ec, void **, 0x48));
            M2C_FIELD(native_data_ov001_022388ec, u32 *, 0x3C) = handle;
            if (handle != 0xFFFFFFFFU) {
                M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x31) = 0x14;
            } else {
                M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x31) = 0x64;
                return 1U;
            }
        }
    } else if (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x31) == 0x14) {
        if (native_fn_ov001_021f14e4() == 0) {
            ov001_begin_state_transition_021f1354(1, 5, (u16)M2C_FIELD(native_data_ov001_022388ec, u32 *, 0x3C), 1);
            ov001_select_mode_id_021f1438(M2C_FIELD(M2C_FIELD(native_data_ov001_022388ec, void **, 0x48), u8 *, 0x31E));
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x31) = 0xA;
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x30) = 0;
        }
    } else if (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x31) == 0x64) {
        native_fn_ov001_021f1324();
        M2C_FIELD(native_data_ov001_022388ec, s8 *, 8) = 0x18;
        M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x31) = 0;
        return 1U;
    }
    return 0U;
}
