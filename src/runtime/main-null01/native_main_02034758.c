#define NULL ((void *)0)
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
extern u32 native_fn_02008430();
extern u32 native_fn_02034480();
extern u32 native_fn_020348ac();
u32 native_main_02034758(void *arg0, void **arg1) {
    s32 var_r0;
    s32 var_r0_2;
    s32 var_r0_3;
    s32 var_r0_4;
    s32 var_r0_5;
    s32 var_r0_6;
    u32 temp_r0;
    s32 var_r4;

    var_r4 = 0;
    if (arg0 != NULL) {
        if ((arg0 != NULL) && (M2C_FIELD(arg0, s32 *, 0) == 0x4E465452)) {
            var_r0 = 1;
        } else {
            var_r0 = 0;
        }
        if (var_r0 != 0) {
            var_r0_2 = 1;
        } else {
            var_r0_2 = 0;
        }
        if (var_r0_2 != 0) {
            if ((arg0 != NULL) && ((u32) M2C_FIELD(arg0, u16 *, 6) >= 0x101U)) {
                var_r0_3 = 1;
            } else {
                var_r0_3 = 0;
            }
            if (var_r0_3 != 0) {
                var_r0_2 = 1;
            } else {
                var_r0_2 = 0;
            }
        }
    } else {
        var_r0_2 = 0;
    }
    if (var_r0_2 == 0) {
        if (arg0 != NULL) {
            if ((arg0 != NULL) && (M2C_FIELD(arg0, s32 *, 0) == 0x4E465452)) {
                var_r0_4 = 1;
            } else {
                var_r0_4 = 0;
            }
            if (var_r0_4 != 0) {
                var_r0_5 = 1;
            } else {
                var_r0_5 = 0;
            }
            if (var_r0_5 != 0) {
                if ((arg0 != NULL) && ((u32) M2C_FIELD(arg0, u16 *, 6) >= 0x100U)) {
                    var_r0_6 = 1;
                } else {
                    var_r0_6 = 0;
                }
                if (var_r0_6 != 0) {
                    var_r0_5 = 1;
                } else {
                    var_r0_5 = 0;
                }
            }
        } else {
            var_r0_5 = 0;
        }
        if (var_r0_5 == 0) {
            native_fn_02008430();
        }
        var_r4 = 1;
    }
    native_fn_020348ac(arg0);
    temp_r0 = native_fn_02034480(arg0, 0x46494E46);
    if (temp_r0 == 0) {
        *arg1 = NULL;
        return 0U;
    }
    *arg1 = temp_r0 + 8;
    if (var_r4 != 0) {
        M2C_FIELD(M2C_FIELD(*arg1, void **, 8), s8 *, 7) = 0;
    }
    return 1U;
}
