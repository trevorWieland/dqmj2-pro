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
extern u32 native_fn_0201d444();
extern u32 native_fn_0202a498();
extern u32 native_fn_0203cc2c();
extern u32 native_fn_020481b8();
extern u32 native_fn_02048308();
extern u8 native_data_ov005_021e7444[];
u32 native_ov005_021df3bc(void) {
    u32 temp_r0;
    u8 sp0[32];

    native_fn_0201d444(&sp0, native_data_ov005_021e7444);
    temp_r0 = native_fn_0203cc2c(&sp0, 2);
    native_fn_020481b8(temp_r0, 0x180, 0x40);
    native_fn_02048308();
    return native_fn_0202a498(2, temp_r0);
}
