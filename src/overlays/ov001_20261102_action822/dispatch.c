#include "context.h"
u32 native_ov001_021f2878(void) {
    u32 sp0[3];
    s16 temp_r4;
    s32 temp_r6;
    u32 temp_r0;
    u32 temp_r0_3;
    u32 temp_r0_4;
    u32 temp_r0_5;
    u32 temp_r0_6;
    u32 temp_r5_2;
    u32 temp_r7;
    s32 var_r8;
    u32 var_r1;
    u32 var_r6;
    u8 var_r1_2;
    void *temp_r4_2;
    void *temp_r5;

    temp_r5 = (void *) native_fn_0207afec((u32) M2C_FIELD(native_data_ov001_0223989c, u16 *, 0x50));
    temp_r4 = M2C_FIELD(temp_r5, s16 *, 0xA);
    if (M2C_FIELD(native_data_ov001_0223989c, u8 *, 0xF) == 0) {
        native_fn_ov001_021f1354(M2C_FIELD(native_data_ov001_0223989c, u8 *, 0xE), M2C_FIELD(native_data_ov001_0223989c, u8 *, 0x23), M2C_FIELD(native_data_ov001_0223989c, u16 *, 0x4E), 1);
        if (M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x15) == -1) {
            native_fn_ov001_021f1438(native_fn_ov001_021f1414((u32) M2C_FIELD(M2C_FIELD(native_data_ov001_0223989c, void **, 0x84), u8 *, 0x31E)));
        } else {
            native_fn_ov001_021f1438((u32) (u8) M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x15));
        }
        native_fn_ov001_021f1d54((u32) (M2C_FIELD(temp_r5, u16 *, 8) << 0x1C) >> 0x1C);
        if (((u32) (M2C_FIELD(temp_r5, u16 *, 8) << 0x1C) >> 0x1C) == 5) {
            var_r1 = 2;
        } else {
            var_r1 = 3;
        }
        native_fn_ov001_021d9494((u32) M2C_FIELD(native_data_ov001_0223989c, void **, 0x84), var_r1, 1U);
        native_fn_ov001_02202528(M2C_FIELD(M2C_FIELD(native_data_ov001_0223989c, void **, 0x84), u8 *, 0x31E), M2C_FIELD(M2C_FIELD(native_data_ov001_0223989c, void **, 0x84), u8 *, 0x31F));
        if (temp_r4 == 0) {
            var_r1_2 = 0x14;
        } else {
            var_r1_2 = 0xA;
        }
        M2C_FIELD(native_data_ov001_0223989c, u8 *, 0xF) = var_r1_2;
    }
    if (M2C_FIELD(native_data_ov001_0223989c, u8 *, 0xF) == 0xA) {
        native_fn_0202ac08(native_data_ov001_0223992c);
        native_fn_ov001_021eea10(temp_r4, 0);
        M2C_FIELD(native_data_ov001_0223989c, u8 *, 0xF) = 0xFU;
    } else if (M2C_FIELD(native_data_ov001_0223989c, u8 *, 0xF) == 0xF) {
        native_fn_0205c904((u32) temp_r4);
        M2C_FIELD(native_data_ov001_0223989c, u8 *, 6) = (u8) native_fn_ov001_021eec7c((u32) temp_r4, (u32) M2C_FIELD(native_data_ov001_0223989c, void **, 0x84), native_fn_0205d790((u32) temp_r4));
        native_fn_ov001_021f94d8(0x99U, 1U);
        M2C_FIELD(native_data_ov001_0223989c, u8 *, 0xF) = 0x14U;
    }
    if (M2C_FIELD(native_data_ov001_0223989c, u8 *, 0xF) == 0x14) {
        temp_r6 = *M2C_FIELD(M2C_FIELD(native_data_ov001_0223989c, void **, 0x84), s32 **, 0x60);
        temp_r5_2 = native_fn_ov001_021d9534((u32) M2C_FIELD(native_data_ov001_0223989c, void **, 0x84), -1U, 6U, 0U);
        temp_r0 = native_fn_ov001_021d9534((u32) M2C_FIELD(native_data_ov001_0223989c, void **, 0x84), -1U, 8U, 0U);
        if (temp_r5_2 <= (u32) (temp_r6 >> 0xC)) {
            M2C_FIELD(native_data_ov001_0223989c, u8 *, 0xF) = 0x64U;
        } else if (temp_r0 <= (u32) (temp_r6 >> 0xC)) {
            M2C_FIELD(native_data_ov001_0223989c, u8 *, 0xF) = 0x6EU;
        }
    }
    if ((M2C_FIELD(native_data_ov001_0223989c, u8 *, 0xF) != 0x64) && (M2C_FIELD(native_data_ov001_0223989c, u8 *, 0xF) != 0x6E)) {

    } else {
        if (temp_r4 != 0) {
            native_fn_0205d718((u32) M2C_FIELD(native_data_ov001_0223989c, u8 *, 6));
            native_fn_ov001_021eeb70((u32) temp_r4);
            native_fn_0202ac4c(native_data_ov001_0223992c);
        }
        native_fn_ov001_021f14a4();
        if (M2C_FIELD(native_data_ov001_0223989c, u8 *, 0xF) == 0x64) {
            var_r6 = 0;
            do {
                sp0[var_r6] = native_fn_ov001_021db438((u32) M2C_FIELD(M2C_FIELD(native_data_ov001_0223989c, void **, 0x84), u8 *, 0x31E), var_r6);
                if (native_fn_ov001_021db8d0(sp0[var_r6]) != 0) {
                    native_fn_ov001_021dbd30(sp0[var_r6]);
                }
                var_r6 += 1;
            } while ((s32) var_r6 < 3);
            native_fn_ov001_021dca54((u32) M2C_FIELD(native_data_ov001_0223989c, void **, 0x84), 0U, 4U);
            if (M2C_FIELD(native_data_ov001_0223989c, u8 *, 0x35) != 1) {
                native_fn_ov001_02202540(M2C_FIELD(M2C_FIELD(native_data_ov001_0223989c, void **, 0x84), u8 *, 0x31E), M2C_FIELD(M2C_FIELD(native_data_ov001_0223989c, void **, 0x84), u8 *, 0x31F));
            }
            temp_r0_3 = native_fn_0207b02c(M2C_FIELD(native_data_ov001_0223989c, u16 *, 0x50), 0x80000400);
            temp_r0_4 = native_fn_ov001_021dd02c((u32) M2C_FIELD(native_data_ov001_0223989c, void **, 0x84), (u32) M2C_FIELD(native_data_ov001_0223989c, u16 *, 0x50), temp_r0_3);
            if ((temp_r0_4 != 0) && (*native_data_ov001_0222ed14 != 0)) {
                if (temp_r0_3 == 0) {
                    temp_r4_2 = M2C_FIELD(native_data_ov001_0223989c, void **, 0x84);
                    temp_r0_5 = native_fn_0207b244(M2C_FIELD(native_data_ov001_0223989c, u16 *, 0x50), native_fn_ov001_021dbd30((u32) temp_r4_2), M2C_FIELD(temp_r4_2, s32 *, 0x1E8) + 0x46);
                    native_fn_ov001_021db834(M2C_FIELD(native_data_ov001_0223989c, void **, 0x84), temp_r0_5);
                    M2C_FIELD(native_data_ov001_0223989c, u32 *, 0x5C) = temp_r0_5;
                    native_fn_ov001_022024d4((u32) M2C_FIELD(M2C_FIELD(native_data_ov001_0223989c, void **, 0x84), u8 *, 0x31E), (u32) M2C_FIELD(M2C_FIELD(native_data_ov001_0223989c, void **, 0x84), u8 *, 0x31F), 0U);
                } else {
                    var_r8 = 0;
                    M2C_FIELD(native_data_ov001_0223989c, u32 *, 0x5C) = 0U;
                    do {
                        temp_r7 = (&sp0[0])[var_r8];
                        if (native_fn_ov001_021db8d0(temp_r7) != 0) {
                            temp_r0_6 = native_fn_0207b244(M2C_FIELD(native_data_ov001_0223989c, u16 *, 0x50), native_fn_ov001_021dbd30(temp_r7), M2C_FIELD(temp_r7, s32 *, 0x1E8) + 0x46);
                            native_fn_ov001_021db834((void *) temp_r7, temp_r0_6);
                            M2C_FIELD(native_data_ov001_0223989c, u32 *, 0x5C) = (u32) (M2C_FIELD(native_data_ov001_0223989c, u32 *, 0x5C) + temp_r0_6);
                            native_fn_ov001_022024d4((u32) M2C_FIELD(temp_r7, u8 *, 0x31E), (u32) M2C_FIELD(temp_r7, u8 *, 0x31F), 0U);
                        }
                        var_r8 += 1;
                    } while (var_r8 < 3);
                }
            }
            if ((M2C_FIELD(M2C_FIELD(native_data_ov001_0223989c, void **, 0x84), s8 *, 0x23C) != 0) && (native_fn_0207b004(M2C_FIELD(native_data_ov001_0223989c, u16 *, 0x50), 2) != 0) && (M2C_FIELD(native_data_ov001_0223989c, u8 *, 0x35) != 1)) {
                M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x1B) = 0x10;
            } else if ((temp_r0_4 == 0) && (*native_data_ov001_0222ed14 != 0) && (M2C_FIELD(native_data_ov001_0223989c, u8 *, 0x35) != 1)) {
                M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x1B) = 0x11;
            } else if ((M2C_FIELD(M2C_FIELD(native_data_ov001_0223989c, void **, 0x84), s8 *, 0x23E) != 0) && (native_fn_0207b004(M2C_FIELD(native_data_ov001_0223989c, u16 *, 0x50), 8) != 0) && (M2C_FIELD(native_data_ov001_0223989c, u8 *, 0x35) != 1)) {
                M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x1B) = 0x12;
            } else if ((M2C_FIELD(M2C_FIELD(native_data_ov001_0223989c, void **, 0x84), s8 *, 0x254) != 0) && (native_fn_0207b004(M2C_FIELD(native_data_ov001_0223989c, u16 *, 0x50), 0x04000000) != 0) && (M2C_FIELD(native_data_ov001_0223989c, u8 *, 0x35) != 1)) {
                M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x1B) = 0x13;
            } else if ((M2C_FIELD(M2C_FIELD(native_data_ov001_0223989c, void **, 0x84), s8 *, 0x23D) != 0) && (native_fn_0207b004(M2C_FIELD(native_data_ov001_0223989c, u16 *, 0x50), 4) != 0) && (M2C_FIELD(native_data_ov001_0223989c, u8 *, 0x35) != 1)) {
                M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x1B) = 0x14;
            } else if ((M2C_FIELD(M2C_FIELD(native_data_ov001_0223989c, void **, 0x84), s8 *, 0x255) != 0) && (native_fn_0207b004(M2C_FIELD(native_data_ov001_0223989c, u16 *, 0x50), 0x02000000) != 0) && (M2C_FIELD(native_data_ov001_0223989c, u8 *, 0x35) != 1)) {
                M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x1B) = 0x15;
            } else if ((native_fn_ov001_021e29e8() & 1) && (native_fn_0207b004(M2C_FIELD(native_data_ov001_0223989c, u16 *, 0x50), 0x20000) != 0) && (M2C_FIELD(native_data_ov001_0223989c, u8 *, 0x35) != 1)) {
                M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x1B) = 0x16;
            } else if ((M2C_FIELD(M2C_FIELD(native_data_ov001_0223989c, void **, 0x84), s8 *, 0x266) != 0) && (((u32) (M2C_FIELD((void *) native_fn_0207afec((u32) M2C_FIELD(native_data_ov001_0223989c, u16 *, 0x50)), u16 *, 8) << 0x14) >> 0x1C) == 4) && (M2C_FIELD((void *) native_fn_0207afec((u32) M2C_FIELD(native_data_ov001_0223989c, u16 *, 0x50)), u8 *, 0x21) == 0x2B) && (M2C_FIELD(native_data_ov001_0223989c, u8 *, 0x35) != 1)) {
                M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x1B) = 0x17;
            } else if ((M2C_FIELD(native_data_ov001_0223989c, u16 *, 0x50) != 0x34) && (M2C_FIELD(native_data_ov001_0223989c, u16 *, 0x50) != 0x35) && (M2C_FIELD(native_data_ov001_0223989c, u16 *, 0x50) != 0xC1)) {
                M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x1B) = 3;
            } else {
                M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x1B) = 2;
            }
        } else {
            M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x1B) = 0x1A;
        }
        M2C_FIELD(native_data_ov001_0223989c, u8 *, 0xF) = 0U;
    }
    return 0U;
}
