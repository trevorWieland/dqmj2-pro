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
extern u32 native_fn_0203d294();
extern u32 native_fn_0207afec();
extern u32 native_fn_0207b674();
u32 native_ov001_0220f1c8(void *arg0, u32 arg1) {
    u32 var_r4;

    var_r4 = 1;
    if (M2C_FIELD((void *) native_fn_0207afec(arg1), s8 *, 0x26) != 0) {
        return 1U;
    }
    if (((s32) native_fn_0207b674(0x4C, M2C_FIELD(arg0, s32 *, 0x1E8) + 0x46) > 0) || ((s32) native_fn_0207b674(0xE9, M2C_FIELD(arg0, s32 *, 0x1E8) + 0x46) > 0) || ((s32) native_fn_0207b674(0xF2, M2C_FIELD(arg0, s32 *, 0x1E8) + 0x46) > 0)) {
        var_r4 = native_fn_0203d294(2) + 1;
    }
    if (((s32) native_fn_0207b674(0x4D, M2C_FIELD(arg0, s32 *, 0x1E8) + 0x46) > 0) || ((s32) native_fn_0207b674(0xE7, M2C_FIELD(arg0, s32 *, 0x1E8) + 0x46) > 0) || ((s32) native_fn_0207b674(0xF0, M2C_FIELD(arg0, s32 *, 0x1E8) + 0x46) > 0)) {
        var_r4 = native_fn_0203d294(3) + 1;
    }
    if (((s32) native_fn_0207b674(0x77, M2C_FIELD(arg0, s32 *, 0x1E8) + 0x46) > 0) || ((s32) native_fn_0207b674(0xE5, M2C_FIELD(arg0, s32 *, 0x1E8) + 0x46) > 0) || ((s32) native_fn_0207b674(0xEE, M2C_FIELD(arg0, s32 *, 0x1E8) + 0x46) > 0)) {
        var_r4 = native_fn_0203d294(2) + 2;
    }
    if (((s32) native_fn_0207b674(0x78, M2C_FIELD(arg0, s32 *, 0x1E8) + 0x46) > 0) || ((s32) native_fn_0207b674(0xE8, M2C_FIELD(arg0, s32 *, 0x1E8) + 0x46) > 0) || ((s32) native_fn_0207b674(0xF1, M2C_FIELD(arg0, s32 *, 0x1E8) + 0x46) > 0)) {
        var_r4 = native_fn_0203d294(5);
    }
    if (M2C_FIELD(arg0, s8 *, 0x263) != 0) {
        var_r4 += 1;
    }
    return var_r4;
}
