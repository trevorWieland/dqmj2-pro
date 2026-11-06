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
extern u32 native_fn_ov001_021db438();
extern u32 native_fn_ov001_021e6a6c();
extern u32 native_fn_ov001_021e81d0();
u32 native_ov001_021e8398(s32 arg0, u32 arg1) {
    s32 var_r0;
    u32 temp_r0;
    u32 temp_r5;
    u32 temp_r6;
    u32 temp_r7;

    temp_r6 = native_fn_ov001_021db438();
    temp_r7 = native_fn_ov001_021db438(arg0, 0);
    if (arg0 == 0) {
        var_r0 = 1;
    } else {
        var_r0 = 0;
    }
    temp_r5 = native_fn_ov001_021db438(var_r0, 0);
    temp_r0 = native_fn_ov001_021e81d0(arg0, arg1);
    native_fn_ov001_021e6a6c(temp_r6, temp_r7, temp_r5, temp_r0, temp_r0 + 2, temp_r0 + 3, 1);
    M2C_FIELD(temp_r0, s8 *, 4) = 0;
    return 0U;
}
