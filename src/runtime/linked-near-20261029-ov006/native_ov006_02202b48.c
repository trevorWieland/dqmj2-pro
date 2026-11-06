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
extern u32 native_fn_0201b248();
extern u32 native_fn_0201d69c();
u32 native_ov006_02202b48(s32 arg0, s32 arg1, s32 arg2) {
    u32 temp_r1;
    u32 temp_r4;

    temp_r4 = native_fn_0201d69c();
    temp_r1 = native_fn_0201d69c(arg1);
    if (((s32) temp_r4 < arg2) || ((s32) temp_r1 < arg2)) {
        return 0U;
    }
    if (native_fn_0201b248(arg0 + (temp_r4 - arg2), arg1 + (temp_r1 - arg2), arg2) == 0) {
        return 1U;
    }
    return 0U;
}
