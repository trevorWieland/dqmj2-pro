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
extern u32 native_fn_02061c1c();
u32 native_ov000_02202948(void) {
    native_fn_02061c1c(6, 2, 2, 0x14, 2, 0, 0);
    native_fn_02061c1c(7, 2, 5, 0x14, 2, 0, 0);
    native_fn_02061c1c(8, 2, 7, 0x14, 2, 0, 0);
    native_fn_02061c1c(9, 2, 9, 0x14, 2, 0, 0);
    native_fn_02061c1c(0xA, 2, 0xC, 0xE, 2, 0, 0);
    native_fn_02061c1c(0xB, 4, 0xE, 4, 2, 0, 0);
    native_fn_02061c1c(0xC, 9, 0xE, 4, 2, 0, 0);
    native_fn_02061c1c(0xD, 0xE, 0xE, 4, 2, 0, 0);
    native_fn_02061c1c(0xE, 0x13, 0xE, 4, 2, 0, 0);
    native_fn_02061c1c(0xF, 4, 0x10, 4, 2, 0, 0);
    native_fn_02061c1c(0x10, 9, 0x10, 4, 2, 0, 0);
    native_fn_02061c1c(0x11, 0xE, 0x10, 4, 2, 0, 0);
    native_fn_02061c1c(0x12, 0x13, 0x10, 4, 2, 0, 0);
    native_fn_02061c1c(0x13, 0x10, 0x12, 0xE, 2, 0, 0);
    return native_fn_02061c1c(0x14, 2, 0x15, 0x1C, 2, 0, 0);
}
