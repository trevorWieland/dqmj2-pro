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
extern u32 native_fn_02041e2c();
extern u32 native_fn_02042e30();
extern u32 native_fn_020449d4();
u32 native_ov000_0220a30c(s32 arg0, u32 arg1) {
    s32 sp4;
    s32 sp0;

    native_fn_02042e30((u8) ((u32) (M2C_FIELD((void *) native_fn_020449d4(arg1), u16 *, 4) << 0x14) >> 0x1C), &sp4, &sp0);
    return native_fn_02041e2c(arg0 + 0x100, sp4, sp0, sp4);
}
