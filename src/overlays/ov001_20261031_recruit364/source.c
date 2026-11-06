#include "context.h"
u32 native_ov001_02209cc0(void) {
    s32 temp_r0;
    u16 temp_r0_3;
    u16 temp_r0_6;
    u32 temp_r0_2;
    u32 temp_r0_4;
    u32 temp_r0_5;
    s32 var_r0;
    s32 var_r4_2;
    u32 var_r4;
    s32 var_r5;
    s32 var_r5_2;
    u32 temp_r6_2;
    void *temp_r6;
    s32 var_r7;

    var_r4 = 1;
    temp_r6 = native_fn_0202a634();
    var_r5 = 1;
    switch (native_data_ov001_0223def8.field_14) {
    case 0:
        if (native_fn_0207e874() != 0) {
            var_r4_2 = 0;
            native_fn_02062e18(native_data_ov001_0223def8.field_1c, native_fn_0207f3b0());
            native_fn_0206de44(1);
            native_fn_0206de64(1);
            var_r5_2 = 0;
            if ((s32) native_fn_02062aa0() > 0) {
                do {
                    temp_r0 = native_fn_02044cdc(M2C_FIELD((void *) native_fn_02062a50(var_r5_2), s16 *, 0x18)) + 1;
                    var_r5_2 += 1;
                    var_r4_2 += temp_r0;
                } while (var_r5_2 < (s32) native_fn_02062aa0());
            }
            if ((s32) (3 - var_r4_2) >= (s32) (native_fn_02044cdc(M2C_FIELD(native_fn_ov001_021fbe70(), s16 *, 0x64)) + 1)) {
                native_fn_02062850(native_data_ov001_0223def8.field_1c);
                var_r4 = 6;
            } else {
                var_r4 = 2;
                native_fn_02041538(1U, 2U, 0x10U);
            }
        }
        var_r5 = 0;
        break;
    case 1:
        var_r7 = 0;
        if (native_fn_ov001_02209c34() != 0) {
            var_r7 = 1;
        }
        if ((var_r7 != 0) && (native_fn_0206c130() == 0) && (native_fn_0206c0b0() == 0)) {
            var_r0 = 1;
        } else {
            var_r0 = 0;
        }
        native_fn_0206be08(0U, (u8) var_r0);
        temp_r0_2 = native_fn_0206a0fc(1);
        if (temp_r0_2 == 1) {
            native_fn_0206bf44();
            native_fn_ov001_02209b4c();
            var_r4 = 6;
        } else if (temp_r0_2 == 2) {
            native_data_ov001_0223def8.field_18 = native_fn_0206bdc8();
            var_r4 = 2;
        } else if (native_fn_0206a49c() == 1) {
            native_fn_ov001_0220a3d8(5, 6, 0x2C);
            native_fn_ov001_0220a3f0(0xFF, 0, 0);
            native_fn_ov001_0220a408();
            var_r4 = 3;
        }
        if (native_fn_0206c0b0() == 0) {
            native_fn_0206940c();
        }
        if (native_fn_0206c0b0() == 0) {
            temp_r0_3 = M2C_FIELD(temp_r6, u16 *, 2);
            if (temp_r0_3 & 1) {
                temp_r0_4 = native_fn_020698f4(1);
                if (temp_r0_4 == 0) {
                    if (native_fn_0206a04c() == 2) {
                        native_fn_ov001_0220a3d8(5, 6, 0x2C);
                        native_fn_ov001_0220a3f0(0xFF, 0, 0);
                        native_fn_ov001_0220a408();
                        var_r4 = 3;
                    }
                } else if (temp_r0_4 == 1) {
                    if (native_fn_ov001_02209c34() != 0) {
                        native_fn_0206bf44();
                        native_fn_ov001_02209b4c();
                        var_r4 = 6;
                    }
                } else if (temp_r0_4 == 2) {
                    native_data_ov001_0223def8.field_18 = native_fn_0206bdc8();
                    var_r4 = 2;
                }
            } else if (temp_r0_3 & 2) {
                native_fn_0206a06c(1);
            } else if (temp_r0_3 & 0x800) {
                if (*(s8 *)native_fn_0206c078() == 0) {
                    native_fn_ov001_0220a3f0(5, 2, 0x3C);
                    native_fn_ov001_0220a3d8(5, 7, 0x39);
                } else if (*(s8 *)native_fn_0206c078() == 1) {
                    native_fn_ov001_0220a3f0(5, 2, 0x3D);
                    native_fn_ov001_0220a3d8(5, 7, 0x3A);
                } else if (*(s8 *)native_fn_0206c078() == 2) {
                    native_fn_ov001_0220a3f0(5, 2, 0x3E);
                    native_fn_ov001_0220a3d8(5, 7, 0x3B);
                } else if ((*(s8 *)native_fn_0206c078() == -1) && (M2C_FIELD(native_fn_0206c078(), u8 *, 2) == 0)) {
                    native_fn_ov001_0220a3f0(5, 2, 0x3F);
                    native_fn_ov001_0220a3d8(5, 7, 0x3C);
                }
                var_r4 = 3;
                native_fn_02068f60(0);
            }
        }
        temp_r0_5 = native_fn_0206be2c();
        if (temp_r0_5 != 0) {
            temp_r6_2 = native_fn_ov001_021dc2f8(temp_r0_5);
            native_fn_0206dcd0(native_fn_02062a10(temp_r0_5));
            if (temp_r6_2 != 0) {
                native_fn_0206de1c(1, temp_r6_2 + 0x1EC);
            } else {
                native_fn_0206de1c(0, 0);
            }
        } else {
            native_fn_0206dcd0(native_fn_02062a10(native_fn_0206bf34()));
        }
        break;
    case 3:
        native_fn_020491f8(native_fn_ov001_02202360(6));
        temp_r0_6 = M2C_FIELD(temp_r6, u16 *, 2);
        if (temp_r0_6 & 1) {
            if (*(s32 *) native_fn_ov001_02202360(6) != 0) {
                var_r4 = 2;
            } else {
                native_fn_02047ff0(native_fn_02062a10(native_data_ov001_0223def8.field_18), 0x14, 0);
                var_r4 = 5;
            }
        } else if (temp_r0_6 & 2) {
            var_r4 = 2;
        } else if (temp_r0_6 & 0x800) {
            var_r4 = 3;
        }
        break;
    }
    if (var_r5 != 0) {
        native_fn_ov001_0220b21c(native_fn_ov001_02202360(6));
        native_fn_ov001_0220a97c(native_fn_ov001_02202360(6));
    }
    return var_r4;
}
