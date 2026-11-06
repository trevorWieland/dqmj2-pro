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
extern u32 native_fn_0202a164();
extern u32 native_fn_02045654();
extern u32 native_fn_0204617c();
extern u32 native_fn_0207aad0();
extern u32 native_fn_02084920();
extern u32 native_fn_ov005_021dbb2c();
extern u32 native_fn_ov005_021dcc10();
extern u32 native_fn_ov005_021df5b8();
u32 native_ov005_021dd7c8(void) {
    native_fn_ov005_021dbb2c();
    native_fn_ov005_021dcc10();
    native_fn_0207aad0(2);
    native_fn_0204617c(0, 2);
    native_fn_02084920();
    native_fn_ov005_021df5b8();
    native_fn_0202a164(2);
    native_fn_0202a164(1);
    native_fn_02045654(0);
    native_fn_02045654(1);
    native_fn_02045654(2);
    native_fn_02045654(3);
    *(s32 *)0x04000018 = 0;
    return 0x04000018U;
}
