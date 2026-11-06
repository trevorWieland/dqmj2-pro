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
extern u32 native_fn_0206dbdc();
extern u32 native_fn_ov000_021ef688();
extern u32 native_fn_ov000_021ef77c();
u32 native_ov000_021ef8e0(s32 arg0, s32 arg1, s32 arg2) {
    u8 temp_r2;

    temp_r2 = ((s32) (native_fn_0206dbdc(9, 2, 0xE) + 7) >> 3) + 4;
    native_fn_ov000_021ef688(0x16, 2, 2, (u8) ((arg0 + arg2 + 2) - temp_r2), arg1, (s32) temp_r2, 2, 0, 1);
    return native_fn_ov000_021ef77c(0x16, 9, 2, 0xE, 0, 1);
}
