#include "context.h"
u32 native_ov001_021e00b4(void) {
    u32 temp_r0;
    void *temp_r0_2;

    if (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x29) == 0x0) {
        temp_r0 = *(native_data_ov001_02238950 + (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x28)));
        if (temp_r0 == 0) {
            if (native_fn_ov001_021dda80() != 0) {
                native_fn_ov001_021ff238(0);
                M2C_FIELD(native_data_ov001_022388ec, s8 *, 8) = 0x36;
            } else {
                M2C_FIELD(native_data_ov001_022388ec, s8 *, 8) = 0x1C;
            }
        } else if (native_fn_ov001_021db8d0(temp_r0) != 0) {
            native_fn_0202ac08(native_data_ov001_02238988);
            native_fn_ov001_021eea10(0x7D, 0);
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x29) = 5;
        } else {
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x28) = (s8) (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x28) + 1);
        }
    }
    else if (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x29) == 0x5) {
        native_fn_ov001_021d7e80(*(native_data_ov001_02238950 + (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x28))));
        M2C_FIELD(native_data_ov001_022388ec, u32 *, 0x44) = native_fn_ov001_021eec7c(0x7DU, *(native_data_ov001_02238950 + (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x28))), native_fn_0205d790(0x7DU));
        native_fn_ov001_021f1294(0x10, 2);
        native_fn_ov001_021f1354(5, 3, 0x3B, 1);
        native_fn_ov001_021f1438(native_fn_ov001_021f1414((u32) M2C_FIELD(*(native_data_ov001_02238950 + (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x28))), u8 *, 0x31E)));
        M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x29) = 6;
    }
    else if (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x29) == 0x6) {
        if (native_fn_0205d6f4(M2C_FIELD(native_data_ov001_022388ec, u32 *, 0x44)) == 0) {
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x29) = 8;
            native_fn_ov001_021f14a4();
        }
    }
    else if (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x29) == 0x8) {
        native_fn_ov001_021dc230(*(native_data_ov001_02238950 + (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x28))), 1);
        native_fn_ov001_021db788(*(native_data_ov001_02238950 + (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x28))), 0);
        M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x29) = 0xA;
    }
    else if (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x29) == 0xA) {
        temp_r0_2 = *(native_data_ov001_02238950 + (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x28)));
        if (native_fn_ov001_021dbb9c((u32) temp_r0_2, (u32) M2C_FIELD(temp_r0_2, u8 *, 0x31E)) != 0) {
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x29) = 0x64;
        }
    }
    else if (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x29) == 0x64) {
        M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x28) = (s8) (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x28) + 1);
        native_fn_ov001_021f1324();
        if (*(native_data_ov001_02238950 + (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x28))) != 0) {
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x29) = 5;
        } else {
            native_fn_0205d718(M2C_FIELD(native_data_ov001_022388ec, u32 *, 0x44));
            native_fn_ov001_021eeb70(0x7DU);
            native_fn_0202ac4c(native_data_ov001_02238988);
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x29) = 0;
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x28) = 0;
            if (native_fn_ov001_021dda80() != 0) {
                native_fn_ov001_021ff238(0);
                M2C_FIELD(native_data_ov001_022388ec, s8 *, 8) = 0x36;
            } else {
                M2C_FIELD(native_data_ov001_022388ec, s8 *, 8) = 0x1C;
            }
        }
    }
    return 0U;
}
