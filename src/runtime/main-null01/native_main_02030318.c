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
extern u32 native_fn_0202e380();
u32 native_main_02030318(void *arg0, u32 arg1, void *arg2) {
    u32 var_r0;
    u8 var_r6;

    if (M2C_FIELD(arg0, u32 (**)(void *), 0x20) != NULL) {
        var_r6 = M2C_FIELD(arg0, u8 *, 0x91);
    } else {
        var_r6 = 0;
    }
    if (var_r6 == 1) {
        M2C_FIELD(arg0, u32 *, 8) = (u32) (M2C_FIELD(arg0, u32 *, 8) & ~0x40);
        M2C_FIELD(arg0, u32 (**)(void *), 0x20)(arg0);
        if (M2C_FIELD(arg0, u32 (**)(void *), 0x20) != NULL) {
            var_r6 = M2C_FIELD(arg0, u8 *, 0x91);
        } else {
            var_r6 = 0;
        }
        var_r0 = M2C_FIELD(arg0, u32 *, 8) & 0x40;
    } else {
        var_r0 = 0;
    }
    if (var_r0 == 0) {
        var_r0 = M2C_FIELD(arg0, u32 *, 8);
        if (!(var_r0 & 0x100)) {
            var_r0 = native_fn_0202e380(arg2 + M2C_FIELD(arg2, s32 *, 8), M2C_FIELD(arg2, s32 *, 0xC));
        }
    }
    if (var_r6 == 2) {
        M2C_FIELD(arg0, u32 *, 8) = (u32) (M2C_FIELD(arg0, u32 *, 8) & ~0x40);
        M2C_FIELD(arg0, u32 (**)(void *), 0x20)(arg0);
        var_r0 = (u32) M2C_FIELD(arg0, u32 (**)(void *), 0x20);
        if (var_r0 != 0) {
            var_r6 = M2C_FIELD(arg0, u8 *, 0x91);
        } else {
            var_r6 = 0;
        }
    }
    if (var_r6 != 3) {
        return var_r0;
    }
    M2C_FIELD(arg0, u32 *, 8) = (u32) (M2C_FIELD(arg0, u32 *, 8) & ~0x40);
    return M2C_FIELD(arg0, u32 (**)(void *), 0x20)(arg0);
}
