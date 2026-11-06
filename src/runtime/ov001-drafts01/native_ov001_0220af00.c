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
extern u32 native_fn_ov001_0220aba0();
extern u32 native_fn_ov001_0220ac58();
u32 native_ov001_0220af00(void *arg0, u32 arg1) {
    native_fn_ov001_0220aba0(0, M2C_FIELD(arg0, s8 *, 0x10), 0x7F, 0, 1, 0x20, 2, 0, 1);
    return native_fn_ov001_0220ac58(0, 5, 4, arg1, 0x10);
}
