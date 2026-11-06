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
u32 native_ov000_02203a10(void) {
    native_fn_02061c1c(6, 2, 8, 0x10, 2, 0, 0);
    native_fn_02061c1c(7, 0x17, 8, 7, 2, 0, 0);
    native_fn_02061c1c(8, 2, 0xB, 6, 2, 0, 0);
    native_fn_02061c1c(9, 8, 0xB, 0xE, 2, 0, 0);
    native_fn_02061c1c(0xA, 2, 0xE, 6, 2, 0, 0);
    native_fn_02061c1c(0xB, 8, 0xE, 0xE, 2, 0, 0);
    native_fn_02061c1c(0xC, 8, 0x10, 0xE, 2, 0, 0);
    native_fn_02061c1c(0xD, 8, 0x12, 0xE, 2, 0, 0);
    return native_fn_02061c1c(0xE, 8, 0x14, 0xE, 2, 0, 0);
}
