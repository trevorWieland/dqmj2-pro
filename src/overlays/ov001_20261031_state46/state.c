#include "context.h"
u32 native_ov001_021eacb0(void) {
    u32 var_r0;

    if ((M2C_FIELD(native_data_ov001_02238d7c, u8 *, 0x10) == 0) && (M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, void **, 0x60), s8 *, 0x1E4) == 0) && (M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, void **, 0x54), s8 *, 0x1E4) == 0)) {
        if (M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, void **, 0x60), u8 *, 0x31E) == 0) {
            var_r0 = 0xDD;
        } else {
            var_r0 = 0xE0;
        }
        native_fn_ov001_021f949c(var_r0, 1);
        if (native_fn_ov001_021f14e4() == 0) {
            native_fn_ov001_021eaa3c(M2C_FIELD(native_data_ov001_02238d7c, u16 *, 0x36));
            if (*native_data_ov001_0222ec84 != 0) {
                native_fn_ov001_021f1438(M2C_FIELD(native_data_ov001_02238d7c, u8 *, 0x29));
            }
        }
        M2C_FIELD(native_data_ov001_02238d7c, u8 *, 0xA) = (u8) native_fn_ov001_021e97c0();
        native_fn_ov001_021db618(M2C_FIELD(native_data_ov001_02238d7c, void **, 0x60), M2C_FIELD(native_data_ov001_02238d7c, void **, 0x54));
        native_fn_ov001_021e9884(M2C_FIELD(native_data_ov001_02238d7c, u8 *, 0xA));
        native_fn_ov001_021d9494(M2C_FIELD(native_data_ov001_02238d7c, void **, 0x60), 1, 1);
        native_fn_ov001_02202528(M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, void **, 0x60), u8 *, 0x31E), M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, void **, 0x60), u8 *, 0x31F));
        M2C_FIELD(native_data_ov001_02238d7c, u8 *, 0x10) = 0xAU;
    }
    if ((M2C_FIELD(native_data_ov001_02238d7c, u8 *, 0x10) == 0xA) && ((native_fn_ov001_021d9534(M2C_FIELD(native_data_ov001_02238d7c, void **, 0x60), -1, 1, 0) - 5) == ((s32) *M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, void **, 0x60), s32 **, 0x60) >> 0xC))) {
        M2C_FIELD(native_data_ov001_02238d7c, u8 *, 0x10) = 0x64U;
    }
    if (M2C_FIELD(native_data_ov001_02238d7c, u8 *, 0x10) == 0x64) {
        M2C_FIELD(native_data_ov001_02238d7c, u8 *, 0x10) = 0U;
        M2C_FIELD(native_data_ov001_02238d7c, s8 *, 0x13) = 5;
    }
    return 0U;
}
