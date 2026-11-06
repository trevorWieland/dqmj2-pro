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
extern u32 native_fn_ov000_02211f08();
extern u32 native_fn_ov000_02211f6c();
extern u32 native_fn_ov000_02211ffc();
extern u32 native_fn_ov000_0221208c();
u32 native_ov000_0221211c(u32 arg0) {
    native_fn_ov000_0221208c();
    native_fn_ov000_02211ffc(arg0);
    native_fn_ov000_02211f6c(arg0);
    native_fn_ov000_02211f08(arg0);
    return 0U;
}
