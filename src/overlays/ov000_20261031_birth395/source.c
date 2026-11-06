#include "context.h"
u32 native_ov000_0221b070(void) {
    u32 temp_r0;
    u32 temp_r0_2;
    u32 var_r0;
    s32 var_r4_3;
    u32 temp_r4;
    u32 var_r4;
    u32 var_r4_2;
    u32 var_r4_4;
    u32 var_r4_5;
    u32 var_r4_6;
    u32 temp_r5;

    switch (native_data_ov000_02246090.field_3) {
    default:
    case 4:
    case 5:
    case 7:
        break;
    case 0:
        var_r4 = native_fn_ov000_0221cf14();
        if (M2C_FIELD(native_data_ov000_022460d4, s8 *, 0x10) == 1) {
            if ((s32) var_r4 > (s32) (native_data_ov000_02246090.field_20 + 1)) {
                do {
                    native_fn_ov000_0221cf60();
                    var_r4 -= 1;
                } while ((s32) var_r4 > (s32) (native_data_ov000_02246090.field_20 + 1));
            }
            native_fn_020620e8(0x10, 1U);
            native_fn_ov000_0222137c();
        } else {
            native_fn_ov000_0221cf24();
        }
        native_fn_020c49e8();
        native_fn_020c4220(2, 3);
        native_fn_ov000_0221d8e0();
        native_fn_ov000_0221deb4(0);
        
        break;
    case 1:
        if ((M2C_FIELD(native_data_ov000_022460d4, s8 *, 0x10) != 2) && (M2C_FIELD(native_data_ov000_022460d4, s8 *, 0x10) != 3)) {
            var_r4_2 = native_fn_ov000_0221cf14();
            if (M2C_FIELD(native_data_ov000_022460d4, s8 *, 0x10) == 0) {
                if (native_fn_02062378() != 0x10) {
                    return 0U;
                }
                if ((s32) var_r4_2 > (s32) (native_data_ov000_02246090.field_20 + 1)) {
                    do {
                        native_fn_ov000_0221cf60();
                        var_r4_2 -= 1;
                    } while ((s32) var_r4_2 > (s32) (native_data_ov000_02246090.field_20 + 1));
                }
                goto block_38;
            }
            if (M2C_FIELD(native_data_ov000_022460d4, s8 *, 0x10) == 0xB) {
                if (native_fn_02062378() != 0x10) {
                    return 0U;
                }
                if ((s32) var_r4_2 > 1) {
                    do {
                        native_fn_ov000_0221cf60();
                        var_r4_2 -= 1;
                    } while ((s32) var_r4_2 > 1);
                }
                goto block_38;
            }
            native_fn_ov000_0221e7e8(0);
            native_fn_ov000_0221cf24();
            native_fn_ov000_0221e808();
            native_fn_ov000_0221e6cc(native_data_ov000_022460d4, native_data_ov000_02246090.field_20);
            native_fn_ov000_0221f354();
block_38:
            if ((native_data_ov000_02246090.field_20 != 0) && ((s8) native_data_ov000_02246090.field_0 != 0)) {
                native_fn_ov000_0221ca0c(0);
            }
            if ((s8) native_data_ov000_02246090.field_0 == 8) {
                native_fn_ov000_0221c980(0);
            }
            native_fn_ov000_02220420(native_data_ov000_022460d4, native_data_ov000_02246090.field_20);
            native_fn_ov000_0221f910();
            native_fn_ov000_0221fa70(native_data_ov000_022460d4, 0);
            native_fn_ov000_0221cb8c();
            native_fn_ov000_0221d05c(0x1F, 0);
            native_fn_020c49e8();
            native_fn_020c4220(4, 3);
            native_fn_ov000_0221e7e8(1);
            if ((s8) native_data_ov000_02246090.field_0 == 8) {
                if (native_data_ov000_02246090.field_20 != 0) {
                    M2C_FIELD(native_data_ov000_022460d4, s32 *, 0) = (s32) (native_fn_ov000_0222130c() + 3);
                } else {
                    M2C_FIELD(native_data_ov000_022460d4, s32 *, 0) = (s32) (native_fn_ov000_0222130c() + 2);
                }
            }
            native_data_ov000_02246090.field_6 = 1;
            if (((s8) native_data_ov000_02246090.field_0 != 0) && ((s8) native_data_ov000_02246090.field_0 != 0xB)) {

            } else {
                native_fn_020620e8(1, 1U);
                native_fn_0206dcd0(NULL);
            }
            if (M2C_FIELD(native_data_ov000_022460d4, s8 *, 0x10) == 8) {
                native_fn_0206de74(0U);
                if (native_fn_02062378() == 6 || native_fn_02062378() == 2) {
                native_fn_020620b4(8);
                native_fn_02062358(1);
                }
            }
            
            break;
        }
        native_fn_ov000_02220afc();
        native_fn_ov000_0221a9e4();
        if ((s8) native_data_ov000_02246090.field_0 == 2) {
            native_fn_ov000_0221fa70(native_data_ov000_022460d4, 0);
            native_fn_ov000_0221d05c(0x1F, 0);
            native_fn_0207ce1c(native_fn_ov000_0221e788(0));
        } else {
            native_fn_ov000_02220160(native_data_ov000_022460d4, 0);
        }
        native_fn_ov000_0221d110(native_data_ov000_022460d4, 0, native_data_ov000_02246090.field_20);
        native_fn_ov000_0221e6cc(native_data_ov000_022460d4, native_data_ov000_02246090.field_20);
        native_fn_020c49e8();
        
        break;
    case 2:
        native_fn_0207ce1c((u32) native_data_ov000_02246090.field_3);
        native_fn_ov000_0221d8e0();
        
        break;
    case 3:
        native_fn_0207ce1c((u32) native_data_ov000_02246090.field_3);
        native_fn_ov000_0221d8e0();
        
        break;
    case 6:
        temp_r5 = native_fn_ov000_02221344();
        temp_r4 = native_fn_ov000_02221358();
        native_fn_ov000_022212f0();
        native_data_ov000_02246090.field_c = native_fn_ov000_0222900c(temp_r5, temp_r4);
        var_r0 = native_fn_ov000_0221f384(native_data_ov000_022460b4);
        native_data_ov000_02246090.field_1c = var_r0;
        var_r4_3 = 0;
        if ((s32) var_r0 > 0) {
            do {
                native_fn_0207aa98((u32) M2C_FIELD((native_data_ov000_02246090.field_24 + ((var_r0 - var_r4_3) * 2)), u8 *, -2));
                native_fn_02062e44(native_data_ov000_02246090.field_c, (s8)var_r4_3, native_data_ov000_02246090.field_24 + (((native_data_ov000_02246090.field_1c - var_r4_3) - 1) * 2));
                var_r0 = native_data_ov000_02246090.field_1c;
                var_r4_3 += 1;
            } while ((s32) var_r4_3 < (s32) var_r0);
        }
        native_fn_020633c8(native_data_ov000_02246090.field_c);
        if ((u32) (u8) (s8) (native_fn_02062378() - 1) <= 4U) {
            native_fn_0206de44(1);
        }
        native_fn_02063d7c();
        temp_r0 = native_fn_ov000_0222136c();
        if (temp_r0 != -1U) {
            native_fn_02062b34(0 - temp_r0);
        }
        native_fn_0206de74(0U);
        
        break;
    case 8:
        if (M2C_FIELD(native_data_ov000_022460d4, s8 *, 0x10) != 9) {
            temp_r0_2 = native_fn_02062378();
            if (temp_r0_2 != 8) {
                if (native_fn_02061294() == 0) {
                    native_fn_020620e8(8, 1U);
                }
                return 0U;
            }
            native_fn_0207ce1c(temp_r0_2);
            native_fn_ov000_0221d8e0();
            var_r4_4 = native_fn_ov000_0221cf14();
            if ((s32) var_r4_4 > 0) {
                do {
                    native_fn_ov000_0221cf60();
                    var_r4_4 -= 1;
                } while ((s32) var_r4_4 > 0);
            }
            native_fn_ov000_022212b8(native_data_ov000_02246098, native_data_ov000_02246091);
            native_fn_ov000_0221e7e8(0);
            native_fn_ov000_0221d110(native_data_ov000_022460d4, 0, native_data_ov000_02246090.field_20);
            native_fn_ov000_0221e808();
            native_fn_ov000_0221e6cc(native_data_ov000_022460d4, native_data_ov000_02246090.field_20);
            goto block_81;
        }
        var_r4_5 = native_fn_ov000_0221cf14();
        if ((s32) var_r4_5 > 1) {
            do {
                native_fn_ov000_0221cf60();
                var_r4_5 -= 1;
            } while ((s32) var_r4_5 > 1);
        }
        native_fn_ov000_0221e7e8(0);
        native_fn_ov000_0221e6cc(native_data_ov000_022460d4, native_data_ov000_02246090.field_20);
block_81:
        native_fn_ov000_0221deb4(0);
        native_fn_020c49e8();
        native_fn_020c4220(2, 3);
        
        break;
    case 9:
        var_r4_6 = native_fn_ov000_0221cf14();
        if ((s32) var_r4_6 > 1) {
            do {
                native_fn_ov000_0221cf60();
                var_r4_6 -= 1;
            } while ((s32) var_r4_6 > 1);
        }
        native_fn_020c49e8();
        native_fn_ov000_0221e808();
        native_fn_ov000_0221e6cc(native_data_ov000_022460d4, native_data_ov000_02246090.field_20);
        
        break;
    case 10:
        native_fn_ov000_0221f46c();
        native_fn_ov000_0221f354();
        native_fn_ov000_0221cf24();
        native_fn_020c49e8();
        native_fn_ov000_022213ec(native_data_ov000_02246090.field_18 - 1);
        
        break;
    case 11:
        native_fn_0207ce1c(native_fn_ov000_0221da3c());
        native_fn_ov000_0221cf24();
        native_fn_020c49e8();
        native_fn_ov000_0221db28();
        
        break;
    }
    return 1U;
}
