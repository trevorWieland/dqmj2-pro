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
extern u32 native_fn_0202a8e0();
extern u32 native_fn_0203cc2c();
extern u32 native_fn_0203cf9c();
extern u32 native_fn_020481b8();
extern u32 native_fn_0204820c();
extern u32 native_fn_02048308();
u32 native_ov000_022096f4(u32 arg0, s32 arg1) {
    u32 temp_r0;

    native_fn_0202a8e0();
    temp_r0 = native_fn_0203cc2c(arg0, 1);
    if (temp_r0 != 0) {
        if (arg1 & 1) {
            native_fn_020481b8(temp_r0, 0, 0x20);
        }
        if (arg1 & 2) {
            native_fn_0204820c(temp_r0, 0, 0x20);
        }
        native_fn_02048308();
        native_fn_0203cf9c(1, temp_r0);
        return 1U;
    }
    return 0U;
}
