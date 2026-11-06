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
extern u32 native_fn_0200235c();
extern u32 native_fn_020028d8();
extern u32 native_fn_02041f90();
u32 native_ov000_021e8b20(void *arg0, s32 arg1, u32 arg2, s32 arg3) {
    u32 temp_r4;

    temp_r4 = M2C_FIELD(arg0, u32 *, 0x8C);
    native_fn_02041f90(arg0, native_fn_0200235c(native_fn_020028d8(arg1 - M2C_FIELD(arg0, s32 *, 0x70), arg3 - M2C_FIELD(arg0, s32 *, 0x78)), 0x47), 0);
    return temp_r4;
}
