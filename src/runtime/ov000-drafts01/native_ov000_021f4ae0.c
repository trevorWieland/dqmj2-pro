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
extern u32 native_fn_01ffb50c();
extern u32 native_fn_01ffb648();
extern u32 native_fn_02061c1c();
extern u32 native_fn_ov000_021f42d8();
extern u8 native_data_ov000_0222f2d0[];
u32 native_ov000_021f4ae0(void) {
    native_fn_02061c1c(0x1B, 3, 0x14, 8, 2, 0, 0);
    native_fn_01ffb50c(0x1B, 0x10, 0xD, 0x5F, 0);
    native_fn_02061c1c(0x1C, 0xF, 0x14, 1, 2, 0, 0);
    native_fn_01ffb648(0x1C, native_data_ov000_0222f2d0);
    native_fn_02061c1c(0x1D, 0x10, 0x14, 8, 2, 0, 0);
    return native_fn_ov000_021f42d8();
}
