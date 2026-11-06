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
extern u32 native_fn_ov000_021ef688();
extern u32 native_fn_ov000_021ef77c();
u32 native_ov000_021ef808(u32 arg0) {
    u32 temp_r0;

    temp_r0 = native_fn_ov000_021ef688(0, 1, 0x7F, 1, 1, 0xF, 2, 1, 1);
    if (temp_r0 == 0) {
        return temp_r0;
    }
    return native_fn_ov000_021ef77c(0, 9, 2, arg0, 8, 0);
}
