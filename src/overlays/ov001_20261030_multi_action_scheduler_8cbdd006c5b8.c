typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
typedef float f32;
typedef double f64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
#define MULT_HI(a, b) ((s32)(((s64)(s32)(a) * (s32)(b)) >> 32))
#define MULTU_HI(a, b) ((u32)(((u64)(u32)(a) * (u32)(b)) >> 32))
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
#define NULL ((void *)0)
extern u32 native_fn_0202ac08();
extern u32 native_fn_0202ac4c();
extern u32 native_fn_02042c2c();
extern u32 native_fn_0207afec();
extern u32 native_fn_ov001_021d75d4(u32);
extern u32 native_fn_ov001_021d77b0();
extern u32 native_fn_ov001_021d94cc(u32, u32);
extern u32 native_fn_ov001_021d9534();
extern u32 ov001_side_slot_record_021db438();
extern u32 ov001_record_is_active_021db8d0(u32);
extern u32 native_fn_ov001_021dbb14();
extern u32 native_fn_ov001_021dbb9c();
extern u32 native_fn_ov001_021dbd24();
extern u32 native_fn_ov001_021dc5d4();
extern u32 native_fn_ov001_021dc940();
extern u32 native_fn_ov001_021e2390();
extern u32 native_fn_ov001_021e9d70();
extern u32 native_fn_ov001_021ea398();
extern u32 native_fn_ov001_021ea428();
extern u32 native_fn_ov001_021eaa88();
extern u32 native_fn_ov001_021eab0c();
extern u32 native_fn_ov001_021eab34();
extern u32 native_fn_ov001_021eab48(u32);
extern u32 native_fn_ov001_021ec03c();
extern u32 native_fn_ov001_021ec620();
extern u32 native_fn_ov001_021ec670();
extern u32 native_fn_ov001_021eea10();
extern u32 native_fn_ov001_021eeb70(u32);
extern u32 ov001_clear_state_flag4_021f14a4();
extern u32 native_fn_ov001_021f14e4();
extern u32 native_fn_ov001_022024d4();
extern u32 native_fn_ov001_0220f600();
extern u32 native_fn_ov001_0220f868();
extern u32 native_fn_ov001_022168e8();
typedef struct {
    u8 field_00;
    u8 unknown_01[2];
    u8 field_03;
    u8 unknown_04[7];
    s8 field_0b;
    u8 unknown_0c[7];
    s8 field_13;
    u8 unknown_14[1];
    u8 field_15;
    u8 unknown_16[3];
    s8 field_19;
    u8 unknown_1a[5];
    u8 field_1f;
    u8 unknown_20[16];
    s16 field_30;
    u8 unknown_32[4];
    u16 field_36;
    u8 unknown_38[20];
    s32 field_4c;
    u8 unknown_50[16];
    void * field_60;
} ActionContext;
extern ActionContext native_data_ov001_02238d7c;
extern u8 native_data_ov001_02238e14[];
extern u8 native_data_ov001_02238e44[];
u32 native_ov001_021ec6c0(void) {
    u32 var_r0;
    u32 var_r0_2;
    s16 temp_r0;
    u32 temp_r0_2;
    s8 var_r1;
    s32 temp_r3;
    u32 var_r5;
    s32 temp_r6_2;
    s32 var_r6;
    u32 temp_r6;
    s32 *temp_r7;
    u32 temp_r7_2;
    u32 temp_r7_3;
    s32 var_r8;
    s32 var_r8_2;
    u32 var_r9;
    u8 *var_r9_2;
    s32 var_r10;
    u32 temp_r4;

    temp_r4 = native_fn_0207afec(native_data_ov001_02238d7c.field_36);
    if (M2C_FIELD(native_data_ov001_02238d7c.field_60, u8 *, 0x31E) == 0) {
        var_r5 = 1;
    } else {
        var_r5 = 0;
    }
    native_fn_ov001_021eab48(M2C_FIELD(native_data_ov001_02238d7c.field_60, u8 *, 0x31E));
    if (native_data_ov001_02238d7c.field_03 == 0) {
        if (M2C_FIELD(native_data_ov001_02238d7c.field_60, u8 *, 0x31E) == 0) {
            native_fn_ov001_021d75d4(0x13U);
        } else {
            native_fn_ov001_021d75d4(0x14U);
        }
        native_fn_ov001_021d77b0(-1, native_fn_02042c2c(native_data_ov001_02238d7c.field_60));
        native_fn_ov001_021d94cc(1U, 1U);
        if (native_data_ov001_02238d7c.field_00 == 0) {
            native_fn_0202ac08(native_data_ov001_02238e14);
            temp_r0 = M2C_FIELD(temp_r4, s16 *, 0xC);
            if (temp_r0 != 0) {
                native_fn_ov001_021eea10(temp_r0, 0);
            }
            if (native_data_ov001_02238d7c.field_36 == 0) {
                native_fn_ov001_021eea10(0xB4, 0);
            }
        }
        native_data_ov001_02238d7c.field_30 = (s16) ((s32) *M2C_FIELD(native_data_ov001_02238d7c.field_60, s32 **, 0x60) >> 0xC);
        native_data_ov001_02238d7c.field_15 = 0U;
        native_data_ov001_02238d7c.field_03 = 0xAU;
        native_data_ov001_02238d7c.field_4c = 0;
    }
    if (native_data_ov001_02238d7c.field_03 == 0xA) {
        temp_r6 = native_fn_ov001_021d9534(native_data_ov001_02238d7c.field_60, -1, 1, native_data_ov001_02238d7c.field_30);
        temp_r0_2 = native_fn_ov001_021d9534(native_data_ov001_02238d7c.field_60, -1, 6, native_data_ov001_02238d7c.field_30);
        temp_r7 = M2C_FIELD(native_data_ov001_02238d7c.field_60, s32 **, 0x60);
        temp_r3 = M2C_FIELD(temp_r7, s32 *, 0);
        temp_r6_2 = temp_r3 >> 0xC;
        if (temp_r6 == (temp_r3 >> 0xC)) {
            native_fn_ov001_021ec03c(native_data_ov001_02238d7c.field_60, native_data_ov001_02238d7c.field_36);
            native_data_ov001_02238d7c.field_30 = (s16) (temp_r6_2 + 1);
            native_data_ov001_02238d7c.field_15 = (u8) (native_data_ov001_02238d7c.field_15 + 1);
            if ((native_fn_ov001_021ec670(var_r5) != 0) && (native_data_ov001_02238d7c.field_4c == 0)) {
                if (native_fn_ov001_021f14e4() != 0) {
                    native_fn_ov001_021eaa88(native_data_ov001_02238d7c.field_36);
                }
                native_fn_ov001_021eab0c(0xB, 0, 0x30, 2);
                native_data_ov001_02238d7c.field_4c = 1;
            }
        } else if (temp_r6_2 == temp_r0_2) {
            native_data_ov001_02238d7c.field_03 = 0x14U;
        } else if (temp_r6_2 >= (s32) (((s32) ((M2C_FIELD(M2C_FIELD(temp_r7, void **, 8), u16 *, 4) << 0xC) - 1) >> 0xC) - 1)) {
            if (M2C_FIELD(native_data_ov001_02238d7c.field_60, u8 *, 0x31E) == 0) {
                var_r0 = 1;
            } else {
                var_r0 = 0;
            }
            var_r9 = ov001_side_slot_record_021db438(var_r0, 0);
            var_r10 = 0;
            do {
                if (ov001_record_is_active_021db8d0((void *) var_r9) != 0) {
                    native_fn_ov001_0220f600(native_data_ov001_02238d7c.field_60, (void *) var_r9, native_data_ov001_02238d7c.field_36, M2C_FIELD((native_data_ov001_02238d7c.field_60 + (M2C_FIELD(var_r9, u8 *, 0x31F) * 2)), s16 *, 0x34E), 1);
                    if (M2C_FIELD(var_r9, s32 *, 0x33C) & 2) {
                        native_fn_ov001_022024d4(M2C_FIELD(var_r9, u8 *, 0x31E), M2C_FIELD(var_r9, u8 *, 0x31F), 0);
                    }
                    native_fn_ov001_021ea428((void *) var_r9, native_data_ov001_02238d7c.field_36);
                }
                if ((s32) M2C_FIELD((native_data_ov001_02238d7c.field_60 + (var_r10 * 2)), s16 *, 0x34E) > 0) {
                    native_fn_ov001_021e2390((void *) var_r9);
                }
                var_r10 += 1;
                var_r9 += 0x440;
            } while (var_r10 < 3);
            if (native_data_ov001_02238d7c.field_0b > 0) {
                native_fn_ov001_021ea398(0, 0xF9);
                native_data_ov001_02238d7c.field_19 = 1;
            } else {
                native_data_ov001_02238d7c.field_19 = 0;
            }
            native_data_ov001_02238d7c.field_03 = 0x32U;
        }
    }
    if (native_data_ov001_02238d7c.field_03 == 0x14) {
        if (native_fn_ov001_021f14e4() != 0) {
            ov001_clear_state_flag4_021f14a4();
        }
        native_fn_ov001_021ec620(native_data_ov001_02238d7c.field_60);
        native_data_ov001_02238d7c.field_03 = 0U;
        native_data_ov001_02238d7c.field_00 += 1;
        native_data_ov001_02238d7c.field_13 = 7;
    }
    if (native_data_ov001_02238d7c.field_03 == 0x32) {
        if (native_fn_ov001_021f14e4() != 0) {
            ov001_clear_state_flag4_021f14a4();
        }
        if (native_fn_ov001_021dbb14(0, var_r5) != 0) {
            native_data_ov001_02238d7c.field_03 = 0x3CU;
        } else {
            if (M2C_FIELD(native_data_ov001_02238d7c.field_60, u8 *, 0x31E) == 0) {
                var_r0_2 = 1;
            } else {
                var_r0_2 = 0;
            }
            if (native_fn_ov001_0220f868(var_r0_2) != 0) {
                native_data_ov001_02238d7c.field_03 = 0x3CU;
            } else {
                native_data_ov001_02238d7c.field_03 = 0x64U;
            }
        }
        var_r9_2 = native_data_ov001_02238e44;
        var_r8 = 0;
        do {
            temp_r7_2 = ov001_side_slot_record_021db438(var_r5, var_r8);
            if ((ov001_record_is_active_021db8d0(temp_r7_2) != 0) && (native_fn_ov001_021dbd24(temp_r7_2) == 0)) {
                *var_r9_2 = 1;
            }
            var_r8 += 1;
            var_r9_2 += 1;
        } while (var_r8 < 3);
    }
    if (native_data_ov001_02238d7c.field_03 == 0x3C) {
        var_r6 = 0;
        if (native_fn_ov001_021dbb9c(0, var_r5) == 0) {
            var_r6 = 1;
        }
        if (native_fn_ov001_022168e8(0, var_r5) == 0) {
            var_r6 = 1;
        }
        if (var_r6 == 0) {
            native_data_ov001_02238d7c.field_03 = 0x64U;
        }
    }
    if ((native_data_ov001_02238d7c.field_03 == 0x64) && (native_fn_ov001_021e9d70() != 0)) {
        native_data_ov001_02238d7c.field_03 = 0xC8U;
    }
    if (native_data_ov001_02238d7c.field_03 == 0xC8) {
        var_r8_2 = 0;
        do {
            temp_r7_3 = ov001_side_slot_record_021db438(var_r5, var_r8_2);
            if (ov001_record_is_active_021db8d0(temp_r7_3) != 0) {
                native_fn_ov001_021dc5d4(temp_r7_3);
                M2C_FIELD(temp_r7_3, s16 *, 0x34C) = 0;
            }
            var_r8_2 += 1;
        } while (var_r8_2 < 3);
        native_fn_ov001_021eab34();
        native_data_ov001_02238d7c.field_03 = 0U;
        native_data_ov001_02238d7c.field_00 = 0;
        if (M2C_FIELD(temp_r4, s16 *, 0xC) != 0) {
            native_fn_ov001_021eeb70(M2C_FIELD(temp_r4, s16 *, 0xC));
        }
        if (native_data_ov001_02238d7c.field_36 == 0) {
            native_fn_ov001_021eeb70(0xB4);
        }
        native_fn_0202ac4c(native_data_ov001_02238e14);
        if (native_data_ov001_02238d7c.field_1f == 0) {
            native_fn_ov001_021dc940(native_data_ov001_02238d7c.field_60, 8);
        }
        native_data_ov001_02238d7c.field_13 = 0xC;
    }
    return 0U;
}
