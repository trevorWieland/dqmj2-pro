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
extern u32 native_fn_0207b004();
extern u32 native_fn_0207b674();
extern u32 native_fn_ov001_021dbe5c();
extern u32 native_fn_ov001_021dcda8();
extern u32 native_fn_ov001_021e29e8();
extern u32 native_fn_ov001_02210ad0();
u32 native_ov001_021e1468(void *arg0, void *arg1, s32 arg2) {
    s32 temp_r0;
    s32 var_r4_2;
    u32 var_r0;
    u32 var_r0_2;
    u32 var_r0_3;
    u32 var_r0_4;
    u32 var_r0_5;
    u32 var_r4;

    if (native_fn_0207b004(arg2, 0x200) == 0) {
        return 0U;
    }
    if (((s32) native_fn_0207b674(7, M2C_FIELD(arg0, s32 *, 0x1E8) + 0x46) > 0) && (M2C_FIELD(arg1, s8 *, 0x24B) == 0) && (arg2 != 0x77) && ((arg2 != 0) || ((s32) native_fn_0207b674(0x2E, M2C_FIELD(arg0, s32 *, 0x1E8) + 0x46) <= 0))) {
        return 0U;
    }
    if (native_fn_ov001_021dcda8(arg1) != 0) {
        return 0U;
    }
    if (M2C_FIELD(arg1, s8 *, 0x235) != 0) {
        return 0U;
    }
    if (M2C_FIELD(arg1, s8 *, 0x236) != 0) {
        return 0U;
    }
    if (M2C_FIELD(arg1, s8 *, 0x238) != 0) {
        return 0U;
    }
    if (M2C_FIELD(arg1, s8 *, 0x239) != 0) {
        return 0U;
    }
    if (M2C_FIELD(arg1, s8 *, 0x23A) != 0) {
        return 0U;
    }
    if (M2C_FIELD(arg1, s8 *, 0x23B) != 0) {
        return 0U;
    }
    if (M2C_FIELD(arg1, s8 *, 0x24E) != 0) {
        return 0U;
    }
    if ((arg2 == 0x77) || ((arg2 == 0) && ((s32) native_fn_0207b674(0x2E, M2C_FIELD(arg0, s32 *, 0x1E8) + 0x46) > 0))) {
        if (native_fn_ov001_02210ad0(arg0, 2, 1) == 0) {
            var_r0_4 = 1;
        } else {
            var_r0_4 = 0;
        }
        if (var_r0_4 != 0) {
            return var_r0_4;
        }
        if (M2C_FIELD(arg1, s8 *, 0x24B) == 0) {
            return var_r0_4;
        }
        if (native_fn_ov001_02210ad0(arg0, 2, 1) == 0) {
            var_r0_3 = 1;
        } else {
            var_r0_3 = 0;
        }
        return var_r0_3;
    }
    if (M2C_FIELD(arg1, s8 *, 0x24B) != 0) {
        if (native_fn_ov001_02210ad0(arg0, 2, 1) == 0) {
            var_r0_2 = 1;
        } else {
            var_r0_2 = 0;
        }
        return var_r0_2;
    }
    if (native_fn_ov001_021e29e8() & 4) {
        var_r4 = native_fn_ov001_021dbe5c(arg0);
        var_r0_5 = native_fn_ov001_021dbe5c(arg1);
    } else {
        var_r4 = native_fn_ov001_021dbe5c(arg1);
        var_r0_5 = native_fn_ov001_021dbe5c(arg0);
    }
    temp_r0 = var_r4 - var_r0_5;
    if (temp_r0 >= 0x1F4) {
        var_r4_2 = 2;
    } else if (temp_r0 >= 0x12C) {
        var_r4_2 = 4;
    } else if (temp_r0 >= 0xC8) {
        var_r4_2 = 8;
    } else if (temp_r0 >= 0x96) {
        var_r4_2 = 0x10;
    } else if (temp_r0 >= 0x64) {
        var_r4_2 = 0x20;
    } else if (temp_r0 >= 0x32) {
        var_r4_2 = 0x30;
    } else if (temp_r0 >= 0) {
        var_r4_2 = 0x50;
    } else {
        var_r4_2 = 0x80;
    }
    if ((s32) native_fn_0207b674(1, M2C_FIELD(arg1, s32 *, 0x1E8) + 0x46) > 0) {
        var_r4_2 = var_r4_2 >> 1;
    }
    if (var_r4_2 < 4) {
        if (native_fn_ov001_02210ad0(arg0, 8, 5) == 0) {
            var_r0 = 1;
        } else {
            var_r0 = 0;
        }
        return var_r0;
    }
    if (native_fn_ov001_02210ad0(arg0, var_r4_2, var_r4_2 - 1) == 0) {
        return 1U;
    }
    return 0U;
}
