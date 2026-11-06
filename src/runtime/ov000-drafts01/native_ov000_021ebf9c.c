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
extern u32 native_fn_ov000_021ebdf0();
extern u32 native_fn_ov000_021ebeec();
u32 native_ov000_021ebf9c(void) {
    native_fn_ov000_021ebdf0(7, 1, 2, 2, 0x11, 0x1C, 2, 0, 1);
    native_fn_ov000_021ebdf0(8, 1, 2, 2, 0x15, 0x1C, 2, 0, 1);
    native_fn_ov000_021ebeec(7, 9, 4, 6, 0x10);
    return native_fn_ov000_021ebeec(8, 9, 4, 7, 0x10);
}
