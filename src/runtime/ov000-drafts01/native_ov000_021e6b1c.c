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
extern u32 native_fn_020283dc();
extern u32 native_fn_ov000_021e63a4();
extern u32 native_fn_ov000_021e63c8();
u32 native_ov000_021e6b1c(u32 arg0, u32 arg1, u32 arg2, u32 arg3) {
    u32 temp_r4;
    u32 temp_r5;

    temp_r5 = native_fn_ov000_021e63a4();
    temp_r4 = native_fn_ov000_021e63c8(arg0);
    native_fn_020283dc(temp_r5, arg1, arg2, arg3);
    M2C_FIELD(temp_r4, s16 *, 0x4E) = 0;
    return 0U;
}
