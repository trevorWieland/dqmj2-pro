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
extern u32 native_fn_02007ff4();
extern u32 native_fn_02008008();
extern u32 native_fn_0208a31c();
extern u32 native_fn_0208b7cc();
u32 native_main_0208b74c(void) {
    u32 temp_r0;
    u32 temp_r4;
    u32 var_r5;

    temp_r4 = native_fn_02007ff4();
    temp_r0 = native_fn_0208a31c();
    var_r5 = 0;
    if ((temp_r0 != 0) && (M2C_FIELD(temp_r0, s32 *, 0x2260) == 9)) {
        var_r5 = native_fn_0208b7cc();
    }
    native_fn_02008008(temp_r4);
    return var_r5;
}
