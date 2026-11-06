#include "context.h"
u32 native_ov000_0221b624(s32 *arg0) {
    s8 var_r4;
    u32 temp_r5;
    u32 temp_r6;
    u32 temp_r7;
    s16 sp8;
    s16 sp6;
    u8 sp5;
    u8 sp4;

    var_r4 = M2C_FIELD(native_data_ov000_022460d4, s8 *, 0x10);
    *arg0 = 0;
    switch (M2C_FIELD(native_data_ov000_022460d4, s8 *, 0x10)) {
    default:
        break;
    case 0:
        switch (M2C_FIELD(native_data_ov000_022460d4, s32 *, 0)) {
        case 0:
            native_fn_0205e7a8(-1U, 0x52U);
            var_r4 = 1;
            if (native_fn_020273c8() != 6) {
                native_fn_020404f0(0x1C);
                native_fn_020407a8();
            }
            native_fn_ov000_0221e7e8(0);
            break;
        case 1:
            native_fn_0205e7a8(-1U, 0x53U);
            M2C_FIELD(native_data_ov000_02246090, s8 *, 7) = 8;
            native_fn_ov000_021eadd0();
            break;
        }
        break;
    case 1:
        switch (M2C_FIELD(native_data_ov000_022460d4, s32 *, 0)) {
        case 0:
        case 1:
            if (native_fn_ov000_022207a0(native_data_ov000_022460d4, M2C_FIELD(native_data_ov000_02246090, s32 *, 0x20)) != 0) {
                native_fn_0205e7a8(-1U, 0x52U);
                var_r4 = 2;
            } else {
                native_fn_0205e7a8(-1U, 0x54U);
            }
            break;
        case 2:
            if (M2C_FIELD(native_data_ov000_02246090, s32 *, 0x20) != 0) {
                native_fn_ov000_022207a0(native_data_ov000_022460d4, M2C_FIELD(native_data_ov000_02246090, s32 *, 0x20));
                native_fn_0205e7a8(-1U, 0x52U);
                var_r4 = 3;
            } else {
            default:
                if (native_fn_ov000_022207a0(native_data_ov000_022460d4, M2C_FIELD(native_data_ov000_02246090, s32 *, 0x20)) != 0) {
                    temp_r7 = native_fn_ov000_02221344();
                    temp_r6 = native_fn_ov000_02221358();
                    temp_r5 = native_fn_ov000_022212f0();
                    native_fn_ov000_022212b8(&sp8, &sp5);
                    native_fn_0205e7a8(-1U, 0x52U);
                    var_r4 = 8;
                    M2C_FIELD(native_data_ov000_02246090, u32 *, 0x1C) = native_fn_ov000_022298ec(temp_r7, temp_r6, sp8, sp5, native_data_ov000_022460b4);
                    M2C_FIELD(native_data_ov000_02246090, u8 **, 0x28) = native_fn_ov000_02229100(temp_r7, temp_r6, (u32) sp8, (u32) sp5, temp_r5);
                } else {
                    native_fn_ov000_022212b8(&sp6, &sp4);
                    if (native_fn_ov000_02220778(sp6) == 0) {
                        native_fn_020c48d0(5, 6, 0x2B);
                    } else if (((u32) M2C_FIELD(native_fn_02062a10(native_fn_ov000_02221344()), u8 *, 0x30) < 0xAU) || ((u32) M2C_FIELD(native_fn_02062a10(native_fn_ov000_02221358()), u8 *, 0x30) < 0xAU)) {
                        native_fn_020c48d0(9, 0, 0x10);
                    } else {
                        native_fn_020c48d0(9, 0, 0x11);
                    }
                    native_fn_020c48bc();
                    native_fn_020c48e8(-1U);
                    native_fn_020c484c(native_fn_02048f7c(1));
                    native_fn_ov000_0221e7e8(0);
                    native_fn_020c48e8(-1U);
                    M2C_FIELD(native_data_ov000_02246090, s8 *, 7) = 5;
                    native_fn_0205e7a8(-1U, 0x54U);
                }
            }
            break;
        }
        break;
    case 2:
        if (native_fn_ov000_0221fbb8() != 0) {
            native_fn_ov000_02221154(native_data_ov000_022460d4, 1, M2C_FIELD(native_data_ov000_02246090, s32 *, 0x20));
            native_fn_0205e7a8(-1U, 0x52U);
            native_fn_ov000_0221e7e8(0);
            var_r4 = 1;
            native_fn_ov000_0221c000(0);
        }
        break;
    case 3:
        if (native_fn_ov000_02220278() != 0) {
            native_fn_ov000_02221154(native_data_ov000_022460d4, 1, M2C_FIELD(native_data_ov000_02246090, s32 *, 0x20));
            native_fn_ov000_0221e7e8(0);
            native_fn_0205e7a8(-1U, 0x52U);
            var_r4 = 1;
        } else {
            native_fn_0205e7a8(-1U, 0x54U);
        }
        break;
    case 8:
        if ((s32) native_fn_ov000_0221ebf4() <= 0) {
            native_fn_ov000_0221e7e8(0);
            var_r4 = 9;
        }
        *arg0 = 1;
        break;
    case 9:
        switch (M2C_FIELD(native_data_ov000_022460d4, s32 *, 0)) {
        case 0:
            native_fn_0205e7a8(-1U, 0x52U);
            native_fn_ov000_0221e6cc(native_data_ov000_022460d4, M2C_FIELD(native_data_ov000_02246090, s32 *, 0x20));
            native_fn_020620e8(0x10, 1U);
            native_fn_02041538(1U, 2U, 0xAU);
            native_fn_0204157c(8);
            var_r4 = 6;
            native_fn_ov000_0221e7e8(0);
            M2C_FIELD(native_data_ov000_02246090, s32 *, 0x30) = 1;
            break;
        case 1:
            native_fn_0205e7a8(-1U, 0x53U);
            var_r4 = 8;
            break;
        }
        break;
    case 10:
        if (native_fn_020698f4(1) != 0) {
            native_fn_0206bf44();
            var_r4 = 0xB;
            native_fn_02041538(1U, 2U, 0xAU);
        } else if (native_fn_0206a04c() == 2) {
            native_fn_020c48bc();
            native_fn_020c48d0(5, 6, 0x2A);
            native_fn_020c48e8(-1U);
            native_fn_02068f60(0);
            native_fn_ov000_0221e6cc(native_data_ov000_022460d4, M2C_FIELD(native_data_ov000_02246090, s32 *, 0x20));
            native_fn_0205e7a8(-1U, 0x54U);
            M2C_FIELD(native_data_ov000_02246090, s8 *, 7) = 5;
        }
        break;
    case 11:
        switch (M2C_FIELD(native_data_ov000_022460d4, s32 *, 0)) {
        case 0:
            native_fn_ov000_0221c6e4();
            native_fn_0205e7a8(-1U, 0x52U);
            native_fn_0206dcd0(NULL);
            native_fn_ov000_021ead88(0, 0);
            native_fn_ov000_0221e7e8(0);
            var_r4 = 1;
            break;
        case 1:
            native_fn_0205e7a8(-1U, 0x53U);
            M2C_FIELD(native_data_ov000_02246090, s8 *, 7) = 8;
            native_fn_ov000_021eadd0();
            break;
        }
        break;
    }
    return (u32) var_r4;
}
