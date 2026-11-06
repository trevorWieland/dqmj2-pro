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
#define NULL ((void *)0)
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_arm7_fn_037fdd00(void);
extern u32 native_arm7_fn_027e0840(u32);
extern u32 native_arm7_fn_027e086c(u32);
extern u32 native_arm7_fn_037fdd14(u32);
extern u8 native_arm7_data_027f8884;
u32 native_arm7_main_027e8428(void *arg0, void *arg1) {
    u16 temp_r0;
    u16 temp_r0_2;
    u16 temp_r0_3;
    u16 temp_r0_4;
    u16 temp_r1_3;
    u16 temp_r1_4;
    u16 temp_r1_5;
    u16 var_r1;
    u16 var_r1_2;
    u16 var_r1_3;
    u32 temp_r1;
    u32 temp_r1_2;
    u32 temp_r3;
    u32 temp_r3_2;
    u32 temp_r5;
    u32 var_r6;
    s32 var_r7;
    u16 *temp_r8;

    temp_r8 = M2C_FIELD((u32) &native_arm7_data_027f8884, u16 **, 0x550);
    var_r7 = M2C_FIELD(arg0, s32 *, 0);
    var_r6 = 0;
    if (((u32) (u16) (M2C_FIELD(temp_r8, u16 *, 0) + 0xFFF7) <= 1U) && (var_r7 & 0x2C00)) {
        var_r7 &= ~0x2C00;
        var_r6 = 3;
    }
    temp_r5 = native_arm7_fn_037fdd00();
    if (arg1 != NULL) {
        M2C_FIELD(arg1, s32 *, 0) = 0x3FFF;
        M2C_FIELD(arg1, u16 *, 4) = (u16) M2C_FIELD(temp_r8, u16 *, 0x58);
        M2C_FIELD(arg1, u16 *, 6) = (u16) M2C_FIELD(temp_r8, u16 *, 0x5A);
        M2C_FIELD(arg1, u16 *, 8) = (u16) M2C_FIELD(temp_r8, u16 *, 0x5C);
        M2C_FIELD(arg1, u16 *, 0xA) = (u16) M2C_FIELD(temp_r8, u16 *, 0x30);
        M2C_FIELD(arg1, u16 *, 0xC) = (u16) M2C_FIELD(temp_r8, u16 *, 0x32);
        M2C_FIELD(arg1, u16 *, 0xE) = (u16) M2C_FIELD(temp_r8, u16 *, 0x44);
        M2C_FIELD(arg1, u16 *, 0x10) = (u16) M2C_FIELD(temp_r8, u16 *, 0x46);
        M2C_FIELD(arg1, u16 *, 0x12) = (u16) M2C_FIELD(temp_r8, u16 *, 0x40);
        M2C_FIELD(arg1, u16 *, 0x14) = (u16) M2C_FIELD(temp_r8, u16 *, 0x42);
        M2C_FIELD(arg1, u16 *, 0x16) = (u16) M2C_FIELD(temp_r8, u16 *, 0x98);
        M2C_FIELD(arg1, s8 *, 0x18) = (s8) M2C_FIELD(temp_r8, u16 *, 0x92);
        M2C_FIELD(arg1, s8 *, 0x19) = (s8) M2C_FIELD(temp_r8, u16 *, 0x94);
        M2C_FIELD(arg1, s8 *, 0x1A) = (s8) M2C_FIELD(temp_r8, u16 *, 0x9A);
        M2C_FIELD(arg1, s8 *, 0x1B) = (s8) M2C_FIELD(temp_r8, u16 *, 0x9C);
    }
    if (var_r7 & 1) {
        var_r1 = M2C_FIELD(arg0, u16 *, 4);
        if (var_r1 == 0) {
            var_r1 = 0x10;
        }
        M2C_FIELD(temp_r8, u16 *, 0x58) = var_r1;
        M2C_FIELD(temp_r8, u16 *, 0x7C0) = var_r1;
    }
    if (var_r7 & 2) {
        var_r1_2 = M2C_FIELD(arg0, u16 *, 6);
        if (var_r1_2 == 0) {
            var_r1_2 = 0x10;
        }
        M2C_FIELD(temp_r8, u16 *, 0x5A) = var_r1_2;
        M2C_FIELD(temp_r8, u16 *, 0x7C2) = var_r1_2;
        if ((s32) M2C_FIELD(temp_r8, s16 *, 0x62) > (s32) var_r1_2) {
            M2C_FIELD(temp_r8, s16 *, 0x62) = (s16) var_r1_2;
        }
    }
    if (var_r7 & 4) {
        var_r1_3 = M2C_FIELD(arg0, u16 *, 8);
        if (var_r1_3 == 0) {
            var_r1_3 = 0x10;
        }
        M2C_FIELD(temp_r8, u16 *, 0x5C) = var_r1_3;
        M2C_FIELD(temp_r8, u16 *, 0x7C4) = var_r1_3;
        if ((s32) M2C_FIELD(temp_r8, s16 *, 0x62) > (s32) var_r1_3) {
            M2C_FIELD(temp_r8, s16 *, 0x62) = (s16) var_r1_3;
        }
    }
    if (var_r7 & 8) {
        temp_r0 = M2C_FIELD(arg0, u16 *, 0xA);
        if ((u32) M2C_FIELD(temp_r8, u16 *, 0x34) < (u32) (u16) ((temp_r0 + 1) & ~1)) {
            var_r6 = 6;
        } else {
            native_arm7_fn_027e0840((u32) temp_r0);
        }
    }
    if (var_r7 & 0x10) {
        temp_r0_2 = M2C_FIELD(arg0, u16 *, 0xC);
        if ((u32) (u16) ((temp_r0_2 + 1) & ~1) > 0x200U) {
            var_r6 = 6;
        } else {
            native_arm7_fn_027e086c((u32) temp_r0_2);
        }
    }
    if (var_r7 & 0x20) {
        temp_r0_3 = M2C_FIELD(arg0, u16 *, 0xE);
        if ((u32) temp_r0_3 > 0x2710U) {
            var_r6 = 6;
        } else {
            M2C_FIELD(temp_r8, u16 *, 0x44) = temp_r0_3;
            M2C_FIELD(temp_r8, u64 *, 0x48) = ((((u64)temp_r0_3 * 0x82EA) / 64) / 1024);

        }
    }
    if (var_r7 & 0x40) {
        temp_r0_4 = M2C_FIELD(arg0, u16 *, 0x10);
        if ((u32) temp_r0_4 > 0x2710U) {
            var_r6 = 6;
        } else {
            M2C_FIELD(temp_r8, u16 *, 0x46) = temp_r0_4;
            M2C_FIELD(temp_r8, u64 *, 0x50) = ((((u64)temp_r0_4 * 0x82EA) / 64) / 1024);

        }
    }
    if (var_r7 & 0x80) {
        temp_r1_3 = M2C_FIELD(arg0, u16 *, 0x12);
        if (((u32) temp_r1_3 <= 0xBEU) || (((u32) temp_r1_3 >= 0xDCU) && ((u32) temp_r1_3 <= 0x106U))) {
            M2C_FIELD(temp_r8, u16 *, 0x40) = temp_r1_3;
        } else {
            var_r6 = 6;
        }
    }
    if (var_r7 & 0x100) {
        temp_r1_4 = M2C_FIELD(arg0, u16 *, 0x14);
        if (((u32) temp_r1_4 <= 0xBEU) || (((u32) temp_r1_4 >= 0xDCU) && ((u32) temp_r1_4 <= 0x106U))) {
            M2C_FIELD(temp_r8, u16 *, 0x42) = temp_r1_4;
        } else {
            var_r6 = 6;
        }
    }
    if (var_r7 & 0x200) {
        temp_r1_5 = M2C_FIELD(arg0, u16 *, 0x16);
        M2C_FIELD(temp_r8, u16 *, 0x98) = temp_r1_5;
        M2C_FIELD(temp_r8, u16 *, 0x7CA) = temp_r1_5;
    }
    if (var_r7 & 0x400) {
        M2C_FIELD(temp_r8, u16 *, 0x92) = (u16) M2C_FIELD(arg0, u8 *, 0x18);
    }
    if (var_r7 & 0x800) {
        M2C_FIELD(temp_r8, u16 *, 0x94) = (u16) M2C_FIELD(arg0, u8 *, 0x19);
    }
    if (var_r7 & 0x1000) {
        M2C_FIELD(temp_r8, u16 *, 0x9A) = (u16) M2C_FIELD(arg0, u8 *, 0x1A);
        M2C_FIELD(temp_r8, u16 *, 0x7CC) = (u16) M2C_FIELD(temp_r8, u16 *, 0x9A);
    }
    if (var_r7 & 0x2000) {
        M2C_FIELD(temp_r8, u16 *, 0x9C) = (u16) M2C_FIELD(arg0, u8 *, 0x1B);
    }
    native_arm7_fn_037fdd14(temp_r5);
    return var_r6;
}
