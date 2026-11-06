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
extern u32 native_fn_ov001_021fd7c4();
extern u32 native_fn_ov001_021fe4ac();
extern u32 native_fn_ov001_021fe5a8();
extern u32 native_fn_ov001_021fe618();
u32 native_ov001_0220364c(void) {
    native_fn_ov001_021fe4ac(1, 8, 0x7F, 0, 1, 0x14, 2, 1, 1);
    native_fn_ov001_021fe5a8(2, 0, 0x7F, 8, 4, 1);
    native_fn_ov001_021fe5a8(3, 1, 0x7F, 0x11, 4, 1);
    native_fn_ov001_021fe618(1, 4, 0, 0x1D, 6, 0x15, 5, 4, 2, 1);
    native_fn_ov001_021fe618(1, 5, 1, 0x1D, 0x12, 0x15, 5, 4, 3, 1);
    return native_fn_ov001_021fd7c4(0x16, 1, 0xA, 1);
}
