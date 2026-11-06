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
extern u32 native_fn_02008d78();
extern u32 native_fn_02008e0c();
extern u32 native_fn_02094530();
extern u32 native_fn_020946ec();
u32 native_main_020944f0(u32 arg0, u32 arg1, s32 arg2, s32 arg3, s32 arg4) {
    u32 temp_r0;
    u32 temp_r4;
    s32 sp0;

    sp0 = arg2;
    temp_r0 = native_fn_020946ec(1);
    temp_r4 = temp_r0;
    if (arg3 != 0) {
        native_fn_02008e0c(arg3, temp_r4 + 0x18, 0xA);
    } else {
        native_fn_02008d78(temp_r0 + 0x18, 0, 0xA);
    }
    M2C_FIELD(temp_r4, s8 *, 0x22) = (s8) arg4;
    return native_fn_02094530(arg0, arg1, sp0);
}
