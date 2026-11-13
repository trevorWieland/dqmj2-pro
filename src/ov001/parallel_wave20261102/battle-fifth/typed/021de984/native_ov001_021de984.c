#include "context.h"
u32 native_ov001_021de984(void) {
    s32 var_r6;
    s32 var_r7;
    s32 var_r8;
    s32 var_r9;
    u32 temp_r0_2;
    u32 temp_r6;
    u32 temp_r6_2;
    u32 var_r0;
    u32 var_r0_2;
    u32 var_r5;
    u8 temp_r0;
    u8 temp_r0_3;
    u8 var_r1;
    u8 var_r1_2;
    void *temp_r4;

    var_r5 = 0;
    var_r6 = 0;
    var_r7 = 0;
    var_r8 = 0;
    var_r9 = 0;
    temp_r4 = native_data_ov001_022389bc + (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0xF) * 3);
    if (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x33) == 0x0) {
        if (M2C_FIELD(temp_r4, u8 *, 0) == 0) {
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 8) = 0x2A;
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 4) = 4;
        } else {
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x33) = 0xA;
            var_r5 = 1;
        }
    }
    else if (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x33) == 0xA) {
        temp_r0 = M2C_FIELD(temp_r4, u8 *, 0);
        if ((s32) temp_r0 == 0x47) {


            var_r7 = 1;
        }
        else if ((s32) temp_r0 == 0x49) {

            var_r7 = 1;
        }
        else if ((s32) temp_r0 == 0x26) {
            var_r7 = 1;
        }
        else if ((s32) temp_r0 == 0x57) {
            native_fn_ov001_021f1bf0(0xABU);
            native_fn_ov001_021f9248(0xBU, 0U, 0x57U, 2U);
            if (M2C_FIELD(temp_r4, u8 *, 1) == 0) {
                var_r1 = 1;
            } else {
                var_r1 = 0;
            }
            var_r5 = 1;
            M2C_FIELD(native_data_ov001_022388ec, u8 *, 0x17) = var_r1;
        }
        else if ((s32) temp_r0 == 0x58) {
            native_fn_ov001_021f1bf0(0xA9U);
            native_fn_ov001_021f9248(0xBU, 0U, 0x58U, 2U);
            if (M2C_FIELD(temp_r4, u8 *, 1) == 0) {
                var_r1_2 = 0;
            } else {
                var_r1_2 = 1;
            }
            var_r5 = 1;
            M2C_FIELD(native_data_ov001_022388ec, u8 *, 0x17) = var_r1_2;
        }
        else if ((s32) temp_r0 == 0x39) {

            var_r5 = 0;
        }
        else if ((s32) temp_r0 == 0x2B) {
            var_r5 = 0;
        }
        else if ((s32) temp_r0 == 0x32) {
            var_r8 = 1;
        }
        else if ((s32) temp_r0 == 0xF9) {

            var_r9 = 1;
        }
        else if ((s32) temp_r0 == 0xC1) {
            var_r9 = 1;
        }
        else {
            var_r6 = 1;
            var_r5 = 0;
        }
        M2C_FIELD(native_data_ov001_022388ec, u32 *, 0x48) = ov001_side_slot_record_021db438((u32) M2C_FIELD(temp_r4, u8 *, 1), (u32) M2C_FIELD(temp_r4, u8 *, 2));
        if (var_r5 != 0) {
            temp_r0_2 = ov001_side_slot_record_021db438((u32) M2C_FIELD(native_data_ov001_022388ec, u8 *, 0x17), 0U);
            M2C_FIELD(native_data_ov001_022388ec, u32 *, 0x40) = temp_r0_2;
            if ((temp_r0_2 != 0) && (ov001_record_is_active_021db8d0(temp_r0_2) == 0) && (M2C_FIELD(M2C_FIELD(native_data_ov001_022388ec, u32 *, 0x40), u8 *, 0x31C) == 0)) {
                M2C_FIELD(native_data_ov001_022388ec, u32 *, 0x40) = native_fn_ov001_021db918(M2C_FIELD(native_data_ov001_022388ec, u8 *, 0x17));
            }
            native_fn_ov001_021f1c68(1U);
            M2C_FIELD(native_data_ov001_022388ec, u8 *, 0x32) = (u8) native_fn_ov001_021f9264(0U);
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x33) = 0x14;
        } else if (var_r6 != 0) {
            temp_r0_3 = M2C_FIELD(temp_r4, u8 *, 1);
            if (((u32) (M2C_FIELD((void *) native_fn_0207afec(native_fn_0207b6e8((u32) M2C_FIELD(temp_r4, u8 *, 0))), u16 *, 8) << 0x14) >> 0x1C) != 0xA) {
                var_r0 = ov001_side_slot_record_021db438((u32) temp_r0_3, (u32) M2C_FIELD(temp_r4, u8 *, 2));
            } else {
                if (temp_r0_3 == 0) {
                    var_r0_2 = 1;
                } else {
                    var_r0_2 = 0;
                }
                var_r0 = ov001_side_slot_record_021db438(var_r0_2, 0U);
            }
            M2C_FIELD(native_data_ov001_022388ec, u32 *, 0x40) = var_r0;
            native_fn_ov001_02217910((u32) M2C_FIELD(temp_r4, u8 *, 0));
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x33) = 0x28;
        } else if (var_r7 != 0) {
            native_fn_ov001_02217910((u32) M2C_FIELD(temp_r4, u8 *, 0));
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x33) = 0x32;
        } else if (var_r8 != 0) {
            native_fn_ov001_02217910((u32) M2C_FIELD(temp_r4, u8 *, 0));
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x33) = 0x3C;
        } else if (var_r9 == 0) {
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x33) = 0x1E;
        } else {
            native_fn_ov001_02217910((u32) M2C_FIELD(temp_r4, u8 *, 0));
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x33) = 0x46;
        }
        var_r5 = 1;
    }
    else if (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x33) == 0x14) {
        if (native_fn_ov001_021f90b4() != 0) {
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x33) = 0;
            native_fn_ov001_021f9264((u32) M2C_FIELD(native_data_ov001_022388ec, u8 *, 0x32));
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 0xF) = (s8) (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0xF) + 1);
        }
    }
    else if (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x33) == 0x1E) {
        if (native_fn_ov001_02216cfc(M2C_FIELD(native_data_ov001_022388ec, u32 *, 0x48), M2C_FIELD(temp_r4, u8 *, 0)) != 0) {
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x33) = 0;
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 0xF) = (s8) (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0xF) + 1);
        }
    }
    else if (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x33) == 0x28) {
        if (native_fn_ov001_02217920(M2C_FIELD(temp_r4, u8 *, 0)) != 0) {
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x33) = 0;
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 0xF) = (s8) (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0xF) + 1);
        }
    }
    else if (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x33) == 0x32) {
        temp_r6 = native_fn_0207b6e8((u32) M2C_FIELD(temp_r4, u8 *, 0));
        if (native_fn_ov001_022170f4(M2C_FIELD(native_data_ov001_022388ec, u32 *, 0x48), temp_r6, native_fn_0207b748((u32) M2C_FIELD(temp_r4, u8 *, 0))) != 0) {
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x33) = 0;
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 0xF) = (s8) (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0xF) + 1);
        }
    }
    else if (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x33) == 0x3C) {
        if (native_fn_ov001_02216cfc(M2C_FIELD(native_data_ov001_022388ec, u32 *, 0x48), M2C_FIELD(temp_r4, u8 *, 0)) != 0) {
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x33) = 0;
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 0xF) = (s8) (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0xF) + 1);
        }
    }
    else if (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x33) == 0x46) {
        temp_r6_2 = native_fn_0207b6e8((u32) M2C_FIELD(temp_r4, u8 *, 0));
        if (native_fn_ov001_022170f4(M2C_FIELD(native_data_ov001_022388ec, u32 *, 0x48), temp_r6_2, native_fn_0207b748((u32) M2C_FIELD(temp_r4, u8 *, 0))) != 0) {
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x33) = 0;
            M2C_FIELD(native_data_ov001_022388ec, s8 *, 0xF) = (s8) (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0xF) + 1);
        }
    }
    return var_r5;
}
