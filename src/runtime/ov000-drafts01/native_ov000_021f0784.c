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
extern u32 native_fn_02004120();
extern u32 native_fn_02004174();
extern u32 native_fn_02008c58();
extern u32 native_fn_ov000_021f0638();
u32 native_ov000_021f0784(void) {
    native_fn_02008c58(0, native_fn_02004120(), 0x8000);
    native_fn_02008c58(0, native_fn_02004174(), 0x8000);
    return native_fn_ov000_021f0638();
}
